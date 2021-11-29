"""
UdaConnect App Microservice version
===================================

Service: gRPCApi
"""

import grpc
import location_pb2
import location_pb2_grpc
import person_pb2
import person_pb2_grpc


INSECURE_GRPC_CHANNEL = 'localhost:5005'


print('Setting up gRPC connection and data...')
grpc_channel = grpc.insecure_channel(INSECURE_GRPC_CHANNEL)
location_test_stub = locations_pb2_grpc.LocationServiceStub(grpc_channel)
person_test_stub = persons_pb2_grpc.PersonServiceStub(grpc_channel)
sample_location = location_pb2.LocationsMessage(person_id=21,
                                                creation_time='Mon, 29 Nov 2021 22:20:10 GMT',
                                                latitude='47.0000',
                                                longitude='19.0000')
sample_person = persons_pb2.PersonsMessage(id = 1,
                                           first_name = 'Axel',
                                           last_name = 'Orszag-krisz Dr.',
                                           company_name = 'Udacity Student')
print('Creating messages...')
response = location_test_stub.Create(sample_location)
print('--- Server response (sample location): {}'.format(response))
response = person_test_stub.Create(sample_person)
print('--- Server response (sample person): {}'.format(response))
print('Test finished.')
