require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const nodemailer = require('nodemailer');

const { poolPromise, sql, getActiveServer } = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

// Gmail SMTP Email Transporter
function getMailTransporter() {
    const user = process.env.EMAIL_USER;
    const pass = process.env.EMAIL_APP_PASS;
    if (user && pass && pass.trim().length > 0) {
        return nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 465,
            secure: true,
            auth: {
                user: user.trim(),
                pass: pass.replace(/\s+/g, '')
            }
        });
    }
    return null;
}

// Send Branded HTML OTP Verification Email
async function sendOtpEmail(toEmail, otpCode, userName) {
    const transporter = getMailTransporter();
    const emailUser = (process.env.EMAIL_USER && process.env.EMAIL_USER.trim()) || 'polisewa.official@gmail.com';

    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 24px; }
                .container { max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }
                .header { background: linear-gradient(135deg, #2563eb, #1d4ed8); padding: 32px 24px; text-align: center; color: #ffffff; }
                .header h1 { margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }
                .header p { margin: 6px 0 0; font-size: 13.5px; opacity: 0.92; }
                .content { padding: 32px 28px; text-align: center; color: #1e293b; }
                .greeting { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
                .text { font-size: 14px; line-height: 1.6; color: #64748b; margin-bottom: 24px; }
                .otp-box { background: #eff6ff; border: 2px dashed #3b82f6; border-radius: 12px; padding: 18px 28px; display: inline-block; margin: 0 auto 20px; letter-spacing: 8px; font-size: 34px; font-weight: 800; color: #1e40af; font-family: 'SF Mono', Consolas, Monaco, monospace, sans-serif; }
                .expiry { font-size: 12.5px; color: #64748b; margin-bottom: 20px; }
                .spam-tip-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 14px 16px; margin: 24px 0 10px; text-align: left; font-size: 12.5px; color: #92400e; line-height: 1.5; }
                .footer { border-top: 1px solid #f1f5f9; padding: 20px 24px; font-size: 12px; color: #94a3b8; text-align: center; background: #f8fafc; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Polisewa</h1>
                    <p>Student Accommodation & Room Rental Platform</p>
                </div>
                <div class="content">
                    <div class="greeting">Hello ${userName || 'there'},</div>
                    <div class="text">Thank you for joining Polisewa. Please use the following 6-digit verification code to activate your account:</div>
                    <div class="otp-box">${otpCode}</div>
                    <div class="expiry">⏱️ This code is valid for <b>10 minutes</b>. Please do not share it with anyone.</div>
                    <div class="spam-tip-box">
                        💡 <b>Delivery Tip:</b> If this email arrived in your <b>Spam folder</b>, please click <b>"Report not spam"</b> to receive future rental inquiries in your Primary Inbox.
                    </div>
                </div>
                <div class="footer">
                    If you did not request this code, please ignore this email.<br>
                    &copy; ${new Date().getFullYear()} Polisewa. Politeknik Kuching Sarawak.
                </div>
            </div>
        </body>
        </html>
    `;

    if (!transporter) {
        console.log(`\n======================================================`);
        console.log(`📧 [EMAIL VERIFICATION - CONSOLE MODE] To: ${toEmail} | OTP: ${otpCode}`);
        console.log(`======================================================\n`);
        return { success: true, simulated: true };
    }

    try {
        const info = await transporter.sendMail({
            from: `"Polisewa Support" <${emailUser}>`,
            replyTo: `"Polisewa Support" <${emailUser}>`,
            to: toEmail,
            subject: `Your Polisewa Verification Code: ${otpCode}`,
            text: `Hello ${userName || 'there'},\n\nYour Polisewa verification code is: ${otpCode}\n\nValid for 10 minutes.\n\nBest regards,\nPolisewa Team`,
            html: htmlContent
        });
        console.log(`✅ Verification email sent to ${toEmail} (ID: ${info.messageId})`);
        return { success: true, simulated: false };
    } catch (err) {
        console.error(`❌ Failed to send verification email to ${toEmail}:`, err.message);
        throw err;
    }
}

// Middleware
app.use(cors());
app.use(express.json());

// Multi-VM headers & Architecture
app.use((req, res, next) => {
    res.setHeader('X-Served-By', process.env.VM_NAME || 'Primary-VM');
    res.setHeader('X-Database-Type', 'mssql');
    next();
});

// System Health & Architecture Status
app.get('/api/health', (req, res) => {
    const isMssqlConnected = !!(mssqlPool && mssqlPool.connected);
    const activeDbServer = getActiveServer ? getActiveServer() : (process.env.DB_SERVER || 'Azure SQL');
    res.status(200).json({
        status: isMssqlConnected ? 'healthy' : 'degraded',
        server: process.env.VM_NAME || 'Primary-VM',
        database: {
            type: 'mssql',
            connected: isMssqlConnected,
            provider: `Azure SQL (${activeDbServer})`,
            activeServer: activeDbServer
        },
        uptimeSeconds: Math.floor(process.uptime()),
        timestamp: new Date().toISOString()
    });
});

// Static frontend serving
app.use(express.static(__dirname));

// Property uploads directory & Multer storage
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}
app.use('/uploads', express.static(UPLOAD_DIR));

const upload = multer({
    storage: multer.diskStorage({
        destination: (req, file, cb) => cb(null, UPLOAD_DIR),
        filename: (req, file, cb) => {
            const unique = Date.now() + '-' + Math.round(Math.random() * 1e9);
            const ext = path.extname(file.originalname).toLowerCase() || '.jpg';
            cb(null, 'property-' + unique + ext);
        }
    }),
    limits: { fileSize: 10 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
        const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (allowed.includes(file.mimetype)) cb(null, true);
        else cb(new Error('Only JPG, PNG, GIF, and WebP images are allowed.'));
    }
});

// --- HELPER FUNCTIONS ---

// Helper: Safely delete property image files from disk
function deletePropertyImages(imageVal) {
    if (!imageVal) return;
    try {
        const parsed = typeof imageVal === 'string' ? JSON.parse(imageVal) : imageVal;
        const urls = Array.isArray(parsed) ? parsed : [parsed];
        urls.forEach(u => {
            if (typeof u === 'string' && u.trim().length > 0) {
                const fp = path.join(UPLOAD_DIR, path.basename(u));
                try { fs.unlinkSync(fp); } catch (e) { }
            }
        });
    } catch (e) {
        if (typeof imageVal === 'string' && imageVal.trim().length > 0) {
            const fp = path.join(UPLOAD_DIR, path.basename(imageVal));
            try { fs.unlinkSync(fp); } catch (e) { }
        }
    }
}

// Helper: Validate administrator credentials for admin-only endpoints
async function verifyAdmin(admin_id, res) {
    if (!admin_id) {
        res.status(401).json({ error: 'Admin authentication required.' });
        return false;
    }
    const adminCheck = await mssqlPool.request()
        .input('admin_id', sql.Int, admin_id)
        .query('SELECT role FROM users WHERE id = @admin_id');
    if (adminCheck.recordset.length === 0 || adminCheck.recordset[0].role !== 'admin') {
        res.status(403).json({ error: 'Unauthorized. Admin privileges required.' });
        return false;
    }
    return true;
}

// Helper: Validate that a property has at least one valid photo
function hasValidPhotos(image) {
    if (!image) return false;
    try {
        const parsed = typeof image === 'string' ? JSON.parse(image) : image;
        if (Array.isArray(parsed)) return parsed.filter(Boolean).length > 0;
        if (typeof parsed === 'string') return parsed.trim().length > 0;
    } catch (e) {
        if (typeof image === 'string') return image.trim().length > 0;
    }
    return false;
}

// Database Connection & Administration Seeding
let mssqlPool = null;

const DEFAULT_ADMINS = [
    { name: 'Abdul Khalil (Admin)', email: 'abdulkhalilpro@gmail.com', password: 'poli@sewaadministrator', phone: '+60123456789', role: 'admin', extra: 'System Administrator' },
    { name: 'Asyarif (Admin)', email: 'asyarif3005@gmail.com', password: '011poliadministrator123', phone: '+60123456789', role: 'admin', extra: 'System Administrator' },
    { name: 'Josh Alzon (Admin)', email: 'joshalzon981@gmail.com', password: 'joshadministrator*123@!', phone: '+60123456789', role: 'admin', extra: 'System Administrator' }
];

async function seedAdminAccounts() {
    if (!mssqlPool) return;
    for (const admin of DEFAULT_ADMINS) {
        const emailLower = admin.email.toLowerCase().trim();
        try {
            const hashedPassword = await bcrypt.hash(admin.password, 10);
            const check = await mssqlPool.request()
                .input('email', sql.NVarChar, emailLower)
                .query('SELECT id FROM users WHERE email = @email');

            if (check.recordset.length === 0) {
                await mssqlPool.request()
                    .input('name', sql.NVarChar, admin.name)
                    .input('email', sql.NVarChar, emailLower)
                    .input('phone', sql.NVarChar, admin.phone)
                    .input('password', sql.NVarChar, hashedPassword)
                    .input('role', sql.NVarChar, admin.role)
                    .input('extra', sql.NVarChar, admin.extra)
                    .query(`INSERT INTO users (name, email, phone, password, role, extra, is_verified, otp_code, otp_expires_at)
                            VALUES (@name, @email, @phone, @password, @role, @extra, 1, '', NULL)`);
                console.log(`🛡️ Seeded administrator account: ${emailLower}`);
            } else {
                await mssqlPool.request()
                    .input('email', sql.NVarChar, emailLower)
                    .input('name', sql.NVarChar, admin.name)
                    .input('password', sql.NVarChar, hashedPassword)
                    .input('role', sql.NVarChar, admin.role)
                    .input('extra', sql.NVarChar, admin.extra)
                    .query(`UPDATE users SET name = @name, password = @password, role = @role, extra = @extra, is_verified = 1 WHERE email = @email`);
            }
        } catch (e) {
            console.error(`Error during admin seeding (${emailLower}):`, e.message);
        }
    }
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
                extra NVARCHAR(MAX),
                is_verified INT DEFAULT 0,
                otp_code NVARCHAR(10),
                otp_expires_at DATETIME
            );
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
                details NVARCHAR(MAX),
                is_verified INT DEFAULT 0,
                created_at DATETIME DEFAULT GETDATE()
            );
        `);
        console.log('Azure SQL tables verified and initialized successfully.');
        await seedAdminAccounts();
    } catch (err) {
        console.error('Error initializing Azure SQL tables:', err.message);
    }
}

async function initDatabase() {
    try {
        mssqlPool = await poolPromise;
        const activeServer = getActiveServer ? getActiveServer() : (process.env.DB_SERVER || 'Azure SQL');
        console.log(`✅ Pangkalan data Azure SQL bersedia (${activeServer}) (Auto-Failover Aktif).`);
        await initMssqlTables(mssqlPool);
    } catch (err) {
        console.error('❌ Sambungan pangkalan data Azure SQL gagal:', err.message);
    }
}

initDatabase();

// --- ROUTES ---

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

// SIGN UP Endpoint (Generates OTP & sends verification email)
app.post('/api/signup', async (req, res) => {
    const { name, email, phone, password, role, extra } = req.body;
    if (!name || !email || !phone || !password || !role) {
        return res.status(400).json({ error: 'All primary fields (name, email, phone, password, role) are required.' });
    }

    const emailLower = email.toLowerCase().trim();
    const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
    const otpExpiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();

    try {
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const checkUser = await mssqlPool.request()
            .input('email', sql.NVarChar, emailLower)
            .query('SELECT * FROM users WHERE email = @email');

        if (checkUser.recordset.length > 0) {
            const existing = checkUser.recordset[0];
            if (existing.is_verified === 1) {
                return res.status(409).json({ error: 'An account with this email address already exists. Please Sign In.' });
            }
            await mssqlPool.request()
                .input('id', sql.Int, existing.id)
                .input('name', sql.NVarChar, name)
                .input('phone', sql.NVarChar, phone)
                .input('password', sql.NVarChar, hashedPassword)
                .input('role', sql.NVarChar, role)
                .input('extra', sql.NVarChar, extra || '')
                .input('otp_code', sql.NVarChar, otpCode)
                .input('otp_expires_at', sql.DateTime, new Date(otpExpiresAt))
                .query(`UPDATE users SET name = @name, phone = @phone, password = @password, role = @role, extra = @extra, otp_code = @otp_code, otp_expires_at = @otp_expires_at, is_verified = 0 WHERE id = @id`);
        } else {
            await mssqlPool.request()
                .input('name', sql.NVarChar, name)
                .input('email', sql.NVarChar, emailLower)
                .input('phone', sql.NVarChar, phone)
                .input('password', sql.NVarChar, hashedPassword)
                .input('role', sql.NVarChar, role)
                .input('extra', sql.NVarChar, extra || '')
                .input('otp_code', sql.NVarChar, otpCode)
                .input('otp_expires_at', sql.DateTime, new Date(otpExpiresAt))
                .query(`INSERT INTO users (name, email, phone, password, role, extra, is_verified, otp_code, otp_expires_at) VALUES (@name, @email, @phone, @password, @role, @extra, 0, @otp_code, @otp_expires_at)`);
        }

        try {
            await sendOtpEmail(emailLower, otpCode, name);
        } catch (emailErr) {
            console.error('Email send failure:', emailErr.message);
        }

        return res.status(200).json({
            message: 'Verification code sent to your email.',
            needsVerification: true,
            email: emailLower
        });
    } catch (err) {
        console.error('Signup error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// VERIFY OTP Endpoint
app.post('/api/verify-otp', async (req, res) => {
    const { email, otp } = req.body;
    if (!email || !otp) {
        return res.status(400).json({ error: 'Email and 6-digit verification code are required.' });
    }

    const emailLower = email.toLowerCase().trim();
    const cleanOtp = String(otp).trim();

    try {
        const result = await mssqlPool.request()
            .input('email', sql.NVarChar, emailLower)
            .query('SELECT * FROM users WHERE email = @email');
        const user = result.recordset[0];

        if (!user) return res.status(404).json({ error: 'User account not found.' });

        if (user.is_verified === 1) {
            const { password: _, otp_code: __, otp_expires_at: ___, ...userData } = user;
            return res.status(200).json({ message: 'Account already verified! Logged in successfully.', user: userData });
        }

        if (!user.otp_code || user.otp_code !== cleanOtp) {
            return res.status(400).json({ error: 'Invalid verification code. Please check your email and try again.' });
        }

        if (user.otp_expires_at && new Date(user.otp_expires_at) < new Date()) {
            return res.status(400).json({ error: 'Verification code has expired. Please click Resend Code.' });
        }

        await mssqlPool.request()
            .input('id', sql.Int, user.id)
            .query(`UPDATE users SET is_verified = 1, otp_code = '', otp_expires_at = NULL WHERE id = @id`);

        const { password: _, otp_code: __, otp_expires_at: ___, ...userData } = user;
        userData.is_verified = 1;

        return res.status(200).json({ message: 'Email verified successfully! Welcome to Polisewa.', user: userData });
    } catch (err) {
        console.error('Verify OTP error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// RESEND OTP Endpoint
app.post('/api/resend-otp', async (req, res) => {
    const { email } = req.body;
    if (!email) return res.status(400).json({ error: 'Email is required.' });

    const emailLower = email.toLowerCase().trim();
    const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
    const otpExpiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();

    try {
        const result = await mssqlPool.request()
            .input('email', sql.NVarChar, emailLower)
            .query('SELECT * FROM users WHERE email = @email');
        const user = result.recordset[0];

        if (!user) return res.status(404).json({ error: 'No account found with this email address.' });
        if (user.is_verified === 1) return res.status(400).json({ error: 'This account is already verified. Please sign in.' });

        await mssqlPool.request()
            .input('id', sql.Int, user.id)
            .input('otp_code', sql.NVarChar, otpCode)
            .input('otp_expires_at', sql.DateTime, new Date(otpExpiresAt))
            .query(`UPDATE users SET otp_code = @otp_code, otp_expires_at = @otp_expires_at WHERE id = @id`);

        try {
            await sendOtpEmail(emailLower, otpCode, user.name);
        } catch (emailErr) {
            console.error('Email resend error:', emailErr.message);
        }

        return res.status(200).json({ message: 'A new 6-digit verification code has been sent to your email.' });
    } catch (err) {
        console.error('Resend OTP error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// SIGN IN Endpoint
app.post('/api/signin', async (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ error: 'Email and password are required.' });

    const emailLower = email.toLowerCase().trim();
    try {
        const result = await mssqlPool.request()
            .input('email', sql.NVarChar, emailLower)
            .query('SELECT * FROM users WHERE email = @email');
        let user = result.recordset[0];

        // Administrator auto-sync
        const defaultAdmin = DEFAULT_ADMINS.find(a => a.email.toLowerCase().trim() === emailLower);
        if (defaultAdmin) {
            const isDefaultPass = (password === defaultAdmin.password);
            let passwordMatch = user ? await bcrypt.compare(password, user.password) : false;

            if (isDefaultPass || passwordMatch) {
                const freshHash = await bcrypt.hash(defaultAdmin.password, 10);
                if (!user) {
                    const insertRes = await mssqlPool.request()
                        .input('name', sql.NVarChar, defaultAdmin.name)
                        .input('email', sql.NVarChar, emailLower)
                        .input('phone', sql.NVarChar, defaultAdmin.phone)
                        .input('password', sql.NVarChar, freshHash)
                        .input('role', sql.NVarChar, defaultAdmin.role)
                        .input('extra', sql.NVarChar, defaultAdmin.extra)
                        .query(`INSERT INTO users (name, email, phone, password, role, extra, is_verified, otp_code, otp_expires_at)
                                OUTPUT INSERTED.*
                                VALUES (@name, @email, @phone, @password, @role, @extra, 1, '', NULL)`);
                    user = insertRes.recordset[0];
                } else if (isDefaultPass && !passwordMatch) {
                    await mssqlPool.request()
                        .input('id', sql.Int, user.id)
                        .input('password', sql.NVarChar, freshHash)
                        .input('role', sql.NVarChar, 'admin')
                        .query(`UPDATE users SET password = @password, role = @role, is_verified = 1 WHERE id = @id`);
                    user.role = 'admin';
                    user.is_verified = 1;
                }

                const { password: _, otp_code: __, otp_expires_at: ___, ...userData } = user;
                return res.status(200).json({ message: 'Welcome Administrator!', user: userData });
            }
        }
        if (!user) return res.status(401).json({ error: 'Invalid email address or password.' });

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) return res.status(401).json({ error: 'Invalid email address or password.' });

        // Unverified user prompt
        if (user.is_verified === 0) {
            const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
            const otpExpiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();

            await mssqlPool.request()
                .input('id', sql.Int, user.id)
                .input('otp_code', sql.NVarChar, otpCode)
                .input('otp_expires_at', sql.DateTime, new Date(otpExpiresAt))
                .query(`UPDATE users SET otp_code = @otp_code, otp_expires_at = @otp_expires_at WHERE id = @id`);

            try { await sendOtpEmail(emailLower, otpCode, user.name); } catch (e) { }

            return res.status(403).json({
                error: 'Your email address is not verified yet. We have sent a verification code to your email.',
                needsVerification: true,
                email: emailLower
            });
        }

        const { password: _, otp_code: __, otp_expires_at: ___, ...userData } = user;
        res.status(200).json({ message: 'Logged in successfully!', user: userData });
    } catch (err) {
        console.error('Signin error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// VERIFY USER SESSION
app.get('/api/auth/verify', async (req, res) => {
    const rawUserId = req.query.user_id;
    const email = req.query.email ? String(req.query.email).toLowerCase().trim() : null;
    const userId = rawUserId ? parseInt(rawUserId, 10) : null;

    if (!userId || isNaN(userId)) return res.status(400).json({ valid: false, error: 'Valid user_id is required.' });

    try {
        const userRes = await mssqlPool.request()
            .input('user_id', sql.Int, userId)
            .query('SELECT id, name, email, phone, role, extra, is_verified FROM users WHERE id = @user_id');
        const user = userRes.recordset.length > 0 ? userRes.recordset[0] : null;

        if (!user) return res.status(401).json({ valid: false, error: 'Account no longer exists or has been deleted.' });
        if (email && user.email.toLowerCase().trim() !== email) return res.status(401).json({ valid: false, error: 'Account session mismatch.' });

        const { password: _, otp_code: __, otp_expires_at: ___, ...userData } = user;
        res.status(200).json({ valid: true, user: userData });
    } catch (err) {
        console.error('Session verify error:', err);
        res.status(500).json({ valid: false, error: 'Database error: ' + err.message });
    }
});

// GET ALL PROPERTIES
app.get('/api/properties', async (req, res) => {
    const rawUserId = req.query.user_id;
    const userId = rawUserId ? parseInt(rawUserId, 10) : null;

    try {
        res.setHeader('Access-Control-Expose-Headers', 'X-User-Deleted');
        let role = 'guest';
        if (userId && !isNaN(userId)) {
            const userRes = await mssqlPool.request()
                .input('user_id', sql.Int, userId)
                .query('SELECT role FROM users WHERE id = @user_id');
            if (userRes.recordset.length > 0) {
                role = userRes.recordset[0].role;
            } else {
                res.setHeader('X-User-Deleted', 'true');
            }
        }

        let query = `
            SELECT 
                p.id, p.user_id, p.name, p.[desc], p.price, p.phone, p.lat, p.lng, p.image, p.details,
                ISNULL(p.is_verified, 0) AS is_verified, u.name AS landlord_name, u.role AS landlord_role
            FROM properties p
            JOIN users u ON p.user_id = u.id
        `;

        const request = mssqlPool.request();
        if (role === 'admin' || role === 'student') {
            // View all listings
        } else if (userId && !isNaN(userId)) {
            query += ` WHERE (p.is_verified = 1 OR p.user_id = @user_id)`;
            request.input('user_id', sql.Int, userId);
        } else {
            query += ` WHERE p.is_verified = 1`;
        }

        const result = await request.query(query);
        res.status(200).json(result.recordset);
    } catch (err) {
        console.error('Fetch properties error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// CREATE PROPERTY
app.post('/api/properties', async (req, res) => {
    const { user_id, name, desc, price, phone, lat, lng, image, details } = req.body;
    const trimmedName = name ? String(name).trim() : '';
    const trimmedDesc = desc ? String(desc).trim() : '';
    const trimmedPrice = price ? String(price).trim() : '';
    const trimmedPhone = phone ? String(phone).trim() : '';
    const detailsStr = typeof details === 'object' ? JSON.stringify(details) : (details ? String(details) : '');

    if (!user_id || !trimmedName || !trimmedDesc || !trimmedPrice || !trimmedPhone || !hasValidPhotos(image) || lat === undefined || lng === undefined) {
        return res.status(400).json({ error: 'All fields (Property Name, Description, Monthly Rent, Contact Phone Number, and at least 1 Photo) are mandatory.' });
    }

    try {
        const userRes = await mssqlPool.request()
            .input('user_id', sql.Int, user_id)
            .query('SELECT role FROM users WHERE id = @user_id');
        if (userRes.recordset.length === 0) {
            return res.status(401).json({ error: 'User account not found or has been deleted.' });
        }
        const isAdmin = userRes.recordset[0].role === 'admin';
        const initialVerified = isAdmin ? 1 : 0;

        if (!isAdmin) {
            const countRes = await mssqlPool.request()
                .input('user_id', sql.Int, user_id)
                .query('SELECT COUNT(*) as count FROM properties WHERE user_id = @user_id');
            if (countRes.recordset[0].count >= 2) {
                return res.status(400).json({ error: 'Maximum 2 properties allowed per landlord.' });
            }
        }

        const result = await mssqlPool.request()
            .input('user_id', sql.Int, user_id)
            .input('name', sql.NVarChar, trimmedName)
            .input('desc', sql.NVarChar, trimmedDesc)
            .input('price', sql.NVarChar, trimmedPrice)
            .input('phone', sql.NVarChar, trimmedPhone)
            .input('lat', sql.Float, lat)
            .input('lng', sql.Float, lng)
            .input('image', sql.NVarChar, image || '')
            .input('details', sql.NVarChar, detailsStr)
            .input('is_verified', sql.Int, initialVerified)
            .query(`INSERT INTO properties (user_id, name, [desc], price, phone, lat, lng, image, details, is_verified)
                    OUTPUT INSERTED.id
                    VALUES (@user_id, @name, @desc, @price, @phone, @lat, @lng, @image, @details, @is_verified)`);

        res.status(201).json({
            id: result.recordset[0].id,
            is_verified: initialVerified,
            message: isAdmin
                ? 'Property created and published.'
                : 'Property submitted! It is pending admin approval and will appear on the map once approved.'
        });
    } catch (err) {
        console.error('Create property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// UPDATE PROPERTY
app.put('/api/properties/:id', async (req, res) => {
    const { id } = req.params;
    const { user_id, name, desc, price, phone, image, details } = req.body;
    const trimmedName = name ? String(name).trim() : '';
    const trimmedDesc = desc ? String(desc).trim() : '';
    const trimmedPrice = price ? String(price).trim() : '';
    const trimmedPhone = phone ? String(phone).trim() : '';
    const detailsStr = typeof details === 'object' ? JSON.stringify(details) : (details ? String(details) : '');

    if (!user_id || !trimmedName || !trimmedDesc || !trimmedPrice || !trimmedPhone || !hasValidPhotos(image)) {
        return res.status(400).json({ error: 'All fields (Property Name, Description, Monthly Rent, Contact Phone Number, and at least 1 Photo) are mandatory.' });
    }

    try {
        const userRes = await mssqlPool.request()
            .input('user_id', sql.Int, user_id)
            .query('SELECT role FROM users WHERE id = @user_id');
        const isAdmin = userRes.recordset.length > 0 && userRes.recordset[0].role === 'admin';

        const query = isAdmin
            ? `UPDATE properties SET name = @name, [desc] = @desc, price = @price, phone = @phone, image = @image, details = @details WHERE id = @id`
            : `UPDATE properties SET name = @name, [desc] = @desc, price = @price, phone = @phone, image = @image, details = @details WHERE id = @id AND user_id = @user_id`;

        const reqObj = mssqlPool.request()
            .input('id', sql.Int, id)
            .input('name', sql.NVarChar, trimmedName)
            .input('desc', sql.NVarChar, trimmedDesc)
            .input('price', sql.NVarChar, trimmedPrice)
            .input('phone', sql.NVarChar, trimmedPhone)
            .input('image', sql.NVarChar, image || '')
            .input('details', sql.NVarChar, detailsStr);
        if (!isAdmin) reqObj.input('user_id', sql.Int, user_id);

        const result = await reqObj.query(query);
        if (result.rowsAffected[0] === 0) {
            return res.status(404).json({ error: 'Property not found or user is not authorized to edit it.' });
        }
        res.status(200).json({ message: 'Property updated successfully.' });
    } catch (err) {
        console.error('Update property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// DELETE PROPERTY
app.delete('/api/properties/:id', async (req, res) => {
    const { id } = req.params;
    const user_id = (req.body && req.body.user_id) ? req.body.user_id : req.query.user_id;
    if (!user_id) return res.status(400).json({ error: 'user_id is required.' });

    try {
        const userRes = await mssqlPool.request()
            .input('user_id', sql.Int, user_id)
            .query('SELECT role FROM users WHERE id = @user_id');
        const isAdmin = userRes.recordset.length > 0 && userRes.recordset[0].role === 'admin';

        const propRes = await mssqlPool.request().input('id', sql.Int, id).query('SELECT image FROM properties WHERE id = @id');
        if (propRes.recordset.length > 0) {
            deletePropertyImages(propRes.recordset[0].image);
        }

        const deleteQuery = isAdmin
            ? `DELETE FROM properties WHERE id = @id`
            : `DELETE FROM properties WHERE id = @id AND user_id = @user_id`;
        const reqObj = mssqlPool.request().input('id', sql.Int, id);
        if (!isAdmin) reqObj.input('user_id', sql.Int, user_id);

        const result = await reqObj.query(deleteQuery);
        if (result.rowsAffected[0] === 0) {
            return res.status(404).json({ error: 'Property not found or user is not authorized to delete it.' });
        }
        res.status(200).json({ message: 'Property deleted successfully.' });
    } catch (err) {
        console.error('Delete property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// TOGGLE PROPERTY VERIFICATION (Admin only)
app.patch('/api/properties/:id/verify', async (req, res) => {
    const { id } = req.params;
    const { admin_id, is_verified } = req.body;
    const newStatus = (is_verified === 1 || is_verified === true || is_verified === '1') ? 1 : 0;

    try {
        if (!(await verifyAdmin(admin_id, res))) return;

        await mssqlPool.request()
            .input('id', sql.Int, id)
            .input('is_verified', sql.Int, newStatus)
            .query('UPDATE properties SET is_verified = @is_verified WHERE id = @id');

        res.status(200).json({
            message: newStatus === 1 ? 'Listing marked as Polisewa Verified!' : 'Listing verification removed.',
            is_verified: newStatus
        });
    } catch (err) {
        console.error('Verify property error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// ADMIN: GET PLATFORM STATISTICS
app.get('/api/admin/stats', async (req, res) => {
    const admin_id = req.query.admin_id;
    try {
        if (!(await verifyAdmin(admin_id, res))) return;

        const statsRes = await mssqlPool.request().query(`
            SELECT
                (SELECT COUNT(*) FROM properties) AS totalProperties,
                (SELECT COUNT(*) FROM properties WHERE is_verified = 1) AS verifiedProperties,
                (SELECT COUNT(*) FROM users WHERE role = 'student') AS totalStudents,
                (SELECT COUNT(*) FROM users WHERE role = 'landlord') AS totalLandlords,
                (SELECT COUNT(*) FROM users WHERE role = 'admin') AS totalAdmins,
                (SELECT COUNT(*) FROM users) AS totalUsers
        `);
        res.status(200).json(statsRes.recordset[0]);
    } catch (err) {
        console.error('Admin stats error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// ADMIN: GET ALL REGISTERED USERS
app.get('/api/admin/users', async (req, res) => {
    const admin_id = req.query.admin_id;
    try {
        if (!(await verifyAdmin(admin_id, res))) return;

        const usersRes = await mssqlPool.request().query(`
            SELECT 
                u.id, u.name, u.email, u.phone, u.role, u.extra, u.is_verified,
                (SELECT COUNT(*) FROM properties p WHERE p.user_id = u.id) AS property_count
            FROM users u
            ORDER BY u.id DESC
        `);
        res.status(200).json(usersRes.recordset);
    } catch (err) {
        console.error('Admin users error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// ADMIN: DELETE USER ACCOUNT
app.delete('/api/admin/users/:id', async (req, res) => {
    const { id } = req.params;
    const admin_id = (req.body && req.body.admin_id) ? req.body.admin_id : req.query.admin_id;
    try {
        if (!(await verifyAdmin(admin_id, res))) return;

        const imgRes = await mssqlPool.request()
            .input('user_id', sql.Int, id)
            .query('SELECT image FROM properties WHERE user_id = @user_id');
        imgRes.recordset.forEach(row => deletePropertyImages(row.image));

        await mssqlPool.request().input('user_id', sql.Int, id).query('DELETE FROM properties WHERE user_id = @user_id');
        await mssqlPool.request().input('id', sql.Int, id).query('DELETE FROM users WHERE id = @id');

        res.status(200).json({ message: 'User account and all associated properties removed.' });
    } catch (err) {
        console.error('Admin delete user error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// ADMIN: TOGGLE USER EMAIL VERIFICATION
app.patch('/api/admin/users/:id/verify', async (req, res) => {
    const { id } = req.params;
    const { admin_id, is_verified } = req.body;
    const newStatus = (is_verified === 1 || is_verified === true || is_verified === '1') ? 1 : 0;

    try {
        if (!(await verifyAdmin(admin_id, res))) return;

        await mssqlPool.request()
            .input('id', sql.Int, id)
            .input('is_verified', sql.Int, newStatus)
            .query('UPDATE users SET is_verified = @is_verified WHERE id = @id');

        res.status(200).json({ message: `User verification updated to ${newStatus === 1 ? 'Verified' : 'Unverified'}.`, is_verified: newStatus });
    } catch (err) {
        console.error('Admin user verify error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// DELETE USER ACCOUNT (Self)
app.delete('/api/user', async (req, res) => {
    const { user_id, password } = req.body;
    if (!user_id || !password) return res.status(400).json({ error: 'user_id and password are required.' });

    try {
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
        imgRes.recordset.forEach(row => deletePropertyImages(row.image));

        await mssqlPool.request().input('user_id', sql.Int, user_id).query('DELETE FROM properties WHERE user_id = @user_id');
        await mssqlPool.request().input('user_id', sql.Int, user_id).query('DELETE FROM users WHERE id = @user_id');

        res.status(200).json({ message: 'Account and all associated data deleted permanently.' });
    } catch (err) {
        console.error('Delete account error:', err);
        res.status(500).json({ error: 'Database error: ' + err.message });
    }
});

// Fallback to serve index.html for undefined frontend routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start listening
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Polisewa server running on port ${PORT}`);
    console.log(`Access endpoint: http://localhost:${PORT}`);
});