import pytest
import json
from app.fracbar.yamb import main

@pytest.fixture
def client():

    with main.app.test_client() as client:
        yield client


def test_create_new_message(client):
    payload = json.dumps({
        "message": "mycoolpassword"
    })

    response = client.post('/message', headers={"Content-Type": "application/json"}, data=payload)
    assert response.status_code == 200

def test_list_message(client):
    response = client.get('/messages', headers={"Content-Type": "application/json"})
    assert response.status_code == 200
