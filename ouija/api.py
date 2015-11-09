from flask import render_template, request, Blueprint
from apikit import jsonify

from ouija.core import engine, metadata
from ouija.util import angular_templates

# TODO: make notes, bookmarks, links

base_api = Blueprint('base', __name__)


def table_data(table):
    return {
        'name': table.name
    }


@base_api.route('/api/tables')
def tables_index():
    tables = []
    for table in metadata.tables.values():
        tables.append(table_data(table))
    return jsonify({
        'tables': tables,
        'table_count': len(tables)
    })


@base_api.route('/')
def index():
    templates = []  # angular_templates()
    return render_template('html/index.html', templates=templates)
