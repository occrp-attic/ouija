from flask import request
from werkzeug.exceptions import Forbidden

USER = 'user'
GUEST = 'guest'


def logged_in():
    return request.logged_in


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")


def tables():
    if not hasattr(request, '_tables'):
        from ouija.model import db
        request._tables = []
        for table in db.tables:
            if request.auth_admin:
                request._tables.append(table.name)
            elif len(request.auth_roles.intersection(table.roles)) > 0:
                request._tables.append(table.name)
    return request._tables


def table(table):
    from ouija.model.database import OuijaTable
    if isinstance(table, OuijaTable):
        table = table.name
    return table in tables()
