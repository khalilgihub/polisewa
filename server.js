require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS and JSON parsing middleware
app.use(cors());
app.use(express.json());

// Serve static frontend files from the root directory
app.use(express.static(__dirname));

// Ensure uploads directory exists and serve it as static files
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}
app.use('/uploads', express.static(UPLOAD_DIR));

// Multer configuration for property image uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, UPLOAD_DIR);
    },
    filename: function (req, file, cb) {
        const unique = Date.now() + '-' + Math.round(Math.random() * 1e9);
        const ext = path.extname(file.originalname).toLowerCase() || '.jpg';
        cb(null, 'property-' + unique + ext);
    }
});
const upload = multer({
    storage: storage,
    limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
    fileFilter: function (req, file, cb) {
        const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (allowed.includes(file.mimetype)) cb(null, true);
        else cb(new Error('Only JPG, PNG, GIF, and WebP images are allowed.'));
    }
});

// Database Abstraction: Azure SQL Database (mssql) with SQLite fallback
let dbType = 'sqlite';
let mssqlPool = null;
let sqliteDb = null;
let sql = null;

async function initDatabase() {
    if (process.env.DB_SERVER) {
        try {
            sql = require('mssql');
            const dbConfig = {
                server: process.env.DB_SERVER,
                database: process.env.DB_DATABASE,
                user: process.env.DB_USER,
                password: process.env.DB_PASSWORD,
                port: parseInt(process.env.DB_PORT, 10) || 1433,
                options: {
                    encrypt: true, // Required for Azure SQL Database
                    trustServerCertificate: false,
                    connectTimeout: 15000
                }
            };
            mssqlPool = await new sql.ConnectionPool(dbConfig).connect();
            dbType = 'mssql';
            console.log(`✅ Connected to Azure SQL Database (${process.env.DB_SERVER}) successfully.`);
            await initMssqlTables(mssqlPool);
            return;
        } catch (err) {
            console.error('⚠️ Azure SQL Connection failed:', err.message);
            console.log('Falling back to local SQLite database...');
        }
    }
    initSqlite();
}

function initSqlite() {
    const sqlite3 = require('sqlite3').verbose();
    dbType = 'sqlite';
    const dbPath = path.join(__dirname, 'database.sqlite');
    sqliteDb = new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error('Error connecting to SQLite database:', err.message);
        } else {
            console.log('Connected to local SQLite database at:', dbPath);
            initSqliteTables();
        }
    });
}

async function initMssqlTables(pool) {
    try {
        await pool.request().query(`
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                email NVARCHAR(255) NOT NULL UNIQUE,
                phone NVARCHAR(50) NOT NULL,
                password NVARCHAR(255) NOT NULL,
                role NVARCHAR(50) NOT NULL,
                extra NVARCHAR(MAX)
            )
        `);
        await pool.request().query(`
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='properties' AND xtype='U')
            CREATE TABLE properties (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL FOREIGN KEY REFERENCES users(id),
                name NVARCHAR(255) NOT NULL,
                [desc] NVARCHAR(MAX),
                price NVARCHAR(100),
                phone NVARCHAR(50),
                lat FLOAT NOT NULL,
                lng FLOAT NOT NULL,
                image NVARCHAR(MAX),
                created_at DATETIME DEFAULT GETDATE()
            )
        `);
        await pool.request().query(`
            IF EXISTS (SELECT * FROM sysobjects WHERE name='properties' AND xtype='U')
            AND NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('properties') AND name = 'image')
            ALTER TABLE properties ADD image NVARCHAR(MAX);
        `);
        console.log('Azure SQL tables verified and initialized successfully.');
    } catch (err) {
        console.error('Error initializing Azure SQL tables:', err.message);
    }
}

