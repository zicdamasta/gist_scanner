import os

from flask import Flask, send_from_directory
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "token1": "admin"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route('/users')
@auth.login_required
def users():
    return send_from_directory('api', 'users.txt')


@app.route('/gists/<username>')
@auth.login_required
def gists(username):
    return send_from_directory('api', f'gists/{username}.txt')


if __name__ == "__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)
