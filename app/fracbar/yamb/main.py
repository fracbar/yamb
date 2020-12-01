from flask import Flask, request, json, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from .memory_board import MemoryBoard
app = Flask(__name__)
FlaskJSON(app)

mb = MemoryBoard()

@app.route('/message', methods=['POST'])
@as_json
def create_new_message():
    data = request.get_json(force=True)
    (message, prio, ttl) = parse_message(data)
    mb.put(None, message, prio, ttl)
    return None, 200

@app.route('/<string:board_id>/message', methods=['POST'])
@as_json
def create_new_message_for_board(board_id):
    (message, prio, ttl) = parse_message(data)
    mb.put(board_id, message, prio, ttl)
    return None, 200

@app.route('/messages', methods=['GET'])
@as_json
def list_message():
    return mb.get()


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