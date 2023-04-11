from kuzco.reducers import Collect


def test_collect(worlds):
    assert Collect()(worlds) == [
        {"id": 1, "world": "Mercury"},
        {"id": 2, "world": "Venus"},
        {"id": 3, "world": "Earth"},
        {"id": 4, "world": "Mars"},
        {"id": 5, "world": "Jupiter"},
        {"id": 6, "world": "Saturn"},
        {"id": 7, "world": "Uranus"},
        {"id": 8, "world": "Neptune"},
    ]
