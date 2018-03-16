import traceback
from functools import wraps

from flask import current_app, request, jsonify

from helper import Helper
from models import User
from constants import json_tag, malformed_request


def expiration_check(f):
    """A decorator for checking if the user's token has expired

    Keyword arguments:
    f -- The incoming function to be wrapped.

    Return the wrapper function.
    """
    @wraps(f)
    def wrapper(claims, *args, **kwargs):
        try:
            token = claims['auth_token']
            token_user = User.verify_auth_token(token)
            if token_user is None:
                return jsonify(error="token expired"), 401, json_tag
            return f(claims, token_user, *args, **kwargs)
        except Exception as e:
            current_app.logger.error(str(e))
            return jsonify(error="token expired."), 401, json_tag
    return wrapper


def protected(f):
    """A decorator for checking if the incoming request has a valid JWT.

    Keyword arguments:
    f -- The incoming function to be wrapped.

    Returns the wrapper function.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        claims = None
        try:
            claims = Helper.verify_jwt(request)
            return f(claims, *args, **kwargs)
        except Exception:
            if not current_app.testing:
                current_app.logger.error(traceback.format_exc())
            return malformed_request()
    return wrapper
