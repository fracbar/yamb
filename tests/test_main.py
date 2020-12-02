import pytest
import json
from app.fracbar.yamb import main

@pytest.fixture
def client():

    with main.app.test_client() as client:
        yield client

def test_create_new_message(client):
    payload = json.dumps({"message": "Broadcast 1"})

    response = client.post('/message', headers={"Content-Type": "application/json"}, data=payload)
    assert response.status_code == 200

def test_create_new_message_for_board(client):
    payload = json.dumps({"message": "Board 1", "ttl": 500, "prio": 2})

    response = client.post('/message/test', headers={"Content-Type": "application/json"}, data=payload)
    assert response.status_code == 200

def test_list_message(client):
    response = client.get('/messages/test', headers={"Content-Type": "application/json"})

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0] == "Broadcast 1"
    assert data[1] == "Board 1"

    # add one more
    payload = json.dumps({"message": "Board 2"})
    response = client.post('/message/test', headers={"Content-Type": "application/json"}, data=payload)

    response = client.get('/messages/test', headers={"Content-Type": "application/json"})
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(data) == 3
    response = client.get('/messages/test?count=2&broadcastCount=2', headers={"Content-Type": "application/json"})
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data[0] == "Broadcast 1"
    assert data[1] == "Board 2"

