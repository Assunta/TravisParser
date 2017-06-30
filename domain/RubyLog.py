import json
import re

import pymysql

from checkTaskGradle import readDbLogin


class RubyLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.nome = nomeBuild
        self.listaCommand = list()
        self.listaDipendenze = list()
        self.listaErrori = list()
        self.listaTest=list()
        self.listaWarning=list()
        self.listaTool=list()

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

    def getWarning(self):
        return self.listaWarning

    def setWarning(self, d):
        self.listaWarning = d

    def getTool(self):
        return self.listaTool

    def setTool(self, d):
        self.listaTool = d

    def addDipendenze(self, list):
        self.listaDipendenze = list

    def getErrori(self):
        return self.listaErrori

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, lista):
        listaErrorParsati=list()
        for e in lista:
            p=self.check(e)
            listaErrorParsati.append(p)
        self.listaErrori = listaErrorParsati

    def check(self, e):
        rules=self.getLista()
        for r in rules:
            if re.match(r.get("espressione"), e):
                e=r.get("categoria")+"->"+e
                return e
        return "->"+e

    def getLista(self):
        lista = list()
        credenziali = readDbLogin()
        connection = pymysql.connect(host=credenziali[0],
                                     user=credenziali[1],
                                     password=credenziali[2],
                                     db='travisdb',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*`FROM `rubyerror`"
                cursor.execute(sql)
                for r in cursor.fetchall():
                    lista.append(r)
        finally:
            connection.close()
            return lista


