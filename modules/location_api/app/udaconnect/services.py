"""
UdaConnect App Microservice version
===================================

Service: LocationApi
"""

# restructured import according to pylint suggestions
import logging
from typing import Dict

from geoalchemy2.functions import ST_AsText, ST_Point
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
from sqlalchemy.sql import text

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema


KAFKA_SERVER = 'kafka.default.svc.cluster.local:9092'
KAFKA_TOPIC = 'udaconnect'


class LocationService:


    @staticmethod
    def retrieve(location_id) -> Location:

        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )
        location.wkt_shape = coord_text
        return location


    @staticmethod
    def create(location: Dict) -> Location:

        # Kept old way for testing purposes.
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        # Kafka workflow
        try:
            kafka_producer.send(KAFKA_TOPIC, json.dumps(location).encode())
            kafka_producer.flush()
            logger.info('LocationService.create(): Kafka flush() seccessful.')
        except KafkaTimeoutError:
            logger.warning('LocationService.create(): Kafka flus() failed.')

        # Kept because of compatibility
        return new_location


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-api")
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
