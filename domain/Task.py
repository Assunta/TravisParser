import json
import re

import pymysql

from checkTaskGradle import readDbLogin
from utility.dbUtility import getGradleTaskRules


class Task:
    def __init__(self,nome):
        self.name = nome
        self.project= ""
        self.isSkipped= False
        self.isUpdate= False
        self.isFailed= False
        self.category=self.checkTask()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def setProjectName(self, p):
        self.project=p

    def setCategory(self, p):
        self.category = p

    def setIsSkipped(self):
        self.isSkipped= True

    def setIsFailed(self):
        self.isFailed= True

    def setIsUpdate(self):
        self.isUpdate= True

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getProjectName(self):
        return self.project

    def isUpdate(self):
        return self.isUpdate

    def isFailed(self):
        return self.isFailed

    def isSkipped(self):
        return self.isSkipped

    def __str__(self):
        return self.project + ":" + self.name + "\tSkip: " + str(self.isSkipped) + "\tFailed: " + str(self.isFailed) + "\tUpdate: " + str(self.isUpdate) + "\nCategoria " + str(self.category)

    def __eq__(self, other):
        return self.name == other.name

    #add category to task
    def checkTask(self):
        listaDB =getGradleTaskRules()
        trovato = False
        for item in listaDB:
            if self.name is not None:
                if re.match(item.get("regex"), self.name.strip()) and not trovato:
                    return (item.get("category"))
        return("other")
