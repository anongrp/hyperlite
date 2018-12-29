import json

with open('test.json','r') as f1:
    # data = json.load(f1)
    data = f1.read()

# print(data[list(data.keys())[0]]["meta"])

# print(data["Insert"]["data"])
print(type(data))

print(data)