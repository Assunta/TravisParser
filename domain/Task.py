class Task:
    def __init__(self,nome):
        self.nome = nome
        self.progetto=""
        self.isSkipped= False
        self.isUpdate= False
        self.isFailed= False
        self.categoria="Non_classificato"

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