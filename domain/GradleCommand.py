import json
class GradleCommand:
    #TODO si potrebbero associare i warning e le note non piu' al log intero ma al singolo command
    def __init__(self, nomeCommand):
        self.nome = nomeCommand
        self.listaTasks = list()

    def getNome(self):
        return self.nome

    def getTasks(self):
        return self.listaTasks

    def addTask(self, t):
        self.listaTasks.append(t)

    def addListaTasks(self, lista):
        self.listaTasks = lista

    def __str__(self):
        ret = self.nome + "\n"
        for s in self.listaTasks:
            ret += str(s) + "\n"
        return ret

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)