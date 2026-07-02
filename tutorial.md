# Polisewa: A to Z Online Deployment Tutorial

This tutorial walks you through setting up, configuring, and deploying the **Polisewa Map Search & Room Rental Platform** from scratch using Node.js, Cloudflare, and Microsoft Azure SQL Database.

---

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Step 1: Create the Azure SQL Database](#step-1-create-the-azure-sql-database)
3. [Step 2: Configure Azure Database Firewall](#step-2-configure-azure-database-firewall)
4. [Step 3: Configure Environment Variables (.env)](#step-3-configure-environment-variables-env)
5. [Step 4: Run and Test Locally](#step-4-run-and-test-locally)
6. [Step 5: Pull and Set Up on Your VM](#step-5-pull-and-set-up-on-your-vm)
7. [Step 6: Connect your Domain (polisewa.me) via Cloudflare Tunnel](#step-6-connect-your-domain-polisewame-via-cloudflare-tunnel)
8. [Step 7: View and Manage User Data](#step-7-view-and-manage-user-data)

---

## 1. Prerequisites
Ensure you have the following installed/created:
- **Node.js** (LTS version recommended)
- **Git**
- **An active Azure account** (e.g., Azure for Students)
- **Cloudflare account** with the domain `polisewa.me` registered/configured

---

## 2. Step 1: Create the Azure SQL Database
1. Go to the [Azure Portal](https://portal.azure.com/).
2. Search for and select **SQL databases**, then click **Create**.
3. Fill in the following details:
   - **Resource group**: Create new or select `polisewa`
   - **Database name**: `polisewa`
   - **Server**: Click *Create new*
     - **Server name**: `polisewa` (final URL will be `polisewa.database.windows.net`)
     - **Location**: select your preferred region (e.g., `Malaysia West`)
     - **Authentication method**: Use `Use SQL authentication`
     - **Login username**: `polisewa`
     - **Password**: `Poli@sewa`
4. Set the **Pricing tier** to a basic or serverless tier (under "Azure for Students" budget).
5. Click **Review + create**, then **Create**.

---

## 3. Step 2: Configure Azure Database Firewall
By default, Azure SQL Database blocks all outside traffic. You must whitelist the IP addresses of both your **laptop** and **VM**.

1. Navigate to your newly created **SQL server** (`polisewa`) in the Azure portal.
2. Under **Security** in the left sidebar, click **Networking**.
3. Under **Firewall rules**, add:
   - **Your Laptop's IP Range** (Allows testing code from your laptop):
     - Rule Name: `Laptop_Range`
     - Start IP: `27.125.243.0`
     - End IP: `27.125.243.255`
   - **Your VM's IP** (Allows VM to connect):
     - Rule Name: `VM_IP`
     - Start IP: `27.125.243.19`
     - End IP: `27.125.243.19`
4. Tick **"Allow Azure services and resources to access this server"** (at the bottom).
5. Click **Save** at the bottom-left.

---

## 4. Step 3: Configure Environment Variables (.env)
Create a file named `.env` in the root folder of your project on both your laptop and your VM. Add the connection secrets:

```env
# Database Credentials
DB_SERVER=polisewa.database.windows.net
DB_DATABASE=polisewa
DB_USER=polisewa
DB_PASSWORD=Poli@sewa

# Node Server Configuration
PORT=3000
```
> [!IMPORTANT]
> The `.env` file should remain local and never be pushed to Git. Ensure `.env` is listed inside your `.gitignore`.

---

## 5. Step 4: Run and Test Locally
Before putting it online, test it on your laptop:
1. Open your terminal in the project directory.
2. Install the SQL Server driver and other dependencies:
   ```bash
   npm install
   ```
3. Start the local server:
   ```bash
   npm start
   ```
4. Verify the terminal outputs:
   - `Connected to Azure SQL Database at: polisewa.database.windows.net`
   - `Users table initialized successfully.`
5. Open `http://localhost:3000` in your browser and try signing up.

---

## 6. Step 5: Pull and Set Up on Your VM
Now, sync the files to your Virtual Machine (VM):
1. Log in to your VM and open the command prompt/terminal inside your `polisewa` directory.
2. Stop any running server (`Ctrl + C`).
3. Fetch the latest code changes from Git:
   ```cmd
   git pull
   ```
4. Make sure your `.env` file on the VM is saved with the correct database details.
5. Install packages:
   ```cmd
   npm install
   ```
6. Start the server on the VM:
   ```cmd
   npm start
   ```

---

## 7. Step 6: Connect your Domain (polisewa.me) via Cloudflare Tunnel
To make the application server running on your VM accessible via `polisewa.me`:

1. Open your **Cloudflare Dashboard** and navigate to **Zero Trust > Networks > Tunnels**.
2. Click **Create a Tunnel** (choose **cloudflared**).
3. Copy the installation command provided for Windows and run it directly in your VM's terminal to start the connector.
4. Under **Public Hostname** settings in Cloudflare:
   - **Subdomain**: (Leave blank or set to `www`)
   - **Domain**: `polisewa.me`
   - **Service Type**: `HTTP`
   - **URL**: `localhost:3000` (This points Cloudflare to your running Node.js server).
5. Click **Save Tunnel**. Now, visiting `polisewa.me` in any browser will route traffic directly to port `3000` on your VM.

---

## 8. Understanding the Connection Flow & `server.js`

For your online database to work, **`server.js` must be running 24/7**. If you close your terminal or stop the node process, your database connection goes offline, and visitors won't be able to register or sign in.

Here is how the data flow connects everything:

```
[ User Browser ]  =====>  [ polisewa.me ]  =====>  [ Node.js Server (server.js) ]  =====>  [ Azure SQL Database ]
(Types credentials)       (Cloudflare Tunnel)          (Listens on Port 3000)          (polisewa.database.windows.net)
```

1. **Frontend to Domain**: A user visits `polisewa.me`, fills in the signup form, and hits "Submit". The browser fires a web request (`/api/signup`).
2. **Domain to Backend**: Cloudflare routes this request through the tunnel to `localhost:3000` inside your VM, where `server.js` is listening.
3. **Backend to Azure DB**: `server.js` takes the input, hashes the password, connects securely to `polisewa.database.windows.net` using the password in your `.env` file, runs the INSERT query, and sends the confirmation back to the user.

---

## 9. Running `server.js` in the Background (24/7)

By default, running `npm start` occupies your terminal. If you close the terminal window, the server shuts down. To run `server.js` permanently in the background:

### Option A: Use PM2 (Recommended Process Manager)
1. Install PM2 globally on your VM:
   ```cmd
   npm install pm2 -g
   ```
2. Start the server using PM2 instead of npm start:
   ```cmd
   pm2 start server.js --name "polisewa"
   ```
3. To monitor, check status, or restart:
   - **Check running status**: `pm2 status`
   - **Restart server**: `pm2 restart polisewa`
   - **Stop server**: `pm2 stop polisewa`
   - **View logs**: `pm2 logs`

---

## 10. Step 7: View and Manage User Data
You can inspect the database content from the cloud without hosting anything locally:

1. Open the Azure Portal and click on your SQL Database `polisewa`.
2. Select **Query editor (preview)** from the left-hand sidebar menu.
3. Log in with your database credentials (`polisewa` / `Poli@sewa`).
4. In the text area, type and run:
   ```sql
   SELECT * FROM users;
   ```
5. You will see a table at the bottom displaying all registered user accounts.

---

## 11. What is inside `server.js`? (The Backend Code)

The `server.js` file is the brain of your backend. It handles all the database connections and processes the signup/signin requests. For the Azure SQL integration to work, `server.js` requires a few specific elements:

### 1. Dependencies (NPM Packages)
It imports essential libraries to function:
- `mssql`: Microsoft's official driver for connecting to Azure SQL Database.
- `dotenv`: Loads your passwords securely from the `.env` file so they aren't hardcoded in the script.
- `bcryptjs`: Encrypts (hashes) user passwords before saving them to the database.
- `express` & `cors`: Sets up the web server to handle HTTP POST requests from your front-end (`index.html`).

### 2. Azure Connection Pool
Instead of opening a new connection for every user, it creates a **Connection Pool** upon startup.
```javascript
const dbConfig = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: true, // Mandatory for Azure SQL
        trustServerCertificate: false
    }
};
const poolPromise = new sql.ConnectionPool(dbConfig).connect();
```
*Note: `encrypt: true` is strictly required for Azure databases to securely encrypt traffic.*

### 3. T-SQL Queries (Azure SQL Syntax)
Azure SQL uses **T-SQL** (Transact-SQL), which is different from your old SQLite setup. 
- **Auto-incrementing IDs**: Instead of SQLite's `AUTOINCREMENT`, Azure SQL uses `IDENTITY(1,1)`.
- **String Types**: Instead of `TEXT`, Azure SQL uses `NVARCHAR(255)`.
- **Insert Queries**: When inserting a user, we use `OUTPUT INSERTED.id` to retrieve the newly generated user ID.

### 4. Parameterized Inputs (Security)
To prevent SQL Injection hackers, the code never pastes user input directly into a query. It explicitly defines SQL parameters:
```javascript
await pool.request()
    .input('email', sql.NVarChar, email)
    .query('SELECT * FROM users WHERE email = @email');
```

### 5. Network Listener
At the very bottom, it listens on `0.0.0.0` rather than just `localhost`. This allows it to accept traffic routed from your Cloudflare Tunnel to the VM's internal network card:
```javascript
app.listen(PORT, '0.0.0.0', () => { ... });
```
