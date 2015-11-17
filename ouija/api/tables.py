from flask import Blueprint
from apikit import jsonify, Pager
from werkzeug.exceptions import NotFound

from ouija.model import db
from ouija.util import QueryPager

tables_api = Blueprint('tables', __name__)


@tables_api.route('/api/tables')
def index():
    return jsonify({
        'results': db.tables,
        'total': len(db.tables)
    })


@tables_api.route('/api/table/<table_name>')
def view(table_name):
    table = db.by_name(table_name)
    if table is None:
        raise NotFound()
    return jsonify(table)


@tables_api.route('/api/table/<table_name>/rows')
def rows(table_name):
    table = db.by_name(table_name)
    if table is None:
        raise NotFound()
    from sqlalchemy import select
    q = select([table.table], from_obj=table.table)
    return jsonify(Pager(QueryPager(table.database.engine, q),
                         table_name=table_name,
                         _external=True))
