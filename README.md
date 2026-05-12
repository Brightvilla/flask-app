# Flask Inventory Management System

A modular REST API with a web frontend built with Flask, SQLAlchemy, and JWT authentication.  
Supports product management, stock tracking, inventory transactions, and role-based access control.

---

## Features

- JWT-based authentication (register, login, protected routes)
- Role-based access control (`admin` vs `user`)
- Full product CRUD with pagination and stock filtering
- Inventory stock-in / stock-out with transaction history
- Password hashing with Flask-Bcrypt
- Request validation with Marshmallow
- Interactive API docs via Swagger UI (Flasgger)
- Web UI (login, register, dashboard)
- Auto database creation and seeding on first run
- Environment-based configuration via `.env`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Flask 3.1 |
| Database ORM | SQLAlchemy, Flask-SQLAlchemy |
| Migrations | Flask-Migrate, Alembic |
| Authentication | Flask-JWT-Extended, PyJWT |
| Password Hashing | Flask-Bcrypt |
| Validation | Marshmallow |
| API Docs | Flasgger (Swagger UI) |
| Config | python-dotenv |

---

## Project Structure

```
flask-app/
├── app/
│   ├── __init__.py          # App factory, extensions init
│   ├── models/
│   │   ├── base.py          # BaseModel with id and created_at
│   │   ├── user.py          # User model
│   │   ├── products.py      # Product model
│   │   └── inventory.py     # InventoryTransaction model
│   ├── routes/
│   │   ├── auth.py          # /auth endpoints
│   │   ├── products.py      # /products endpoints
│   │   └── inventory.py     # /inventory endpoints
│   ├── schemas/
│   │   └── user_schema.py   # Marshmallow schemas
│   ├── utils/
│   │   └── decorators.py    # role_required decorator
│   └── templates/
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
├── config.py                # Config class (reads from .env)
├── run.py                   # Entry point — starts app and seeds DB
├── seed.py                  # Standalone DB reset + seed script
├── cleanup.py               # Removes pycache, .pyc, .sqlite3 files
├── requirements.txt
└── .env                     # Environment variables (not committed)
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- `python3-venv` or equivalent

### 2. Clone the repository

```bash
git clone https://github.com/aminSHARIFF/flask-app
cd flask-app
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-minimum-32-characters
JWT_SECRET_KEY=your-jwt-secret-key-minimum-32-characters
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
```

> For production, replace `SQLALCHEMY_DATABASE_URI` with a PostgreSQL or MySQL URI:
> ```
> SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:password@localhost:5432/dbname
> ```

### 6. Run the app

```bash
python run.py
```

On first run, this automatically:
- Creates all database tables
- Seeds two default users and three sample products

The app will be available at **http://127.0.0.1:5001**

---

## Default Credentials

| Role | Email | Password | Access |
|---|---|---|---|
| Admin | `admin@test.com` | `password` | Full access |
| User | `user@test.com` | `password` | View only |

---

## Web UI

| URL | Page |
|---|---|
| `http://127.0.0.1:5001/login` | Login |
| `http://127.0.0.1:5001/register` | Register |
| `http://127.0.0.1:5001/dashboard` | Dashboard (products + inventory controls) |
| `http://127.0.0.1:5001/apidocs` | Swagger API documentation |

---

## API Reference

All JSON responses follow this structure:
```json
{ "status": "success" | "error", "data": {}, "message": "" }
```

All protected routes require the header:
```
Authorization: Bearer <access_token>
```

---

### Auth — `/auth`

#### `POST /auth/register`
Register a new user.

**Body:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Validation:**
- `username`: 3–80 characters, must be unique
- `email`: valid email format, must be unique
- `password`: minimum 6 characters

**Response `201`:**
```json
{
  "status": "success",
  "message": "account created",
  "data": { "id": 1, "username": "john", "email": "john@example.com", "role": "user" }
}
```

---

#### `POST /auth/login`
Login and receive a JWT token.

**Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response `200`:**
```json
{
  "status": "success",
  "data": {
    "token": "<JWT_ACCESS_TOKEN>",
    "user": { "id": 1, "username": "john", "email": "john@example.com", "role": "user" }
  }
}
```

---

#### `GET /auth/me` 🔒
Returns the currently authenticated user.

**Response `200`:**
```json
{
  "status": "success",
  "data": { "id": 1, "username": "john", "email": "john@example.com", "role": "user" }
}
```

---

### Products — `/products`

#### `GET /products/`
Returns a paginated list of products. Public.

