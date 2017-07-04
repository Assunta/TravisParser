import json
import re

import pymysql

from checkTaskGradle import readDbLogin


class Task:
    def __init__(self,nome):
        self.nome = nome
        self.progetto=""
        self.isSkipped= False
        self.isUpdate= False
        self.isFailed= False
        self.categoria=self.checkTask()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def setNomeProgetto(self, p):
        self.progetto=p

    def setCategoria(self, p):
        self.categoria = p

    def setIsSkipped(self):
        self.isSkipped= True

    def setIsFailed(self):
        self.isFailed= True

    def setIsUpdate(self):
        self.isUpdate= True

    def getNome(self):
        return self.nome

    def getCategoria(self):
        return self.categoria

    def getNomeProgetto(self):
        return self.progetto

    def isUpdate(self):
        return self.isUpdate

    def isFailed(self):
        return self.isFailed

    def isSkipped(self):
        return self.isSkipped

    def __str__(self):
        return self.progetto+":"+self.nome+"\tSkip: "+str(self.isSkipped)+"\tFailed: "+str(self.isFailed)+"\tUpdate: "+str(self.isUpdate)+"\nCategoria "+str(self.categoria)

    def __eq__(self, other):
        return self.nome==other.nome

    def getTaskDb(self):
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
                sql = "SELECT `*`FROM `regoletaskgradle`"
                cursor.execute(sql)
                for r in cursor.fetchall():
                    lista.append(r)
        finally:
            connection.close()
            return lista

    def checkTask(self):
        # leggo i task classificati dal db
        listaDB = self.getTaskDb()
        trovato = False
        for item in listaDB:
            if self.nome is not None:
                if re.match(item.get("EspressioneRegolare"), self.nome.strip()) and not trovato:
                    return (item.get("Categoria"))
        return("other")
