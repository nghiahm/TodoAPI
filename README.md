# TodoAPI

## Introduction
TodoAPI is a simple RESTful API built with Django REST Framework. The project uses Docker for containerization, Makefile for automation, and Pre-commit for code quality enforcement.

## Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)
- [Pre-commit](https://pre-commit.com/)

## Installation and Setup

### 1️. Clone the Repository
```sh
git clone https://github.com/nghiahm/TodoAPI.git
cd TodoAPI
```

### 2️. Configure Environment Variables
Copy the sample environment file and modify it if necessary:
```sh
```

### 3. Run the Application
Build and start the application using Docker:
```sh
make build
make start
```

### 4. Apply Migrations and Create Superuser (Optional)
```sh
make migrate
make createsuperuser
```

### 5. Run Pre-commit Hooks
Ensure the code follows quality standards:
```sh
pre-commit install
pre-commit run --all-files # Optional
```

### 6. Access the Application
Admin page will be available at:
```sh
http://localhost:8000/admin
```

## Running Tests
Run tests inside the Docker container:
```sh
make test
```
