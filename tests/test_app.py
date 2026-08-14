import pytest
from app import app, init
from lib import Config


@pytest.fixture
def client():
    app.testing = True

    config = Config()
    config["stage"] = "tests/stage"
    config["title"] = "XYZ"

    init(**config)

    with app.test_client() as client:
        yield client


def test_app(client):
    resp = client.get('/')
    assert resp.status_code == 200

    assert "<title>XYZ" in resp.text
