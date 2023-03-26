# Base image
FROM python:3.8-slim-buster

# Set the working directory in the container
# WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files to the container
COPY . .

EXPOSE 1234

# Set the command to run the Flask app
CMD ["python", "app.py"]