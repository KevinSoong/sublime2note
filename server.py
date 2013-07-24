import sys
import pickle
ACCESS_TOKEN_PATH = '.sublime2note-token'

sys.path.append("./lib")

import oauth2 as oauth
from oauth2 import Consumer, Client, Token
oauth.__dict__['Consumer'] = Consumer
oauth.__dict__['Client'] = Client
oauth.__dict__['Token'] = Token

import argparse
parser = argparse.ArgumentParser(description='Sublime2Note Server')
parser.add_argument('port_number', type=int, default=5000, help='Server port number (Default=5000)')
args = parser.parse_args()

try:
    import flask
    from flask import Flask, request, session
except Exception, e:
    print e
    pass
from evernote.api.client import EvernoteClient

app = Flask(__name__)
client = EvernoteClient(
    consumer_key='kjsery',
    consumer_secret='e819b5887b9342c7',
    sandbox=False
)

request_token = client.get_request_token('http://127.0.0.1:%d/token' % args.port_number)

@app.route("/")
def hello():
    authorize_url = client.get_authorize_url(request_token)
    return flask.redirect(authorize_url)

@app.route("/token")
def token():
    access_token = client.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        str(request.args.get('oauth_verifier'))
    )
    with open(ACCESS_TOKEN_PATH, 'w') as f:
        pickle.dump(access_token,f)
    import subprocess
    proc = subprocess.Popen("python sublime2note-tool.py finish", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return app.send_static_file('connected.html')

if __name__ == "__main__":
    app.run(port=args.port_number)