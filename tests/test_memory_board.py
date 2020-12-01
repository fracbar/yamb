from app.fracbar.yamb import memory_board

def test_get():
    mb = memory_board.MemoryBoard()
    assert len(mb.get()) == 0

def test_put():
    mb = memory_board.MemoryBoard()
    mb.put(None, "test", 2, 300)

    assert len(mb.get()) == 1