function initSqliteTables() {
    sqliteDb.run(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('student', 'landlord')) NOT NULL,
            extra TEXT
        )
    `, (err) => {
        if (err) console.error('Error creating users table:', err.message);
        else console.log('Users table initialized successfully.');
    });

    sqliteDb.run(`
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            desc TEXT DEFAULT '',
            price TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            image TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    `, (err) => {
        if (err) {
            console.error('Error creating properties table:', err.message);
        } else {
            console.log('Properties table initialized successfully.');
            sqliteDb.run(`ALTER TABLE properties ADD COLUMN image TEXT DEFAULT ''`, (alterErr) => {
                if (alterErr && !alterErr.message.includes('duplicate column')) {
                    console.error('Error adding image column:', alterErr.message);
                }
            });
        }
    });
}

// Initialize Database Connection
initDatabase();

// --- ROUTES ---

// Upload single property image (legacy/fallback)
app.post('/api/properties/upload-image', upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No image file provided.' });
    const url = '/uploads/' + req.file.filename;
    res.status(201).json({
        message: 'Image uploaded.',
        imageUrl: url,
        imageUrls: [url]
    });
});

// Upload multiple property images
app.post('/api/properties/upload-images', upload.array('images', 10), (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.status(400).json({ error: 'No image files provided.' });
    }
    const imageUrls = req.files.map(f => '/uploads/' + f.filename);
    res.status(201).json({
        message: `${imageUrls.length} images uploaded.`,
        imageUrls: imageUrls
    });
});

// SIGN UP Endpoint
app.post('/api/signup', async (req, res) => {
    const { name, email, phone, password, role, extra } = req.body;
    if (!name || !email || !phone || !password || !role) {
        return res.status(400).json({ error: 'All primary fields (name, email, phone, password, role) are required.' });
    }

    const emailLower = email.toLowerCase().trim();
    try {
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        if (dbType === 'mssql') {
            const result = await mssqlPool.request()
                .input('name', sql.NVarChar, name)
                .input('email', sql.NVarChar, emailLower)
                .input('phone', sql.NVarChar, phone)
                .input('password', sql.NVarChar, hashedPassword)
                .input('role', sql.NVarChar, role)
                .input('extra', sql.NVarChar, extra || '')
                .query(`
                    INSERT INTO users (name, email, phone, password, role, extra)
                    OUTPUT INSERTED.id
                    VALUES (@name, @email, @phone, @password, @role, @extra)
                `);

            const newUserId = result.recordset[0].id;
            return res.status(201).json({
                message: 'Account created successfully!',
                user: { id: newUserId, name, email: emailLower, phone, role, extra: extra || '' },
                userId: newUserId
            });
        } else {
            const sqlQuery = `INSERT INTO users (name, email, phone, password, role, extra) VALUES (?, ?, ?, ?, ?, ?)`;
            sqliteDb.run(sqlQuery, [name, emailLower, phone, hashedPassword, role, extra || ''], function(err) {
                if (err) {
                    if (err.message.includes('UNIQUE constraint failed')) {
                        return res.status(409).json({ error: 'An account with this email address already exists.' });
                    }
                    return res.status(500).json({ error: 'Database error: ' + err.message });
                }
                const newUserId = this.lastID;
                sqliteDb.get(`SELECT id, name, email, phone, role, extra FROM users WHERE id = ?`, [newUserId], (err2, user) => {
                    if (err2) return res.status(500).json({ error: 'Database error: ' + err2.message });
                    res.status(201).json({
                        message: 'Account created successfully!',
                        user: user,
                        userId: newUserId
                    });
                });
            });
        }
    } catch (err) {
        console.error('Signup error:', err);
        if (err.number === 2627 || err.number === 2601 || (err.message && (err.message.includes('unique') || err.message.includes('duplicate')))) {
            return res.status(409).json({ error: 'An account with this email address already exists.' });
        }
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// SIGN IN Endpoint
app.post('/api/signin', async (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) {
        return res.status(400).json({ error: 'Email and password are required.' });
    }

    const emailLower = email.toLowerCase().trim();
    try {
        let user = null;
        if (dbType === 'mssql') {
            const result = await mssqlPool.request()
                .input('email', sql.NVarChar, emailLower)
                .query('SELECT * FROM users WHERE email = @email');
            user = result.recordset[0];
        } else {
            user = await new Promise((resolve, reject) => {
                sqliteDb.get(`SELECT * FROM users WHERE email = ?`, [emailLower], (err, row) => {
                    if (err) reject(err);
                    else resolve(row);
                });
            });
        }

        if (!user) {
            return res.status(401).json({ error: 'Invalid email address or password.' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({ error: 'Invalid email address or password.' });
        }

        const { password: _, ...userData } = user;
        res.status(200).json({
            message: 'Logged in successfully!',
            user: userData
        });
    } catch (err) {
        console.error('Signin error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// GET ALL PROPERTIES
app.get('/api/properties', async (req, res) => {
    try {
        if (dbType === 'mssql') {
            const result = await mssqlPool.request().query(`
                SELECT 
                    p.id, 
                    p.user_id, 
                    p.name, 
                    p.[desc], 
                    p.price, 
                    p.phone, 
                    p.lat, 
                    p.lng, 
                    p.image,
                    u.name AS landlord_name
                FROM properties p
                JOIN users u ON p.user_id = u.id
            `);
            res.status(200).json(result.recordset);
        } else {
            const sqlQuery = `SELECT properties.*, users.name as landlord_name FROM properties JOIN users ON properties.user_id = users.id`;
            sqliteDb.all(sqlQuery, [], (err, rows) => {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                res.json(rows);
            });
        }
    } catch (err) {
        console.error('Fetch properties error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// CREATE PROPERTY (Max 2 per landlord)
app.post('/api/properties', async (req, res) => {
    const { user_id, name, desc, price, phone, lat, lng, image } = req.body;
    if (!user_id || !name || lat === undefined || lng === undefined) {
        return res.status(400).json({ error: 'user_id, name, lat, and lng are required.' });
    }

    try {
        if (dbType === 'mssql') {
            const countRes = await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('SELECT COUNT(*) as count FROM properties WHERE user_id = @user_id');
            if (countRes.recordset[0].count >= 2) {
                return res.status(400).json({ error: 'Maximum 2 properties allowed per landlord.' });
            }

            const result = await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .input('name', sql.NVarChar, name)
                .input('desc', sql.NVarChar, desc || '')
                .input('price', sql.NVarChar, price || '')
                .input('phone', sql.NVarChar, phone || '')
                .input('lat', sql.Float, lat)
                .input('lng', sql.Float, lng)
                .input('image', sql.NVarChar, image || '')
                .query(`
                    INSERT INTO properties (user_id, name, [desc], price, phone, lat, lng, image)
                    OUTPUT INSERTED.id
                    VALUES (@user_id, @name, @desc, @price, @phone, @lat, @lng, @image)
                `);

            res.status(201).json({ id: result.recordset[0].id, message: 'Property created.' });
        } else {
            sqliteDb.get(`SELECT COUNT(*) as count FROM properties WHERE user_id = ?`, [user_id], (err, row) => {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                if (row.count >= 2) {
                    return res.status(400).json({ error: 'Maximum 2 properties allowed per landlord.' });
                }

                const sqlQuery = `INSERT INTO properties (user_id, name, desc, price, phone, lat, lng, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`;
                sqliteDb.run(sqlQuery, [user_id, name, desc || '', price || '', phone || '', lat, lng, image || ''], function(err2) {
                    if (err2) return res.status(500).json({ error: 'Database error: ' + err2.message });
                    res.status(201).json({ id: this.lastID, message: 'Property created.' });
                });
            });
        }
    } catch (err) {
        console.error('Create property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// UPDATE PROPERTY
app.put('/api/properties/:id', async (req, res) => {
    const { id } = req.params;
    const { user_id, name, desc, price, phone, image } = req.body;
    if (!user_id || !name) {
        return res.status(400).json({ error: 'user_id and name are required.' });
    }

    try {
        if (dbType === 'mssql') {
            const result = await mssqlPool.request()
                .input('id', sql.Int, id)
                .input('user_id', sql.Int, user_id)
                .input('name', sql.NVarChar, name)
                .input('desc', sql.NVarChar, desc || '')
                .input('price', sql.NVarChar, price || '')
                .input('phone', sql.NVarChar, phone || '')
                .input('image', sql.NVarChar, image || '')
                .query(`
                    UPDATE properties
                    SET name = @name, [desc] = @desc, price = @price, phone = @phone, image = @image
                    WHERE id = @id AND user_id = @user_id
                `);
            if (result.rowsAffected[0] === 0) {
                return res.status(404).json({ error: 'Property not found or user is not authorized to edit it.' });
            }
            res.status(200).json({ message: 'Property updated.' });
        } else {
            const sqlQuery = `UPDATE properties SET name = ?, desc = ?, price = ?, phone = ?, image = ? WHERE id = ? AND user_id = ?`;
            sqliteDb.run(sqlQuery, [name, desc || '', price || '', phone || '', image || '', id, user_id], function(err) {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                if (this.changes === 0) return res.status(404).json({ error: 'Property not found or not owned by you.' });
                res.json({ message: 'Property updated.' });
            });
        }
    } catch (err) {
        console.error('Update property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// DELETE PROPERTY
app.delete('/api/properties/:id', async (req, res) => {
    const { id } = req.params;
    const { user_id } = req.body;
    if (!user_id) return res.status(400).json({ error: 'user_id is required.' });

    try {
        if (dbType === 'mssql') {
            const result = await mssqlPool.request()
                .input('id', sql.Int, id)
                .input('user_id', sql.Int, user_id)
                .query(`DELETE FROM properties WHERE id = @id AND user_id = @user_id`);
            if (result.rowsAffected[0] === 0) {
                return res.status(404).json({ error: 'Property not found or user is not authorized to delete it.' });
            }
            res.status(200).json({ message: 'Property deleted.' });
        } else {
            const sqlQuery = `DELETE FROM properties WHERE id = ? AND user_id = ?`;
            sqliteDb.run(sqlQuery, [id, user_id], function(err) {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                if (this.changes === 0) return res.status(404).json({ error: 'Property not found or not owned by you.' });
                res.json({ message: 'Property deleted.' });
            });
        }
    } catch (err) {
        console.error('Delete property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// DELETE USER ACCOUNT
app.delete('/api/user', async (req, res) => {
    const { user_id, password } = req.body;
    if (!user_id || !password) return res.status(400).json({ error: 'user_id and password are required.' });

    try {
        if (dbType === 'mssql') {
            const userRes = await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('SELECT * FROM users WHERE id = @user_id');
            const user = userRes.recordset[0];
            if (!user) return res.status(404).json({ error: 'User not found.' });

            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) return res.status(401).json({ error: 'Incorrect password.' });

            const imgRes = await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('SELECT image FROM properties WHERE user_id = @user_id');
            imgRes.recordset.forEach(row => {
                if (row.image) {
                    const filePath = path.join(UPLOAD_DIR, path.basename(row.image));
                    try { fs.unlinkSync(filePath); } catch (e) {}
                }
            });

            await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('DELETE FROM properties WHERE user_id = @user_id');

            await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('DELETE FROM users WHERE id = @user_id');

            res.status(200).json({ message: 'Account and all associated data deleted permanently.' });
        } else {
            sqliteDb.get(`SELECT * FROM users WHERE id = ?`, [user_id], async (err, user) => {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                if (!user) return res.status(404).json({ error: 'User not found.' });

                try {
                    const isMatch = await bcrypt.compare(password, user.password);
                    if (!isMatch) return res.status(401).json({ error: 'Incorrect password.' });
                } catch (e) {
                    return res.status(500).json({ error: 'Server error.' });
                }

                sqliteDb.all(`SELECT image FROM properties WHERE user_id = ?`, [user_id], (err2, rows) => {
                    if (err2) return res.status(500).json({ error: 'Database error: ' + err2.message });
                    if (rows) {
                        rows.forEach(row => {
                            if (row.image) {
                                const filePath = path.join(UPLOAD_DIR, path.basename(row.image));
                                try { fs.unlinkSync(filePath); } catch (e) {}
                            }
                        });
                    }

                    sqliteDb.run(`DELETE FROM properties WHERE user_id = ?`, [user_id], (err3) => {
                        if (err3) return res.status(500).json({ error: 'Database error: ' + err3.message });
                        sqliteDb.run(`DELETE FROM users WHERE id = ?`, [user_id], (err4) => {
                            if (err4) return res.status(500).json({ error: 'Database error: ' + err4.message });
                            res.json({ message: 'Account and all associated data deleted permanently.' });
                        });
                    });
                });
            });
        }
    } catch (err) {
        console.error('Delete account error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// Fallback to serve index.html for undefined frontend routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start listening on all network interfaces
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Polisewa server running on port ${PORT}`);
    console.log(`Access endpoint: http://localhost:${PORT}`);
});
