import json
import socket
import sys 
from confluent_kafka import Consumer
from confluent_kafka.error import KafkaError,KafkaException

from services import LocationService
from confluent_kafka.admin import AdminClient, NewTopic


global running
running = True
conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname(), 'group.id': "UdaConnect",
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
    topic_list=["Location_Creation"]
    try:
        admin_client = AdminClient({ "bootstrap.servers": "localhost:9092"})
        admin_client.create_topics(topic_list)
    except:
        sys.stderr.write('Either the topic already exists or issue happened')

    basic_consume_loop(c,topic_list)

if __name__ == "__main__":
    serve()