# Polisewa - Online Deployment Guide

This guide documents the online architecture of **Polisewa Map Search & Room Rental Platform**, utilizing **Microsoft Azure SQL Database** as the centralized cloud database.

---

## 1. Cloud Architecture

Unlike the local environment which runs on a local SQLite file, the online setup uses a single, centralized database in the cloud:

```
               +--------------------------------------+
               |          Azure SQL Database          |
               |  (polisewa.database.windows.net)     |
               +--------------------------------------+
                                   ^
                                   |
         +-------------------------+-------------------------+
         |                                                   |
+------------------+                               +------------------+
|     VM Server    |                               |   Local Laptop   |
| (Runs Node.js)   |                               |  (Development)   |
+------------------+                               +------------------+
```

---

## 2. Environment Configuration (`.env`)

To connect any server instance to the Azure SQL Database, create a `.env` file in the root directory:

```env
# Database Credentials
DB_SERVER=polisewa.database.windows.net
DB_DATABASE=polisewa
DB_USER=polisewa
DB_PASSWORD=Poli@sewa

# Server Port
PORT=3000
```

> [!WARNING]
> **Security Warning**: Do not commit the `.env` file containing passwords to GitHub. It is ignored by Git automatically via `.gitignore`.

---

## 3. Firewall Configuration

Azure SQL Databases block all incoming traffic by default. Any server attempting to connect must have its public IP address whitelisted in the Azure portal.

### Steps to Allow Access:
1. Log in to the **Azure Portal**.
2. Navigate to your **SQL Server** resource (`polisewa`).
3. Click on **Networking** under the **Security** tab in the left sidebar.
4. Under **Firewall rules**, add the IP address of the machine running the server:
   - **Laptop Range (Local Dev)**: Start IP `27.125.243.0` to End IP `27.125.243.255`
   - **VM Server**: IP `27.125.243.19`
5. Enable **"Allow Azure services and resources to access this server"** (allows other Azure hosting services to connect).
6. Click **Save**.

---

## 4. Running the Application

### VM Server Setup:
1. Pull the latest code on your VM:
   ```cmd
   git pull
   ```
2. Install dependencies:
   ```cmd
   npm install
   ```
3. Ensure `.env` is created and saved.
4. Start the server:
   ```cmd
   npm start
   ```

---

## 5. Viewing the Cloud Database

Because the database resides in the cloud, you can view and query it using the following methods:

### Method A: Azure Portal Query Editor (No Installation Required)
1. Go to your SQL Database `polisewa` in the Azure Portal.
2. Select **Query editor (preview)** from the left menu.
3. Log in with:
   - **Login**: `polisewa`
   - **Password**: `Poli@sewa`
4. Run queries directly in your browser:
   ```sql
   SELECT * FROM users;
   ```

### Method B: VS Code Extension (mssql)
1. Install the **SQL Server (mssql)** extension in VS Code.
2. Add a new connection profile with:
   - **Server name**: `polisewa.database.windows.net`
   - **Database**: `polisewa`
   - **Authentication Type**: SQL Login
   - **User name**: `polisewa`
   - **Password**: `Poli@sewa`
