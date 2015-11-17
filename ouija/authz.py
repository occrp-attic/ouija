from flask import request
from werkzeug.exceptions import Forbidden

USER = 'user'
GUEST = 'guest'


def logged_in():
    return request.logged_in


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
