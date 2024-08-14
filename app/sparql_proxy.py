# from werkzeug.wsgi import wrap_file
import requests


class SparqlProxy:

    def __init__(self, api):
        self.api = api

    def request(self, request):
        # Supported parameters as defined by SPARQL protocol specification
        query = request.values.get("query", "")
        # TODO: support POST with full body: see https://www.w3.org/TR/2013/REC-sparql11-protocol-20130321/#query-operation

        headers = {
            "Content-Type": "application/sparql-query"
        }
        # Copy selected headers from original request (TODO: which more?)
        copyHeaders = ["Accept", "Accept-Encoding", "Accept-Language"]
        for name in copyHeaders:
            if name in request.headers:
                headers[name] = request.headers[name]

        params = {}
        copyParams = ["default-graph-uri", "named-graph-uri"]
        for name in copyParams:
            if name in request.values:
                params[name] = request.values[name]

        # TODO: pass result via werkzeug.wsgi.wrap_file to avoid re-parsing of response
        resp = requests.post(self.api, data=query,
                             params=params, headers=headers, stream=True)
        return resp.raw.read(), resp.status_code, resp.headers.items()
