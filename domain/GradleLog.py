import re

from domain.Error import Error
from domain.GradleCommand import GradleCommand
import json

class GradleLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.nome = nomeBuild
        self.listaCommand = list()
        self.listaDipendenze = list()
        self.listaErrori = list()
        self.listaNote = set()
        self.listaErroriStatus=list()

    def getCommand(self):
        return self.listaCommand

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    def getDipendenze(self):
        return self.listaDipendenze

    def addDipendenze(self, list):
        self.listaDipendenze = list

    def getErrori(self):
        return self.listaErrori

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, lista):
        listaErroriParsati=list()
        for e in lista:
            error= Error(e.split("\t")[2].replace(">","").strip())
            error.setCategory(e.split("\t")[1])
            error.setTask(e.split("\t")[0])
            #potrei aggiungere altre regole per matchare errori che non appartengono a un task classificato
            if re.match("(.)*No such file or directory(.)*", error.getName()):
                error.setCategory("dependencies")
            listaErroriParsati.append(error)
        self.listaErrori =listaErroriParsati

    def addNote(self, s):
        self.listaNote.append(s)

    def addListaNote(self, list):
        self.listaNote = list

    def setCommand(self, nome):
        self.listaCommand.append(GradleCommand(nome))

    def addCommands(self, commands):
        self.listaCommand=commands

    def setListaErroriStatus(self, lista):
        self.listaErroriStatus=lista

    def getListaErroriStatus(self):
        return self.listaErroriStatus

    def toJSON(self):
        self.listaNote=list(self.listaNote)
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)