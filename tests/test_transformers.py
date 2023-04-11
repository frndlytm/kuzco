import pytest

from kuzco import Message
from kuzco.transformers import Apply, Chain, Composite, Identity


def greet(message: Message) -> Message:
    # Update the message to add a greeting property
    message["greeting"] = f"Hello, {message.get('world')}!"
    # Return the updated message
    return message


def empty(message: Message) -> Message:
    return {}


@pytest.fixture
def earth(worlds):
    yield list(worlds)[2]


def test_apply(earth):
    expect = dict(earth, greeting="Hello, Earth!")
    assert Apply(greet).transform(earth) == expect


def test_chain(earth):
    # Construct of Chain of transforms to compose together
    transform = (
        Chain()
        .then(Apply(greet))
        .then(Apply(empty))
    )

    # Call the Chain on the message
    assert transform(earth) == {}


def test_composite(earth):
    expect = dict(earth, greeting="Hello, Earth!", properties={})

    # Configure a Composite transform
    transform = (
        Composite(greet)
        .add("properties", Apply(empty))
    )

    # Call the Composite
    assert transform(earth) == expect


def test_identity(earth):
    assert Identity().transform(earth) == earth
