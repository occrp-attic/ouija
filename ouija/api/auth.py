from flask import request, Blueprint, session, redirect
from flask_oauthlib.client import OAuthException
from apikit import jsonify

from ouija import authz
from ouija.core import oauth_provider, url_for

auth_api = Blueprint('auth', __name__)


@oauth_provider.tokengetter
def get_oauth_token():
    if 'oauth' in session:
        sig = session.get('oauth')
        return (sig.get('access_token'), '')


@auth_api.before_app_request
def load_user():
    request.auth_roles = session.get('roles', [authz.GUEST])
    request.auth_user = session.get('user')
    request.auth_admin = False
    request.logged_in = request.auth_user is not None
    if request.logged_in:
        request.auth_admin = request.auth_user.get('is_admin', False)


@auth_api.route('/api/session')
def get_session():
    return jsonify({
        'logged_in': request.logged_in,
        'user': request.auth_user,
        'roles': list(request.auth_roles),
        'login_uri': url_for('auth.authorize')
    })


@auth_api.route('/auth/authorize')
def authorize():
    return oauth_provider.authorize(callback=url_for('auth.callback'))


@auth_api.route('/auth/reset')
def reset():
    authz.require(authz.logged_in())
    session.clear()
    return redirect(url_for('base.index'))


@auth_api.route('/auth/callback')
def callback():
    next_url = url_for('base.index')
    resp = oauth_provider.authorized_response()
    if resp is None or isinstance(resp, OAuthException):
        # FIXME: notify the user, somehow.
        return redirect(next_url)
    session['oauth'] = resp
    session['roles'] = [authz.GUEST, authz.USER]
    if 'googleapis.com' in oauth_provider.base_url:
        me = oauth_provider.get('userinfo')
        session['user'] = {
            'id': me.data.get('id'),
            'name': me.data.get('name'),
            'email': me.data.get('email'),
            'is_admin': False
        }
        session['roles'].append(me.data.get('email'))
    elif 'occrp.org' in oauth_provider.base_url or \
            'investigativedashboard.org' in oauth_provider.base_url:
        me = oauth_provider.get('api/2/accounts/profile/')
        session['user'] = {
            'id': me.data.get('id'),
            'name': me.data.get('display_name'),
            'email': me.data.get('email'),
            'is_admin': me.data.get('is_admin', False)
        }
        session['roles'].append(me.data.get('email'))
        for group in me.data.get('groups', []):
            group_id = 'idashboard:%s' % group.get('id')
            session['roles'].append(group_id)
    else:
        raise RuntimeError("Unknown OAuth URL: %r" % oauth_provider.base_url)
    return redirect(next_url)
