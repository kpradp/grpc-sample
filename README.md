# gRPC Sample

This project demonstrates a gRPC service with both gRPC and HTTP/REST endpoints using Python. It includes a gRPC server with HTTP gateway support and API documentation.

## Project Structure

```
.
├── protos/
│   ├── services.proto    # Protocol buffer definitions
│   └── __init__.py      # Python package marker
├── server/
│   ├── server.py        # gRPC server implementation
│   ├── http_server.py   # HTTP gateway
│   ├── start.sh         # Script to start both servers
│   └── requirements.txt # Python dependencies
└── Dockerfile          # Container configuration
```

## Prerequisites

- Python 3.9+
- Podman or Docker
- grpcurl (for testing gRPC endpoints)
- curl (for testing HTTP endpoints)

## Setup and Running

### Local Development

1. Install dependencies:
   ```bash
   pip install -r server/requirements.txt
   ```

2. Run the servers using start script:
   ```bash
   cd server
   chmod +x start.sh
   ./start.sh
   ```

This will start:
- gRPC server on port 50051
- HTTP gateway on port 8080

### Running with Podman

1. Build the container:
   ```bash
   podman build -t grpc-server .
   ```

2. Run the container:
   ```bash
   podman run -p 50051:50051 -p 8080:8080 --name grpc-server-container grpc-server
   ```

## Testing the Service

### gRPC Testing (using grpcurl)

1. List available services:
   ```bash
   grpcurl -plaintext localhost:50051 list
   ```

2. Test the greeting service:
   ```bash
   grpcurl -plaintext -d '{"name": "World"}' localhost:50051 services.Greeter/SayHello
   ```

### HTTP Testing (using curl)

1. GET request:
   ```bash
   curl "http://localhost:8080/hello?name=World"
   ```

2. POST request:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"name":"World"}' \
        http://localhost:8080/hello
   ```

## API Documentation

### Swagger UI
- Access the Swagger UI documentation at: http://localhost:8080/docs
- Interactive API testing interface
- Request/response schema documentation
- Example requests

### gRPC Reflection
The server supports gRPC reflection, allowing tools like grpcurl to discover available services and methods automatically.

## Container Management

### Stop the container:
```bash
podman stop grpc-server-container
```

### Remove the container:
```bash
podman rm grpc-server-container
```

### Remove dangling images:
```bash
podman image prune -f
``` 