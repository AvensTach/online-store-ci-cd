# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disk and ensure console output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/