import sqlite3
import os

db_path = 'database.sqlite'

if not os.path.exists(db_path):
    print(f"Error: Database file '{db_path}' not found. Make sure the server has run at least once.")
    exit(1)

def print_users(cursor):
    cursor.execute("SELECT id, name, email, phone, role, extra FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("\nThe database is currently empty (no users registered yet).")
        return False
    else:
        print("\n" + "=" * 105)
        print(f"{'ID':<4} | {'Name':<20} | {'Email':<25} | {'Phone':<15} | {'Role':<10} | {'Extra Info':<20}")
        print("=" * 105)
        for user in users:
            uid, name, email, phone, role, extra = user
            name = (name[:17] + '...') if len(name) > 20 else name
            email = (email[:22] + '...') if len(email) > 25 else email
            extra = (extra[:17] + '...') if len(extra) > 20 else extra
            
            print(f"{uid:<4} | {name:<20} | {email:<25} | {phone:<15} | {role:<10} | {extra:<20}")
        print("=" * 105)
        return True

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    while True:
        has_users = print_users(cursor)
        
        if not has_users:
            break
            
        print("\nOptions:")
        print("  - Enter a User ID (number) to delete that user (e.g. '2')")
        print("  - Press [Enter] to exit")
        
        user_input = input("\nEnter choice: ").strip()
        
        if not user_input:
            break
            
        if user_input.isdigit():
            user_id = int(user_input)
            cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                confirm = input(f"Are you sure you want to delete user '{user[0]}' (ID: {user_id})? (y/n): ").strip().lower()
                if confirm == 'y':
                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                    print(f"\n>>> Success: User '{user[0]}' (ID: {user_id}) has been deleted.")
                else:
                    print("\n>>> Deletion cancelled.")
            else:
                print(f"\n>>> Error: No user found with ID {user_id}.")
        else:
            print("\n>>> Invalid input. Please enter a valid number ID or press Enter to exit.")
            
    conn.close()
    print("\nExited database viewer.")
except Exception as e:
    print("Error:", e)
