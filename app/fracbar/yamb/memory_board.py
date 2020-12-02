from datetime import datetime, timedelta
import functools


def sort_message(item1, item2):
    prio_sort = item1[1]["prio"] - item2[1]["prio"]
    if prio_sort == 0:
        return item2[1]["create"] - item1[1]["create"]
    else:
        return prio_sort

class MemoryBoard:

    broadcast_board = "__all__"

    def __init__(self):
        self.board = {}

    def put(self, board, message, prio, ttl):
        if not board:
            board = MemoryBoard.broadcast_board

        if board not in self.board:
            self.board[board] = {}

        now = datetime.now()
        # process message
        expire = now + timedelta(seconds=ttl)
        self.board[board][message] = {"prio": prio, "ttl": ttl, "create": now.timestamp(), "expires": expire.timestamp()}

        # remove expired from this board
        for item in self.board[board].items():
            if item[1]["expires"] < datetime.now().timestamp():
                self.board[board].pop(item[0], None)

    def get(self, board, count=-1, broadcast_count=-1):
        count = int(count)
        broadcast_count = int(broadcast_count)

        answer = []

        answer += self.retrieve_messages(MemoryBoard.broadcast_board, broadcast_count)
        current_count = len(answer)
        if count == -1 or current_count < count:
            answer += self.retrieve_messages(board, count if count == -1 else count - current_count)

        return answer

    def retrieve_messages(self, board, count):
        answer = []

        if board in self.board:
            for item in sorted(self.board[board].items(), key=functools.cmp_to_key(sort_message)):
                if item[1]["expires"] >= datetime.now().timestamp():
                    answer.append(item[0])

                    if count != -1 and len(answer) >= count:
                        break

        return answer
