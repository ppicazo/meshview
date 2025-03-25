# Use a base image like `python:3.9-slim`
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DATABASE_CONNECTION_STRING=postgresql+asyncpg://user:password@db:5432/meshview
ENV MQTT_SERVER=mqtt.example.com
ENV MQTT_PORT=1883
ENV MQTT_TOPICS='["topic1", "topic2"]'
ENV MQTT_USERNAME=username
ENV MQTT_PASSWORD=password
ENV BIND_ADDRESS=0.0.0.0
ENV STATIC_PATH=/app/static

# Define the command to run the application
CMD ["python", "mvrun.py"]
