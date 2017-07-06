import pymysql
from openpyxl import load_workbook

from checkTaskGradle import readDbLogin
from domain.MavenLog import MavenLog
from parserMaven import maven_parser
#TODO non va bene impostato cosi'
def getGoalDb():
    lista= list()
    credenziali= readDbLogin()
    connection = pymysql.connect(host=credenziali[0],
                                 user=credenziali[1],
                                 password=credenziali[2],
                                 db='travisdb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `goalmaven`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                lista.append(r)
    finally:
        connection.close()
        return lista

listaFile=getGoalDb()
listaGoals=list()
# per eliminare la parte iniziale del nome che io non ho...
for f in listaFile:
    f2=f.get("Goal")
    print f2
    if len(f2.split(":"))>2:
        listaGoals.append(f2.split(":")[1].strip()+":"+f2.split(":")[2].strip())

reponame="tinkerpop/gremlin"
f = open('logs\\maven\\tinkerpop_gremlin\\gremlin-184-170106235.txt', 'r')
mavenLog = maven_parser(f, MavenLog(reponame))
#controllo quali goal non sono presenti in tabella
for snap in mavenLog.getSnapshots():
    snapGoal= list()
    for g in snap.getGoals():
        snapGoal.append(g.getName())
    diff=set(snapGoal)-set(listaGoals)
    if len(diff)>0:
        # stampa
        wb = load_workbook("goalsMancanti.xlsx")
        ws = wb.active
        for item in diff:
            #print item
            ws.append([item])

        wb.save("goalsMancanti.xlsx")