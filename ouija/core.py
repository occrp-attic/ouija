import os

from flask import Flask, url_for as _url_for
from flask.ext.assets import Environment
from sqlalchemy import create_engine, MetaData

from ouija import default_settings

folder = os.path.join(os.path.dirname(__file__), '..', 'ui')

app = Flask('ouija')
app.config.from_object(default_settings)
app.config.from_envvar('OUIJA_SETTINGS', silent=True)
assets = Environment(app)

engine = create_engine(app.config.get('DATABASE_URI'))
metadata = MetaData(bind=engine)
metadata.reflect(engine)


def url_for(*a, **kw):
    """ Always generate external URLs. """
    try:
        kw['_external'] = True
        # if app.config.get('PREFERRED_URL_SCHEME'):
        #    kw['_scheme'] = app.config.get('PREFERRED_URL_SCHEME')
        return _url_for(*a, **kw)
    except RuntimeError:
        return None
