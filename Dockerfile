# Use the official Python image
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
