from travispy import TravisPy
import sys

#usa questo script da riga di comando fornendo come parametro il nome del progetto di cui avere il log della last build
# reindirizando l'output su un file
# es python logsTavis.py Assunta/example > example.txt

# N.B c'è un problema se nel log ci sono carateri unicode fallisce la scrittura su file

t = TravisPy.github_auth("8d3479c909b4c1398b8841fac2c3dcf0bd6f19bd")
if len(sys.argv)>1:
    repo = t.repo(str(sys.argv[1]))
    build = t.build(repo.last_build_id)
    for job in build.jobs:
        print t.log(job.log_id).body
else:
    print "Inserire il parametro a riga di comando con il nome del repository di cui vuoi avere la build"