**Query params:**

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `limit` | int | 5 | Items per page |
| `min_stock` | int | — | Filter by minimum stock |
| `max_stock` | int | — | Filter by maximum stock |

**Response `200`:**
```json
{
  "status": "success",
  "data": [
    { "id": 1, "name": "Laptop", "price": 50000.0, "stock": 10 }
  ],
  "meta": { "page": 1, "limit": 5, "total": 3, "pages": 1 }
}
```

---

#### `GET /products/<id>`
Get a single product by ID. Public.

**Response `200`:**
```json
{
  "status": "success",
  "data": { "id": 1, "name": "Laptop", "price": 50000.0, "stock": 10 }
}
```

---

#### `POST /products/` 🔒 Admin only
Create a new product.

**Body:**
```json
{
  "name": "Monitor",
  "price": 15000,
  "stock": 5
}
```

**Response `201`:**
```json
{
  "status": "success",
  "message": "Product created successfully",
  "data": { "id": 4, "name": "Monitor", "price": 15000.0, "stock": 5 }
}
```

---

#### `PATCH /products/<id>` 🔒 Admin only
Update one or more fields of a product.

**Body (all fields optional):**
```json
{
  "name": "Gaming Monitor",
  "price": 18000,
  "stock": 8
}
```

**Response `200`:**
```json
{
  "status": "success",
  "message": "Product updated successfully",
  "data": { "id": 4, "name": "Gaming Monitor", "price": 18000.0, "stock": 8 }
}
```

---

#### `DELETE /products/<id>` 🔒 Admin only
Delete a product and all its inventory transactions.

**Response `200`:**
```json
{
  "status": "success",
  "message": "Product deleted successfully"
}
```

---

### Inventory — `/inventory`

#### `GET /inventory/`
Returns current stock levels for all products. Public.

**Response `200`:**
```json
{
  "status": "success",
  "data": [
    { "product_id": 1, "name": "Laptop", "stock": 10 }
  ]
}
```

---

#### `POST /inventory/in/<product_id>` 🔒 Admin only
Add stock to a product.

**Body:**
```json
{ "quantity": 10 }
```

**Response `200`:**
```json
{
  "status": "success",
  "message": "Added 10 units to stock",
  "data": { "product_id": 1, "name": "Laptop", "new_stock": 20 }
}
```

---

#### `POST /inventory/out/<product_id>` 🔒 Admin only
Remove stock from a product.

**Body:**
```json
{ "quantity": 3 }
```

**Response `200`:**
```json
{
  "status": "success",
  "message": "Removed 3 units from stock",
  "data": { "product_id": 1, "name": "Laptop", "new_stock": 17 }
}
```

> Returns `400` if quantity exceeds available stock.

---

#### `GET /inventory/transactions/<product_id>` 🔒
Returns the full transaction history for a product.

**Response `200`:**
```json
{
  "status": "success",
  "data": [
    { "id": 1, "quantity": 10, "type": "IN", "created_at": "2026-05-12T12:00:00" },
    { "id": 2, "quantity": 3, "type": "OUT", "created_at": "2026-05-12T13:00:00" }
  ]
}
```

---

## Role Permissions Summary

| Action | Admin | User |
|---|---|---|
| Register / Login | ✅ | ✅ |
| View products | ✅ | ✅ |
| View inventory | ✅ | ✅ |
| Create product | ✅ | ❌ |
| Update product | ✅ | ❌ |
| Delete product | ✅ | ❌ |
| Stock in / out | ✅ | ❌ |
| View transactions | ✅ | ✅ |

---

## Database Management

**Reset and re-seed the database:**
```bash
python seed.py
```
> This drops all tables, recreates them, and inserts fresh seed data.

**Clean up cache and build files:**
```bash
python cleanup.py
```

**Run migrations (if using Flask-Migrate):**
```bash
flask db init        # first time only
flask db migrate -m "describe change"
flask db upgrade
```

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Port 5000 is in use` | Another process on port 5000 | Run `flask run --port 5001` |
| `externally-managed-environment` | No virtual environment active | Run `source venv/bin/activate` |
| `401 Unauthorized` | Missing or expired token | Login again to get a new token |
| `403 Forbidden` | Logged in as `user`, not `admin` | Use admin credentials |

---

## License

MIT License

---

## Maintainer

**Group 9 Project**  
Email: brightmahonga7@gmail.com  
GitHub: https://github.com/aminSHARIFF/flask-app
