import json
import re
from TestMaven import TestMaven


class Snapshot:
    def __init__(self,nome):
        self.name=nome
        self.goalList= list()
        self.test=list()

    def addGoal(self, goal):
        self.goalList.append(goal)

    def addTest(self, test):
        if re.match("Running(.)*", test):
            t=TestMaven(test.replace("Running","").strip())
            self.test.append(t)
        elif re.match("Total Tests:(.)*", test):
            t=TestMaven(test.strip())
            self.test.append(t)
        else:
            try:
                t=self.test.pop(-1)
                dati = test.split(",")
            except IndexError:
                t = TestMaven(test.split("- in")[1].strip())
                self.test.append(t)
                dati= test.split("- in")[0].split(",")
            t.setRun(dati[0].replace("Tests run:", "").strip())
            t.setFailures(dati[1].replace("Failures:", "").strip())
            t.setErrors(dati[2].replace("Errors:", "").strip())
            t.setSkipped(dati[3].replace("Skipped:", "").strip())
            try:
                t.setTime(dati[4].replace("Time elapsed: ","").strip().split("s")[0])
            except IndexError:
                t.setTime("")
            self.test.append(t)




    def getName(self):
        return self.name

    def getGoals(self):
        return self.goalList

    def getTest(self):
        return self.test

    def __str__(self):
        str=""
        str+= self.name
        for g in self.goalList:
            str+="\n" +g.__str__()
        str+="\n"+ self.test
        return str

    def __eq__(self, other):
        return self.name == other.getName()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)