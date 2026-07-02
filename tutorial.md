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

## 8. Step 7: View and Manage User Data
You can inspect the database content from the cloud without hosting anything locally:

1. Open the Azure Portal and click on your SQL Database `polisewa`.
2. Select **Query editor (preview)** from the left-hand sidebar menu.
3. Log in with your database credentials (`polisewa` / `Poli@sewa`).
4. In the text area, type and run:
   ```sql
   SELECT * FROM users;
   ```
5. You will see a table at the bottom displaying all registered user accounts.
