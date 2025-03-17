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
- grpcui (for interactive gRPC testing)
- Protocol Buffers compiler (protoc)

## Setup and Running

### Generate Python Code from Proto Files

Before running the server, you need to generate the Python code from the Protocol Buffer definition:

1. Install the Protocol Buffers compiler (protoc):
   ```bash
   # Mac
   brew install protobuf

   # Ubuntu/Debian
   apt-get install protobuf-compiler

   # CentOS/RHEL
   yum install protobuf-compiler
   ```

2. Generate Python files:
   ```bash
   # From project root
   python -m grpc_tools.protoc \
       --proto_path=protos/ \
       --python_out=protos/ \
       --grpc_python_out=protos/ \
       protos/services.proto
   ```

This will generate two files in the `protos` directory:
- `services_pb2.py`: Contains message classes
- `services_pb2_grpc.py`: Contains gRPC service classes

Note: You need to regenerate these files whenever you modify the `services.proto` file.

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

### Interactive gRPC Testing (using gRPCUI)

gRPCUI provides a web interface for interacting with gRPC services, making it easier to test your endpoints.

1. Install gRPCUI:
   ```bash
   # Mac
   brew install grpcui

   # Linux
   go install github.com/fullstorydev/grpcui/cmd/grpcui@latest
   ```

2. Start the gRPCUI web interface:
   ```bash
   grpcui -plaintext localhost:50051
   ```

This will open a web browser with an interactive UI where you can:
- View all available gRPC services and methods
- Create and send requests with a form interface
- See detailed request and response messages
- View real-time API documentation
- Test streaming endpoints

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
The server supports gRPC reflection, allowing tools like grpcurl and gRPCUI to discover available services and methods automatically.

### Testing Tools Comparison

1. **gRPCUI**
   - Web-based interactive interface
   - Best for development and testing
   - Visual form-based request builder
   - Real-time API documentation
   - Support for streaming endpoints

2. **grpcurl**
   - Command-line tool
   - Good for automation and scripts
   - Quick service inspection
   - Lightweight and fast

3. **Swagger UI**
   - Web-based REST API documentation
   - HTTP/REST endpoint testing
   - OpenAPI specification
   - Easy to share with team members

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