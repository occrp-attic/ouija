from flask import Blueprint
from apikit import jsonify, Pager
from werkzeug.exceptions import NotFound

from ouija import authz
from ouija.model import db, OuijaQuery

tables_api = Blueprint('tables', __name__)


@tables_api.route('/api/tables')
def index():
    tables = [t for t in db.tables if authz.table(t)]
    return jsonify({
        'results': tables,
        'total': len(tables)
    })


@tables_api.route('/api/table/<table_name>')
def view(table_name):
    table = db.get(table_name)
    if table is None:
        raise NotFound()
    authz.require(authz.table(table))
    return jsonify(table)


@tables_api.route('/api/table/<table_name>/rows')
def rows(table_name):
    table = db.get(table_name)
    if table is None:
        raise NotFound()
    authz.require(authz.table(table))
    q = OuijaQuery(db, {
        'columns': [{'table': table_name}]
    })
    return jsonify(Pager(q, table_name=table_name, _external=True))
