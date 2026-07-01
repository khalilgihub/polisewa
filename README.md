# Polisewa - Map Search & Room Rental Platform

Polisewa is a lightweight web application designed for students looking for room rentals near **Politeknik Kuching Sarawak (PKS)** in Matang, Kuching. It displays a map of Kuching with district boundaries, pins major landmarks, and includes a secure member registration system for both students and landlords.

---

## 📚 Key Concepts Explained

If you are new to web development, here is a quick guide to the technologies used in this project:

*   **Node.js**: The core runtime engine that allows us to run JavaScript code directly on our computer/server (instead of only running it inside a web browser). It is what executes our backend file, `server.js`.
*   **npm (Node Package Manager)**: A tool that acts like an "app store" for coding libraries. We use it to download and install helper packages (like `express` for the server, `bcryptjs` for security, and `sqlite3` for the database) using commands like `npm install`.
*   **SQLite**: A lightweight, serverless database. Instead of requiring a massive database installation that runs as a separate background service, SQLite stores all your tables, columns, and registered users inside a single local file (`database.sqlite`) in your project folder.
*   **Cloudflare Tunnels (`cloudflared`)**: A network utility that builds a secure, private "bridge" from a local computer (like your VMware VM) to the public internet. This allows users from other countries to visit your local website without you needing to do dangerous router configurations (Port Forwarding) or exposing your home IP address.
*   **Git & GitHub**: Git is a version control tool that tracks changes in your code files. GitHub is a cloud storage platform. We use them together to easily push code from your host laptop and pull it into your VMware VM (`git pull origin main`).

---

## 📂 Project Structure

```text
polisewa/
├── index.html            # Main web interface (Leaflet Map + Search + Auth Modal)
├── style.css             # Premium custom stylesheets (Glassmorphism layout)
├── boundary.js           # Compiled boundary coordinates (loaded locally to bypass CORS)
├── server.js             # Node.js + Express backend server
├── view_db.py            # Python interactive script to inspect and delete users
├── database.sqlite       # Local database file (created automatically on server start)
├── .gitignore            # Excludes temporary, system, and database files from GitHub
└── package.json          # Node.js project configuration and dependencies
```

---

## 🛠️ How the Database Works

Polisewa uses **SQLite** as its database system. Unlike traditional databases (like MySQL or PostgreSQL) which require separate server installations, SQLite is **serverless and file-based**.

### 1. File Location
All database tables and users are stored in a single binary file named **`database.sqlite`** created directly in the project directory when the server runs.
* **VM database vs. Host database**: The database inside your VMware VM is the **active database** because your Node.js server runs there. The project folder on your Windows host computer is a separate copy and does not receive user updates.

### 2. Table Schema
The database contains a `users` table configured as follows:

| Column Name | Data Type | Key / Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | Primary Key, Auto-increment | Unique identifier for each account |
| `name` | TEXT | Not Null | User's full name |
| `email` | TEXT | Unique, Not Null | Log-in address (forced lowercase & trimmed) |
| `phone` | TEXT | Not Null | User's phone number (e.g. +6012...) |
| `password` | TEXT | Not Null | Securely hashed password string |
| `role` | TEXT | Not Null (`student` / `landlord`) | Determines account interface capabilities |
| `extra` | TEXT | Nullable | *Student*: College name \| *Landlord*: Company name |

### 3. Password Hashing (Security)
For security, user passwords are **never** stored in plain text. 
* We use **`bcryptjs`** to automatically generate a cryptographic "salt" and hash passwords before inserting them into SQLite.
* During sign-in, the server reads the hash from the database and compares it mathematically with the input password.

---

## ⚙️ Setting Up and Running the Server (Inside VMware VM)

To run the backend and database on your Windows Server virtual machine:

### 1. First-time Setup
Install Node.js in your VM, open the Command Prompt/PowerShell in your project directory, and run:
```cmd
git pull origin main
npm install
```

### 2. Start the Web Server
Run the following command to start Node.js:
```cmd
npm start
```
*The server will boot up and listen on port **`3000`** on all network interfaces (`0.0.0.0`), allowing local and external connections.*

---

## 🌐 Deploying Publicly via Cloudflare Tunnels (For Users in Other Countries)

To allow users around the world to visit `polisewa.me` and write to your VM's database:

1. **Add Domain to Cloudflare**: Point your domain `polisewa.me` nameservers to your Cloudflare account.
2. **Create a Tunnel**: Go to the Cloudflare Zero Trust Dashboard $\rightarrow$ **Access** $\rightarrow$ **Tunnels** and create a tunnel (e.g. `polisewa-database`).
3. **Route Domain**: Under Hostname configurations, route `polisewa.me` and `www.polisewa.me` to:
   * **Service**: `HTTP`
   * **URL**: `localhost:3000`
4. **Run the Connector in VM**:
   * Go to the tunnel **Overview** tab, select **Windows** (64-bit), and copy the powershell command.
   * Run the command in an **Administrator PowerShell** inside your VM.
5. **Go Live**: Once the connector is connected (turns green in Cloudflare), anyone going to `https://polisewa.me` will be securely routed straight to your VM!

---

## 📊 Viewing and Deleting Users from the Database

Since SQLite is a binary file, you can manage it directly in your VM terminal using the custom Python tool we created:

### 1. How to run it:
Open your VM Command Prompt and run:
```cmd
python view_db.py
```

### 2. Options:
* **View Users**: The script prints a clean, formatted table of all registered student and landlord accounts.
* **Delete a User**: Type the **ID number** (e.g. `2` or `3`) of the user you want to delete and press Enter. Type `y` to confirm the deletion.
* **Exit**: Press `Enter` on an empty line to close the viewer.
