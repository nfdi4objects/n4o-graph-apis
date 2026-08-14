from collections import UserDict
import yaml
from pathlib import Path
import re
import os


def get_queries(path):
    path = Path(path)
    queries = []
    if path.is_dir():
        for file in path.glob('*.rq'):
            lines = open(file).read().split("\n")
            name = re.sub(r"^#\s*", "", lines[0])
            queries.append({"name": name, "query": "\n".join(lines)})
    return queries


defaults = {
    'stage': 'stage',
    'title': 'NFDI4Objects Knowledge Graph',
    'sparql': 'http://localhost:3030/n4o',
    'base': 'https://graph.nfdi4objects.net/',
    'queries': 'queries',
    'reports': 'reports'
}


class Config(UserDict):
    def __init__(self, file=None, debug=False):
        self.data = {}
        if file:
            try:
                with open(file) as stream:
                    self.data = yaml.safe_load(stream)
                if not self.data:
                    self.data = {}
            except yaml.YAMLError as err:
                msg = "Error in %s" % (file)
                if hasattr(err, 'problem_mark'):
                    mark = err.problem_mark
                    msg += " at line %s char %s" % (mark.line + 1,
                                                    mark.column + 1)
                raise Exception(msg)

        for name in defaults:
            if name not in self.data:
                self.data[name] = os.getenv(name.upper(), defaults[name])

        if debug:
            self.data["debug"] = True
        elif "debug" not in self.data:
            self.data["debug"] = False

        if "tools" not in self.data:
            self.data["tools"] = []
