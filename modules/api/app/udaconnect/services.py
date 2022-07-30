import json
import logging
from datetime import datetime, timedelta
import os
from typing import Dict, List
import requests
from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from confluent_kafka import Producer,Consumer
import socket

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")
conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}

locationServiceUrl = "http://localhost"

class ConnectionService:
    @staticmethod
    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    @staticmethod
    def add_connections_to_Kafka(person_id: int, connections: List[Connection]):
        """ A method to cach the connections. """
        p = Producer(conf)
        p.poll(0)
        p.produce(f'Person_{person_id}', json.dump(connections).encode('utf-8'), callback=ConnectionService.delivery_report)
    
    def get_connections_from_Kafka(person_id: int )->List[Connection]:
        """ A method to cach the connections. """
        c = Consumer(conf)
        c.subscribe(f'Person_{person_id}')
        msg = c.poll(1.0)  
        if msg is None:
            return []
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            return []
        result =json.loads(msg.value().decode('utf-8'))
        c.close() 
        return result

    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        

        result: List[Connection] = []
        result = ConnectionService.get_connections_from_Kafka(person_id)
        if len(result) == 0:
            # Cache all users in memory for quick lookup

            person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}

            location_apiUrl = f'{locationServiceUrl}:{os.environ["LOCATION_API_PORT"]}/api/locations/connectionslocations?person_id={person_id}&start_date={start_date}&end_date={end_date}&distance={meters}'
            response = requests.get(location_apiUrl)
            locations = json.loads(response.json())
            result: List[Connection] = []
            for location in locations:
                result.append(
                        Connection(
                            person=person_map[location.person_id], location=location,
                        )
                )       
            ConnectionService.add_connections_to_Kafka(person_id , result)
            return result
        else:
            return result

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
