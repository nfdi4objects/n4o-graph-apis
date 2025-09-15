import pytest
from app import app, init
from lib import Config


@pytest.fixture
def client():
    app.testing = True

    config = Config()
    config["stage"] = "tests/stage"
    # data = Path(__file__).parent
    # init(title="N4O Graph Import API TEST",
    #     stage=stage, sparql=sparqlApi, data=data)
    init(**config)

    with app.test_client() as client:
        yield client


def test_app(client):
    resp = client.get('/')
    assert resp.status_code == 200
