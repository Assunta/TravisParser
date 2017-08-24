import re

from domain.Error import Error
from domain.GradleCommand import GradleCommand
import json

from utility.dbUtility import getGradleErrorsRules


class GradleLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.name = nomeBuild
        self.commandList = list()
        self.dependenciesList = list()
        self.errorList = list()
        self.noteList = list()
        self.statusErrorList=list()
        self.typeOfError="other"
        self.buildTool = "Gradle"

    def getTypeOfError(self):
        return self.typeOfError

    def getBuildTool(self):
        return  self.buildTool

    def getCommand(self):
        return self.commandList

    def getNome(self):
        return self.name

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    def getDependencies(self):
        return self.dependenciesList

    def addDependencies(self, list):
        self.dependenciesList = list

    def getError(self):
        return self.errorList

    def addError(self, s):
        self.errorList.append(s)

    def addErrorList(self, listError, listStatus):
        listaErroriParsati=list()
        listErrorsDb= getGradleErrorsRules()
        for e in listError:
            checkDB = False
            # check error outside tasks
            for eDB in listErrorsDb:
                if re.match(eDB.get("regex"), e):
                    error = Error(e.split("\t")[2].replace(">", "").strip())
                    error.setCategory(eDB.get("category"))
                    error.setTask("")
                    listaErroriParsati.append(error)
                    checkDB = True
                    break;
            if(not checkDB):
                error= Error(e.split("\t")[2].replace(">","").strip())
                error.setCategory(e.split("\t")[1])
                error.setTask(e.split("\t")[0])
                listaErroriParsati.append(error)

        for e in listStatus:
            # check status errors
            for eDB in listErrorsDb:
                if re.match(eDB.get("regex"), e):
                    error = Error(e)
                    error.setCategory(eDB.get("category"))
                    error.setTask("")
                    listaErroriParsati.append(error)


        if listaErroriParsati.__len__()>0:
            self.typeOfError = listaErroriParsati[-1].getCategory()
        else:
            try:
                self.typeOfError = listError[-1].split("\t")[1]
            except:
                self.typeOfError ="other"
        self.errorList =listaErroriParsati

    def addNote(self, s):
        self.noteList.append(s)

    def addListaNote(self, list):
        self.noteList = list

    def setCommand(self, nome):
        self.commandList.append(GradleCommand(nome))

    def addCommands(self, commands):
        self.commandList=commands

    def setListaErroriStatus(self, lista):
        self.statusErrorList=lista

    def getListaErroriStatus(self):
        return self.statusErrorList

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)