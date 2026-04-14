# JWT-Based Authentication API using Flask

## Overview

This project is a secure REST API built using Flask that demonstrates user authentication and authorization using JSON Web Tokens (JWT). It allows users to register and log in securely, with passwords stored using hashing (bcrypt).

Once authenticated, users receive a JWT token, which must be included in requests to access protected endpoints. The API validates this token to ensure only authorized users can access sensitive routes.

The project focuses on implementing core security concepts such as password hashing, token-based authentication, and route protection in a simple and practical way. It is designed as a demonstration of backend security fundamentals commonly used in real-world applications.

---

## Features

* User Registration
* User Login
* Password Hashing using bcrypt
* JWT Token Generation
* Protected Routes (Token Required)

---

## Tech Stack

* Python (Flask)
* SQLite
* bcrypt
* PyJWT

---

## Tools Used
- Postman (API testing)

---

## Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd <project-folder>
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Create Database

```
python create_db.py
```

### 4. Run the application

```
python secure.py
```

---

## API Endpoints

### Register

```
POST /register
```

### Login

```
POST /login
```

### Protected Route

```
GET /protected
```

Requires JWT token in header:

```
Authorization: Bearer <your_token>
```

---

## Notes
- API can be tested using Postman
- Include JWT token in Authorization header for protected routes
- Database is created locally using create_db.py