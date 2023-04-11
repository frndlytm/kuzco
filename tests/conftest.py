import pytest

import kuzco


@pytest.fixture
def worlds():
    yield kuzco.chan(
        *[
            {"id": 1, "world": "Mercury"},
            {"id": 2, "world": "Venus"},
            {"id": 3, "world": "Earth"},
            {"id": 4, "world": "Mars"},
            {"id": 5, "world": "Jupiter"},
            {"id": 6, "world": "Saturn"},
            {"id": 7, "world": "Uranus"},
            {"id": 8, "world": "Neptune"},
        ]
    )


@pytest.fixture
def earth(worlds):
    yield list(worlds)[2]
