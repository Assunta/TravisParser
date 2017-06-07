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
    #espressioni regolari per la code coverage
            #nel caso in cui si usa uno strumento per la code coverage es Coveralls
        elif re.match("\ACoverage is", line):
            print line
            #se non c'e' la code coverage
        elif re.match("\ACode coverage not enabled", line):
            print line
            # per vedere se si usa Bullet (The Bullet gem is designed to help you increase your application's performance by reducing the number of queries it makes. )
        elif re.match("\ABullet not enabled",line):
            print line
    #espressione per matchare tutti i comandi $ bundle exec
        elif re.match("(.)*bundle exec(.)*", line):
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

    print "Dipendenze "
    for dip in listaDipendenze:
        print dip
