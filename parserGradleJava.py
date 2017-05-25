from travispy import TravisPy
import sys
import re
# N.B c'e' un problema se nel log ci sono carateri unicode fallisce la scrittura su file
# per risolverlo stackoverflow suggerisce questo...
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('token.config', 'r')
token=f.readline()
t = TravisPy.github_auth(str(token))

listaTask=[]
listaMessErrore=[]
# repo = t.repo("mockito/mockito")
# build = t.build(repo.last_build_id)
# print build.state
f = open('logs\\mockito.txt', 'r')

# qui va la parte comune dove prendiamo
#  nome progetto, il commit, la build, il tempo, quanti job, chi ha fatto il commit e tutte le informazioni che vogliamo
#  anche dai file di configurazione ecc ecc

#dopo di che se identigfichiamo che si usa gradle si esegue quanto di seguito

#questo ciclo for lo dovremmo fare per tutti i logs associati ai jobs di una certa build
#per ora leggiamo un file, ma poi dovremmo iterare su una stringa qulla che ritorna da t.log(job.log_id).body
for line in f:
    #espressione regolare per matchare i task di uno script gradle
    if re.match("\A:\w+", line):
        print line
        listaTask.append(line)
    # espressione regolare per matchare il motivo di un failure
    if re.match("\A>|   >", line) : # and la build sappiamo che e' fallita
        print line
        listaMessErrore.append(line)

#nella lista dei task ci potrebbero essere alcuni che sono falliti e che cmq non hanno inficiato
#sul buon esito della build. Esempio
#:assertReleaseNeeded FAILED
#>   Release is needed: false
print "************************************"
for task in listaTask:
    if re.match("(.)*FAILED", task):
        print task
    # e poi ci sono anche quelli UP-TO-DATE che dovrebbero essere quelli che sono gia' aggiornati e quindi non serve eseguirli credo...
    if re.match("(.)*UP-TO-DATE", task):
        print task

