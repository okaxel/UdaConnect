"""
UdaConnect App Microservice version
===================================

Service: LocationApi
"""

# restructured import according to pylint suggestions
from marshmallow import Schema, fields

from app.udaconnect.models import Location


class LocationSchema(Schema):

    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location
