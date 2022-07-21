import os

from flask import Flask, send_from_directory
from flask_httpauth import HTTPTokenAuth

from api.users.get_users import get_users

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

token = os.environ.get('BEARER_TOKEN', 'token')

tokens = {
    token: "admin"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route('/users')
@auth.login_required
def users():
    return get_users('api/user')


@app.route('/user/<username>')
@auth.login_required
def gists(username):
    return send_from_directory('api', f'user/{username}.txt')


if __name__ == "__main__":
    print(get_users('api/user'))
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)
