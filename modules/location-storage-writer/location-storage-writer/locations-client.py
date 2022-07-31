import grpc
import location_pb2_grpc as pb2_grpc
import location_pb2 as pb2
from location_pb2 import LocationRequest


class UnaryClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def Create(self, request):
        """
        Client function to call the rpc for Create
        """
        
        message = pb2.LocationRequest(request) 
        print(f'{message}')
        return self.stub.Create(message)

if __name__ == '__main__':
    client = UnaryClient()
    requet = LocationRequest(person_id=1, longitude="1.2.3",latitude="3.4.5")
    result = client.Create(requet)
    print(f'{result}')