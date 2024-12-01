# Auth API Service

`Auth API Service` is a simple authentication service built using **FastAPI** and **MongoDB**. It provides user authentication, token-based access, and token management functionalities.

## Usage

### 1. Clone the repository
```bash
git clone https://github.com/anant0059/auth-api-service.git
cd auth-api-service
```

### 2. Run the application using Docker Compose
```bash
docker-compose up --build
```

## API Endpoints

### 1. Sign Up - POST /signup
Create a new user with email and password.

Request:
```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"email": "newuser@example.com", "password": "password123"}'
```

Response:
```bash
{
  "message": "User created successfully",
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### 2. Sign In - POST /signin
Authenticate the user with email and password, returning a JWT token.

Request:
```bash
curl -X POST http://localhost:8000/signin -H "Content-Type: application/json" -d '{"email": "newuser@example.com", "password": "password123"}'
```

Response:
```bash
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### 3. Protected Endpoint - GET /protected-endpoint
Access a protected route by providing a valid JWT token.

Request:
```bash
curl -X GET http://localhost:8000/protected-endpoint -H "Authorization: Bearer <token>"
```

Response:
```bash
{
  "message": "Access granted",
  "user": "<user_data>"
}
```

### 4. Token Revocation - POST /revoke-token
Revoke a token so that it can no longer be used for authentication.

Request:
```bash
curl -X POST http://localhost:8000/revoke-token -H "Authorization: Bearer <token>"
```

Response:
```bash
{
  "message": "Token revoked successfully"
}
```

### 5. Refresh Token - POST /refresh-token
Refresh an expired token to get a new valid token.

Request:
```bash
curl -X POST http://localhost:8000/refresh-token -H "Authorization: Bearer <token>"
```

Response:
```bash
{
  "access_token": "<new_token>",
  "token_type": "bearer"
}
```

### Stopping the Application
To stop the application, run the following command:
```bash
docker-compose down
```
