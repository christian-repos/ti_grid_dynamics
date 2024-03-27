from fastapi.testclient import TestClient

from configs import Config
from main import app

client = TestClient(app)


def get_auth_token():
    return {"Authorization": Config.HARDCODED_EXAMPLE_TOKEN}


def test_create_vector():
    response = client.get("/create_vector", headers=get_auth_token())
    assert response.status_code == 201
    assert response.text == "Database created successfully."


def test_ask():
    test_query = "What criteria are used to deduplicate a list of ORM-mapped objects?"
    response = client.get("/ask", headers=get_auth_token(), params={"query": test_query})
    assert response.status_code == 200
