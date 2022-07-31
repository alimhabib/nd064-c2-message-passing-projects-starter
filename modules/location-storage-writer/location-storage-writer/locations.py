from ast import Dict
from concurrent import futures
import datetime
import json
import socket

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from confluent_kafka import Producer 

import location_pb2_grpc

class LocationStorageWritersService(location_pb2_grpc.LocationStorageWriterServicer):
    @staticmethod
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def Create(self, request, context):
        conf = {"bootstrap.servers": "kafka-service:9092", 'group.id': "UdaConnect",
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}
        location: Dict = {
            "person_id" : request.person_id,
            "creation_time":datetime.utcnow(),
            "latitude":request.latitude,
            "longitude":request.longitude            
        }
        p = Producer(conf)
        p.poll(0)
        p.produce(f'Location_Creation', json.dump(location).encode('utf-8'), callback=LocationStorageWritersService.delivery_report)
        request.LocationRequest 

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    location_pb2_grpc.add_LocationStorageWriterServicer_to_server(
        LocationStorageWritersService(), server
    ) 
    server.add_insecure_port("[::]:5000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()