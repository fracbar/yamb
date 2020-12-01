class MemoryBoard:

    broadcast_board = "__all__"

    def __init__(self):
        self.board = {}

    def put(self, board, message, prio, ttl):
        if not board:
            board = MemoryBoard.broadcast_board

        if board not in self.board:
            self.board[board] = {}

        # process message
        self.board[board][message] = {"prio": prio, "ttl": ttl}

    def get(self):
        return self.board[MemoryBoard.broadcast_board].keys()
