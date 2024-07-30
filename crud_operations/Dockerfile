FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5002

# # Define environment variable
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["python", "/app/app.py"]
