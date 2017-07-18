import re

from travispy import TravisPy
import sys

#usa questo script da riga di comando fornendo come parametro il nome del progetto di cui avere il log della last build
# reindirizando l'output su un file
# es python logsTavis.py Assunta/example > example.txt

# N.B c'e' un problema se nel log ci sono carateri unicode fallisce la scrittura su file
# per risolverlo stackoverflow suggerisce questo...
reload(sys)
sys.setdefaultencoding('utf-8')


maxnumberbuilds=2


ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
token=f.readline()
t = TravisPy.github_auth(str(token))
if len(sys.argv)>1:
    repo = t.repo(str(sys.argv[1]))
    builds = t.builds(slug=repo.slug)
    for count in range(0,min(maxnumberbuilds,len(builds))):
        build=builds[count]
        for job_id in build.job_ids:
            job=t.job(job_id)
            fOut = open('logs/' + sys.argv[1].split('/')[-1] + '-' + build.number + '-'+str(job.log_id)+'.txt', 'w+')
            text=t.log(job.log_id).body
            text=ansi_escape.sub('', text)
            print fOut.name
            fOut.write(text)
else:
    print ("Inserire il parametro a riga di comando con il nome del repository di cui vuoi avere la build")

