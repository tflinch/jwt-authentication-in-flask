# Flask Authentication API
This project is a Flask-based authentication API that includes JWT token generation and validation, user signup and login, and secure access to a VIP lounge endpoint using custom middleware.

## Table of Contents
- Installation
- Environment Variables
- Usage
- API Endpoints
## Installation
### Prerequisites
Ensure you have the following installed:

- Python 3.7 or later
- Pipenv (for dependency management)
- PostgreSQL (for database)
## Setup
Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
Create a Pipenv virtual environment and install dependencies:
```
```bash
pipenv install --dev
```
This will install all the dependencies listed in the Pipfile.

Activate the Pipenv shell:

```bash
pipenv shell
```
This command will activate the virtual environment, and your terminal prompt should change to indicate that you are now inside the Pipenv shell.

Environment Variables
Create a .env file in the root of your project and add the following environment variables:

```bash
POSTGRES_USERNAME=<your-postgres-username>
POSTGRES_PASSWORD=<your-postgres-password>
JWT_SECRET=<your-secret-key>
```
Replace the placeholders with your actual PostgreSQL credentials and a secret key for JWT encoding.

Usage
Running the Flask App
Start the PostgreSQL database server if it's not already running.

Run the Flask application:

```bash
python app.py
```
The server will start running on http://127.0.0.1:5000/.

Database Setup
Ensure that your PostgreSQL database is set up with a users table. You can create it using the following SQL command:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```
API Endpoints
1. GET /sign-token
Generates a JWT token for a mock user.

Response:

```json
{
    "token": "<jwt-token>"
}
```
2. POST /auth/signup
Registers a new user and returns a JWT token.

Request Body:

```json
{
    "username": "testuser",
    "password": "password123"
}
```
Response:

```json
{
    "token": "<jwt-token>",
    "user": {
        "username": "testuser"
    }
}
```
3. POST /auth/signin
Signs in a user and returns a JWT token.

Request Body:

```json
{
    "username": "testuser",
    "password": "password123"
}
```
Response:

```json
{
    "message": "Successful credentials.",
    "token": "<jwt-token>"
}
```
4. POST /verify-token
Verifies a JWT token and returns the user data.

Headers:

```json
{
    "Authorization": "Bearer <jwt-token>"
}
```
Response:

```json
{
    "user": {
        "username": "testuser",
        "id": 1
    }
}
```
5. GET /vip-lounge
Access a protected route that requires a valid JWT token.

Headers:

```json
{
    "Authorization": "Bearer <jwt-token>"
}
```
Response:

```json
"Welcome to the party, testuser"
```