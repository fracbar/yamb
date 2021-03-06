from flask import Flask, request, json, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from .memory_board import MemoryBoard
app = Flask(__name__)
FlaskJSON(app)

mb = MemoryBoard()

@app.route('/broadcast-message/<string:group>', methods=['PUT'])
@as_json
def create_new_group(group):
    data = request.get_json(force=True)
    (message, prio, ttl) = parse_message(data)
    mb.put(None, message, group=group, prio=prio, ttl=ttl)
    return None, 200

@app.route('/broadcast-message', methods=['PUT'])
@as_json
def create_new_message():
    data = request.get_json(force=True)
    (message, prio, ttl) = parse_message(data)
    mb.put(None, message, group=None, prio=prio, ttl=ttl)
    return None, 200

@app.route('/message/<string:board_id>/<string:group>', methods=['PUT'])
@as_json
def create_new_group_for_board(board_id, group):
    data = request.get_json(force=True)
    (message, prio, ttl) = parse_message(data)
    mb.put(board_id, message, group=group, prio=prio, ttl=ttl)
    return None, 200

@app.route('/message/<string:board_id>', methods=['PUT'])
@as_json
def create_new_message_for_board(board_id):
    data = request.get_json(force=True)
    (message, prio, ttl) = parse_message(data)
    mb.put(board_id, message, group=None, prio=prio, ttl=ttl)
    return None, 200

@app.route('/messages/<string:board_id>', methods=['GET'])
@as_json
def list_message(board_id):
    count = int(request.args.get('count', -1))
    broadcast_count = request.args.get('broadcastCount', -1)

    fill_empty = False
    if "fillWithBlanks" in request.args and count > 0:
        fill_empty = True

    messages = mb.get(board_id, count=count, broadcast_count=broadcast_count)
    if fill_empty and len(messages) < count:
        messages.extend([''] * (count - len(messages)))

    return {"messages": messages}

@app.route('/broadcast-message/<string:group_or_message>', methods=['DELETE'])
@as_json
def delete_message(group_or_message):
    mb.delete(None, group=group_or_message)
    return None, 200

@app.route('/message/<string:board_id>/<string:group_or_message>', methods=['DELETE'])
@as_json
def delete_message_from_board(board_id, group_or_message):
    mb.delete(board_id, group=group_or_message)
    return None, 200

def parse_message(req):
    if not req['message']:
        return 'bad request, missing message!', 400
    else:
        message = req['message']

    prio = 2
    if "prio" in req:
        prio = int(req['prio'])

    ttl = 300
    if "ttl" in req:
        ttl = int(req['ttl'])

    return message, prio, ttl


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)