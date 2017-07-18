import re

from domain.Error import Error
from domain.GradleCommand import GradleCommand
import json

class GradleLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.name = nomeBuild
        self.commandList = list()
        self.dependenciesList = list()
        self.errorList = list()
        self.noteList = list()
        self.statusErrorList=list()
        self.typeOfError=""

    def getTypeOfError(self):
        return self.typeOfError


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

    def addErrorList(self, lista):
        listaErroriParsati=list()
        for e in lista:
            error= Error(e.split("\t")[2].replace(">","").strip())
            error.setCategory(e.split("\t")[1])
            error.setTask(e.split("\t")[0])
            # #potrei aggiungere altre regole per matchare errori che non appartengono a un task classificato
            # if re.match("(.)*No such file or directory(.)*", error.getName()):
            #     error.setCategory("dependencies")
            listaErroriParsati.append(error)
        if lista.__len__()>0:
            try:
                self.typeOfError =listaErroriParsati[-1].getCategory()
            except:
                self.typeOfError=lista[-1].split("\t")[1]
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