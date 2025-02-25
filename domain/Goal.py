import pymysql
import json

from checkTaskGradle import readDbLogin
from utility.dbUtility import findCategory


class Goal:
    def __init__(self,username,nome):
        self.name = nome
        self.category=findCategory(username,self.name)

    def setCategory(self, p):
        self.category = p

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def __str__(self):
        return self.name + "\t" + str(self.category)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)