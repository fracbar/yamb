from app.fracbar.yamb import memory_board
import time

def assert_list(lists, asserts):
    for i in range(len(asserts)):
        assert lists[i] == asserts[i], "non-expected value in index " + str(i)

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
    test = mb.get("Flur")
    assert len(test) == 3
    assert_list(test, ["test 2", "test", "test 3"])

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

    mb.put("Flur", "test")
    mb.put("Flur", "test 2")
    test = mb.get("Flur")
    assert len(test) == 2
    assert_list(test, ["test 2", "test"])
    # always try to fill count, here with board
    test = mb.get("Flur", count=2, broadcast_count=1)
    assert len(test) == 2
    assert_list(test, ["test 2", "test"])

    mb.put(None, "btest")
    test = mb.get("Flur")
    assert len(test) == 3
    assert_list(test, ["test 2", "test", "btest"])


    mb.put(None, "btest 2")
    test = mb.get("Flur")
    assert len(test) == 4
    assert_list(test, ["test 2", "test", "btest 2", "btest"])

    test = mb.get("Flur", count=3)
    assert len(test) == 3
    assert_list(test, ["test 2", "btest 2", "btest"])

    test = mb.get("Flur", broadcast_count=1)
    assert len(test) == 3
    assert_list(test, ["test 2", "test", "btest 2"])

    # always try to fill count with broadcast, if broadcast acceptable
    test = mb.get("Flur", count=4, broadcast_count=1)
    assert len(test) == 4
    assert_list(test, ["test 2", "test", "btest 2", "btest"])

    test = mb.get("Flur", count=4, broadcast_count=-1)
    assert len(test) == 4
    assert_list(test, ["test 2", "test", "btest 2", "btest"])

    test = mb.get("Flur", count=3, broadcast_count=0)
    assert len(test) == 2
    assert_list(test, ["test 2", "test"])




