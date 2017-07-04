import json
import re
from TestMaven import TestMaven


class Snapshot:
    def __init__(self,nome):
        self.nome=nome
        self.listaGoal= list()
        self.test=list()

    def addGoal(self, goal):
        self.listaGoal.append(goal)

    def addTest(self, test):
        if re.match("Running(.)*", test):
            t=TestMaven(test.replace("Running","").strip())
            self.test.append(t)
            print t.toJSON()
        elif re.match("Total Tests:(.)*", test):
            t=TestMaven(test.strip())
            self.test.append(t)
            print t.toJSON()
        else:
            dati=test.split(",")
            t=self.test.pop(-1)
            t.setRun(dati[0].replace("Tests run:", "").strip())
            t.setFailures(dati[1].replace("Failures:", "").strip())
            t.setErrors(dati[2].replace("Errors:", "").strip())
            t.setSkipped(dati[3].replace("Skipped:", "").strip())
            try:
                t.setTime(dati[4].replace("Time elapsed: ","").strip().split("sec")[0])
            except IndexError:
                t.setTime("")
            self.test.append(t)
            print t.toJSON()


    def getNome(self):
        return self.nome

    def getGoals(self):
        return self.listaGoal

    def getTest(self):
        return self.test

    def __str__(self):
        str=""
        str+= self.nome
        for g in self.listaGoal:
            str+="\n" +g.__str__()
        str+="\n"+ self.test
        return str

    def __eq__(self, other):
        return self.nome==other.getNome()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)