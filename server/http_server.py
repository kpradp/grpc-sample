import json
from aiohttp import web
import grpc
import sys
import os
from aiohttp_swagger import setup_swagger

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protos import services_pb2
from protos import services_pb2_grpc

# Create a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
stub = services_pb2_grpc.GreeterStub(channel)

async def say_hello(request):
    try:
        # Get the name from query parameters or JSON body
        if request.method == 'GET':
            name = request.query.get('name', 'pp')
        else:
            data = await request.json()
            name = data.get('name', 'pp')

        # Make the gRPC call
        response = stub.SayHello(services_pb2.HelloRequest(name=name))
        
        # Return the response as JSON
        return web.Response(
            text=json.dumps({'message': response.message}),
            content_type='application/json'
        )
    except Exception as e:
        return web.Response(
            text=json.dumps({'error': str(e)}),
            status=500,
            content_type='application/json'
        )

async def init_app():
    app = web.Application()
    # Add routes for both GET and POST
    app.router.add_get('/hello', say_hello)
    app.router.add_post('/hello', say_hello)
    
    # Setup Swagger documentation
    setup_swagger(
        app,
        swagger_url="/docs",  # Swagger UI
        swagger_from_file="openapi.yaml",
        api_base_url='/',
        description="HTTP Gateway for gRPC Greeter Service",
        api_version="1.0.0",
        title="Greeter Service API",
        ui_version=2  # Use Swagger UI 2.x for better compatibility
    )
    
    return app

if __name__ == '__main__':
    web.run_app(init_app(), port=8080) 