from flask import Blueprint
from apikit import jsonify, Pager
from sqlalchemy import Table
from werkzeug.exceptions import NotFound

from ouija.core import engine, metadata, url_for
from ouija.util import QueryPager

tables_api = Blueprint('tables', __name__)


def normalize_column_type(column):
    name = unicode(column.type).lower()
    if name.startswith('varchar') or name.startswith('char'):
        return 'text'
    if name.startswith('numeric'):
        return 'float'
    return name


def table_data(table, detailed=True):
    from sqlalchemy import select
    q = select([table], from_obj=table)

    data = {
        'name': table.name,
        'label': table.name,
        'metadata_uri': url_for('tables.view', table_name=table.name),
        'rows_uri': url_for('tables.rows', table_name=table.name),
        'columns_num': len(table.columns),
        'rows_num': 0  # len(QueryPager(engine, q))
    }
    if detailed:
        data['columns'] = []
        for column in table.columns:
            data['columns'].append({
                'name': column.name,
                'label': column.name,
                'type': normalize_column_type(column)
            })
    return data


def get_table_by_name(name):
    if name not in metadata.tables.keys():
        raise NotFound()
    return Table(name, metadata, autoload=True, autoload_with=engine)


@tables_api.route('/api/tables')
def index():
    tables = []
    for table in metadata.tables.values():
        tables.append(table_data(table, detailed=False))
    return jsonify({
        'results': tables,
        'total': len(tables)
    })


@tables_api.route('/api/table/<table_name>')
def view(table_name):
    table = get_table_by_name(table_name)
    return jsonify(table_data(table))


@tables_api.route('/api/table/<table_name>/rows')
def rows(table_name):
    table = get_table_by_name(table_name)
    from sqlalchemy import select
    q = select([table], from_obj=table)
    return jsonify(Pager(QueryPager(engine, q), table_name=table_name,
                         _external=True))
