import pytest
import json
from app.fracbar.yamb import main

@pytest.fixture
def client():

    with main.app.test_client() as client:
        yield client

def test_create_new_message(client):
    payload = json.dumps({"message": "Broadcast 1"})
    response = client.put('/broadcast-message', headers={"Content-Type": "application/json"}, data=payload)

    assert response.status_code == 200

def test_create_new_message_for_board(client):
    payload = json.dumps({"message": "Board 1", "ttl": 500, "prio": 2})
    response = client.put('/message/test', headers={"Content-Type": "application/json"}, data=payload)

    assert response.status_code == 200

def test_list_message(client):
    response = client.get('/messages/test', headers={"Content-Type": "application/json"})

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "messages" in data
    assert len(data["messages"]) == 2
    assert data["messages"][0] == "Board 1"
    assert data["messages"][1] == "Broadcast 1"

    # add one more
    payload = json.dumps({"message": "Board 2"})
    response = client.put('/message/test', headers={"Content-Type": "application/json"}, data=payload)

    data = assert_message(client, '/messages/test', 3)

    data = assert_message(client, '/messages/test?count=2&broadcastCount=2', 2)
    assert data["messages"][0] == "Board 2"
    assert data["messages"][1] == "Broadcast 1"

    # test emptyString
    data = assert_message(client, '/messages/test?count=10&fillWithBlanks=true', 10)
    assert data["messages"][9] == ""

def test_delete_message(client):
    data_cmp = assert_message(client, '/messages/to_delete')

    payload = json.dumps({"message": "Board_2", "ttl": 500, "prio": 2})
    response = client.put('/broadcast-message/to_delete', headers={"Content-Type": "application/json"}, data=payload)

    # test record
    data = assert_message(client, '/messages/to_delete')
    assert len(data) + 1, len(data_cmp)

    # delete
    client.delete('/broadcast-message/to_delete', headers={"Content-Type": "application/json"}, data=None)
    data = assert_message(client, '/messages/to_delete')
    assert len(data), len(data_cmp)

def test_delete_message_from_board(client):
    data_cmp = assert_message(client, '/messages/to_delete')

    payload = json.dumps({"message": "Board_2", "ttl": 500, "prio": 2})
    response = client.put('/message/to_delete', headers={"Content-Type": "application/json"}, data=payload)

    # test record
    data = assert_message(client, '/messages/to_delete')
    assert len(data) + 1, len(data_cmp)

    # delete
    client.delete('/message/to_delete', headers={"Content-Type": "application/json"}, data=None)
    data = assert_message(client, '/messages/to_delete')
    assert len(data), len(data_cmp)

def assert_message(client, url, count=None):
    response = client.get(url, headers={"Content-Type": "application/json"})
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "messages" in data
    if count:
        assert len(data["messages"]) == count
    return data


