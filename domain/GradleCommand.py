import json

class GradleCommand:
    #TODO si potrebbero associare i warning e le note non piu' al log intero ma al singolo command
    def __init__(self, nomeCommand):
        self.name = nomeCommand
        self.taskList = list()

    def getNome(self):
        return self.name

    def getTasks(self):
        return self.taskList

    def addTask(self, t):
        self.taskList.append(t)

    def addListaTasks(self, lista):
        self.taskList = lista

    def __str__(self):
        ret = self.name + "\n"
        for s in self.taskList:
            ret += str(s) + "\n"
        return ret

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)