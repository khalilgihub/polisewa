const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
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

// Initialize SQLite database
const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error connecting to database:', err.message);
    } else {
        console.log('Connected to SQLite database at:', dbPath);
        createTable();
    }
});

// Create users table if it doesn't exist
function createTable() {
    db.run(`
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
        if (err) {
            console.error('Error creating users table:', err.message);
        } else {
            console.log('Users table initialized successfully.');
        }
    });

    db.run(`
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
            // Add image column to pre-existing tables (safe migration)
            db.run(`ALTER TABLE properties ADD COLUMN image TEXT DEFAULT ''`, (alterErr) => {
                if (alterErr && !alterErr.message.includes('duplicate column')) {
                    console.error('Error adding image column:', alterErr.message);
                }
            });
        }
    });
}

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

// SIGN UP Endpoint
app.post('/api/signup', async (req, res) => {
    const { name, email, phone, password, role, extra } = req.body;

    if (!name || !email || !phone || !password || !role) {
        return res.status(400).json({ error: 'All primary fields (name, email, phone, password, role) are required.' });
    }

    try {
        // Hash the password securely using bcrypt
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const sql = `INSERT INTO users (name, email, phone, password, role, extra) VALUES (?, ?, ?, ?, ?, ?)`;
        const params = [name, email.toLowerCase().trim(), phone, hashedPassword, role, extra || ''];

        db.run(sql, params, function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed: users.email')) {
                    return res.status(409).json({ error: 'An account with this email address already exists.' });
                }
                return res.status(500).json({ error: 'Database error: ' + err.message });
            }
            // Return the user object so the client can persist it in localStorage
            const newUserId = this.lastID;
            db.get(`SELECT id, name, email, phone, role, extra FROM users WHERE id = ?`, [newUserId], (err2, user) => {
                if (err2) return res.status(500).json({ error: 'Database error: ' + err2.message });
                res.status(201).json({ 
                    message: 'Account created successfully!', 
                    user: user,
                    userId: newUserId
                });
            });
        });
    } catch (err) {
        console.error('Signup error:', err);
        res.status(500).json({ error: 'Server error occurred during sign up.' });
    }
});

// SIGN IN Endpoint
app.post('/api/signin', (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ error: 'Email and password are required.' });
    }

    const sql = `SELECT * FROM users WHERE email = ?`;
    db.get(sql, [email.toLowerCase().trim()], async (err, user) => {
        if (err) {
            return res.status(500).json({ error: 'Database error: ' + err.message });
        }
        if (!user) {
            return res.status(401).json({ error: 'Invalid email address or password.' });
        }

        try {
            // Compare hashed password
            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                return res.status(401).json({ error: 'Invalid email address or password.' });
            }

            // Authentication success (omit password from returned object)
            const { password: _, ...userData } = user;
            res.status(200).json({ 
                message: 'Logged in successfully!', 
                user: userData 
            });
        } catch (err) {
            console.error('Signin error:', err);
            res.status(500).json({ error: 'Server error occurred during sign in.' });
        }
    });
});

// GET all properties (visible to everyone)
app.get('/api/properties', (req, res) => {
    const sql = `SELECT properties.*, users.name as landlord_name FROM properties JOIN users ON properties.user_id = users.id`;
    db.all(sql, [], (err, rows) => {
        if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
        res.json(rows);
    });
});

// Upload a property image (landlord only). Returns the public URL of the saved image.
app.post('/api/properties/upload-image', upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No image file provided.' });
    res.status(201).json({
        message: 'Image uploaded.',
        imageUrl: '/uploads/' + req.file.filename
    });
});

// POST create property (landlord only)
app.post('/api/properties', (req, res) => {
    const { user_id, name, desc, price, phone, lat, lng, image } = req.body;
    if (!user_id || !name || lat === undefined || lng === undefined) {
        return res.status(400).json({ error: 'user_id, name, lat, and lng are required.' });
    }

    const countSql = `SELECT COUNT(*) as count FROM properties WHERE user_id = ?`;
    db.get(countSql, [user_id], (err, row) => {
        if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
        if (row.count >= 2) {
            return res.status(400).json({ error: 'Maximum 2 properties allowed per landlord.' });
        }

        const sql = `INSERT INTO properties (user_id, name, desc, price, phone, lat, lng, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`;
        db.run(sql, [user_id, name, desc || '', price || '', phone || '', lat, lng, image || ''], function(err) {
            if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
            res.status(201).json({ id: this.lastID, message: 'Property created.' });
        });
    });
});

// PUT update property
app.put('/api/properties/:id', (req, res) => {
    const { id } = req.params;
    const { user_id, name, desc, price, phone, image } = req.body;
    if (!user_id || !name) {
        return res.status(400).json({ error: 'user_id and name are required.' });
    }

    const sql = `UPDATE properties SET name = ?, desc = ?, price = ?, phone = ?, image = ? WHERE id = ? AND user_id = ?`;
    db.run(sql, [name, desc || '', price || '', phone || '', image || '', id, user_id], function(err) {
        if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
        if (this.changes === 0) return res.status(404).json({ error: 'Property not found or not owned by you.' });
        res.json({ message: 'Property updated.' });
    });
});

// DELETE property
app.delete('/api/properties/:id', (req, res) => {
    const { id } = req.params;
    const { user_id } = req.body;
    if (!user_id) return res.status(400).json({ error: 'user_id is required.' });

    const sql = `DELETE FROM properties WHERE id = ? AND user_id = ?`;
    db.run(sql, [id, user_id], function(err) {
        if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
        if (this.changes === 0) return res.status(404).json({ error: 'Property not found or not owned by you.' });
        res.json({ message: 'Property deleted.' });
    });
});

// DELETE user account (cascades to delete properties and their images)
app.delete('/api/user', async (req, res) => {
    const { user_id, password } = req.body;
    if (!user_id || !password) return res.status(400).json({ error: 'user_id and password are required.' });

    const userSql = `SELECT * FROM users WHERE id = ?`;
    db.get(userSql, [user_id], async (err, user) => {
        if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
        if (!user) return res.status(404).json({ error: 'User not found.' });

        try {
            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) return res.status(401).json({ error: 'Incorrect password.' });
        } catch (e) {
            return res.status(500).json({ error: 'Server error.' });
        }

        // Get all images to clean up from disk
        const imgSql = `SELECT image FROM properties WHERE user_id = ?`;
        db.all(imgSql, [user_id], (err, rows) => {
            if (err) return res.status(500).json({ error: 'Database error: ' + err.message });

            if (rows) {
                rows.forEach(function(row) {
                    if (row.image) {
                        var filePath = path.join(UPLOAD_DIR, path.basename(row.image));
                        try { fs.unlinkSync(filePath); } catch(e) { /* ignore missing files */ }
                    }
                });
            }

            db.run(`DELETE FROM properties WHERE user_id = ?`, [user_id], function(err) {
                if (err) return res.status(500).json({ error: 'Database error: ' + err.message });

                db.run(`DELETE FROM users WHERE id = ?`, [user_id], function(err) {
                    if (err) return res.status(500).json({ error: 'Database error: ' + err.message });
                    res.json({ message: 'Account and all associated data deleted permanently.' });
                });
            });
        });
    });
});

// Fallback to serve index.html for undefined frontend routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start listening on all network interfaces (important for VMware networking)
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Polisewa local server running on port ${PORT}`);
    console.log(`To access from other machines/VMs, use: http://<YOUR_IP_ADDRESS>:${PORT}`);
});
