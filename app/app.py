from __future__ import print_function
import flask
import os
import sys
import socket
import json
from flask import request


app = flask.Flask(__name__)
app.config.update(DEBUG=True)

_HC_URL = os.environ.get("HC_URL", "/")
_TIMEOUT = int(os.environ.get("CONN_TIMEOUT", "10"))
_PORT = int(os.environ.get("CONTAINER_PORT", "5000"))
_PREFIX = os.environ.get("URL_PREFIX", "/")
_SINGLE_APP = os.environ.get("SINGLE_APP", "/app")


def testconn(proto, endpoint):
    try:
        (host, port) = endpoint.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = socket.gethostbyname(host)
        s.settimeout(_TIMEOUT)
        s.connect((remote_ip, int(port)))
        (res, msg) = ("OK", "all ok.")
    except Exception as e:
        print(e)
        (res, msg) = ("NG", e)
    finally:
        return '{{"result": "{0}", "message": "{1}"}}'.format(res, msg)


@app.route(_HC_URL)
def healthcheck():
    return '{"status": "OK"}'

@app.route(_SINGLE_APP, methods = ["POST"])
def singleapp():
    try:
        j = request.get_json()
        print(j['endpoint'])
        return testconn('tcp', j['endpoint'])
    except Exception as e:
        return '{{"result": "NG", "message": "{1}"}}'.format(e)

@app.route(_PREFIX + 'tcp/<endpoint>')
def tcpconn(endpoint):
    return testconn('tcp', endpoint)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=_PORT)
