import re
from openpyxl import load_workbook

from domain.GradleLog import GradleLog
from parserGradle import gradle_parser


def checkTipoTask(task):
    if re.match("(.)*compile(.)*", task):
        print task+"\tcompile"
    elif re.match("(.)*packag(.)*", task):
        print task+"\tpackaging"
    else:
        if re.match("(.)*lint(.)*|(.)*Lint(.)*", task):
            print task+"\t Lint"
        elif re.match("(.)*pmd(.)*|(.)*findbug(.)*|(.)*Findbug(.)*|(.)*checkstyle(.)*|(.)*Checkstyle(.)*", task):
            print task+"\t Code analisys"
        elif re.match("(.)*espresso(.)*", task):
            print task+"\t Espresso"
        elif re.match("(.)*generate(.)*", task):
            print task+"\t Task tipo generate"
        elif re.match("(.)*merge(.)*", task):
            print task + "\t Task tipo merge"
        elif re.match("(.)*prepare(.)*", task):
            print task + "\t Task tipo prepare"
        elif re.match("(.)*test(.)*|(.)*Test(.)*", task):
            print task + "\t Test"
        elif re.match("(.)*Jar(.)*|(.)*jar(.)*", task):
            print task + "\t Packaging"
        else:
            print task+"\t NO CLASSIFICATION!!!!!!!"


listaTask=["compileJava","processResources","classes","compileTestJava","jar","javadoc","test","testClasses","processTestResources",
"uploadArchives","clean","cleanTaskName","assemble","check","build","buildNeeded","buildDependents",
"buildConfigName","uploadConfigName","war","ear","jettyRun","jettyRunWar","jettyStop","run","startScripts",
"installDist","distZip","distTar","distZip","compileGroovy","compileTestGroovy","compileSourceSetGroovy",
"groovydoc","compileScala","compileTestScala","compileSourceSetScala","scaladoc","generateGrammarSource",
"generateTestGrammarSource","generateSourceSetGrammarSource","checkstyle","checkstyleMain","checkstyleTest","checkstyleSourceSet",
"codenarcMain","codenarcTest","codenarcSourceSet","findbugsMain","findbugsTest","findbugsSourceSet","jdependMain",
"jdependTest","jdependSourceSet","pmdMain","pmdTest","pmdSourceSet","jacocoTestReport"]


# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\gradle\\jakenjarvis_Android-OrmLiteContentProvider\\Android-OrmLiteContentProvider-161-42820687.txt', 'r')
reponame="square/picasso"
f = open('logs\\gradle\\square_picasso\\picasso-1351-174648005.txt', 'r')
gradleLog = gradle_parser(f, GradleLog(reponame))
#controllo quali goal non sono presenti in tabella
listaTaskDaControllare=list()
for task in gradleLog.getTask():
    listaTaskDaControllare.append(task.getNome().strip())
diff=set(listaTaskDaControllare)-set(listaTask)
if len(diff)>0:
    # stampa
    # wb = load_workbook("taskMancanti.xlsx")
    # ws = wb.active
    # for item in diff:
    #     ws.append([str(item)])
    #     print item
    # wb.save("taskMancanti.xlsx")
    for item in diff:
        checkTipoTask(item)

