# Gemini Code Assistant Context: `sistema-reservas`

This document provides context for the Gemini code assistant to understand and effectively assist with development tasks in the `sistema-reservas` project.

## Project Overview

This is a web application for managing reservations, built with the Django framework in Python.

The project is in an early stage of development. It is organized into several logical applications: `usuarios`, `reservas`, and `eventos`. Currently, only the `usuarios` application has a defined data model and basic API endpoints. The other applications (`reservas`, `eventos`) appear to be placeholders for future development.

### Key Technologies

*   **Backend:** Django
*   **API:** Django REST Framework
*   **Database:** PostgreSQL (using the `psycopg` driver)
*   **Dependencies:** Managed in `requirements.txt`.
*   **Code Style:** `ruff` is likely used for linting and formatting, as indicated by the `.ruff_cache` directory.

### Architecture

*   **Project Root:** The `config` directory acts as the main project configuration, handling settings (`settings.py`) and root URL routing (`urls.py`).
*   **`usuarios` app:** This app implements a custom user model (`models.py:Usuario`) instead of Django's built-in `User` model. It handles password hashing manually using `bcrypt`. It exposes a RESTful API endpoint for user management at `/api/usuarios/`.
*   **`reservas` & `eventos` apps:** These apps are included in `INSTALLED_APPS` but do not contain any models or views yet. They are intended to hold the logic for reservations and events, respectively.
*   **Environment Configuration:** Database credentials and other secrets are intended to be loaded from a `.env` file at the project root, as seen in `config/settings.py`.

## Building and Running

### 1. Initial Setup

**Install Dependencies:**
It is recommended to use a virtual environment. The project uses `uv`, but `pip` can also be used.

```sh
# Using uv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

**Configure Environment:**
Create a `.env` file in the project root. The database connection depends on it.

```env
# .env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Database Migration

Once the environment is configured, apply the database migrations to set up the schema.

```sh
python manage.py migrate
```

### 3. Running the Development Server

Start the Django development server.

```sh
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000`.

*   The admin panel is at `/admin/`.
*   The user API is at `/api/usuarios/`.
*   The user-related web views are under `/user/`.

### 4. Running Tests

Execute the test suite for the project.

```sh
python manage.py test
```

## Development Conventions

*   **Modular Design:** The project is structured into discrete Django apps. New features should be organized into the most relevant app or a new app if necessary.
*   **Custom User Model:** All user-related logic must work with the `usuarios.models.Usuario` model, not the default Django user. Authentication logic is custom and uses the `check_password` and `set_password` methods on the model.
*   **API Development:** For new API endpoints, use Django REST Framework and register new `ViewSet`s in the appropriate `urls.py` or in the root `config/urls.py`.
*   **Secret Management:** Do not hard-code secrets like database passwords. Use the `.env` file for all environment-specific variables.
*   **Code Formatting:** Run `ruff format .` and `ruff check .` before committing to maintain code quality.
