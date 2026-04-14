# from flask import Flask, request, jsonify
# import sqlite3
# import bcrypt
# import jwt
# import datetime

# app = Flask(__name__)

# SECRET_KEY = "mysecretkey"  # change in real apps

# # DB connection
# def get_db():
#     return sqlite3.connect("users.db")

# # Init DB
# def init_db():
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT,
#         password TEXT
#     )
#     """)
#     conn.commit()
#     conn.close()

# init_db()

# # ✅ Register (HASHED PASSWORD)
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data['username']
#     password = data['password']

#     # 🔐 hash password
#     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     conn = get_db()
#     cursor = conn.cursor()

#     query = "INSERT INTO users (username, password) VALUES (?, ?)"
#     cursor.execute(query, (username, hashed))

#     conn.commit()
#     conn.close()

#     return jsonify({"message": "User registered"})


# # ✅ Login (JWT TOKEN)
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data['username']
#     password = data['password']

#     conn = get_db()
#     cursor = conn.cursor()

#     query = "SELECT * FROM users WHERE username = ?"
#     cursor.execute(query, (username,))
#     user = cursor.fetchone()
#     conn.close()

#     if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
#         # 🔐 create token
#         token = jwt.encode({
#             "user": username,
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
#         }, SECRET_KEY, algorithm="HS256")

#         return jsonify({"token": token})
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401


# # 🔒 Protected route
# @app.route('/users', methods=['GET'])
# def get_users():
#     token = request.headers.get("Authorization")

#     if not token:
#         return jsonify({"message": "Token missing"}), 401

#     try:
#         jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#     except:
#         return jsonify({"message": "Invalid token"}), 401

#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username FROM users")
#     users = cursor.fetchall()
#     conn.close()

#     return jsonify({"users": users})


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

SECRET_KEY = "my_super_secret_key_123"


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data['username']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hashed))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"message": "User already exists"}), 400
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


# ✅ ADD ONLY THIS (no duplicate login above it)
@app.route('/login_insecure', methods=['POST'])
def login_insecure():
    data = request.get_json()

    username = data['username']
    password = data['password']

    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful (INSECURE)"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                return jsonify({"message": "Invalid token format"}), 401

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({"message": "Welcome! You accessed protected route"})


if __name__ == '__main__':
    app.run(debug=True)