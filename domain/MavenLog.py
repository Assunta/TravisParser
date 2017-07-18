import re
import json
from Error import Error
from utility.dbUtility import getMavenErrors


class MavenLog:
    def __init__(self, nomeBuild):
        self.status=""
        self.name = nomeBuild
        self.snapshotList = list()
        self.dependenciesList=list()
        self.errorList=list()
        self.warningList=list()
        self.parsedErrorsList=list()
        self.statusErrorList=list()
        self.typeOfError = ""

    def getTypeOfError(self):
        return self.typeOfError

    def getNome(self):
        return self.name

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status=s

    def getSnapshots(self):
        return self.snapshotList

    def getDependencies(self):
        return self.dependenciesList

    def setDependencies(self, l):
        self.dependenciesList=l

    def getError(self):
        self.parseError()
        return self.errorList

    def addSnapshot(self,s):
        self.snapshotList.append(s)

    def addSnapshotList(self, list):
        self.snapshotList=list

    def addError(self, s):
        self.errorList.append(s)

    def addErrorList(self, list):
        self.errorList = list

    def addWarning(self, s):
        self.warningList.append(s)

    def addWarningList(self, list):
        self.warningList = list

    def setStatusError(self, lista):
        self.statusErrorList=lista

    def getStatusError(self):
        return self.statusErrorList

    def __str__(self):
        ret= self.name + "\n" + self.status + "\n"
        for s in self.snapshotList:
            ret+=str(s) +"\n"
        return ret

    def parseError(self):
        errorsDB = getMavenErrors()
        errori= set()
        for t in self.errorList:
            for e in errorsDB:
                if re.match(e.get("regex"), t):
                    e = Error(t.split("[ERROR]")[1].strip())
                    e.setCategory(t.split("[ERROR]")[0].split("\t")[1])
                    e.setTask(t.split("[ERROR]")[0].split("\t")[0])
                    errori.add(e)
        self.parsedErrorsList= list(errori)
        if self.errorList.__len__()>0:
            try:
                self.typeOfError =self.parsedErrorsList[-1].getCategory()
            except:
                self.typeOfError=self.errorList[-1].split("[ERROR]")[0].split("\t")[1]
        return errori

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
