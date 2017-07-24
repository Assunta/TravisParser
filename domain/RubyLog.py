import json

class RubyLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.name = nomeBuild
        self.commandList = list()
        self.dependenciesList = list()
        self.errorList = list()
        self.testList=list()
        self.warningList=list()
        self.toolList=list()
        self.statusMessageList=list()
        self.typeOfError = ""
        self.buildTool = "Rake"

    def getBuildTool(self):
        return  self.buildTool

    def getTypeOfError(self):
        return self.typeOfError

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def getCommand(self):
        return self.commandList

    def setCommand(self,c):
        self.commandList=c

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    def getDependencies(self):
        return self.dependenciesList

    def setDependencies(self, d):
        self.dependenciesList=d

    def getTest(self):
        return self.testList

    def setTest(self, d):
        self.testList = d

    def getWarning(self):
        return self.warningList

    def setWarning(self, d):
        self.warningList = d

    def getTool(self):
        return self.toolList

    def setTool(self, d):
        self.toolList = d

    def addDependencies(self, list):
        self.dependenciesList = list

    def getError(self):
        return self.errorList

    def addError(self, s):
        self.errorList.append(s)

    def addErrorList(self, lista):
        self.errorList = lista
        try:
            self.typeOfError=lista[-1].getCategory();
        except:
            self.typeOfError=""
    def setStatusMessages(self, l):
        self.statusMessageList=l

    def getStatusMessages(self):
        return self.statusMessageList

