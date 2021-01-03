from datetime import datetime, timedelta
import functools

def sort_message(item1, item2):
    prio_sort = item1[1]["prio"] - item2[1]["prio"]
    if prio_sort == 0:
        return item2[1]["create"] - item1[1]["create"]
    else:
        return prio_sort

class MemoryBoard:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryBoard, cls).__new__(cls)
            # Put any initialization here.
            cls.board = {}
        return cls._instance

    broadcast_board = "__all__"

    def put(self, board, message, group=None, prio=2, ttl=300):
        if not board:
            board = MemoryBoard.broadcast_board

        if board not in self.board:
            self.board[board] = {}

        if not group:
            group = message

        # print("Erstelle msg %s (%s) für board %s" % (message, group, board))

        now = datetime.now()
        # process message
        expire = now + timedelta(seconds=ttl)
        self.board[board][group] = {"message": message, "prio": prio, "ttl": ttl, "create": now.timestamp(), "expires": expire.timestamp()}

        # remove expired from this board
        self._clean(board)

    def get(self, board, count=-1, broadcast_count=-1):

        count = int(count)
        broadcast_count = int(broadcast_count)

        answer = []
        if count == 0:
            return answer

        board_messages = self.retrieve_messages(board, count)
        broadcast_messages = self.retrieve_messages(MemoryBoard.broadcast_board, broadcast_count if count == -1 else count)
        if count == -1:
            answer += board_messages
            answer += broadcast_messages
        elif broadcast_count == -1 or count <= broadcast_count:
            if len(broadcast_messages) < count:
                answer += board_messages[: count - len(broadcast_messages)]

            answer += broadcast_messages[:count]
        else:
            board_count = count - broadcast_count

            answer += board_messages[: board_count]
            if broadcast_count > 0:
                if len(broadcast_messages) < broadcast_count:
                    # fill with board
                    answer += board_messages[board_count: board_count + (broadcast_count - len(broadcast_messages))]

                if len(board_messages) < board_count:
                    answer += broadcast_messages[: count - len(board_messages)]
                else:
                    answer += broadcast_messages[:broadcast_count]

        return answer

    def delete(self, board, group):
        if board in self.board:
            del self.board[group]

    def retrieve_messages(self, board, count):
        answer = []

        if board in self.board:
            for item in sorted(self.board[board].copy().items(), key=functools.cmp_to_key(sort_message)):
                if item[1]["expires"] >= datetime.now().timestamp():
                    answer.append(item[1]["message"])

                    if count != -1 and len(answer) >= count:
                        break

        return answer

    def clear(self):
        self.board = {}

    def _clean(self, board):
        items_to_delete = []
        for item in self.board[board].copy().items():
            if item[1]["expires"] < datetime.now().timestamp():
                items_to_delete.append(item[0])

        count_to_clean = len(items_to_delete)
        if count_to_clean > 0:
            print("Clean %s entries in board %s" % (count_to_clean, board))
            for item in items_to_delete:
                self.board[board].pop(item, None)
