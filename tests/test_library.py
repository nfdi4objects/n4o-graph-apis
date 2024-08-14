import unittest

from app import CypherBackend

config = {
    "uri": "bolt://example.org",
    "password": "",
    "user": ""
}


class TestLibrary(unittest.TestCase):

    def test_valid_test_cases(self):
        backend = CypherBackend(config)
        self.assertTrue(backend)
        backend.close()
