import re
import json
from Error import Error
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
        errori= set()
        for t in self.listaErrori:
            e = Error(t.split("[ERROR]")[1].strip())
            e.setCategory(t.split("[ERROR]")[0].split("\t")[1])
            e.setTask(t.split("[ERROR]")[0].split("\t")[0])
            if re.match("(.)* Failed to execute goal", t):
                errori.add(e)
                # if re.match("(.)*Compilation failure(.)*", t):
                #     # print "Errore di compilazione"
                #     errori.add("Compilation error")
            #errori in fase di test
            elif re.match("(.)*<<< FAILURE!(.)*", t):
                # print t
                errori.add(e)
            #errori di dipendenze
            elif re.match("(.)*The build could not read", t):
                errori.add(e)
                #errori.add("Dependency Error: "+t.replace("[ERROR]", "").strip())
            #errori di risoluzione
            elif re.match("(.)*cannot be resolved(.)*",t):
                # print t
                errori.add(e)
            #errori di lettura file
            elif re.match("(.)*error reading(.)*", t):
                # print t
                errori.add(e)
        self.listaErroriParsati= list(errori)
        return errori

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
