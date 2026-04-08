# Dockerfile for the ASDN Web Application — SOLUTION
# ====================================================

# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
# If requirements don't change, this layer is cached even when code changes
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/app.py .

# Expose the application port (documentation)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
