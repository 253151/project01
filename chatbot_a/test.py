import jsonlines

items = [
    {'a': 1, 'b': 2},
    {'a': 123, 'b': 456},
]
with jsonlines.open('output.jsonl', 'w') as writer:
    writer.write_all(items)