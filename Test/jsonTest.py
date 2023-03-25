import json

data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

# Save data to JSON file
with open("data.json", "w") as f:
    json.dump(data, f)

with open('data.json', 'r') as r:
    print(json.load(r))