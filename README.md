# n4o-graph-api

> API and minimal web interface to [NFDI4Objects Knowledge Graph](https://nfdi4objects.github.io/n4o-graph/).

This repository implements a public web API to the NFDI4Objects Knowledge Graph. See the [Knowledge Graph Manual](https://nfdi4objects.github.io/n4o-graph/) (in German) for details.

## Installation

Install required Python dependencies with virtualenv:

~~~sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
~~~

Then locally run for testing:

~~~sh
python app.py --help
~~~

And deploy [by method of your choice](https://flask.palletsprojects.com/en/2.0.x/deploying/#self-hosted-options).

## Configuration

A local file `config.json` is needed with configuration. Use this as boilerplate:

~~~json
{
  "cypher": {
    "uri": "bolt://esx-120.gbv.de:7687",
    "user": "",
    "password": "",
    "timeout": 30,
    "example": "MATCH (n:E21_Person) RETURN n LIMIT 10"
  },
  "sparql": {
     "endpoint": "http://example.org/sparql"
  }
}
~~~

Make sure the Neo4j (or compatible) database is read-only because this application does not guarantee to filter out write queries!

## Usage

### SPARQL API

...

### Cypher Propert Graph API

The property graph API expects a HTTP GET query parameter `query` with a CYPHER query and returns a (possibly empty) JSON array of result objects on success. On failure, an error object is returned. Each response objects is maps query variables to values. Each value is one of:

- number, string, boolean, or null
- array of values
- [PG-JSONL]() node or edge object for nodes and edges
- [PG-JSON]() graph object for pathes

## Development

Please run `make lint` to detect Python coding style violations and `make fix` to fix some of these violations.

