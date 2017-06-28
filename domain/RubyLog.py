import json
class RubyLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.nome = nomeBuild
        self.listaCommand = list()
        self.listaDipendenze = list()
        self.listaErrori = list()
        self.listaTest=list()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def getCommand(self):
        return self.listaCommand

    def setCommand(self,c):
        self.listaCommand=c

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    def getDipendenze(self):
        return self.listaDipendenze

    def setDipendenze(self,d):
        self.listaDipendenze=d

    def getTest(self):
        return self.listaTest

    def setTest(self, d):
        self.listaTest = d

    def addDipendenze(self, list):
        self.listaDipendenze = list

    def getErrori(self):
        return self.listaErrori

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, list):
        self.listaErrori = list