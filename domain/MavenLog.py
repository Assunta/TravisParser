import re
import json
from Error import Error
from utility.dbUtility import getMavenErrors


class MavenLog:
    def __init__(self, nomeBuild):
        self.status=""
        self.nome = nomeBuild
        self.listaSnapshot = list()
        self.listaDipendenze=list()
        self.listaErrori=list()
        self.listaWarning=list()
        self.listaErroriParsati=list()
        self.listaErroriStatus=list()

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

    def setDipendenze(self, l):
        self.listaDipendenze=l

    def getErrori(self):
        self.parseErrori()
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

    def setErroriStatus(self,lista):
        self.listaErroriStatus=lista

    def getErroriStatus(self):
        return self.listaErroriStatus

    def __str__(self):
        ret= self.nome+"\n"+self.status+"\n"
        for s in self.listaSnapshot:
            ret+=str(s) +"\n"
        return ret

    def parseErrori(self):
        errorsDB = getMavenErrors()
        errori= set()
        for t in self.listaErrori:
            for e in errorsDB:
                if re.match(e.get("regex"), t):
                    e = Error(t.split("[ERROR]")[1].strip())
                    e.setCategory(t.split("[ERROR]")[0].split("\t")[1])
                    e.setTask(t.split("[ERROR]")[0].split("\t")[0])
                    errori.add(e)
        self.listaErroriParsati= list(errori)
        return errori

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
