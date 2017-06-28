import re

from domain.RubyLog import RubyLog

listaErrori = list()
listaDipendenze = list()
listaComandi = list()
listaTest = list()

def parserRake(f, log):
    for line in f:
      #espressioni regolari usate per matchare le dipendenze: Using dipendenza, Installing dipendenza
        if re.match("\AUsing ([^//])|\AInstalling", line):
            listaDipendenze.append(line.split(" ")[1].strip()+" "+line.split(" ")[2].strip())
      #espressione regolare per matchare la fine delle dipendenze
            #Bundle complete! 107 Gemfile dependencies, 203 gems now installed.
        elif re.match("Bundle complete!", line):
            listaDipendenze.append((line.strip()))
            print line
    #espressione per matchare errori GEM
            #Gem::InstallError: public_suffix requires Ruby version >= 2.0.
        elif re.match("\AGem::", line):
            #print line
            listaErrori.append(line.strip())
    #espressioni per matchare eventuali errori:
            #The command "git checkout -qf 4e5e0a4120e70724806f96262005226aa80cdb64" failed and exited with 128 during.
            #The command "bundle exec rake test_$DB" exited with 1.
        elif re.match("\AThe command(.)*(failed|exited with 1)(.)*", line):
            listaErrori.append(line.strip())
            #print "Messaggio di errore: "+line
        # The job exceeded the maximum time limit for jobs, and has been terminated.
        elif re.match("(.)*maximum time limit(.)*has been terminated(.)*",line):
            listaErrori.append(line.strip())
            #print "Messaggio di errore: "+line
    #espressioni regolari per la code coverage
        elif re.match("\ACoverage is", line):
            #print line
            listaTest.append(line.strip())
            #se non c'e' la code coverage
        elif re.match("\ACode coverage not enabled", line):
            listaTest.append(line.strip())
            #print line
    #espressione per matchare tutti i comandi $ bundle exec o del tipo $ bin/xxxxx, o $ rake o ./script/ci/build.sh o script/cibuild o $ bash -c "${CMD}
            #mi becca anche questo "export CMD='bundle exec rake spec SPEC_OPTS=\"--tag content\"'",
        elif re.match("(.)*[$] bash(.)*[$]|(.)*[$] script/|(.)*[$] \./scr|(.)*[$] rake|(.)*[$] bundle clean|(.)*[$] bundle install|(.)*[$](.)*bundle exec|(.)*[$](.)*bin/(.)*", line):
            if re.match("(.)*exited with 0", line):
                print ("Messaggio ok: "+line)
            elif re.match("(.)*exited with 1", line):
                listaErrori.append(line.split("$")[1].strip())
                #print ("Messaggio di errore: "+line)
            else:
                listaComandi.append(line.split("$",1)[1].strip())
            print line.split("$")[1].strip()
    # espressioni per i match dei test
        elif re.match("\A(.)* assertions,", line):
            listaTest.append(line.strip())
            #print line
    # match di WARNING:
        elif re.match("\AWARNING: ", line):
            print line
    #match espressioni che riguardano il db (es metasploit)
        elif re.match("== ",line.strip()):
            print line
    # match 178 examples, 2 failures, 12 pending (scenari?) oppure 164 examples, 1 failure
        elif re.match("(\d)* examples, (\d)* failure", line):
            listaTest.append(line.strip())
            #print line
    # match 3564 files, 14440 examples, 36128 expectations, 0 failures, 0 errors
        elif re.match("(\d)* files,", line):
            listaTest.append(line.strip())
    # match rake aborted! No Rakefile found
        elif re.match("\Arake aborted!|\ANo Rakefile found", line):
            listaErrori.append(line.strip())
            #print line
    #match altri messaggi di errori: The job exceeded the maximum time limit for jobs, and has been terminated.
        elif re.match("The job exceeded the maximum time limit for jobs, and has been terminated.", line):
            listaErrori.append(line.strip())
            #print line
    #match 1048 files inspected, no offenses detected  OFFENSES     es(puppet-12769-181370799)
        elif re.match("(\d)* files inspected",line):
            listaTest.append(line.strip())
    #match 258 scenarios (258 passed) e 2730 steps (2730 passed)
        elif re.match("(\d)* (scenarios|steps)",line):
            listaTest.append(line.strip())
    #test failure 1) Refinery::CrudDummyController#update_positions sorts numerically rather than by string key
            #N.B ci saranno questi errori anche quando ci sono esempi pending, pero' cmq il test non fallisce
        elif re.match("\A  (\d)*\)", line):
            listaErrori.append(line.strip())
    # errori di dipendenze
        elif re.match("\ASome gems seem to be missing", line):
            listaErrori.append(line)
    #match Done: Job Cancelled
        elif re.match("\ADone: Job Cancelled",line):
            listaErrori.append(line.strip())
        else:
            checkOtherTools(line,log)

    log.setDipendenze(listaDipendenze)
    log.addListaErrori(listaErrori)
    log.setTest(listaTest)
    log.setCommand(listaComandi)
    print log.toJSON()
    return log

def checkOtherTools(line, log):
    # messaggi di Coveralls (code coverage tool)
    if re.match("\A\[Coveralls\](.)*", line):
        print line
    # check for use NPM (npm is the package manager for JavaScript and the world 's largest software registry.)
    elif re.match("\Anpm (.)*", line):
        print "NPM"+line
    # check BRAKEMAN A static analysis security vulnerability scanner for Ruby
    # progetto (ManageIQ/manageiq)
    # i risultati dell'analisi sono nel tipo
    # | Controllers       | 71    |
    elif re.match("\|(.)*\|(.)*\|",line):
        print "BRAKEMAN "+line
        listaTest.append(line)
    # per vedere se si usa Bullet (The Bullet gem is designed to help you increase your application's performance by reducing the number of queries it makes. )
    elif re.match("\ABullet not enabled", line):
        print line
    # check uso RuboCop (is a Ruby static code analyzer)
    #TODO da testare
    elif re.match("\ATesting with RuboCop(.)*", line):
        print "Uso RuboCop "
    # Lo becco anche sopra
    # elif re.match("\A(.)*files inspected,(.)*", line):
    #     print line
    elif re.match("\ARuboCop failed!", line):
        listaErrori.append(line)

