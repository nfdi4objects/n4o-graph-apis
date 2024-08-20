import json
import yaml
import sys
from flask import Flask, render_template, request, make_response
from waitress import serve
import argparse

from app import CypherBackend, SparqlProxy, ApiError


def jsonify(data, status=200, indent=3, sort_keys=False):
    response = make_response(json.dumps(
        data, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status_code = status
    return response


app = Flask(__name__)


@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response


@app.errorhandler(Exception)
def handle_exception(error):
    if hasattr(error, 'message'):
        message = error.message
    else:
        message = str(error)
    return handle_api_error(ApiError(message))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cypher', methods=('GET', 'POST'))
def cypher_api():
    query = ''
    if 'query' in request.args:     # GET
        query = request.args.get('query')
    elif request.data:              # POST
        query = request.data.decode('UTF-8')

    if query and query != '':
        answer = app.config["cypher-backend"].execute(query)
    else:
        raise ApiError('missing or empty "query" parameter', 400)

    return jsonify(answer)


@app.route('/api/sparql', methods=('GET', 'POST'))
def sparql_api():
    return app.config["sparql-proxy"].request(request)


@app.route('/cypher')
def cypher_form():
    return render_template('cypher.html')


@app.route('/sparql')
def sparql_form():
    return render_template('sparql.html', **config["sparql"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        default=8000, help="Server port")
    parser.add_argument(
        '-w', '--wsgi', action=argparse.BooleanOptionalAction, help="Use WSGI server")
    parser.add_argument('-c', '--config', type=str,
                        default="config.yaml", help="Config file")
    parser.add_argument('-d', '--debug', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    opts = {"port": args.port}
    if args.debug:
        opts["debug"] = True

    with open(args.config) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            msg = "Error in %s" % (args.config)
            if hasattr(err, 'problem_mark'):
                mark = err.problem_mark
                msg += " at line %s char %s" % (mark.line + 1, mark.column + 1)
            print(msg, file=sys.stderr)
            sys.exit(1)

    for key in config.keys():
        app.config[key] = config[key]
    app.config["cypher-backend"] = CypherBackend(config['cypher'])
    app.config["sparql-proxy"] = SparqlProxy(
        config["sparql"]["endpoint"], args.debug)

    if args.wsgi:
        serve(app, host="0.0.0.0", **opts)
    else:
        app.run(host="0.0.0.0", **opts)
