from kuzco.filters import Exclude, Flatten, Include, Map


def test_exclude(worlds):
    assert list(Exclude(lambda m: m.get("id") > 3)(worlds)) == [
        {"id": 1, "world": "Mercury"},
        {"id": 2, "world": "Venus"},
        {"id": 3, "world": "Earth"},
    ]


def test_include(worlds):
    assert list(Include(lambda m: m.get("id") <= 3)(worlds)) == [
        {"id": 1, "world": "Mercury"},
        {"id": 2, "world": "Venus"},
        {"id": 3, "world": "Earth"},
    ]


def test_map(worlds):
    assert list(Map(lambda m: {"msg": f"Hello, {m.get('world')}!"})(worlds)) == [
        {"msg": "Hello, Mercury!"},
        {"msg": "Hello, Venus!"},
        {"msg": "Hello, Earth!"},
        {"msg": "Hello, Mars!"},
        {"msg": "Hello, Jupiter!"},
        {"msg": "Hello, Saturn!"},
        {"msg": "Hello, Uranus!"},
        {"msg": "Hello, Neptune!"},
    ]


def test_flatten(worlds):
    data = list(worlds)
    assert list(Flatten()([data, data])) == [*data, *data]
