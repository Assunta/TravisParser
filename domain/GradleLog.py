from domain.GradleCommand import GradleCommand


class GradleLog:
    def __init__(self,nomeBuild):
        self.status = ""
        self.nome = nomeBuild
        self.listaCommand = list()
        #self.listaTasks = list()
        self.listaDipendenze = list()
        #TODO potrei mettere listaErrori come Task e String
        self.listaErrori = list()
        self.listaNote = set()

    def getCommand(self):
        return self.listaCommand

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def setStatus(self, s):
        self.status = s

    # def getTask(self):
    #     return self.listaTasks

    def getDipendenze(self):
        return self.listaDipendenze

    def addDipendenze(self, list):
        self.listaDipendenze = list

    def getErrori(self):
        return self.listaErrori

    # def addTask(self, t):
    #     self.listaTasks.append(t)

    # def addListaTasks(self, list):
    #     self.listaTasks = list

    def addErrore(self, s):
        self.listaErrori.append(s)

    def addListaErrori(self, list):
        self.listaErrori = list

    def addNote(self, s):
        self.listaNote.append(s)

    def addListaNote(self, list):
        self.listaNote = list

    def setCommand(self, nome):
        self.listaCommand.append(GradleCommand(nome))

    def addCommands(self, commands):
        self.listaCommand=commands

    def __str__(self):
        ret = self.nome + "\n" + self.status + "\n"
        ret+= "Dipendenze:\n"
        for d in self.listaDipendenze:
            ret+= str(d)+"\t"
        ret+= "NOTE:\n"
        for n in self.listaNote:
            ret+= str(n)+"\n"
        ret+= "Errori:\n"
        for e in self.listaErrori:
            ret+= str(e)+"\n"
        ret+="Comandi:\n"
        for c in self.listaCommand:
            ret+=str(c)+"\n"
        return ret