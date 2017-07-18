# coding=utf-8
from travispy import TravisPy
from domain.Build import Build
import sys
import re
import mmap
import json
# N.B c'e' un problema se nel log ci sono carateri unicode fallisce la scrittura su file
# per risolverlo stackoverflow suggerisce questo...
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
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
def checkGradleMavenFile(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find ('[INFO] Scanning for projects') != -1:
        return "maven"
    else:
        return "gradle"

def checkGradleMaven(f):
    if any('[INFO] Scanning for projects' in s for s in f):
        return "maven"
    else:
        return "gradle"


# qui va la parte comune dove prendiamo
#  nome progetto, il commit, la build, il tempo, quanti job, chi ha fatto il commit e tutte le informazioni che vogliamo
#  anche dai file di configurazione ecc ecc
#  Di norma avremo gia l'oggetto build su cui lavorare
def common_parse(reponame, build_id):
    repo= t.repo(reponame)
    b = Build(build_id)
    #TODO settare la giusta build, non la last
    if (build_id==-1):
        print "*/*/*/*/*/Build non trovata nel log uso la last build */*/*/*/*/*/*"
        build = repo.last_build
        b = Build(repo.last_build)
    else:
         build= t.build(build_id)
         b = Build(build_id)
    commit=build.commit
    msg=""
    msg+="Nome : "+repo.slug
    msg += "\nStato: " + build.state
    b.setStatus(build.state)
    if repo.description is not None:
        msg +="\nDescrizione: " +repo.description
        b.setDescription(repo.description)
    msg +="\nCommit ID: " + str(build.commit_id)
    b.setCommitId(build.commit_id)
    msg +="\nPull request?: "+str(build.pull_request)
    b.setIsPullRequest(build.pull_request)
    if(build.pull_request):
        msg += "\nTitolo pull request: "+build.pull_request_title
        b.setTitlePull(build.pull_request_title)
        msg += "\nNumero pull request: "+str(build.pull_request_number)
        b.setPullId(str(build.pull_request_number))
    msg += "\nIniziato a: "+str(build.started_at)
    b.setStart(str(build.started_at))
    msg += "\nFinito a: "+str(build.finished_at)
    b.setFinish(str(build.finished_at))
    msg += "\nDurata: "+'%02d:%02d' % ((build.duration/60),build.duration%60) # build.duration da isecondi
    b.setDuration(build.duration)
    msg += "\nCommit SHA: " + commit.sha
    b.setCommitSHA(commit.sha)
    msg += "\nBranch: "+commit.branch
    b.setBranch(commit.branch)
    msg += "\nCommit message: "+commit.message
    b.setCommit(commit.message)
    if commit.committed_at is not None:
        msg += "\nData commit: "+ commit.committed_at
        b.setCommitDate(commit.committed_at)
    msg += "\nAutore commit: "+ commit.author_name
    b.setAuthor(commit.author_name)
    msg += "\nEmail Autore commit: "+ commit.author_email
    b.setEmail(commit.author_email)
    #informazioni file travis.yml
    # potremmo estrarre qualche informazione da qui
    #msg += "\n"+build.config
    msg += "\nLanguage: "+build.config["language"]
    b.setLanguage(build.config["language"])
    msg += "\nNumero jobs: "+str(len(build.jobs))
    b.setNumJobs(len(build.jobs))
    msg += "\n"+build.config["language"]
    print msg
    return b



# #se invece si usa maven
# def maven_parse(f):
#     # Leggo tutto il log
#     for line in f:
#         # Task gradle. i task sono rappresentati nella forma \r\r\rnomeTask\r\r\r:
#         # è probabilmente sucfficienete individuare solo lo \r prima e dopo il task per essere sicuri che sia un task
#         if re.match("\A\w+:$",line):
#             print line
#             listaTask.append(line)
#         # espressione regolare per matchare gli errori che hanno portato al fallimento
#         elif re.match("\A\[ERROR\]", line):
#             print line
#             listaMessErrore.append(line)
#         # espressione regolare per matchere i warning di maven. potrebbero esserci informazioni utili
#         elif re.match("\A\[WARNING\]", line):
#             print line
#             listaMavenWarning.append(line)
#         #espressione regolare per matchare la lista delle dipendenze scaricate
#         elif re.match("\[INFO\] Downloaded:", line):
#             str=line.split(" ")[2].split('/')[-1][:-4]
#             print str
#             listaDipendenze.append(str)

