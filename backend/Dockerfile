# ============================================================
# ExtraaLearn Lead Conversion API
# ============================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are immediately displayed
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . .

# Define the command to start the application using Gunicorn with 4 worker processes
# - `-w 4`: Uses 4 worker processes for handling requests
# - `-b 0.0.0.0:7860`: Binds the server to port 7860 on all network interfaces
# - `app:app`: Runs the Flask app (assuming `app.py` contains the Flask instance named `app`)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]