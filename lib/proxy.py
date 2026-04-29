import requests
from flask import request, make_response, Response

# Simple HTTP Proxy
# TODO: may better be done like shown at <https://stackoverflow.com/a/36601467>

excluded_headers = ['content-encoding',
                    'content-length', 'transfer-encoding', 'connection']


def cleanHeaders(res):
    return [(k, v) for k, v in res.raw.headers.items() if k.lower() not in excluded_headers]


def enable_proxy(app, backend, base):
    @app.route(f'{base}', methods=['GET', 'POST', 'DELETE'], defaults={'path': ''})
    @app.route(f'{base}<path:path>', methods=['GET', 'POST', 'DELETE'])
    def action(path):
        target_url = f'{backend}{path}'
        if request.method == 'GET':
            resp = requests.get(
                target_url, headers=request.headers, data=request.data)
        elif request.method == 'DELETE':
            resp = requests.delete(
                target_url, headers=request.headers, data=request.data)
        elif request.method == 'POST':
            resp = requests.post(target_url, json=request.json,
                                 data=request.form, files=request.files)
        else:
            resp = make_response(f'Not supported method {request.method}', 500)
        return Response(resp.content, resp.status_code, cleanHeaders(resp))
