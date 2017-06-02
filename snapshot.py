class Snapshot:
    def __init__(self,nome):
        self.nome=nome
        self.listaGoal= list()
        self.test=""

    def addGoal(self, goal):
        self.listaGoal.append(goal)

    def addTest(self, test):
        self.test+= test

    def getNome(self):
        return self.nome

    def getGoals(self):
        return self.listaGoal

    def getTest(self):
        return self.test

    def __str__(self):
        str=""
        str+= self.nome
        for g in self.listaGoal:
            str+="\n" +g
        str+="\n"+ self.test
        return str