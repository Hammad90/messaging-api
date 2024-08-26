# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    dnsutils \
    curl \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /opt

# Copy the requirements file to the working directory
COPY requirements.txt /opt/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application code to the working directory
COPY . /opt/

# Expose the port your Django app runs on
EXPOSE 8000
WORKDIR /opt/messaging_app
# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
