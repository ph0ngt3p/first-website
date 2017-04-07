import jwt
from MovieDatabaseApp import app
from functools import wraps
from flask import current_app, request, session, flash, redirect, url_for
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack
from flask_jwt_extended.exceptions import WrongTokenError
from flask_jwt_extended.utils import _get_secret_key, _decode_jwt
from flask_jwt_extended.config import get_algorithm

def token_required(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		token = request.args.get('access_token')
		secret = _get_secret_key()
		algorithm = get_algorithm()
		jwt_data = _decode_jwt(token, secret, algorithm)

		if jwt_data['type'] != 'access':
			raise WrongTokenError('Only access tokens can access this endpoint')

		ctx_stack.top.jwt = jwt_data
		return fn(*args, **kwargs)
	return wrapper

def refresh_token_required(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		token = request.args.get('refresh_token')
		secret = _get_secret_key()
		algorithm = get_algorithm()
		jwt_data = _decode_jwt(token, secret, algorithm)

		if jwt_data['type'] != 'refresh':
			raise WrongTokenError('Only refresh tokens can access this endpoint')

		ctx_stack.top.jwt = jwt_data
		return fn(*args, **kwargs)
	return wrapper

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return fn(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))
    return wrapper

class BackRedirect(object):
    cfg = app.config.get
    cookie = cfg('REDIRECT_BACK_COOKIE', 'back')
    default_view = cfg('REDIRECT_BACK_DEFAULT', 'index')

    @staticmethod
    def anchor(func, cookie=cookie):
        @wraps(func)
        def result(*args, **kwargs):
            session[cookie] = request.url
            return func(*args, **kwargs)
        return result

    @staticmethod
    def url(default=default_view, cookie=cookie):
        return session.get(cookie, url_for(default))

    @staticmethod
    def redirect(default=default_view, cookie=cookie):
        return redirect(BackRedirect.url(default, cookie))