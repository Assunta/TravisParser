class MavenLog:
    def __init__(self, nomeBuild):
        self.status=""
        self.nome = nomeBuild
        self.listaSnapshot = list()
        self.listaDipendenze=list()
        self.listaErrori=list()
        self.listaWarning=list()

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status=s

    def getSnapshots(self):
        return self.listaSnapshot

    def getDipendenze(self):
        return self.listaDipendenze

    def getErrori(self):
        return self.listaErrori

    def addSnapshot(self,s):
        self.listaSnapshot.append(s)

    def addListaSnapshot(self, list):
        self.listaSnapshot=list

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, list):
        self.listaErrori = list

    def addWarning(self, s):
        self.listaWarning.append(s)

    def addListaWarning(self, list):
        self.listaWarning = list

    def __str__(self):
        ret= self.nome+"\n"+self.status+"\n"
        for s in self.listaSnapshot:
            ret+=str(s) +"\n"
        return ret