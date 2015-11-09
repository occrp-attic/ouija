from flask import Flask
from flask.ext.assets import Environment
from sqlalchemy import create_engine

from ouija import default_settings

app = Flask('ouija')
app.config.from_object(default_settings)
app.config.from_envvar('OUIJA_SETTINGS', silent=True)
assets = Environment()

engine = create_engine(app.config.get('DATABASE_URI'))
