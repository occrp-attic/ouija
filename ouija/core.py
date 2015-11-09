from flask import Flask
from flask.ext.assets import Environment

from ouija import default_settings

app = Flask('ouija')
app.config.from_object(default_settings)
app.config.from_envvar('OUIJA_SETTINGS', silent=True)
assets = Environment()
