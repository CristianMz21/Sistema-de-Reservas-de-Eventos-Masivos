# Sistema de Reservas de Eventos Masivos

Welcome to the **Sistema de Reservas** project! This is a robust web application built with **Django** and **Django REST Framework** designed to manage users, events, and reservations efficiently.

## 🚀 Key Features

-   **User Management**:
    -   Custom User Model extending `AbstractBaseUser` for maximum flexibility.
    -   UUID-based identification for security.
    -   Role-based access (Client, Organizer, Admin).
    -   Soft-delete functionality for user deactivation.
-   **Authentication**:
    -   Secure password handling via standard Django auth.
    -   JWT Authentication ready (configured in settings).
-   **Modular Architecture**:
    -   Separation of concerns: `usuarios`, `reservas`, `eventos`.

## 🛠 Technology Stack

-   **Python**: 3.12+
-   **Framework**: Django 6.0
-   **API**: Django REST Framework 3.16
-   **Database**: PostgreSQL
-   **Package Manager**: uv (recommended) or pip
-   **Linting/Formatting**: Ruff

## ⚙️ Installation & Setup

### 1. Prerequisites

Ensure you have Python and PostgreSQL installed on your system.

### 2. Clone the Repository

```bash
git clone https://github.com/CristianMz21/Sistema-de-Reservas-de-Eventos-Masivos.git
cd sistema-reservas
```

### 3. Environment Setup

This project uses `uv` for dependency management, but supports `pip` as well.

**Using uv (Recommended):**
```bash
uv sync
source .venv/bin/activate
```

**Using pip:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file in the project root based on `.env_example`:

```env
# Database Configuration
DB_NAME=nombre_de_tu_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Security
SECRET_KEY=tu_secret_key_super_segura
DEBUG=True
```

### 5. Database Migrations

Apply the migrations to create the database schema:

```bash
python manage.py migrate
```

## 🏃‍♂️ Usage

### Running the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`.

### API Endpoints

**Authentication (`/api/token/`)**

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/token/` | Obtain access & refresh tokens | ❌ No |
| `POST` | `/api/token/refresh/` | Refresh access token | ❌ No |

**Usuarios (`/api/usuarios/`)**

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/usuarios/` | List all users (Active only) | ✅ Yes |
| `POST` | `/api/usuarios/` | Register a new user | ❌ No (Public) |
| `GET` | `/api/usuarios/<uuid>/` | Retrieve user details | ✅ Yes |
| `PUT` | `/api/usuarios/<uuid>/` | Update user profile | ✅ Yes |
| `PATCH` | `/api/usuarios/<uuid>/` | Partial update | ✅ Yes |
| `DELETE` | `/api/usuarios/<uuid>/` | Soft delete user | ✅ Yes |

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
python manage.py test
```

## 📝 Development Guidelines

-   **Code Style**: This project uses `ruff` for code formatting and linting.
    ```bash
    ruff check .
    ruff format .
    ```
-   **Safe Constraints**: The `Usuario` model enforces unique emails and usernames for active accounts.

## 📂 Project Structure

```
sistema-reservas/
├── config/             # Project configuration (settings, urls)
├── usuarios/           # User management app (Models, Views, Serializers)
├── reservas/           # (Planned) Reservation logic
├── eventos/            # (Planned) Event management
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```
