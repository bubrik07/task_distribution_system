# Choosing the base image
FROM python:3.10

# Setting the working directory inside the container
WORKDIR /task_distribution_system

# Copying only the requirements.txt first to utilize cache for pip
COPY requirements.txt /task_distribution_system/

# Installing dependencies
RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copying the project files into the container
COPY . /task_distribution_system

# Exposing the port for Django
EXPOSE 8000

# Specifying the entrypoint script to be executed
ENTRYPOINT ["/bin/bash", "/task_distribution_system/entrypoint.sh"]

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]