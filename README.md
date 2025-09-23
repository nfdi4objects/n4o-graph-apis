# n4o-graph-api

[![License](https://img.shields.io/github/license/nfdi4objects/n4o-graph-apis.svg)](https://github.com/nfdi4objects/n4o-graph-apis/blob/master/LICENSE)
[![Test](https://github.com/nfdi4objects/n4o-graph-apis/actions/workflows/test.yml/badge.svg)](https://github.com/nfdi4objects/n4o-graph-apis/actions/workflows/test.yml)
[![Docker](https://img.shields.io/badge/Docker-ghcr.io%2Fnfdi4objects%2Fn4o--graph--apis-informational)](https://github.com/nfdi4objects/n4o-graph-apis/pkgs/container/n4o-graph-apis)

> API and minimal web interface to the NFDI4Objects Knowledge Graph (N4O KG)

This repository implements public web APIs to the NFDI4Objects Knowledge Graph,
available at <https://graph.nfdi4objects.net/>. The Knowledge Graph database
can be queried [with SPARQL](#sparql-api) using the API endpoints provided by
this web application. In addition, collection URIs starting with
<https://graph.nfdi4objects.net/collection/> are served as linked open data and
import reports can be inspected.

For additional information see the [Knowledge Graph Manual](https://nfdi4objects.github.io/n4o-graph/) (in German).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
  - [SPARQL](#sparql)
  - [Tools](#tools)
- [Usage](#usage)
  - [SPARQL API](#sparql-api)
  - [Linked Open Data](#linked-open-data)
- [Development](#development)
- [License](#license)

## Requirements

Requires Python >= 3.6 to run from sources (Python modules are listed in `requirements.txt`) or Docker.

A backend API (SPARQL) must be available and [configured](#configuration).

File system read access to the import staging area is required, if enabled via configuration.

## Installation

Use Python flask [deployment method of your choice](https://flask.palletsprojects.com/en/2.0.x/deploying/#self-hosted-options)
or Docker.

Docker images are generated and [published at GitHub](https://github.com/nfdi4objects/n4o-graph-apis/pkgs/container/n4o-graph-apis) from the `main` branch (alternatively build the image locally [as described below](#development)).

There is a [`docker-compose.yml`](docker-compose.yml) for deployment. If needed, it can be configured with a local file `.env` to set Docker image (`IMAGE`), Docker container name (`CONTAINER`), Docker network (`NETWORK`), config file (`CONFIG`), port (`PORT`) and staging area (`STAGE`). 

~~~sh
docker network create n4onetwork # unless it already exists
docker compose create
docker compose start
docker compose stop
~~~~

To test with a local triple store at <http://localhost:3030/n4o>, use this URL in the config file and use `docker-compose-host.yml`:

~~~sh
docker compose -f docker-compose-host.yml create
~~~

## Configuration

A local file `config.yaml` is needed with configuration. See [`config.example.yaml`](config.example.yaml) as boilerplate and documentation. Configuration is only loaded once at startup.

In addition the following environment variables can be used:

- `SPARQL`: backend API endpoint. Default: `http://localhost:3030/n4o/`
- `STAGE`: readable stage directory. Default: `stage`
- `QUERIES`: directory with sample SPARQL queries with file extension `.rq`. Default: `queries`

The RDF database is expected to be grouped in named graphs:

- Graph `https://graph.nfdi4objects.net/collection/` contains information about collections
- Graphs `https://graph.nfdi4objects.net/collection/X` where X is an integer contain information from individual collections
- Graph `https://graph.nfdi4objects.net/terminology/` contains information about terminologies
- Graphs `http://bartoc.org/en/node/X` where X is an integer contain information from individual terminologies
- The default graph must be configured as union graph.

See [n4o-fuseki](https://github.com/nfdi4objects/n4o-fuseki#readme) for preconfigured Triple store and [n4o-graph-importer](https://github.com/nfdi4objects/n4o-graph-importer#readme) for a component to ensure RDF data is only imported into the triple store as expected.

### Tools

Configuration key `tools` can be used to add web applications either as simple links or made available at an URL path via HTTP Proxy. Each tool requires

- a `name` and a `description`
- either an `url` with an external link, or both an URL `path` and a `backend` URL to pass queries to 

## Usage

### SPARQL API

This webservice implements [SPARQL query API](https://www.w3.org/TR/2013/REC-sparql11-protocol-20130321/#query-operation) at `/api/sparl`. The query is transformed to a POST request and passed to the backend SPARQL endpoint.

### Linked Open Data

Information about collections, each identified by an URI starting with <https://graph.nfdi4objects.net/collection/>, can be retrieved as Linked Open Data (LOD) at path `/collection` in HTML and in RDF serializations. The data is retrieved via [SPARQL API](#sparql-api), so retrieving <https://graph.nfdi4objects.net/collection/1> results in the same data as this SPARQL query from graph <https://graph.nfdi4objects.net/collection/>:

~~~sparql
DESCRIBE <https://graph.nfdi4objects.net/collection/1> FROM <https://graph.nfdi4objects.net/collection/>
~~~

The RDF serialization is determined via HTTP Content Negotiation or with optional query parameter `format`.

Information about terminologies will be made available from <https://graph.nfdi4objects.net/terminology/>.

## Development

To locally run the application first install required Python dependencies with virtualenv:

~~~sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
~~~

Then locally run for testing:

~~~sh
python app.py --help
~~~

Alternatively run `make .venv` and `make dev`.

Please run `make lint` to detect Python coding style violations and `make fix` to fix some of these violations. Some unit tests are run with `make test`.

To populate the configured knowledge graph databases with actual data, see the source code repository <https://github.com/nfdi4objects/n4o-import>.

To locally build the Docker image run `make docker`. The container is named `n4o-graph-apis`, so it can be run for testing:

~~~sh
docker run --rm --net=host -p 8000:8000 -v ./config.yaml:/app/config.yaml:ro n4o-graph-apis
~~~

To use custom queries, mount your local directory to `/app/queries`

## License

MIT License

