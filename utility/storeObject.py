import json

def store(o, title):
    with open(title+'.json', 'w') as fp:
        json.dump(o, fp, default=lambda o: o.__dict__)

def restore(title):
    with open(title+'.json', 'r') as fp:
        data = json.load(fp)
        return data