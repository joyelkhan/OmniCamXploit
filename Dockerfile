# OmniCamXploit Docker Container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY omnicamxploit.py .
COPY modules/ modules/

# Set entrypoint
ENTRYPOINT ["python", "omnicamxploit.py"]

# Default command (shows help)
CMD ["--help"]
