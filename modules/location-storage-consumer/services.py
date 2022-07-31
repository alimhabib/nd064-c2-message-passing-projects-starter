    
from datetime import datetime, timedelta
import os
from typing import Dict, List
from models import Location
from schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point

import sqlalchemy as sa
import sqlalchemy.orm as orm
 
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = sa.create_engine( f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results: 
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        factory = orm.sessionmaker(bind=engine)
        session = factory()
        session.add(new_location)
        session.commit()
        return new_location 