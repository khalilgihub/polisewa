# 🚀 Polisewa - Changelog & New Features Summary

This document summarizes all the new features, UI redesigns, security enhancements, and system upgrades implemented today.

---

## 1. ✉️ 6-Digit OTP Email Verification System
- **Gmail SMTP Integration (`nodemailer`)**:
  - Integrated with the official app email: **`polisewa.official@gmail.com`**.
  - Configured over secure **SSL (Port 465)** for reliable cloud VM and localhost delivery.
  - Generates secure random **6-digit OTP codes** with a **10-minute expiration**.
- **Modern 6-Box Grid UI (`index.html` & `style.css`)**:
  - Replaced single input field with **6 individual digit boxes** (`[ ][ ][ ][ ][ ][ ]`).
  - **Auto-Advance**: Typing automatically moves to the next box.
  - **Backspace Auto-Retreat**: Deleting moves focus back to previous box.
  - **Smart Clipboard Paste**: Pasting a 6-digit code automatically distributes digits across all 6 boxes and submits instantly.
  - **60-Second Cooldown Timer**: Shows countdown timer (*"Resend in 45s"*) to prevent spamming.
- **Anti-Spam & Deliverability Optimization**:
  - Added clean `Reply-To`, `From: Polisewa Support`, and matched plaintext/HTML bodies.
  - Built-in in-modal and in-email helper tips instructing users to mark *"Report not spam"*, successfully warming up Google's spam filter for direct Primary Inbox delivery.
- **Database Schema Upgrades (`server.js`)**:
  - Added `is_verified` (INT, default `0`), `otp_code` (NVARCHAR), and `otp_expires_at` (DATETIME) to `users` table in both **Azure SQL** and **SQLite**.
- **New REST API Endpoints**:
  - `POST /api/verify-otp` – Validates code and marks account verified.
  - `POST /api/resend-otp` – Generates and dispatches a fresh OTP code.
  - `POST /api/signup` – Creates unverified user and triggers verification.
  - `POST /api/signin` – Detects unverified status and prompts instant OTP verification.

---

## 2. 🔍 Unified Search & UI Bug Fixes
- **Decoupled Floating Dropdown Architecture**:
  - Fixed the distorted/oval search box bug where results caused the container to stretch into an egg shape.
  - The search input bar retains a clean pill shape (`border-radius: 9999px`), while results float below in an independent elevated card (`position: absolute; border-radius: 16px; box-shadow: ...`).
- **Dual Query Results**:
  - Live 250ms debounced search combining **Registered Landlord Properties** (name, description, landlord, price) and **OpenStreetMap Nominatim Places** in Kuching.
  - Grouped with sticky category headers (`🏠 Rental Properties` and `📍 Kuching Locations`).
  - Clicking any property zooms the map directly to the marker and opens its detailed popup.

---

## 3. 📝 Mandatory Property Listing Validation
- **Client-Side Enforcement**:
  - Added required red asterisks (`*`) to all property input fields (Title, Description, Monthly Rent, Contact Number, Photos).
  - Explicit validation prevents submitting empty strings, invalid or negative prices, and missing photo uploads.
- **Server-Side Enforcement**:
  - `POST /api/properties` and `PUT /api/properties/:id` strictly validate that all fields and at least one image are present before saving to Azure SQL or SQLite.

---

## 4. 📸 Multi-Photo Property Uploads
- Supported up to 10 property photos uploaded simultaneously via `multer` (`POST /api/properties/upload-images`).
- Responsive image previews in detail drawers and Leaflet map popups.

---

## 5. 🗑️ Permanent Account Deletion
- Secure account deletion endpoint (`DELETE /api/user`) requiring user password verification.
- Automatically cascades and cleans up all listings and uploaded property images from the disk.

---

## 6. 📄 Documentation & Repo Maintenance
- Complete update of **`README.md`** with up-to-date API endpoints, database schemas, feature overviews, and PM2 deployment instructions.
- All code formatted, tested, committed, and pushed to `main` at **https://github.com/khalilgihub/polisewa.git**.
