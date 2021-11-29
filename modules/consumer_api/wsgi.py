"""
UdaConnect App Microservice version
===================================

Service: ConsumerApi
"""

import json
import logging

from flask import Flask
import grpc
from kafka import KafkaConsumer

from app import db
from app.config import config_by_name
import location_pb2
import location_pb2_grpc
import person_pb2
import person_pb2_grpc


INSECURE_GRPC_CHANNEL = 'localhost:5005'
KAFKA_SERVER = 'kafka.default.svc.cluster.local:9092'
KAFKA_TOPIC = 'udaconnect'


def locationify(location):

    channel = grpc.insecure_channel(INSECURE_GRPC_CHANNEL)
    stub = location_pb2_grpc.LocationServiceStub(channel)
    locations = location_pb2.LocationsMessage(person_id=location['person_id'],
                                               creation_time=location['creation_time'],
                                               coord_lat=location['coord_lat'],
                                               coord_lang=location['coord_lang'])
    stub.Create(locations)
    logger.info('ConsumerApi::locationify(): success.')


def personify(person):

    channel = grpc.insecure_channel(INSECURE_GRPC_CHANNEL)
    stub = person_pb2_grpc.PersonServiceStub(channel)
    persons = person_pb2.PersonsMessage(first_name = person['first_name'],
                                         last_name = person['last_name'],
                                         company_name = person['company_name'])
    stub.Create(persons)
    logger.info('ConsumerApi::personify(): success.')


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-consumer-api")

app = Flask(__name__)
app.config.from_object(config_by_name['prod'])
db.init_app(app)

kafka_consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER])

for message in kafka_consumer:
    json_data = json.loads((message.value.decode('utf-8')))
    if all(['first_name' in json_data, 'last_name' in json_data,
             'company_name' in json_data]):
        # Person check: strict
        personify(json_data)
    elif 'coord_lat' in json_data or 'coord_long' in json_data:
        # Location check: lazy
        locationify(d_msg)
    else:
        logger.warning('ConsumerApi::mainloop: Invalid JSON data received.')
