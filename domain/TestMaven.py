import json


class TestMaven:
    def __init__(self, nome):
        self.testClass=nome
        self.run=""
        self.failures=""
        self.errors=""
        self.skipped=""
        self.time=""

    def getClasse(self):
        return self.testClass

    def getRun(self):
        return self.run

    def getFailures(self):
        return self.failures

    def getErrors(self):
        return self.errors

    def getSkipped(self):
        return self.skipped

    def getTime(self):
        return self.time

    def setClasse(self,n):
        self.testClass=n

    def setRun(self,r):
        self.run=r

    def setFailures(self,s):
        self.failures=s

    def setErrors(self,e):
        self.errors=e

    def setSkipped(self,s):
        self.skipped=s

    def setTime(self,time):
        self.time=time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)