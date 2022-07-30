from app.locations.models import Connection, Location, Person  # noqa
from app.locations.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.locations.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
