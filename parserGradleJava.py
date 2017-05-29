from travispy import TravisPy
import sys
import re
# N.B c'e' un problema se nel log ci sono carateri unicode fallisce la scrittura su file
# per risolverlo stackoverflow suggerisce questo...
reload(sys)
sys.setdefaultencoding('utf-8')

reponame="OneBusAway/onebusaway-android"
f = open('token.config', 'r')
token=f.readline()
t = TravisPy.github_auth(str(token))

listaTask=[]
listaMessErrore=[]
listaTaskSkippati=[]
listaErroriPrecedentiAiTask=[]
listNote=[]
# repo = t.repo("mockito/mockito")
# build = t.build(repo.last_build_id)
# print build.state
f = open('logs\\oneBusWay.txt', 'r')



#dopo di che se identigfichiamo che si usa gradle si esegue quanto di seguito
def gradle_parse():
    # questo ciclo for lo dovremmo fare per tutti i logs associati ai jobs di una certa build
    # per ora leggiamo un file, ma poi dovremmo iterare su una stringa qulla che ritorna da t.log(job.log_id).body
    for line in f:
        # espressione regolare per matchare i task di uno script gradle
        if re.match("\A:\w+", line):
            print line
            listaTask.append(line)
        # espressione regolare per matchare il motivo di un failure
        elif re.match("\A( )*>", line):  # and la build sappiamo che e' fallita
            print line
            listaMessErrore.append(line)
        # espressioni del tipo Skipping task xxxxx per questo motivo
        elif re.match("\ASkipping task", line):
            print line
            listaTaskSkippati.append(line)
        # espressione regolare per matchare messaggi del tipo Note: /example/picasso/PicassoSampleAdapter.java uses or overrides a deprecated API.
        # che cmq potrebbero essere informazioni interessanti
        elif re.match("Note: ", line):
            print line
            listNote.append(line)
        # a volte la build fallisce ancor prima che iniziano i task con messaggi di errore del tipo
        #    Error: Invalid - -abiarmeabi - v7a for the selected target.
        # le stringhe precedenti non matchano niente in questo caso qindi aggiungo:
        elif re.match("\AError", line):
            print line
            listaErroriPrecedentiAiTask.append(line)

    # nella lista dei task ci potrebbero essere alcuni che sono falliti e che cmq non hanno inficiato
    # sul buon esito della build. Esempio
    #:assertReleaseNeeded FAILED
    # >   Release is needed: false
    print "************************************"
    for task in listaTask:
        if re.match("(.)*FAILED", task):
            print task
        # e poi ci sono anche quelli UP-TO-DATE che dovrebbero essere quelli che sono gia' aggiornati e quindi non serve eseguirli credo...
        if re.match("(.)*UP-TO-DATE", task):
            print task

        # nella lista dei task possiamo distinguere anche tra task che appartengono a progetti diversi
        # (es in un progetto android ci potrebbe essere un modulo app, e un modulo library )
    modules = set([])
    for task in listaTask:
        if task.count(":") == 2:
            module_name = task.split(":")[1]
            modules.add(module_name)
        else:
            modules.add(" ")  # nel caso in cui non sia specificato il nome del modulo
    for m in modules:
        print m

        # N.B in lista task ci possono essere anche dei duplicati perche' alcuni task sono del tipo:
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) started.
        # :sample:compileDebugUnitTestSources
        # Skipping task ':sample:compileDebugUnitTestSources' as it has no actions.
        # :sample:compileDebugUnitTestSources UP-TO-DATE
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) completed. Took 0.0 secs.



# qui va la parte comune dove prendiamo
#  nome progetto, il commit, la build, il tempo, quanti job, chi ha fatto il commit e tutte le informazioni che vogliamo
#  anche dai file di configurazione ecc ecc
#  Di norma avremo gia l'oggetto build su cui lavorare
def common_parse():
    repo= t.repo(reponame)
    build=repo.last_build
    commit=build.commit
    print "Nome : "+repo.slug
    print "Descrizione: " +repo.description
    print "Build number: " + build.number
    print "Commit ID: " + str(build.commit_id)
    print "Pull request?: "+str(build.pull_request)
    if(build.pull_request):
        print "Titolo pull request: "+build.pull_request_title
        print "Numero pull request: "+str(build.pull_request_number)
    print "Iniziato a: "+str(build.started_at)
    print "Finito a: "+str(build.finished_at)

    print "Commit SHA: " + commit.sha
    print "Branch: "+commit.branch
    print "Commit message: "+commit.message
    print "Data commit: "+ commit.committed_at
    print "Autore commit: "+ commit.author_name
    print "Email Autore commit: "+ commit.author_email


    pass


common_parse()
gradle_parse()