import re

def gradle_parser(f):
    listaTask = list()
    listaTaskUPDATE= list()
    listaTaskFailed=list()
    listaMessErrore = list()
    listaTaskSkippati = list()
    listaErroriPrecedentiAiTask = list()
    listNote =list()
    # questo ciclo for lo dovremmo fare per tutti i logs associati ai jobs di una certa build
    # per ora leggiamo un file, ma poi dovremmo iterare su una stringa qulla che ritorna da t.log(job.log_id).body
    for line in f:
        # espressione regolare per matchare i task di uno script gradle
        if re.match("\A:\w+", line):
            task=line.split(" ")[0]
            listaTask.append(task)
            if re.match("(.)*UP-TO-DATE", line):
                listaTaskUPDATE.append(line)
            elif re.match("(.)*FAILED", line):
                listaTaskFailed.append(line)
            # espressione regolare per matchare messaggi del tipo Note: /example/picasso/PicassoSampleAdapter.java uses or overrides a deprecated API.
            # che cmq potrebbero essere informazioni interessanti
        elif re.match("Note: ", line):
            listNote.append(listaTask[-1]+"\t"+line)
        #espressioni del tipo Skipping task xxxxx per questo motivo
        elif re.match("\ASkipping task", line):
            listaTaskSkippati.append(listaTask[-1]+"\t"+line)
        # espressione regolare per matchare il motivo di un failure
        elif re.match("\A( )*>", line):  # and la build sappiamo che e' fallita
            print line
            listaMessErrore.append(listaTask[-1]+"\t"+line)


        # a volte la build fallisce ancor prima che iniziano i task con messaggi di errore del tipo
        #    Error: Invalid - -abiarmeabi - v7a for the selected target.
        # le stringhe precedenti non matchano niente in questo caso qindi aggiungo:
        elif re.match("\AError", line):
            print line
            listaErroriPrecedentiAiTask.append(line)

           # nella lista dei task possiamo distinguere anche tra task che appartengono a progetti diversi
            # (es in un progetto android ci potrebbe essere un modulo app, e un modulo library )
    modules = set([])
    for task in listaTask:
        if task.count(":") == 2:
            module_name = task.split(":")[1]
            modules.add(module_name)
        else:
            modules.add(" ")  # nel caso in cui non sia specificato il nome del modulo
    print "TASKS: "

    for task in set(listaTask):
        print task
    print "TASKS UPDATE: "
    for task in listaTaskUPDATE:
        print task
    print "TASKS: Failed\n"
    for task in listaTaskFailed:
        print task
    print "Task with note"
    for task in listNote:
        print task
    print "Task skippati\n"
    for task in listaTaskSkippati:
        print task
    print "Progetti a cui appartengono i task\n"
    for m in modules:
        print m
    # nella lista dei task ci potrebbero essere alcuni che sono falliti e che cmq non hanno inficiato
    # sul buon esito della build. Esempio
    #:assertReleaseNeeded FAILED
    # >   Release is needed: false



        # N.B in lista task ci possono essere anche dei duplicati perche' alcuni task sono del tipo:
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) started.
        # :sample:compileDebugUnitTestSources
        # Skipping task ':sample:compileDebugUnitTestSources' as it has no actions.
        # :sample:compileDebugUnitTestSources UP-TO-DATE
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) completed. Took 0.0 secs.

