from __future__ import print_function
import flask
import os
import sys
import socket


app = flask.Flask(__name__)
app.config.update(DEBUG=True)

_HC_URL = os.environ.get("HC_URL", "/")
_TIMEOUT = int(os.environ.get("CONN_TIMEOUT", "10"))
_PORT = int(os.environ.get("CONTAINER_PORT", "5000"))

@app.route(_HC_URL)
def healthcheck():
    return '{"status": "OK"}'

@app.route('/tcp/<endpoint>')
def testconn(endpoint):
    try:
        (host, port) = endpoint.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = socket.gethostbyname(host)
        s.settimeout(_TIMEOUT)
        s.connect((remote_ip, int(port)))
        (res, msg) = ("OK", "all ok.")
    except socket.gaierror, e:
        print(e)
        (res, msg) = ("NG", e)
    except socket.error, e:
        print(e)
        (res, msg) = ("NG", e)

    return '{{"result": "{0}", "message": "{1}"}}'.format(res, msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=_PORT)
