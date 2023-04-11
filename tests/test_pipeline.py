import kuzco
from kuzco import filters, reducers, transforms


def greet(message: kuzco.Message) -> kuzco.Message:
    # Update the message to add a greeting property
    message["greeting"] = f"Hello, {message.get('world')}!"
    # Return the updated message
    return message


def empty(_: kuzco.Message) -> kuzco.Message:
    return {}


def test_pipeline(worlds):
    pipeline = (
        kuzco.Pipeline()
        | filters.Exclude(lambda m: m.get("id") > 3)
        | transforms.Composite(greet).add("properties", transforms.Apply(empty))
        | reducers.Collect()
    )

    assert pipeline.run(worlds) == [
        {"id": 1, "world": "Mercury", "greeting": "Hello, Mercury!", "properties": {}},
        {"id": 2, "world": "Venus", "greeting": "Hello, Venus!", "properties": {}},
        {"id": 3, "world": "Earth", "greeting": "Hello, Earth!", "properties": {}},
    ]
