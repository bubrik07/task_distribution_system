# Task Distribution System

### A task distribution project using Django and Celery for asynchronous task processing.

## Project Structure
```
task_distribution_system/
│
├── task_distribution_system/                     # Main module
│   ├── __init__.py                               # Module initialization
│   ├── asgi.py                                   # ASGI configuration for async servers (e.g., Daphne, Uvicorn)
│   ├── celery.py                                 # Celery configuration
│   ├── settings.py                               # Project settings (e.g., database, other parameters)
│   ├── urls.py                                   # URL configuration for your project
│   └── wsgi.py                                   # WSGI entry point for traditional servers (e.g., Gunicorn)
│
├── tasks/                                        # Task module
│   ├── __init__.py                               # Module initialization
│   ├── admin.py                                  # Admin configuration for tasks
│   ├── apps.py                                   # App configuration for tasks
│   ├── migrations/                               # Database migrations
│   │   ├── 0001_initial.py                       # Creating tables
│   │   ├── 0002_add_initial_task_status.py       # Filling task statuses
│   │   └── 0003_add_initial_task_priority.py     # Filling task priorities
│   ├── models.py                                 # Models for tasks
│   ├── serializer.py                             # Serializers for tasks
│   ├── tasks.py                                  # Task definitions (e.g., for Celery)
│   ├── tests.py                                  # Tests for tasks (do not used)
│   ├── urls.py                                   # URL configuration for tasks
│   └── views.py                                  # Views for tasks (tasks, executors, monitoring, statuses, priorities)
│
├── Dockerfile                                    # Dockerfile for building the container
├── docker-compose.yml                            # Docker Compose configuration
├── entrypoint.sh                                 # Container initialization script
├── manage.py                                     # Django command line script
├── requirements.txt                              # Python dependencies
└── swagger.py                                    # Swagger API documentation configuration
```


## Deploying the Project with Docker

### Step 1: Clone the Repository (to your local machine):
```
git clone https://github.com/yourusername/task_distribution_system.git
cd task_distribution_system
```

### Step 2: Set Up the Environment

Make sure you have Docker and Docker Compose installed. 
If you don't have them yet, you can follow the official installation guides:
    [Docker](https://www.docker.com/), 
    [Docker Compose](https://docs.docker.com/compose/)


### Step 3: Configure the Files

Ensure that your configuration files are correctly set up for Docker usage. 
All the necessary configurations should be in docker-compose.yml and Dockerfile.

### Step 4: Start the Containers

Run the project with Docker Compose:
```
docker-compose up --build
```
This command will build Docker images for the project and start the necessary containers. If everything is set up correctly, you will see messages indicating that the containers are running.

### Step 5: Access Swagger Documentation

If you have configured Swagger, you can access the API documentation at the following address:
```
http://localhost:8000/swagger/
```
