# coding=utf-8
from travispy import TravisPy
import sys
import re
import mmap
import json
# N.B c'e' un problema se nel log ci sono carateri unicode fallisce la scrittura su file
# per risolverlo stackoverflow suggerisce questo...
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('token.config', 'r')
token=f.readline()
t = TravisPy.github_auth(str(token))

listaDipendenze=list()
listaTask=list()
listaMavenWarning=list()
listaMessErrore=list()
listaTaskSkippati=list()
listaErroriPrecedentiAiTask=list()
listNote=list()
# repo = t.repo("mockito/mockito")
# build = t.build(repo.last_build_id)
# print build.state




#check gradle o maven
# you can alleviate the possible memory problems by using mmap.mmap()
# to create a "string-like" object that uses the underlying file
# (instead of reading the whole file in memory):
def checkGradleMaven(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find ('[INFO] Scanning for projects') != -1:
        return "maven"
    else:
        return "gradle"




# qui va la parte comune dove prendiamo
#  nome progetto, il commit, la build, il tempo, quanti job, chi ha fatto il commit e tutte le informazioni che vogliamo
#  anche dai file di configurazione ecc ecc
#  Di norma avremo gia l'oggetto build su cui lavorare
def common_parse(reponame, build_id):
    repo= t.repo(reponame)
    #TODO settare la giusta build, non la last
    # build= t.build(build_id)
    build=repo.last_build
    commit=build.commit
    print "Nome : "+repo.slug
    print "Stato: " + build.state
    if repo.description is not None:
         print "Descrizione: " +repo.description
    print "Build number: " + build.number
    print "Commit ID: " + str(build.commit_id)
    print "Pull request?: "+str(build.pull_request)
    if(build.pull_request):
        print "Titolo pull request: "+build.pull_request_title
        print "Numero pull request: "+str(build.pull_request_number)
    print "Iniziato a: "+str(build.started_at)
    print "Finito a: "+str(build.finished_at)
    print "Durata: "+'%02d:%02d' % ((build.duration/60),build.duration%60) # build.duration da isecondi
    print "Commit SHA: " + commit.sha
    print "Branch: "+commit.branch
    print "Commit message: "+commit.message
    print "Data commit: "+ commit.committed_at
    print "Autore commit: "+ commit.author_name
    print "Email Autore commit: "+ commit.author_email
    #informazioni file travis.yml
    # potremmo estrarre qualche informazione da qui
    print build.config
    print "Language: "+build.config["language"]
    print "Numero jobs: "+str(len(build.jobs))
    pass



#se invece si usa maven
def maven_parse(f):
    # Leggo tutto il log
    for line in f:
        # Task gradle. i task sono rappresentati nella forma \r\r\rnomeTask\r\r\r:
        # è probabilmente sucfficienete individuare solo lo \r prima e dopo il task per essere sicuri che sia un task
        if re.match("\A\w+:$",line):
            print line
            listaTask.append(line)
        # espressione regolare per matchare gli errori che hanno portato al fallimento
        elif re.match("\A\[ERROR\]", line):
            print line
            listaMessErrore.append(line)
        # espressione regolare per matchere i warning di maven. potrebbero esserci informazioni utili
        elif re.match("\A\[WARNING\]", line):
            print line
            listaMavenWarning.append(line)
        #espressione regolare per matchare la lista delle dipendenze scaricate
        elif re.match("\[INFO\] Downloaded:", line):
            str=line.split(" ")[2].split('/')[-1][:-4]
            print str
            listaDipendenze.append(str)

