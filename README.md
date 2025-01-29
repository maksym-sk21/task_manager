# Task Manager Application

Task Manager is a task management web application developed in Django using PostgreSQL and deployed in Docker.

## Functionality
- Create/update/delete projects.
- Add tasks to project.
- Update/delete tasks.
- Prioritize tasks into a project.
- Choose deadline for tasks.
- Mark a task as 'done'.

## Technologies Used
- Python 3
- Django — the main framework for the web application
- PostgreSQL — database
- Docker and docker-compose — for containerization
- For a full list of dependencies, check the requirements.txt file.

## Steps to run the application

### 1. Clone repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/maksym-sk21/task_manager.git
cd task_manager
```

### 2. Configure environment variables

Rename example.env to .env and update the POSTGRES_PASSWORD variable:

```bash
mv example.env .env  # Linux/macOS
ren example.env .env  # Windows
```

### 3. Run Docker

To start the application, use the following command:

```bash
docker-compose up --build
```

This command will:
- Build and run the containers
- Apply database migrations
- Start the web server

Once started, the application will be available at http://localhost:8000

## Tests

To run the tests, use the following command:

```bash
docker-compose run web python manage.py test
```
