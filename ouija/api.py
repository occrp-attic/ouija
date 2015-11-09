from flask import render_template, request, Blueprint
from apikit import jsonify

from ouija.core import app

# TODO: make notes, bookmarks, links

base_api = Blueprint('base', __name__)


@base_api.route('/api/metadata')
def metadata():
    return jsonify({})


@base_api.route('/')
def index():
    templates = []  # angular_templates()
    return render_template('index.html', templates=templates)
