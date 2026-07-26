require('dotenv').config();
const express = require('express');
const cors = require('cors');
const sql = require('mssql');
const bcrypt = require('bcryptjs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS and JSON parsing middleware
app.use(cors());
app.use(express.json());

// Set custom header to identify which VM served the request
app.use((req, res, next) => {
    res.setHeader('X-Served-By', process.env.VM_NAME || 'Unknown-VM');
    next();
});

// Serve static frontend files from the root directory
app.use(express.static(__dirname));

// Database connection configuration
const dbConfig = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: true, // Use encryption for Azure SQL
        trustServerCertificate: false
    }
};

// Initialize Azure SQL Connection Pool
const poolPromise = new sql.ConnectionPool(dbConfig)
    .connect()
    .then(pool => {
        console.log('Connected to Azure SQL Database at:', process.env.DB_SERVER);
        createTables(pool);
        return pool;
    })
    .catch(err => {
        console.error('Database connection failed! Bad Config:', err.message);
        process.exit(1);
    });

// Create database tables if they don't exist (T-SQL syntax)
async function createTables(pool) {
    try {
        const request = pool.request();
        
        // Create users table
        await request.query(`
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                email NVARCHAR(255) UNIQUE NOT NULL,
                phone NVARCHAR(50) NOT NULL,
                password NVARCHAR(255) NOT NULL,
                role NVARCHAR(50) CHECK(role IN ('student', 'landlord')) NOT NULL,
                extra NVARCHAR(MAX)
            )
        `);
        console.log('Users table initialized successfully.');

        // Create properties table
        await request.query(`
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='properties' AND xtype='U')
            CREATE TABLE properties (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
                name NVARCHAR(255) NOT NULL,
                [desc] NVARCHAR(MAX),
                price NVARCHAR(100),
                phone NVARCHAR(50),
                lat FLOAT NOT NULL,
                lng FLOAT NOT NULL
            )
        `);
        console.log('Properties table initialized successfully.');
    } catch (err) {
        console.error('Error initializing tables:', err.message);
    }
}

// SIGN UP Endpoint
app.post('/api/signup', async (req, res) => {
    const { name, email, phone, password, role, extra } = req.body;

    if (!name || !email || !phone || !password || !role) {
        return res.status(400).json({ error: 'All primary fields (name, email, phone, password, role) are required.' });
    }

    try {
        const pool = await poolPromise;
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);
        const emailLower = email.toLowerCase().trim();

        const result = await pool.request()
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

        res.status(201).json({ 
            message: 'Account created successfully!', 
            userId: newUserId,
            user: {
                id: newUserId,
                name: name,
                email: emailLower,
                phone: phone,
                role: role,
                extra: extra || ''
            }
        });
    } catch (err) {
        console.error('Signup error:', err);
        if (err.number === 2627 || err.number === 2601 || err.message.includes('unique') || err.message.includes('duplicate')) {
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

    try {
        const pool = await poolPromise;
        const emailLower = email.toLowerCase().trim();

        const result = await pool.request()
            .input('email', sql.NVarChar, emailLower)
            .query('SELECT * FROM users WHERE email = @email');

        const user = result.recordset[0];
        if (!user) {
            return res.status(401).json({ error: 'Invalid email address or password.' });
        }

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
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// --- PROPERTIES ENDPOINTS ---

// 1. GET ALL PROPERTIES
app.get('/api/properties', async (req, res) => {
    try {
        const pool = await poolPromise;
        const result = await pool.request().query(`
            SELECT 
                p.id, 
                p.user_id, 
                p.name, 
                p.[desc], 
                p.price, 
                p.phone, 
                p.lat, 
                p.lng, 
                u.name AS landlord_name
            FROM properties p
            JOIN users u ON p.user_id = u.id
        `);
        res.status(200).json(result.recordset);
    } catch (err) {
        console.error('Fetch properties error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// 2. CREATE A PROPERTY
app.post('/api/properties', async (req, res) => {
    const { user_id, name, desc, price, phone, lat, lng } = req.body;

    if (!user_id || !name || lat === undefined || lng === undefined) {
        return res.status(400).json({ error: 'User ID, name, lat, and lng are required.' });
    }

    try {
        const pool = await poolPromise;
        const result = await pool.request()
            .input('user_id', sql.Int, user_id)
            .input('name', sql.NVarChar, name)
            .input('desc', sql.NVarChar, desc || '')
            .input('price', sql.NVarChar, price || '')
            .input('phone', sql.NVarChar, phone || '')
            .input('lat', sql.Float, lat)
            .input('lng', sql.Float, lng)
            .query(`
                INSERT INTO properties (user_id, name, [desc], price, phone, lat, lng)
                OUTPUT INSERTED.id
                VALUES (@user_id, @name, @desc, @price, @phone, @lat, @lng)
            `);

        const newPropertyId = result.recordset[0].id;
        res.status(201).json({
            message: 'Property created successfully!',
            id: newPropertyId
        });
    } catch (err) {
        console.error('Create property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// 3. UPDATE A PROPERTY
app.put('/api/properties/:id', async (req, res) => {
    const propertyId = req.params.id;
    const { user_id, name, desc, price, phone } = req.body;

    if (!user_id || !name) {
        return res.status(400).json({ error: 'User ID and name are required.' });
    }

    try {
        const pool = await poolPromise;
        const result = await pool.request()
            .input('id', sql.Int, propertyId)
            .input('user_id', sql.Int, user_id)
            .input('name', sql.NVarChar, name)
            .input('desc', sql.NVarChar, desc || '')
            .input('price', sql.NVarChar, price || '')
            .input('phone', sql.NVarChar, phone || '')
            .query(`
                UPDATE properties
                SET name = @name, [desc] = @desc, price = @price, phone = @phone
                WHERE id = @id AND user_id = @user_id
            `);

        if (result.rowsAffected[0] === 0) {
            return res.status(404).json({ error: 'Property not found or user is not authorized to edit it.' });
        }

        res.status(200).json({ message: 'Property updated successfully!' });
    } catch (err) {
        console.error('Update property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// 4. DELETE A PROPERTY
app.delete('/api/properties/:id', async (req, res) => {
    const propertyId = req.params.id;
    const { user_id } = req.body;

    if (!user_id) {
        return res.status(400).json({ error: 'User ID is required.' });
    }

    try {
        const pool = await poolPromise;
        const result = await pool.request()
            .input('id', sql.Int, propertyId)
            .input('user_id', sql.Int, user_id)
            .query(`
                DELETE FROM properties
                WHERE id = @id AND user_id = @user_id
            `);

        if (result.rowsAffected[0] === 0) {
            return res.status(404).json({ error: 'Property not found or user is not authorized to delete it.' });
        }

        res.status(200).json({ message: 'Property deleted successfully!' });
    } catch (err) {
        console.error('Delete property error:', err);
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
    console.log(`To access from other machines/VMs, use: http://<YOUR_IP_ADDRESS>:${PORT}`);
});
