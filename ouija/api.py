from flask import render_template, request, Blueprint
from apikit import jsonify
from sqlalchemy import Table
from werkzeug.exceptions import NotFound

from ouija.core import engine, metadata, url_for
from ouija.util import angular_templates

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
        'metadata_uri': url_for('base.tables_view', name=table.name),
        'rows_uri': url_for('base.tables_rows', name=table.name),
        'columns_num': len(table.columns)
    }
    if detailed or True:
        data['columns'] = []
        for column in table.columns:
            data['columns'].append({
                'name': column.name,
                'label': column.name,
                'type': normalize_column_type(column)
            })
    return data


@base_api.route('/api/tables')
def tables_index():
    tables = []
    for table in metadata.tables.values():
        tables.append(table_data(table, detailed=False))
    return jsonify({
        'tables': tables,
        'table_count': len(tables)
    })


@base_api.route('/api/table/<name>')
def tables_view(name):
    if name not in metadata.tables.keys():
        raise NotFound()
    table = Table(name, metadata, autoload=True, autoload_with=engine)
    return jsonify(table_data(table))


@base_api.route('/api/table/<name>/rows')
def tables_rows(name):
    return jsonify({
    })


@base_api.route('/')
def index():
    templates = angular_templates()
    return render_template('html/index.html', templates=templates)
