# n4o-graph-api

> API and minimal web interface to [NFDI4Objects Knowledge Graph](https://nfdi4objects.github.io/n4o-graph/).

This repository implements a public web API to the NFDI4Objects Knowledge Graph. See the [Knowledge Graph Manual](https://nfdi4objects.github.io/n4o-graph/) (in German) for details.

## Installation

Required Python modules are listed in `requirements.txt`. Use [deployment method of your choice](https://flask.palletsprojects.com/en/2.0.x/deploying/#self-hosted-options). The application must be [configured](#configuration) first.

## Configuration

A local file `config.yaml` is needed with configuration. Use this as boilerplate:

~~~yaml
---
cypher: 
  uri: "bolt://localhost:7687"
  user: ""
  password: "" 
  timeout: 30
  examples:
    - name: Get some people
      query: "MATCH (n:E21_Person) RETURN n LIMIT 10"
    - name: List all classes (= node labels)
      query: "MATCH (n)\n RETURN distinct labels(n) AS classes, count(*) AS count"
sparql:
  endpoint: "http://dbpedia.org/query"
  examples:
    - name: List all classes
      query: |
        SELECT DISTINCT ?class WHERE { [] a ?class }
    - name: Get number of triples
      query: |
        SELECT (COUNT(*) as ?triples) 
        WHERE { ?s ?p ?o } 
    - name: List all named graphs with metadata
      query: |
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?graph ?title ?source ?issued
        WHERE {
          GRAPH ?graph { }
          OPTIONAL { ?graph dct:title ?title }
          OPTIONAL { ?graph dct:source ?source }  
          OPTIONAL { ?graph dct:issued ?issued }
        }
~~~

Set `endpoint` to `null` to disable SPARQL API.

Make sure the Neo4j (or compatible) database is read-only because this application does not guarantee to filter out write queries!

## Usage

### SPARQL API

This webservice implements [SPARQL query API](https://www.w3.org/TR/2013/REC-sparql11-protocol-20130321/#query-operation) at `/api/sparl`. The query is transformed to a POST request and passed to the backend SPARQL endpoint.

### Cypher Propert Graph API

The property graph API at `/api/cypher` expects a HTTP GET query parameter `query` with a CYPHER query and returns a (possibly empty) JSON array of result objects on success. On failure, an error object is returned. Each response objects is maps query variables to values. Each value is one of:

- number, string, boolean, or null
- array of values
- [PG-JSONL](https://pg-format.github.io/specification/#pg-json) node or edge object for nodes and edges
- [PG-JSON](https://pg-format.github.io/specification/#pg-jsonl) graph object for pathes

## Development

To locally run the application first install required Python dependencies with virtualenv:

~~~sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
~~~

Then locally run for testing:

~~~sh
python app.py --help
~~~

Please run `make lint` to detect Python coding style violations and `make fix` to fix some of these violations.

## License

MIT License

