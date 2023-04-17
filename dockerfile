FROM python:3.10.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    nano

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Download Model
RUN git lfs install
RUN git clone https://huggingface.co/guillaumekln/faster-whisper-small

# RUN APP
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "wsgi:server"]