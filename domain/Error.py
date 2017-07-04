import json


class Error:
    def __init__(self,errorName):
        self.name=errorName
        self.category="other"
        self.task=""

    def setCategory(self, c):
        self.category=c

    def setTask(self, t):
        self.task=t

    def setName(self, n):
        self.name=n

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getTask(self):
        return self.task

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name)



