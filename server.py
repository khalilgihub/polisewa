import os
import mysql.connector
import bcrypt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app, telling it to serve static files from the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS

# Database connection configuration for MariaDB
def get_db_connection():
    host = os.getenv('DB_HOST', '127.0.0.1')
    port = int(os.getenv('DB_PORT', 3306))
    database = os.getenv('DB_DATABASE', 'polisewa')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

# Create users table if it doesn't exist
def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('student', 'landlord') NOT NULL,
                extra TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        print("Users table initialized successfully in MariaDB.")
    except Exception as e:
        print("Error creating users table in MariaDB:", e)
    finally:
        if conn and conn.is_connected():
            conn.close()

# Initialize DB on startup
init_db()

# SIGN UP Endpoint
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role')
    extra = data.get('extra', '')

    if not all([name, email, phone, password, role]):
        return jsonify({'error': 'All primary fields (name, email, phone, password, role) are required.'}), 400

    email_lower = email.lower().strip()
    
    # Hash password using bcrypt
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert user and return the new ID
        cursor.execute('''
            INSERT INTO users (name, email, phone, password, role, extra)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email_lower, phone, hashed_password, role, extra))
        
        user_id = cursor.lastrowid
        conn.commit()

        return jsonify({
            'message': 'Account created and logged in successfully!',
            'userId': user_id,
            'user': {
                'id': user_id,
                'name': name,
                'email': email_lower,
                'phone': phone,
                'role': role,
                'extra': extra
            }
        }), 201

    except mysql.connector.Error as err:
        if err.errno == 1062:  # ER_DUP_ENTRY
            return jsonify({'error': 'An account with this email address already exists.'}), 409
        return jsonify({'error': 'Database error: ' + str(err)}), 500
    except Exception as e:
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# SIGN IN Endpoint
@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    email_lower = email.lower().strip()
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email_lower,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid email address or password.'}), 401
            
        # Verify the password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'error': 'Invalid email address or password.'}), 401
            
        # Omit password from the response
        del user['password']
        
        return jsonify({
            'message': 'Logged in successfully!',
            'user': user
        }), 200

    except Exception as e:
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# Fallback to serve index.html for undefined routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f"Polisewa Python local server running on port {port}")
    print(f"To access from other machines/VMs, use: http://<YOUR_IP_ADDRESS>:{port}")
    app.run(host='0.0.0.0', port=port)
