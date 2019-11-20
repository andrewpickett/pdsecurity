import datetime
import functools

import flask
import jwt

from pdsecurity_config import pdsecurity_config


def protect_with_jwt(f):
    """
    This is a decorator function for validating requests from the user to ensure they have a valid JWT token
    on them. If the JWT doesn't exist or is invalid, then flask will abort the request with a 401 status code.

    :param f: The function to decorate
    :return: The decorator for the function
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not check_jwt_filter(flask.request):
            flask.abort(401)

        return f(*args, **kwargs)

    return wrapper


def check_jwt_filter(request):
    """
    Validates that the request contains a valid JWT token.

    :param request: The request from the user to validate.
    :return: True if the request has a valid JWT token, False otherwise.
    """
    try:
        auth_token = get_jwt_token_from_request(request)
        auth_request = parse_jwt_token(auth_token)

        if auth_request and auth_request["iss"] == pdsecurity_config['jwt']['issuer'] and datetime.datetime.now() < datetime.datetime.fromtimestamp(auth_request["exp"]):
            # TODO: Save auth to some context? or at least just allow them in.
            pass
        else:
            raise KeyError("Couldn't parse claims and/or expired token detected.")
    except KeyError:
        return False

    return True


def get_jwt_object_from_request(request):
    return parse_jwt_token(get_jwt_token_from_request(request))


def get_jwt_token_from_request(request):
    header = request.headers["Authorization"]
    if header.startswith('Bearer '):
        return header.replace('Bearer ', '')
    else:
        raise KeyError("No valid JWT token available on request.")


def parse_jwt_token(jwt_token):
    """
    Decode the encoded JWT token into the object.

    :param jwt_token: The JWT token to decode
    :return: The decoded JWT object
    """
    try:
        return jwt.decode(jwt_token, pdsecurity_config['jwt']['secret_key'], algorithms=[pdsecurity_config['jwt']['algorithm']])
    except jwt.InvalidTokenError:
        return None
