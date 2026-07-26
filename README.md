# 🏠 PoliSewa - Interactive Map Search & Room Rental Platform

[![Node.js](https://img.shields.io/badge/Node.js-v18%2B-green.svg)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-v4.18-blue.svg)](https://expressjs.com/)
[![Database](https://img.shields.io/badge/Database-Azure%20SQL%20%7C%20SQLite-0078D4.svg)](https://azure.microsoft.com/en-us/products/azure-sql/database)
[![Map Engine](https://img.shields.io/badge/Map-Leaflet.js-brightgreen.svg)](https://leafletjs.com/)

**PoliSewa** is an interactive, map-based room and house rental platform tailored specifically for students at **Politeknik Kuching Sarawak (PKS)** and residents in Matang, Kuching. The platform empowers students to easily find rental accommodation near campus while enabling landlords to register and showcase their rental properties directly on an interactive map.

---

## 🌟 Key Features

- 🗺️ **Interactive Leaflet.js Map**: Full-screen map of Kuching featuring a highlighted landmark pin for the **Politeknik Kuching Sarawak (PKS)** campus.
- 📐 **Automatic Distance Calculation**: Automatically computes the geodesic distance (in kilometers) from any rental property listing to the PKS campus.
- 🗺️ **District Boundary Overlay (GeoJSON)**: Displays local Kuching district boundaries (`boundary.js`) pre-loaded locally to avoid CORS restrictions.
- 🔍 **Real-Time Geocoding Search**: Location search powered by the OpenStreetMap Nominatim API for quick place and address lookup.
- 🔐 **Secure Role-Based Authentication**: Dedicated registration and login portals for **Students** and **Landlords** secured with **Bcrypt** password hashing.
- 🏠 **Full Property Management (CRUD)**: Landlords can place custom pins on the map, set monthly rent rates, update property descriptions, and remove listings.
- ☁️ **Dual Database Support**: Seamless backend compatibility with both Azure SQL Database (Production/Cloud) and SQLite (Local Development).
- 🌐 **Cloudflare Tunnel Ready**: Supports secure public access via Cloudflare Zero Trust Tunnels without requiring router port forwarding.

---

## 📂 Project Structure

```text
polisewa/
├── index.html            # Main Web Interface (Leaflet Map, Search & Auth Modals)
├── style.css             # Custom CSS Styling (Glassmorphism UI & Responsive Layout)
├── boundary.js           # Kuching District GeoJSON Boundary Coordinates
├── server.js             # Express.js Backend Server (REST API & Azure SQL Driver)
├── view_db.py            # Python CLI Tool for Inspecting & Managing Users
├── pluscodetocoordinate.py # Google Plus Code to Lat/Lng Coordinate Converter Utility
├── get_boundary.py       # Helper Script for Fetching & Compiling Boundary Data
├── CNAME                 # Custom Domain Configuration for GitHub Pages
├── .env                  # Environment Variables Configuration
├── .gitignore            # Git Ignored Files Configuration
└── package.json          # Node.js Metadata & Package Dependencies
```

---

## 📊 Database Schema

### 1. `users` Table
Stores registered Student and Landlord account details.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | Primary Key, Auto-increment | Unique User Identifier |
| `name` | `NVARCHAR(255)` | NOT NULL | Full Name |
| `email` | `NVARCHAR(255)` | UNIQUE, NOT NULL | Login Email Address |
| `phone` | `NVARCHAR(50)` | NOT NULL | Contact Phone Number |
| `password` | `NVARCHAR(255)` | NOT NULL | Bcrypt Hashed Password |
| `role` | `NVARCHAR(50)` | CHECK (`student`, `landlord`) | User Role |
| `extra` | `NVARCHAR(MAX)` | NULLABLE | College (Student) / Company (Landlord) |

### 2. `properties` Table
Stores location and listing details for rental properties.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | Primary Key, Auto-increment | Unique Property Identifier |
| `user_id` | `INT` | Foreign Key (`users.id`) | Owner's User ID (Landlord) |
| `name` | `NVARCHAR(255)` | NOT NULL | Property Title / Name |
| `desc` | `NVARCHAR(MAX)` | NULLABLE | Detailed Description & Amenities |
| `price` | `NVARCHAR(100)` | NULLABLE | Monthly Rental Price (e.g. RM 350/month) |
| `phone` | `NVARCHAR(50)` | NULLABLE | Landlord Contact Phone |
| `lat` | `FLOAT` | NOT NULL | Latitude Coordinate |
| `lng` | `FLOAT` | NOT NULL | Longitude Coordinate |

---

## 🛠️ API Endpoints

### Authentication
- **`POST /api/signup`** – Register a new student or landlord account.
- **`POST /api/signin`** – Authenticate user and initiate session.

### Property Management
- **`GET /api/properties`** – Fetch all registered rental property listings.
- **`POST /api/properties`** – Create a new rental property listing (Landlords only).
- **`PUT /api/properties/:id`** – Update an existing property listing.
- **`DELETE /api/properties/:id`** – Delete a property listing from the map.

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **npm** (Node Package Manager)
- **Python 3.x** (For CLI utility scripts)

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
npm install
```

### 3. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory (do not commit sensitive secrets to public repositories):
```env
DB_SERVER=your_database_server_address
DB_DATABASE=your_database_name
DB_USER=your_database_username
DB_PASSWORD=your_database_password
PORT=3000
VM_NAME=Primary-VM
```

### 4. Start the Application Server
```bash
npm start
```
The server will boot up at **`http://localhost:3000`**. Access the URL in your web browser.
