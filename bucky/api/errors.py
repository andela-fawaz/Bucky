from flask import jsonify, make_response
from bucky.exceptions import ValidationError


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def register_routes(api):
    @api.errorhandler(ValidationError)
    def validation_error(e):
        return bad_request(e.args[0])

    @api.errorhandler(404)
    def not_found(error):
        print 'called'
        return make_response(jsonify({'error': 'Resource not found.'}), 404)
