import re


def parserRake(f):
    listaDipendenze= list()
    for line in f:
      #espressioni regolari usate per matchare le dipendenze: Using dipendenza, Installing dipendenza
        if re.match("\AUsing ([^//])|\AInstalling", line):
            listaDipendenze.append(line.split(" ")[1]+" "+line.split(" ")[2])
      #espressione regolare per matchare la fine delle dipendenze
            #Bundle complete! 107 Gemfile dependencies, 203 gems now installed.
        elif re.match("Bundle complete!", line):
            print line
    #espressione per matchare errori GEM
            #Gem::InstallError: public_suffix requires Ruby version >= 2.0.
        elif re.match("\AGem::", line):
            print line
    #espressioni per matchare eventuali errori:
            #The command "git checkout -qf 4e5e0a4120e70724806f96262005226aa80cdb64" failed and exited with 128 during.
            #The command "bundle exec rake test_$DB" exited with 1.
        elif re.match("\AThe command(.)*(failed|exited with 1)(.)*", line):
            print "Messaggio di errore: "+line
        # The job exceeded the maximum time limit for jobs, and has been terminated.
        elif re.match("(.)*maximum time limit(.)*has been terminated(.)*",line):
            print "Messaggio di errore: "+line
    #espressioni regolari per la code coverage
        elif re.match("\ACoverage is", line):
            print line
            #se non c'e' la code coverage
        elif re.match("\ACode coverage not enabled", line):
            print line
            # per vedere se si usa Bullet (The Bullet gem is designed to help you increase your application's performance by reducing the number of queries it makes. )
        elif re.match("\ABullet not enabled",line):
            print line
    #espressione per matchare tutti i comandi $ bundle exec
            #TODO sistemare, perche' potrebbe matchare anche altro
        elif re.match("([^export])*bundle exec(.)*", line):
            if re.match("(.)*exited with 0", line):
                print ("Messaggio ok: "+line)
            elif re.match("(.)*exited with 1", line):
                print ("Messaggio di errore: "+line)
            print line
    # espressioni per i match dei test
        elif re.match("\A(.)* assertions,", line):
            print line
    # match di WARNING:
        elif re.match("\AWARNING: ", line):
            print line
    #match espressioni che riguardano il db (es metasploit)
        elif re.match("== ",line):
            print line
        else:
            checkOtherTools(line)

    # print "Dipendenze "
    # for dip in listaDipendenze:
    #     print dip

def checkOtherTools(line):
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
    # check uso RuboCop (is a Ruby static code analyzer)
    #TODO da testare
    elif re.match("\ATesting with RuboCop(.)*", line):
        print "Uso RuboCop "
    elif re.match("\A(.)*files inspected,(.)*", line):
        print "Result rubocop"
