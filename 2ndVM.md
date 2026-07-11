# Polisewa - Scaling with a Second VM (Load Balancing & High Availability)

This guide walks you through setting up a **second Virtual Machine (VM2)** on Azure and configuring it to work in an active-active load-balancing and failover configuration alongside your first VM (VM1) using **Cloudflare Tunnels**. 

By running the same tunnel token on both VMs, Cloudflare automatically distributes incoming visitor traffic between them and provides instant failover if one of the VMs crashes or undergoes maintenance.

---

## Architecture Overview

```
                        +----------------------+
                        |     polisewa.me      |
                        +----------------------+
                                   |
                         (Cloudflare Tunnel)
                       /                        \
            (Connector 1)                      (Connector 2)
                   /                                \
        +------------------+                 +------------------+
        |    VM 1 (Live)   |                 |    VM 2 (New)    |
        | (Port 3000 Node) |                 | (Port 3000 Node) |
        +------------------+                 +------------------+
                   \                                /
                    +---> [ Azure SQL Database ] <--+
```

---

## Step 1: Provision the Second Azure VM (VM2)
1. Log in to the **Azure Portal**.
2. Go to **Virtual Machines** and click **Create** -> **Azure Virtual Machine**.
3. Configure VM2 with the same settings as VM1:
   * **Resource Group**: `polisewa`
   * **Region**: Same as VM1 (e.g., `West US` or `West Europe`)
   * **OS Image**: Ubuntu or Debian (64-bit)
   * **Size**: Shared/Basic tier (e.g., Standard_B1s)
4. SSH into the new VM2 once it is created.

---

## Step 2: Deploy the Application on VM2
Run the following commands in the terminal of VM2 to pull the repository and install the application dependencies:

```bash
# 1. Update package list and install Node.js and Git
sudo apt update
sudo apt install -y nodejs npm git

# 2. Clone the repository
git clone https://github.com/khalilgihub/polisewa.git
cd polisewa

# 3. Install packages
npm install
```

---

## Step 3: Configure Environment Variables (.env) on VM2
Since the database connection string and credentials must be identical to VM1, create the `.env` file inside the `polisewa` directory of VM2:

```bash
cat << 'EOF' > .env
# Database Configuration (Azure SQL Database)
DB_SERVER=polisewa.database.windows.net
DB_DATABASE=polisewa
DB_USER=polisewa
DB_PASSWORD=Poli@sewa

# Server Configuration
PORT=3000
EOF
```

---

## Step 4: Run the Server under PM2 on VM2
Install PM2 globally on VM2 and start the application so it runs continuously in the background:

```bash
# 1. Install PM2 globally
sudo npm install -g pm2

# 2. Start the server
pm2 start server.js --name "polisewa"

# 3. Configure PM2 to start on boot
pm2 startup
pm2 save
```

---

## Step 5: Whitelist VM2 in Azure SQL Firewall
Azure SQL database needs to recognize the outbound IP address of VM2:
1. Navigate to your **SQL Server** (`polisewa`) in the Azure Portal.
2. Select **Networking** under the **Security** tab.
3. Ensure **"Allow Azure services and resources to access this server"** is checked.
4. If it is unchecked, retrieve VM2's outbound IP (by running `curl ifconfig.me` on VM2) and add it to the **Firewall rules**.
5. Click **Save**.

---

## Step 6: Connect VM2 to your Cloudflare Tunnel
Now, connect VM2 to the existing Cloudflare Tunnel so Cloudflare knows it can route traffic to this machine.

1. **Install cloudflared on VM2:**
   ```bash
   curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared.deb
   ```

2. **Register the connector using your specific tunnel token:**
   Run the following command exactly as shown:
   ```bash
   sudo cloudflared service install eyJhIjoiNTEyNDM1YjE5OTg1YzZkYjc4MDYyYTgyNjJhMjZmYzAiLCJ0IjoiMmRlNmY1ODYtMjlkYi00ZmIxLTg3ZWQtZjFlMzIxMDUwMjk2IiwicyI6IlpqY3hOMlpoTTJJdFl6RmpOQzAwWXpZMExUazVZV1l0TXpCbVpERTFOamxpWkdVNCJ9
   ```

3. **Verify the service is running:**
   ```bash
   sudo systemctl status cloudflared
   ```

---

## Step 7: Verify Active-Active Load Balancing
1. Open your **Cloudflare Zero Trust Dashboard** $\rightarrow$ **Access** $\rightarrow$ **Tunnels**.
2. Click on the `polisewa-database` tunnel.
3. You will see both connectors are listed and show a green **Active** status. 
4. **Test Failover:**
   * Run `pm2 stop polisewa` on **VM1**.
   * Visit `https://polisewa.me` in your browser. The website will still work because Cloudflare immediately routes all traffic to **VM2**.
   * Restart it back on VM1: `pm2 start polisewa`.
