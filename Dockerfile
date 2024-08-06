# Use the official Python image from the Docker Hub
FROM python:3.12-bullseye AS base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Install pytest
RUN pip install pytest

# Run pytest
FROM base AS test
CMD ["pytest"]

# Final stage
FROM base AS final
CMD ["python", "pager/application/pager_application_service.py"]