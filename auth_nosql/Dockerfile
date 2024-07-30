# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable to ensure the output is sent straight to the terminal (not buffered)
# ENV PYTHONUNBUFFERED=1

# Set environment variables for MongoDB
# ENV MONGO_HOST=mongodb
# ENV MONGO_PORT=27017
# ENV MONGO_DB=Microservice
# ENV MONGO_USER=root
# ENV MONGO_PASSWORD=XHyZVbDB8nRF9IYl 

# Run app.py when the container launches
CMD ["python", "app.py"]
