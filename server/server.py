import grpc
import sys
import os
from concurrent import futures
from grpc_reflection.v1alpha import reflection

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protos import services_pb2
from protos import services_pb2_grpc

# Implement the Greeter service
class Greeter(services_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return services_pb2.HelloReply(message=f"Hello, {request.name}!")

# Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    
    # Enable reflection
    SERVICE_NAMES = (
        services_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port("[::]:50051")
    print("Server is running on port 50051...")
    print("gRPC reflection enabled. You can use grpcui to interact with the API.")
    print("To view API documentation, install grpcui and run:")
    print("grpcui -plaintext localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
