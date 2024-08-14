from neo4j import GraphDatabase, graph
from neo4j.exceptions import CypherSyntaxError, CypherTypeError, ConstraintError, DriverError, Neo4jError
from .error import ApiError


class CypherBackend:

    def __init__(self, config):
        self.driver = GraphDatabase.driver(
            config["uri"], auth=(config["user"], config["password"]),
            connection_timeout=2,  # backend should be reachable, so 2s is enough
        )
        self.timeout = config["timeout"] if "timeout" in config else None

    def close(self):
        self.driver.close()

    def execute(self, cmd):
        with self.driver.session() as session:
            try:
                result = session.run(cmd, timeout=self.timeout)
            except (CypherSyntaxError, CypherTypeError, ConstraintError) as error:
                raise ApiError(error.message, 400)  # Bad Request
            except (DriverError, Neo4jError) as error:
                # Bad configuration or network error
                raise ApiError(type(error).__name__, 503)
            except Exception as error:
                raise ApiError(error, 500)
            return [outputDict(record) for record in result]


def node2dict(node: graph.Node):
    props = dict((key, value) for key, value in node.items())
    return {'id': node.element_id, 'labels': list(node.labels), 'type': 'node', 'properties': props}


def rs2dict(rs: graph.Relationship):
    props = dict((key, value) for key, value in rs.items())
    return {
        'type': 'edge', 'id': rs.element_id,
        'labels': [rs.type], 'properties': props, 'from': rs.start_node.element_id, 'to': rs.end_node.element_id}


def path2dict(path: graph.Path):
    nodes = [node2dict(x) for x in path.nodes]
    rss = [rs2dict(x) for x in path.relationships]
    return {'type': 'graph', 'nodes': nodes, 'edges': rss}


def outputDict(record):
    resultDict = {}
    for key, value in record.items():
        if isinstance(value, graph.Node):
            resultDict[key] = node2dict(value)
        elif isinstance(value, graph.Relationship):
            resultDict[key] = rs2dict(value)
        elif isinstance(value, graph.Path):
            resultDict[key] = path2dict(value)
        else:
            resultDict[key] = value
    return resultDict
