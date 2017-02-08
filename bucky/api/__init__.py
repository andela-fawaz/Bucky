from flask import Blueprint
import bucketlists
import items
import errors
import authentication


def create_api():
    api = Blueprint('api', __name__, url_prefix='/api/v1.0')
    bucketlists.register_routes(api)
    items.register_routes(api)
    errors.register_routes(api)
    authentication.register_routes(api)
    return api


api = create_api()
