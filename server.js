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
        createTable(pool);
        return pool;
    })
    .catch(err => {
        console.error('Database connection failed! Bad Config:', err.message);
        process.exit(1);
    });

// Create users table if it doesn't exist (T-SQL syntax)
async function createTable(pool) {
    try {
        const request = pool.request();
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
    } catch (err) {
        console.error('Error creating users table:', err.message);
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

// Fallback to serve index.html for undefined frontend routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start listening on all network interfaces
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Polisewa server running on port ${PORT}`);
    console.log(`To access from other machines/VMs, use: http://<YOUR_IP_ADDRESS>:${PORT}`);
});
