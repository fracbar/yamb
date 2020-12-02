from app.fracbar.yamb import memory_board
import time

def test_board():
    mb = memory_board.MemoryBoard()
    assert len(mb.get("Flur")) == 0

    mb.put("Wohnzimmer", "test", 2, 300)
    assert len(mb.get("Flur")) == 0
    assert len(mb.get("Wohnzimmer")) == 1

    # order und prio testen
    mb.put("Flur", "test", 2, 300)
    assert mb.get("Flur")[0] == "test"
    mb.put("Flur", "test 2", 2, 300)
    assert mb.get("Flur")[0] == "test 2" # letzte nachricht immer die wichtigste
    # prio wichtiger als letzte nachricht
    mb.put("Flur", "test 3", 3, 300)
    assert mb.get("Flur")[0] == "test 2"
    assert mb.get("Flur")[1] == "test"
    assert mb.get("Flur")[2] == "test 3"

    # count
    mb.put("Wohnzimmer", "weitere Nachricht", 2, 1)
    assert len(mb.get("Wohnzimmer")) == 2
    assert len(mb.get("Wohnzimmer", count=1)) == 1

    # am Ende ttl testen
    assert len(mb.get("Wohnzimmer")) == 2
    time.sleep(1)
    assert len(mb.get("Wohnzimmer")) == 1

def test_board_and_broadcast():
    mb = memory_board.MemoryBoard()
    mb.put(None, "test", 2, 300)
    assert len(mb.get("Flur")) == 1
    mb.put("Flur", "test", 2, 300)
    assert len(mb.get("Flur")) == 2



