import sqlite3
import os

db_path = 'database.sqlite'

if not os.path.exists(db_path):
    print(f"Error: Database file '{db_path}' not found. Make sure the server has run at least once.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to fetch all users
    cursor.execute("SELECT id, name, email, phone, role, extra FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("The database is currently empty (no users registered yet).")
    else:
        print("=" * 105)
        print(f"{'ID':<4} | {'Name':<20} | {'Email':<25} | {'Phone':<15} | {'Role':<10} | {'Extra Info':<20}")
        print("=" * 105)
        for user in users:
            uid, name, email, phone, role, extra = user
            # Truncate strings if they are too long for the table display
            name = (name[:17] + '...') if len(name) > 20 else name
            email = (email[:22] + '...') if len(email) > 25 else email
            extra = (extra[:17] + '...') if len(extra) > 20 else extra
            
            print(f"{uid:<4} | {name:<20} | {email:<25} | {phone:<15} | {role:<10} | {extra:<20}")
        print("=" * 105)
        
    conn.close()
except Exception as e:
    print("Error reading database:", e)
