import pytest

from locklib.locks.life_lock.graph import LocksGraph
from locklib.errors import DeadLockError


def test_multiple_set_and_get():
    graph = LocksGraph()

    graph.add_link(1, 2)
    graph.add_link(1, 3)
    graph.add_link(1, 4)

    assert graph.get_links_from(1) == {2, 3, 4}

    assert graph.get_links_from(2) == set()

    assert graph.get_links_from(5) == set()


def test_reverse_deleting_of_nodes():
    graph = LocksGraph()

    graph.add_link(1, 6)

    graph.add_link(6, 3)
    graph.add_link(6, 4)
    graph.add_link(6, 5)

    assert len(graph.search_cycles(1, 5)) == 3


def test_set_get_delete_and_get():
    graph = LocksGraph()

    graph.add_link(1, 2)
    graph.add_link(1, 3)
    graph.add_link(1, 4)

    assert graph.get_links_from(1) == {2, 3, 4}

    graph.delete_link(1, 2)

    assert graph.get_links_from(1) == {3, 4}


def test_detect_simple_cycle():
    graph = LocksGraph()

    graph.add_link(1, 2)

    with pytest.raises(DeadLockError):
        graph.add_link(2, 1)


def test_detect_difficult_cycle():
    graph = LocksGraph()

    graph.add_link(1, 2)
    graph.add_link(2, 3)
    graph.add_link(3, 4)
    graph.add_link(4, 5)
    graph.add_link(5, 6)
    graph.add_link(6, 7)
    graph.add_link(7, 8)
    graph.add_link(8, 9)

    with pytest.raises(DeadLockError):
        graph.add_link(9, 1)
