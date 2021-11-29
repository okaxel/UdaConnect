"""
UdaConnect App Microservice version
===================================

Service: gRPCApi
"""

from concurrent import futures
import json
import logging
from time import sleep

from flask import Flask
from geoalchemy2.functions import ST_Point
import grpc

from app import db
from app.udaconnect.models import Location, Person
from app.config import config_by_name
import location_pb2
import location_pb2_grpc
import person_pb2
import person_pb2_grpc


GRPC_INSECURE_PORT = '[::]:5005'
POOL_EXECUTOR_WORKER_COUNT = 2
SLEEP_DURATION = 86400 # secs


class LocationsServicer(location_pb2_grpc.LocationServiceServicer):


    def Create(self, request, context):

        request_value = {
            'person_id': request.person_id,
            'creation_time': request.creation_time,
            'coord_lat': request.coord_lat,
            'coord_lang': request.coord_lang,
        }
        location_data = location_pb2.LocationsMessage(**request_value)
        logger.info('New lcation protobuf object commited to db. Data: {}'.format(location_data))
        location_record = Location()
        location_record.person_id = location_data.person_id
        location_record.creation_time = location_data.creation_time
        location_record.coordinate = ST_Point(location_data.coord_lat, location_data.coord_lang)
        with app.app_context():
            db.session.add(location_record)
            db.session.commit()
        logger.info('Lcation committed successfully. Data: {}'.format(location_data))
        return location_data


class PersonsServicer(person_pb2_grpc.PersonServiceServicer):


    def Create(self, request, context):

        request_value = {
            'first_name': request.first_name,
            'last_name': request.last_name,
            'company_name': request.company_name,
        }
        person_data = person_pb2.PersonsMessage(**request_value)
        logger.info('New person protobuf object commited to db. Data: {}'.format(person_data))
        person_record = Person()
        person_record.first_name = person_data.first_name
        person_record.last_name = person_data.last_name
        person_record.company_name = person_data.company_name
        with app.app_context():
            db.session.add(person_record)
            db.session.commit()
        logger.info('Person committed successfully. Data: {}'.format(person_data))
        return person_data


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('udaconnect-grpc-api')

app = Flask(__name__)
app.config.from_object(config_by_name['prod'])
db.init_app(app)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=POOL_EXECUTOR_WORKER_COUNT))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationsServicer(), server)
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonsServicer(), server)

logger.info('Starting insecure port at: {}'.format(GRPC_INSECURE_PORT))
server.add_insecure_port(GRPC_INSECURE_PORT)
server.start()
mainloop_alive = True
while mainloop_alive:
    try:
        sleep(SLEEP_DURATION)
    except KeyboardInterrupt:
        mainloop_alive = False
server.stop(0)
