# 🎓 PoliSewa - Interactive Map Search & Student Room Rental Platform

[![Node.js](https://img.shields.io/badge/Node.js-v18%2B-green.svg)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-v4.18-blue.svg)](https://expressjs.com/)
[![Database](https://img.shields.io/badge/Database-Azure%20SQL%20%7C%20SQLite-0078D4.svg)](https://azure.microsoft.com/en-us/products/azure-sql/database)
[![Map Engine](https://img.shields.io/badge/Map-Leaflet.js-brightgreen.svg)](https://leafletjs.com/)
[![Email](https://img.shields.io/badge/Email-Gmail%20SMTP%20%7C%20Nodemailer-EA4335.svg)](https://nodemailer.com/)
[![Cloudflare](https://img.shields.io/badge/Tunnel-Cloudflare%20Zero%20Trust-F38020.svg)](https://www.cloudflare.com/)

**PoliSewa** is a modern, map-based room and house rental platform designed specifically for students at **Politeknik Kuching Sarawak (PKS)** and property owners in Matang, Kuching. The platform empowers students to discover safe, affordable accommodation near campus while enabling landlords to list and manage rental properties directly on an interactive map.

🌐 **Live Website**: [https://polisewa.me](https://polisewa.me)

---

## 🌟 Key Features

- 🗺️ **Interactive Leaflet.js Map**: Full-screen map of Kuching with high-precision GPS geocoding, smooth zooming, and a dedicated landmark marker for **Politeknik Kuching Sarawak (PKS)**.
- ✉️ **6-Digit OTP Email Verification**: Secure user verification powered by **Nodemailer & Gmail SMTP**. Features a modern 6-box input grid with auto-advance, smart paste, 60s cooldown timer, and 10-minute code expiry.
- 🔍 **Unified Property & Location Search**: Live, debounced search that simultaneously queries registered rental properties (matching title, description, landlord, and price) and Kuching places via the **OpenStreetMap Nominatim API**.
- 📸 **Multi-Photo Property Uploads**: Landlords can upload multiple property photos stored with disk management and previewed in responsive carousels and detail panels.
- 📐 **Automatic Distance Calculator**: Computes exact geodesic distance (in kilometers) from any rental listing to the PKS campus.
- 🔐 **Role-Based Portals**: Dedicated authentication workflows for **Students** and **Landlords** with salted **Bcrypt** password hashing.
- 🏠 **Full Property CRUD**: Landlords can create listings, adjust rental pricing, edit amenities, and delete properties with automatic image cleanup.
- 📱 **Responsive Glassmorphism UI**: Modern bottom sheet on mobile devices and expandable sidebar drawer on desktop.
- ☁️ **Dual Database Architecture**: Seamless compatibility with **Azure SQL Database** (Cloud Production) and **SQLite** (Local Development Fallback).
- 🗑️ **Permanent Account Deletion**: Secure account deletion endpoint requiring password confirmation with cascaded removal of all owned properties and uploaded photos.

---

## 📂 Project Structure

```text
polisewa/
├── index.html            # Main Single-Page App (Leaflet Map, 6-Box OTP, Search & Auth UI)
├── style.css             # Glassmorphism Stylesheet, Responsive Bottom Sheet & Map Controls
├── boundary.js           # Kuching District GeoJSON Boundary Polygon
├── server.js             # Express.js REST API, Nodemailer SMTP & Azure SQL / SQLite Engine
├── uploads/              # Local Storage for Uploaded Property Images
├── view_db.py            # Python CLI Utility for Database Inspection
├── pluscodetocoordinate.py # Utility for Converting Google Plus Codes to Lat/Lng
├── get_boundary.py       # Helper Script for Compiling Boundary GeoJSON
├── .env                  # Environment Variables (Database & SMTP Credentials)
├── .gitignore            # Git Ignored Secrets & Build Files
└── package.json          # Node.js Dependencies & NPM Scripts
```

---

## 📊 Database Schema

### 1. `users` Table
Stores student and landlord credentials and email verification state.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | Primary Key, Auto-increment | Unique User Identifier |
| `name` | `NVARCHAR(255)` | NOT NULL | User's Full Name |
| `email` | `NVARCHAR(255)` | UNIQUE, NOT NULL | Account Email Address |
| `phone` | `NVARCHAR(50)` | NOT NULL | Contact Phone Number |
| `password` | `NVARCHAR(255)` | NOT NULL | Bcrypt Hashed Password |
| `role` | `NVARCHAR(50)` | CHECK (`student`, `landlord`) | User Account Type |
| `extra` | `NVARCHAR(MAX)` | NULLABLE | University (Student) / Agency (Landlord) |
| `is_verified` | `INT` | DEFAULT `0` | Email Verification Status (`1` = Verified) |
| `otp_code` | `NVARCHAR(10)` | NULLABLE | Current 6-digit OTP verification code |
| `otp_expires_at` | `DATETIME` | NULLABLE | Verification code expiration timestamp |

### 2. `properties` Table
Stores location, pricing, and multimedia for rental listings.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | Primary Key, Auto-increment | Unique Property Identifier |
| `user_id` | `INT` | Foreign Key (`users.id`) | Owner's User ID (Landlord) |
| `name` | `NVARCHAR(255)` | NOT NULL | Property Name / Headline |
| `desc` | `NVARCHAR(MAX)` | NOT NULL | Room Description & Amenities |
| `price` | `NVARCHAR(100)` | NOT NULL | Monthly Rent (e.g., `RM 350`) |
| `phone` | `NVARCHAR(50)` | NOT NULL | Contact WhatsApp / Phone Number |
| `lat` | `FLOAT` | NOT NULL | Latitude Coordinate |
| `lng` | `FLOAT` | NOT NULL | Longitude Coordinate |
| `image` | `NVARCHAR(MAX)` | NOT NULL | Comma-separated image URLs or single path |
| `created_at` | `DATETIME` | DEFAULT `CURRENT_TIMESTAMP` | Listing Creation Date |

---

## 🛠️ REST API Endpoints

### 🔐 Authentication & Verification
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/signup` | Register a new user and dispatch a 6-digit OTP verification email. |
| `POST` | `/api/verify-otp` | Validate the 6-digit code and activate the user account. |
| `POST` | `/api/resend-otp` | Generate and dispatch a fresh 6-digit OTP email. |
| `POST` | `/api/signin` | Authenticate user credentials (prompts OTP if unverified). |
| `DELETE` | `/api/user` | Permanently delete account and all associated properties/photos. |

### 🏠 Property Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/properties` | Fetch all registered rental property listings. |
| `POST` | `/api/properties` | Create a new property listing with mandatory validations (Landlord only). |
| `PUT` | `/api/properties/:id` | Update an existing property listing (Owner only). |
| `DELETE` | `/api/properties/:id` | Delete a property listing and remove associated image files. |
| `POST` | `/api/properties/upload-images` | Upload up to 10 photos simultaneously using `multer`. |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **npm** (Node Package Manager)
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/khalilgihub/polisewa.git
cd polisewa
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory:

```env
# Database Configuration (Azure SQL Database)
DB_SERVER=your_azure_sql_server.database.windows.net
DB_DATABASE=polisewa
DB_USER=your_db_username
DB_PASSWORD=your_db_password
PORT=3000
VM_NAME=Primary-VM

# Email Verification (Gmail SMTP)
EMAIL_USER=polisewa.official@gmail.com
EMAIL_APP_PASS=your_16_digit_app_password
```

> **Note**: If Azure SQL credentials are not provided or connection fails, the server automatically initializes and connects to a local **SQLite** database (`database.sqlite`).

### 5. Start the Application

#### Development Mode:
```bash
node server.js
```

#### Production Mode (PM2):
```bash
pm2 start server.js --name "polisewa"
```

Open **`http://localhost:3000`** in your browser.
