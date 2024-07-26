# Use Python Alpine base image
FROM python:3.11-alpine

# Install dependencies
RUN apk update \
    && apk add --no-cache git postgresql postgresql-client postgresql-dev gcc python3-dev musl-dev su-exec libffi-dev

# Set environment variables for PostgreSQL
ENV PGDATA=/var/lib/postgresql/data   

# Create necessary directories and set permissions
RUN mkdir -p /var/lib/postgresql/data /var/run/postgresql \
    && chown -R postgres:postgres /var/lib/postgresql /var/run/postgresql

# Switch to the postgres user
USER postgres

# Initialize the PostgreSQL database
RUN initdb -D /var/lib/postgresql/data

# Switch back to root to install Python dependencies
USER root

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 for Flask and 5432 for PostgreSQL
EXPOSE 5000 5432

# Command to start PostgreSQL and the Flask application
CMD ["sh", "-c", "su-exec postgres pg_ctl start -D /var/lib/postgresql/data && sleep 5 && su-exec postgres psql --command 'CREATE DATABASE Microservice;' && exec flask run --host=0.0.0.0"]
