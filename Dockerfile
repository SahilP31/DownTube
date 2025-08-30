# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg

# Create the videos directory and set permissions
RUN mkdir -p /app/videos && chmod -R 777 /app/videos

# Copy all necessary files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Command to run your application
CMD ["streamlit", "run", "main.py"]
