import re

from snapshot import Snapshot

listaMavenWarning=list()
listaTask=list()
listaMessErrore=list()
listaDipendenze=list()
listaSnapshot=list()
#se invece si usa maven
def maven_parser(f):
    # Leggo tutto il log
    for line in f:
        # Task gradle. i task sono rappresentati nella forma \r\r\rnomeTask\r\r\r:
        # e' probabilmente sucfficienete individuare solo lo \r prima e dopo il task per essere sicuri che sia un task
        #per matchare task ant
        # if re.match("\A\w+:$",line):
        #     print line
        #     listaTask.append(line)
        # espressione regolare per matchare le snapshot
        if re.match("\A\[INFO\] Building ([^:])*SNAPSHOT", line) :
            print line
            listaSnapshot.append(Snapshot(line))
        elif re.match("\A\[INFO\] --- ",line):
            print line
            listaSnapshot[-1].addGoal(line.split("---")[1])
        # espressione regolare per matchare gli errori che hanno portato al fallimento
        elif re.match("\A\[ERROR\]", line):
            print line
            listaMessErrore.append(line)
        # espressione regolare per matchere i warning di maven. potrebbero esserci informazioni utili
        elif re.match("\A\[WARNING\]", line):
           # print line
            listaMavenWarning.append(line)
        #espressione regolare per matchare la lista delle dipendenze scaricate
        elif re.match("\[INFO\] Downloaded:", line):
            #str=line.split(" ")[2].split('/')[-1][:-4]
            if not(re.match("./maven/plugin.", line) or re.match("(.)*plugin(s)*", line) or re.match("(.)*/maven/(.)*maven-(.)*", line) ):
                str=line.split(" ")[2].split('/')[-1][:-4]
               # print str
                #print "***"+line
                listaDipendenze.append(str)

    #print str(len(listaSnapshot))
    for s in listaSnapshot:
        print s