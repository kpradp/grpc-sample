# gRPC Sample

This project demonstrates a gRPC service with both gRPC and HTTP/REST endpoints using Python. It includes a gRPC server with HTTP gateway support and API documentation.

## Summary

This project showcases:

### Core Features
- gRPC server implementation in Python
- HTTP/REST gateway for gRPC services
- Swagger UI for API documentation
- Interactive gRPC UI for testing
- Support for both gRPC and HTTP clients

### Integration Options
1. **Direct gRPC Access** (Port 50051):
   - Python clients using generated stubs
   - Node.js clients using proto loader
   - Any language with gRPC support

2. **HTTP Gateway** (Port 8080):
   - REST API endpoints
   - Swagger UI documentation
   - Standard HTTP/JSON interface

### Frontend Options
1. **Node.js Integration**:
   - Dynamic proto loading (recommended)
   - Generated JavaScript code
   - HTTP/REST client option

2. **FastAPI Integration**:
   - Python-based frontend
   - Uses same proto files as server
   - Template-based UI example

### Testing Tools
1. **gRPCUI**: Interactive web interface for gRPC
2. **grpcurl**: Command-line gRPC testing
3. **Swagger UI**: HTTP API documentation and testing
4. **curl**: HTTP endpoint testing

### Deployment
- Containerized using Podman/Docker
- Multi-service orchestration
- Environment-agnostic setup

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

## Proto Files Management

### Source Control
- Only commit the source `.proto` files
- DO NOT commit generated files (`*_pb2.py`, `*_pb2_grpc.py`)
- Generated files should be created locally in each environment

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

## Frontend Integration Options

### 1. Node.js Frontend

You can create a Node.js frontend using either the gRPC or HTTP endpoints. For gRPC, you have two options for handling proto files:

#### Option A: Using Proto Loader (Recommended)
1. Install required packages:
   ```bash
   npm install @grpc/grpc-js @grpc/proto-loader
   ```

2. Load proto file directly (no generation needed):
   ```javascript
   const grpc = require('@grpc/grpc-js');
   const protoLoader = require('@grpc/proto-loader');

   const PROTO_PATH = '../protos/services.proto';
   const packageDefinition = protoLoader.loadSync(PROTO_PATH);
   const services = grpc.loadPackageDefinition(packageDefinition);

   const client = new services.Greeter('localhost:50051', grpc.credentials.createInsecure());

   // Make gRPC call
   client.sayHello({ name: 'World' }, (err, response) => {
     console.log(response.message);
   });
   ```

#### Option B: Generate JavaScript Code
1. Install required packages:
   ```bash
   npm install @grpc/grpc-js grpc-tools
   ```

2. Generate JavaScript code from proto:
   ```bash
   grpc_tools_node_protoc \
       --js_out=import_style=commonjs,binary:./src \
       --grpc_out=grpc_js:./src \
       --proto_path=../protos \
       ../protos/services.proto
   ```

#### Using HTTP Gateway:
If you prefer to avoid proto files entirely, you can use the HTTP gateway:
```javascript
// GET request
fetch('http://localhost:8080/hello?name=World')
  .then(response => response.json())
  .then(data => console.log(data));

// POST request
fetch('http://localhost:8080/hello', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'World' })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### 2. FastAPI Frontend

FastAPI requires the same generated Python proto files as the gRPC server:

1. Generate Python files (if not already done):
   ```bash
   # From project root
   python -m grpc_tools.protoc \
       --proto_path=protos/ \
       --python_out=protos/ \
       --grpc_python_out=protos/ \
       protos/services.proto
   ```

2. Install FastAPI and dependencies:
   ```bash
   pip install fastapi uvicorn jinja2
   ```

3. Example FastAPI application:
   ```python
   from fastapi import FastAPI, Request
   from fastapi.templating import Jinja2Templates
   import grpc
   # Import the generated proto files
   from protos import services_pb2, services_pb2_grpc

   app = FastAPI()
   templates = Jinja2Templates(directory="templates")

   # Create gRPC channel
   channel = grpc.insecure_channel('localhost:50051')
   stub = services_pb2_grpc.GreeterStub(channel)

   @app.get("/")
   async def home(request: Request):
       return templates.TemplateResponse(
           "index.html",
           {"request": request}
       )

   @app.post("/greet")
   async def greet(name: str):
       # Use the generated proto classes
       response = stub.SayHello(services_pb2.HelloRequest(name=name))
       return {"message": response.message}
   ```

3. Example template (`templates/index.html`):
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>gRPC Greeter</title>
   </head>
   <body>
       <h1>gRPC Greeter</h1>
       <input type="text" id="name" placeholder="Enter name">
       <button onclick="greet()">Greet</button>
       <div id="result"></div>

       <script>
       async function greet() {
           const name = document.getElementById('name').value;
           const response = await fetch('/greet?name=' + name);
           const data = await response.json();
           document.getElementById('result').textContent = data.message;
       }
       </script>
   </body>
   </html>
   ```

Choose the frontend option that best fits your needs:
- Node.js: Good for complex SPAs, rich UI frameworks available
- FastAPI: Good for Python-centric development, simple setup
- HTTP Gateway: Use any frontend framework, simpler integration

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