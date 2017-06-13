class GradleLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.nome = nomeBuild
        self.listaTasks = list()
        self.listaDipendenze = list()
        self.listaErrori = list()
        self.listaNote = list()

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    def getTask(self):
        return self.listaTasks

    def getDipendenze(self):
        return self.listaDipendenze

    def getErrori(self):
        return self.listaErrori

    def addTask(self, t):
        self.listaTasks.append(t)

    def addListaTasks(self, list):
        self.listaTasks = list

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, list):
        self.listaErrori = list

    def addNote(self, s):
        self.listaNote.append(s)

    def addListaNote(self, list):
        self.listaNote = list

    def __str__(self):
        ret = self.nome + "\n" + self.status + "\n"
        for s in self.listaTasks:
            ret += str(s) + "\n"
        return ret