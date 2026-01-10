# SIP House Backend

This is a FastAPI-based backend for a SIP house construction company, designed to manage projects, images, completed projects, and customer messages. It features a robust database schema with SQLAlchemy, Alembic for migrations, and supports image uploads and PDF document handling.

## Key Features

- **Project Management**: Create, read, update, and delete construction projects with details like name, description, price, and associated PDF documents.
- **Image Management**: Handle multiple images for each project and completed project, including a flag for the main image and sorting capabilities.
- **Completed Projects Showcase**: Manage and display information about finished construction projects, including their addresses and associated images.
- **Customer Messaging**: Record and retrieve customer messages with details such as username, phone, email, object type, and comments.
- **File Uploads**: Supports uploading files (likely images and PDFs) for projects.
- **Database Migrations**: Utilizes Alembic for efficient and version-controlled database schema migrations.
- **API Endpoints**: Provides a structured RESTful API for interacting with project, image, message, and file resources.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapper (ORM) that gives application developers the full power and flexibility of SQL.
- **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy.
- **MySQL**: A popular open-source relational database management system (used via Docker).
- **uvicorn**: A lightning-fast ASGI server, for running the FastAPI application.
- **Pydantic**: Data validation and settings management using Python type hints.
- **Pillow**: The friendly PIL fork (Python Imaging Library), for image processing.
- **python-magic**: File type identification using `libmagic`.
- **aiofiles**: Support for Python's `async` and `await` keywords when working with files.
- **cryptography**: A package designed to provide cryptographic recipes and primitives to Python developers.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX.

## Setup Instructions

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/RKirill28/sip-house-backend
    cd sip-house-backend
    ```

2.  **Python Environment**:
    This project uses Python 3.13. It's recommended to use a virtual environment.

    ```bash
    python3.13 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    Install the project dependencies using `pip`:

    ```bash
    pip install -e .
    ```

4.  **Database Setup (MySQL with Docker)**:
    The project uses MySQL. You can easily set up a MySQL database using Docker and `docker-compose.yaml` file.

    ```bash
    docker-compose up -d db
    ```

    This will start a MySQL container with the following details:
    - Host: `localhost`
    - Port: `3306`
    - Root Password: `root`
    - Database Name: `sip-house`

5.  **Environment Variables**:
    Copy the `.env.template` file to `.env` and fill in the necessary environment variables.

    ```bash
    cp .env.template .env
    ```

    Make sure to configure your database connection string in the `.env` file according to your MySQL setup.

6.  **Run Database Migrations**:
    Apply the database migrations using Alembic:
    ```bash
    alembic upgrade head
    ```

## Running the Application

To run the FastAPI application, use `uvicorn`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation will be available at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

## API Endpoints

The application exposes a set of RESTful API endpoints for managing various resources:

- **/projects/**: Endpoints for managing construction projects (CRUD operations).
- **/images/**: Endpoints for handling image uploads and management.
- **/done_projects/**: Endpoints for managing completed construction projects.
- **/messages/**: Endpoints for submitting and retrieving customer messages.
- **/files/**: Endpoints for general file operations, likely related to uploads.

Detailed API documentation can be found at `/docs` or `/redoc` when the application is running.

