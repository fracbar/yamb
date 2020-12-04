from app.fracbar.yamb import memory_board
import time

def test_board():
    mb = memory_board.MemoryBoard()
    mb.clear()

    assert len(mb.get("Flur")) == 0

    # mit und ohne groups
    mb.put("Wohnzimmer", "test")
    assert len(mb.get("Flur")) == 0
    assert len(mb.get("Wohnzimmer")) == 1
    mb.put("Wohnzimmer", "test")
    assert len(mb.get("Wohnzimmer")) == 1
    mb.put("Schlafzimmer", "test", group="test 2")
    assert len(mb.get("Schlafzimmer")) == 1
    mb.put("Schlafzimmer", "test 2", group="test 2")

    # mit Gruppe order und prio testen
    mb.put("Flur", "test")
    assert mb.get("Flur")[0] == "test"
    mb.put("Flur", "test 2")
    assert mb.get("Flur")[0] == "test 2" # letzte nachricht immer die wichtigste
    # prio wichtiger als letzte nachricht
    mb.put("Flur", "test 3", prio=3)
    assert mb.get("Flur")[0] == "test 2"
    assert mb.get("Flur")[1] == "test"
    assert mb.get("Flur")[2] == "test 3"

    # count
    mb.put("Wohnzimmer", "weitere Nachricht", prio=2, ttl=1)
    assert len(mb.get("Wohnzimmer")) == 2
    assert len(mb.get("Wohnzimmer", count=1)) == 1

    # am Ende ttl testen
    assert len(mb.get("Wohnzimmer")) == 2
    time.sleep(1.1)
    assert len(mb.get("Wohnzimmer")) == 1
    assert len(mb.board["Wohnzimmer"]) == 2 # one is to delete
    mb.put("Wohnzimmer", "weitere Nachricht 2", prio=2, ttl=1) # trigger delete
    assert len(mb.board["Wohnzimmer"]) == 2 # one added and another deleted

def test_board_and_broadcast():
    mb = memory_board.MemoryBoard()
    mb.clear()

    mb.put(None, "test")
    assert len(mb.get("Flur")) == 1
    mb.put("Flur", "test")
    assert len(mb.get("Flur")) == 2



