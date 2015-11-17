from flask import render_template, Blueprint

from ouija.util import angular_templates

base_api = Blueprint('base', __name__)


@base_api.route('/')
def index():
    templates = angular_templates()
    return render_template('index.html', templates=templates)
