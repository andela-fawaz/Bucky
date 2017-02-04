# from functools import wraps
from flask import jsonify, g, request
from flask_httpauth import HTTPBasicAuth
from ..models import User
from ..exceptions import ValidationError
from .errors import bad_request, unauthorized
from .. import db


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user


@auth.error_handler
def auth_error():
    return unauthorized('Authentication Error.')


def register_routes(api):

    @api.route('/login', methods=['POST'])
    def login():
        # get the post data
        email = request.json.get('email')
        password = request.json.get('password')

        if email is None or email == '' or password is None or password == '':
            raise ValidationError('email and password required.')
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if not user:
            return auth_error()
        if not user.verify_password(password):
            return auth_error()
        g.current_user = user

        token = g.current_user.generate_auth_token(expiration=3600)
        return jsonify({
            'token': token.decode('ascii'),
            'expiration': 3600
        })

    @api.route('/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        if username is None or password is None or email is None:
            return ValidationError
        # check if username exists
        if User.query.filter_by(username=username).first() is not None:
            return bad_request('Username Exists!')

        # check if email esxists
        if User.query.filter_by(email=email).first() is not None:
            return bad_request('bad request')
        user = User(username=username, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username}), 201
