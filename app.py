import json
import sys
import os
import io
from flask import Flask, render_template, request, make_response, send_from_directory
from waitress import serve
from argparse import ArgumentParser, BooleanOptionalAction
import mimeparse
import traceback
from rdflib import URIRef
from datetime import datetime
import requests

from lib import SparqlProxy, ApiError, Config, enable_proxy


def file_info(path, name):
    stat = os.stat(os.path.join(path, name))
    return {
        "name": name,
        "time": datetime.fromtimestamp(stat.st_mtime),
        "size": stat.st_size
    }


def jsonify(data, status=200, indent=3, sort_keys=False):
    response = make_response(json.dumps(
        data, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status_code = status
    return response


app = Flask(__name__)


def render(template, **vars):
    # TODO: better title?
    title = template.split(".")[0]
    return render_template(template, title=title, **vars)


@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response


@app.errorhandler(Exception)
def handle_exception(error):
    if app.config["debug"]:
        print(traceback.format_exc())
    if hasattr(error, 'message'):
        message = error.message
    else:
        message = str(error)
    return handle_api_error(ApiError(message))


@app.route('/')
def index():
    return render('index.html')


@app.route('/license')
def license():
    return render('license.html')


@app.context_processor
def utility_processor():
    return dict(URIRef=URIRef)


rdf_formats = {
    'application/x-turtle': 'turtle',
    'text/turtle': 'turtle',
    'application/rdf+xml': 'xml',
    'application/trix': 'trix',
    'application/n-quads': 'nquads',
    'application/n-triples': 'nt',
    'text/n-triples': 'nt',
    'text/rdf+nt': 'nt',
    'application/n3': 'n3',
    'text/n3': 'n3',
    'text/rdf+n3': 'n3'
}


@app.route('/terminology')
@app.route('/terminology/')
def terminology():
    # TODO: server RDF as well
    return render('terminologies.html')


@app.route('/mappings')
@app.route('/mappings/')
def mappings():
    return render('mappings.html')


@app.route('/collection', defaults={'id': None, 'path': None})
@app.route('/collection/', defaults={'id': None, 'path': None})
@app.route('/collection/<int:id>', defaults={'path': None})
@app.route('/collection/<int:id>/', defaults={'path': ""})
@app.route('/collection/<int:id>/<path:path>')
def collection(id, path):
    if not id:
        # TODO: server RDF as well
        return render('collections.html')

    format = request.args.get("format")
    html_wanted = "html" in request.headers["Accept"] or format == "html"

    # TODO: make stage optional
    stage_base = app.config.get("stage")
    stage_path = os.path.join(stage_base, 'collection',
                              str(id)) if stage_base else None
    if path is not None:
        if stage_base:
            if path == "":
                files = map(lambda f: file_info(stage_path, f),
                            os.listdir(stage_path))
                return render('import.html', files=files, id=id)
            else:
                return send_from_directory(stage_path, path)
        # TODO: more beautiful message
        return "Not found!"

    uri = "https://graph.nfdi4objects.net/collection/" + str(id)
    graph = app.config["sparql-proxy"].request(
        "DESCRIBE <" + uri + ">",
        {"named-graph-uri": "https://graph.nfdi4objects.net/collection/"})

    if html_wanted:
        if len(graph) > 0:
            stage = "./" + \
                str(id) + "/" if stage_path and os.path.isdir(stage_path) else None
            return render('collection.html', uri=uri, graph=graph, stage=stage)
        else:
            return render('collection.html', uri=uri, graph=None), 404
    else:
        mimetype = "text/plain"
        if format in set(rdf_formats.values()):
            mimetype = [
                type for type in rdf_formats if rdf_formats[type] == format][0]
        else:
            accept = request.headers.get("Accept")
            types = list(rdf_formats.keys())
            mimetype = mimeparse.best_match(types, accept)
            if mimetype in rdf_formats:
                format = rdf_formats[mimetype]
            else:
                format = "turtle"
                mimetype = "text/turtle"

        response = make_response("Not found", 404)
        response.mimetype = "text/plain"
        if len(graph) > 0:
            # TODO: add known namespaces for pretty Turtle
            response = make_response(graph.serialize(format=format), 200)
            response.mimetype = mimetype
        return response


@app.route('/api/sparql', methods=('GET', 'POST'))
def sparql_api():
    return app.config["sparql-proxy"].proxyRequest(request)


@app.route('/sparql')
def sparql_form():
    return render('sparql.html', **config)


@app.route('/tools')
def tools():
    return render('tools.html')

def quit(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def init(**config):
    for key in config.keys():
        app.config[key] = config[key]

    endpoint = config["sparql"]
    app.config["sparql-proxy"] = SparqlProxy(endpoint, config["debug"])

    stage = config.get("stage")
    if stage and not os.path.isdir(stage):
        quit(f"N4o import directory {stage} is not available!")

    if "tools" in config:
        for tool in config["tools"]:
            if "proxy" in tool and "path" in tool:
                enable_proxy(app, tool["proxy"], tool["path"])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        default=8000, help="Server port")
    parser.add_argument(
        '-w', '--wsgi', action=BooleanOptionalAction, help="Use WSGI server")
    parser.add_argument('-c', '--config', type=str,
                        default="config.yaml", help="Config file")
    parser.add_argument('-d', '--debug', action=BooleanOptionalAction)
    args = parser.parse_args()

    try:
        config = Config(args.config, args.debug)
    except Exception as err:
        quit(str(err))

    init(**config)

    if args.wsgi:
        print(f"Starting WSGI server at http://localhost:{args.port}/")
        serve(app, host="0.0.0.0", port=args.port, threads=8)
    else:
        app.run(host="0.0.0.0", port=args.port, debug=config["debug"])
