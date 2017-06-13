from openpyxl import load_workbook

from domain.GradleLog import GradleLog
from parserGradle import gradle_parser


listaTask=["compileJava","processResources","classes","compileTestJava","jar","javadoc","test","testClasses","processTestResources",
"uploadArchives","clean","cleanTaskName","assemble","check","build","buildNeeded","buildDependents",
"buildConfigName","uploadConfigName","war","ear","jettyRun","jettyRunWar","jettyStop","run","startScripts",
"installDist","distZip","distTar","distZip","compileGroovy","compileTestGroovy","compileSourceSetGroovy",
"groovydoc","compileScala","compileTestScala","compileSourceSetScala","scaladoc","generateGrammarSource",
"generateTestGrammarSource","generateSourceSetGrammarSource","checkstyle","checkstyleMain","checkstyleTest","checkstyleSourceSet",
"codenarcMain","codenarcTest","codenarcSourceSet","findbugsMain","findbugsTest","findbugsSourceSet","jdependMain",
"jdependTest","jdependSourceSet","pmdMain","pmdTest","pmdSourceSet","jacocoTestReport"]


reponame="jakenjarvis/Android-OrmLiteContentProvider"
f = open('logs\\gradle\\jakenjarvis_Android-OrmLiteContentProvider\\Android-OrmLiteContentProvider-161-42820687.txt', 'r')
# reponame="jAssunta/example"
# f = open('logs\\old\\example.txt', 'r')
gradleLog = gradle_parser(f, GradleLog(reponame))
#controllo quali goal non sono presenti in tabella
listaTaskDaControllare=list()
for task in gradleLog.getTask():
    listaTaskDaControllare.append(task.getNome().strip())
diff=set(listaTaskDaControllare)-set(listaTask)
if len(diff)>0:
    # stampa
    wb = load_workbook("taskMancanti.xlsx")
    ws = wb.active
    for item in diff:
        ws.append([str(item)])
        print item
    wb.save("taskMancanti.xlsx")