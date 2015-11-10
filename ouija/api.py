from flask import render_template, request, Blueprint
from apikit import jsonify, Pager
from sqlalchemy import Table
from werkzeug.exceptions import NotFound

from ouija.core import engine, metadata, url_for
from ouija.util import angular_templates, QueryPager

base_api = Blueprint('base', __name__)


def normalize_column_type(column):
    name = unicode(column.type).lower()
    if name.startswith('varchar') or name.startswith('char'):
        return 'text'
    if name.startswith('numeric'):
        return 'float'
    return name


def table_data(table, detailed=True):
    data = {
        'name': table.name,
        'label': table.name,
        'metadata_uri': url_for('base.tables_view', table_name=table.name),
        'rows_uri': url_for('base.tables_rows', table_name=table.name),
        'columns_num': len(table.columns)
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


@base_api.route('/api/tables')
def tables_index():
    tables = []
    for table in metadata.tables.values():
        tables.append(table_data(table, detailed=False))
    return jsonify({
        'results': tables,
        'total': len(tables)
    })


@base_api.route('/api/table/<table_name>')
def tables_view(table_name):
    table = get_table_by_name(table_name)
    return jsonify(table_data(table))


@base_api.route('/api/table/<table_name>/rows')
def tables_rows(table_name):
    table = get_table_by_name(table_name)
    from sqlalchemy import select
    q = select([table], from_obj=table)
    return jsonify(Pager(QueryPager(engine, q), table_name=table_name,
                         _external=True))


@base_api.route('/')
def index():
    templates = angular_templates()
    return render_template('html/index.html', templates=templates)
