import os

from flask import Flask
from flask.ext.assets import Environment
from sqlalchemy import create_engine, MetaData

from ouija import default_settings

folder = os.path.join(os.path.dirname(__file__), '..', 'ui')

app = Flask('ouija', static_folder=folder, template_folder=folder)
app.config.from_object(default_settings)
app.config.from_envvar('OUIJA_SETTINGS', silent=True)
assets = Environment()

engine = create_engine(app.config.get('DATABASE_URI'))
metadata = MetaData(bind=engine)
metadata.reflect(engine)
