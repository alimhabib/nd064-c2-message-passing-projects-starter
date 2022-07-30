from app.locations.models import  Location # noqa
from app.locations.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.locations.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
