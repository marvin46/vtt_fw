FROM python:3.10.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano

# Set working directory
WORKDIR /app

# Create log directory
RUN mkdir -p /var/log/gunicorn

# Copy source code
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# handle error log gunicorn
RUN touch /var/log/gunicorn/error.log && \
    chmod 777 /var/log/gunicorn/error.log