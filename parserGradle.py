import re

from checkTaskGradle import checkTask
from domain.GradleCommand import GradleCommand
from domain.Task import Task


def gradle_parser(f, gradleLog):
    listaTask = list()
    listaCommand=list()
    #metto un comando default nel caso in cui non viene eseguito nessun comando, teoricamente non dovrebbe mai avere task
    listaCommand.append(GradleCommand("DEFAULT"))
    listaMessErrore = list()
    #TODO!!!!!!!!!!!!!! gli errori precedenti ai task per ora non sono inseriti nella lista degli errori
    listaErroriPrecedentiAiTask = list()
    listNote =list()
    listaDipendenze=list()
    # questo ciclo for lo dovremmo fare per tutti i logs associati ai jobs di una certa build
    # per ora leggiamo un file, ma poi dovremmo iterare su una stringa qulla che ritorna da t.log(job.log_id).body
    for line in f:
        #espressione regolare per matchare i vari comandi per distinguere i task a quale comando fanno riferimento
        if re.match("(.)*[$](.)*./gradlew|(.)*[$] *gradle", line):
            #aggiungo i task al command precedente e ne creo un altro
            listaCommand[-1].addListaTasks(listaTask)
            listaTask= list()
            listaCommand.append(GradleCommand(line.strip()))
        # espressione regolare per matchare i task di uno script gradle
        if re.match("\A:\w+", line):
            task=line.split(" ")[0]
            if task.count(":") == 2:
                module_name = task.split(":")[1]
                task_name = task.split(":")[2]
                t=Task(task_name)
                t.setNomeProgetto(module_name)
            else:
                t = Task(task.replace(":","").strip())
                t.setNomeProgetto(" ")

            if re.match("(.)*UP-TO-DATE", line):
                t.setIsUpdate()
            elif re.match("(.)*FAILED", line) or re.match("(.)*EXCEPTION", line):
                t.setIsFailed()
            elif re.match("(.)*SKIPPED", line):
                t.setIsSkipped()

            if len(listaTask)>0:
                taskOld=listaTask.pop(-1)
                listaTask.append(taskOld)
                if taskOld is not None and not taskOld.__eq__(t):
                    listaTask.append(t)
            else:
                listaTask.append(t)
            # espressione regolare per matchare messaggi del tipo Note: /example/square_picasso/PicassoSampleAdapter.java uses or overrides a deprecated API.
            # che cmq potrebbero essere informazioni interessanti
        elif re.match("Note: ", line):
            try:
                listNote.append(listaTask[-1].getNome()+"\t"+line)
            except IndexError:
                listNote.append("NO_TASK" + "\t" + line)
        #espressioni del tipo Skipping task xxxxx per questo motivo
        elif re.match("\ASkipping task(.)*", line):
            #listaTaskSkippati.append(listaTask[-1]+"\t"+line)
            listaTask[-1].setIsSkipped()
            #listaTask.append(t)
        # espressione regolare per matchare il motivo di un failure
        elif re.match("\A( )*>|Task (.)* not found ", line):  # and la build sappiamo che e' fallita
            try:
                listaMessErrore.append(listaTask[-1].getNome()+"\t"+line)
            except IndexError:
                listaMessErrore.append("NO_TASK" + "\t" + line)
        # nella lista dei task ci potrebbero essere alcuni che sono falliti e che cmq non hanno inficiato
        # sul buon esito della build. Esempio
        #:assertReleaseNeeded FAILED
        # >   Release is needed: false

        # a volte la build fallisce ancor prima che iniziano i task con messaggi di errore del tipo
        #    Error: Invalid - -abiarmeabi - v7a for the selected target.
        # le stringhe precedenti non matchano niente in questo caso qindi aggiungo:
        elif re.match("\AError|\AThe command(.)*failed and exited(.)*|\ANo output has been received", line):
            print line
            listaErroriPrecedentiAiTask.append(line)
        elif re.match("\ADownload ", line):
            listaDipendenze.append(line)



    #print "**********"+str(len(listaCommand))
    listaCommand[-1].addListaTasks(listaTask)
    gradleLog.addCommands(listaCommand)
    #gradleLog.addListaTasks(listaTask)
    gradleLog.addListaErrori(listaMessErrore)
    gradleLog.addListaNote(set(listNote))
    gradleLog.addDipendenze(listaDipendenze)
    checkTask(gradleLog)

    print gradleLog
    return gradleLog



        # N.B in lista task ci possono essere anche dei duplicati perche' alcuni task sono del tipo:
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) started.
        # :sample:compileDebugUnitTestSources
        # Skipping task ':sample:compileDebugUnitTestSources' as it has no actions.
        # :sample:compileDebugUnitTestSources UP-TO-DATE
        # :sample:compileDebugUnitTestSources (Thread[Daemon worker,5,main]) completed. Took 0.0 secs.

