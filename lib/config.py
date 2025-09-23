from collections import UserDict
import yaml
from pathlib import Path
import glob
import re
import os
import subprocess


def get_queries(path):
    path = Path(path)
    queries = []
    if path.is_dir():
        for file in path.glob('*.rq'):
            lines = open(file).read().split("\n")
            name = re.sub(r"^#\s*", "", lines[0])
            queries.append({"name": name, "query": "\n".join(lines)})
    return queries


class Config(UserDict):
    def __init__(self, file=None, debug=False):
        if file:
            try:
                with open(file) as stream:
                    self.data = yaml.safe_load(stream)
            except yaml.YAMLError as err:
                msg = "Error in %s" % (file)
                if hasattr(err, 'problem_mark'):
                    mark = err.problem_mark
                    msg += " at line %s char %s" % (mark.line + 1,
                                                    mark.column + 1)
                raise Exception(msg)
        else:
            self.data = {}

        self.data["stage"] = os.getenv('STAGE', 'stage')
        self.data["sparql"] = os.getenv('SPARQL', "http://localhost:3030/n4o")

        if debug:
            self.data["debug"] = True
        elif "debug" not in self.data:
            self.data["debug"] = False

        self.data["queries"] = get_queries(os.getenv('QUERIES', 'queries'))

        if "tools" not in self.data:
            self.data["tools"] = []
