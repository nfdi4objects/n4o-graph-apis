import requests
from flask import request, Response

# Simple HTTP Proxy
# TODO: may better be done like shown at <https://stackoverflow.com/a/36601467>

excluded_headers = ['content-encoding',
                    'content-length', 'transfer-encoding', 'connection']


def cleanHeaders(res):
    return [(k, v) for k, v in res.raw.headers.items() if k.lower() not in excluded_headers]


def enable_proxy(app, backend, base):
    @app.route(base, methods=['GET', 'POST', 'DELETE'], defaults={'path': ''})
    @app.route(f"{base}<path:path>", methods=["GET", "POST", "DELETE"])
    def action(path):
        match request.method:
            case 'GET':
                res = requests.get(f"{backend}{path}")
            case 'DELETE':
                res = requests.delete(
                    f"{backend}{path}", headers=request.headers, data=request.data)
            case "POST":
                res = requests.post(
                    f"{backend}{path}", headers=request.headers, json=request.json, data=request.data)
            case _:
                res = f'Unsupported method {request.method}'
        return Response(res.content, res.status_code, cleanHeaders(res))
