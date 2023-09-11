FROM python:3.8-slim-buster

# Create working directory
WORKDIR /app

# Install pre-dependencies and dependecies
COPY requirements.txt ./
RUN apt-get update && apt-get install -y cargo
RUN pip install -r requirements.txt

# Copy the app code
COPY . .

# Expose the port
EXPOSE 5000

# Define the environment variable for Flask app
ENV FLASK_APP=app.py

# Run the Flask app
CMD flask run --host=0.0.0.0