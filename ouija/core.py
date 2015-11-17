import os

from flask import Flask, url_for as _url_for
from flask.ext.assets import Environment
from flask_oauthlib.client import OAuth

from ouija import default_settings

folder = os.path.join(os.path.dirname(__file__), '..', 'ui')

app = Flask('ouija')
app.config.from_object(default_settings)
app.config.from_envvar('OUIJA_SETTINGS', silent=True)
assets = Environment(app)
oauth = OAuth()
oauth_provider = oauth.remote_app('provider', app_key='OAUTH')


def url_for(*a, **kw):
    """ Always generate external URLs. """
    try:
        kw['_external'] = True
        if app.config.get('PREFERRED_URL_SCHEME'):
            kw['_scheme'] = app.config.get('PREFERRED_URL_SCHEME')
        return _url_for(*a, **kw)
    except RuntimeError:
        return None
