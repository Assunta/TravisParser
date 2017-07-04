import re

from domain.Goal import Goal
from domain.snapshot import Snapshot

listaMavenWarning=list()
listaTask=list()
listaMessErrore=list()
listaDipendenze=list()
listaSnapshot=list()
listaErroriStatus=list()
#se invece si usa maven
def maven_parser(f, mavenLog):
    # Leggo tutto il log
    for line in f:
        status="passed"
        #zip: /home/travis/build/Nodeclipse/nodeclipse-1/org.nodeclipse.site/target/org.nodeclipse.site-1.0.2-SNAPSHOT.zip lo becca
        # espressione regolare per matchare le snapshot

        if re.match("\A\[INFO\] Building ([^//])*SNAPSHOT", line):
            # print line
            listaSnapshot.append(Snapshot((line.split("[INFO] Building",1)[1]).strip()))
            #potrebbe non esserci snapshot
        elif re.match("\A\[INFO\] Building ([^jar:])([^//])*", line):
            # print line
            listaSnapshot.append(Snapshot((line.split("[INFO] Building",1)[1]).strip()))
        elif re.match("\A\[INFO\] --- ",line):
            # in teoria questo controllo non dovrebbe servire perche' non si dovrebbe poter realizzare una situazione del genere in cui si eseguono goal senza aver dichiarato snapshot
            # if len(listaSnapshot)==0:
            #     listaSnapshot.append(Snapshot("no SNAPSHOT"))
            goal=(line.split("---")[1]).split("@")[0]
            #remove num version
            goal=re.sub(":((\d)*\.)*(\d)*:" , ":", goal).strip()
            #faccio un altro split per eliminare la descrizione del tipo (default-test)
            try:
                listaSnapshot[-1].addGoal(Goal(goal.split("(")[0].strip()))
            except IndexError:
                listaSnapshot.append(Snapshot("EMPTY_SNAPSHOT"))
        #espressione regolare per matchare il running di un test es # Running test ExampleTest
        elif re.match("\ARunning (.)*Test(.*)", line):
            # print line
            try:
                listaSnapshot[-1].addTest(line)
            except IndexError:
                listaSnapshot.append(Snapshot("EMPTY_SNAPSHOT"))
            #espressione per matchare il risultato di un test
        elif re.match("\ATests run:", line):
            # print line
            if not re.match("(.)*Time elapsed:", line):
                listaSnapshot[-1].addTest("Total Tests: \n")
            listaSnapshot[-1].addTest(line)
        # espressione regolare per matchare gli errori che hanno portato al fallimento
        elif re.match("\A\[ERROR\]", line):
            try:
                listaMessErrore.append((listaSnapshot[-1].getGoals())[-1].__str__()+line)
            except IndexError:
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
        elif re.match("\ADone. Your build exited with 1", line):
            listaErroriStatus.append(line.strip())
            status = "failed"
        elif re.match("\ADone. Your build exited with 0", line):
            listaErroriStatus.append(line.strip())
            status = "passed"
        elif re.match("\AYour build has been stopped", line):
            listaErroriStatus.append(line.strip())
            status = "errored"



    # nei log le snapshot appaiono duplicate, non ho capito perche'..
    # quindi sono duplicate anche qui, pero' nella seconda replica fa anche i test, nella prima no
    warning=set(listaMavenWarning)
    mavenLog.addListaErrori(listaMessErrore)
    mavenLog.addListaSnapshot(listaSnapshot)
    mavenLog.addListaWarning(list(warning))
    mavenLog.getErrori()
    mavenLog.setStatus(status)
    mavenLog.setErroriStatus(listaErroriStatus)
    print mavenLog.toJSON()
    return mavenLog