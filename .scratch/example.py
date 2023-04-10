
class ExampleTransform(ITransformer):
    def transform(self, message):
        return {"hello": message.get("world")}
    

f = (
    Pipeline() 
    | Mapper(ExampleTransform())
    | Exclude(lambda m: m.get("hello") == "Mars")
)

messageset = [
    {"world": "Mercury"},
    {"world": "Venus"},
    {"world": "Mars"},
]
results = f(messageset)
# results = [{"hello": "Mars"}]

ExampleTransform()({"world": "Mercury"})