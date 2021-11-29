"""
UdaConnect App Microservice version
===================================

Service: PersonAndConnectionApi
"""

from app.udaconnect.models import Connection, Person
from app.udaconnect.schemas import ConnectionSchema, PersonSchema


def register_routes(api, app, root="api"):

    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
