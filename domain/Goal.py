import pymysql
import json

from checkTaskGradle import readDbLogin


class Goal:
    def __init__(self,nome):
        self.nome = nome
        self.categoria = "Non_classificato"
        self.findCategoria(nome)
    #TODO ogni volta che creo un goal faccio una nuova connessione, non mi sembra il caso, da ottimizzare
    def findCategoria(self, nome):
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
                sql = "SELECT * FROM `goalmaven` WHERE `Goal`LIKE %s"
                if cursor.execute(sql, ("%"+nome+"%")) >0:
                    result = cursor.fetchone()
                    self.setCategoria(result.get("Category"))
        finally:
            connection.close()
            return lista
    def setCategoria(self, p):
        self.categoria = p

    def getNome(self):
        return self.nome

    def getCategoria(self):
        return self.categoria

    def __str__(self):
        return self.nome+"\t"+str(self.categoria)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)