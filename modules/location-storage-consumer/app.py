import json
import socket
import sys 
from confluent_kafka import Consumer
from confluent_kafka.error import KafkaError,KafkaException

from services import LocationService
 


global running
running = True
conf = {"bootstrap.servers": "kafka-service:9092", 'group.id': "UdaConnect",
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                LocationService.create(json.loads(msg.value().decode('utf-8')))
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

def serve():
    running = True
    c = Consumer(conf)
    basic_consume_loop(c,["Location_Creation"])

if __name__ == "__main__":
    serve()