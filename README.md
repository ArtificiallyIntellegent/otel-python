# Dice Roller App with Jaeger Tracing

This repository contains a simple Python Flask application that simulates rolling a dice. The app is instrumented with OpenTelemetry to send trace data to a Jaeger instance, allowing you to visualize and monitor traces. This setup uses Docker Compose to run both the Python app and Jaeger.

## Files

- `docker-compose.yml`: Defines services for the Python application and Jaeger using Docker Compose.
- `app.py`: The Flask application that simulates rolling a dice and is configured to send tracing data to Jaeger.

## Requirements

- Docker
- Docker Compose

## How to Run the Application and View Traces in Jaeger

### Step 1: Clone the Repository

Start by cloning the repository and navigating into the directory:

```bash
git clone https://github.com/ArtificiallyIntellegent/otel-python.git
cd otel-python
```

### Step 2: Build and Start the Containers
Run the following command to build and start both the Python app and Jaeger using Docker Compose:
```
docker compose up --build

```
This command will:

 - Build the Python Flask app image.
 - Start the Flask app on http://127.0.0.1:5000
 - Start Jaeger, accessible on http://localhost:16686

Each request simulates rolling a dice, and a trace will be generated and sent to Jaeger.

### Step 4: View Traces in Jaeger
You can now view the traces in the Jaeger UI:

Open your browser and go to http://localhost:16686.
In the Service dropdown, look for dice-server (or unknown_service if the service name is not set).
You should be able to see the traces from your dice roll requests, with a roll operation representing the dice roll logic.

### Step 5: Stop the Application
When you're done, you can stop the services by running:

```
docker compose down
```
This will stop and remove all running containers.


