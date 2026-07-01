const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS and JSON parsing middleware
app.use(cors());
app.use(express.json());

// Serve static frontend files from the root directory
app.use(express.static(__dirname));

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
}

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
            res.status(201).json({ 
                message: 'Account created successfully!', 
                userId: this.lastID 
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

// Fallback to serve index.html for undefined frontend routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start listening on all network interfaces (important for VMware networking)
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Polisewa local server running on port ${PORT}`);
    console.log(`To access from other machines/VMs, use: http://<YOUR_IP_ADDRESS>:${PORT}`);
});
