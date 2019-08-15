import json

data = []
for line in open('FlaskApp/static/submissions.json', 'r'):
    data.append(json.loads(line))

# print(data)


def list():
    return data
