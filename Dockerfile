FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code and protos
COPY server/*.py .
COPY server/openapi.yaml .
COPY protos/*.py protos/
COPY protos/__init__.py protos/

# Create an empty __init__.py if it doesn't exist
RUN touch protos/__init__.py

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/app

# Expose ports for gRPC and HTTP
EXPOSE 50051 8080

# Start both servers using a shell script
COPY server/start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"] 