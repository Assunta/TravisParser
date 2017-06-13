from openpyxl import load_workbook

from domain.MavenLog import MavenLog
from parserMaven import maven_parser


def loadfile():
    lista=list()
    wb = load_workbook('C:\\Users\\Assunta\\Desktop\\TESI\\TAXONOMY_PUBLISHED.xlsx')
    sheets = wb.sheetnames
    ws = wb[sheets[0]]
    Myrange= range(3,188,1)
    for i in Myrange:
        item="D"+str(i)
        # print ws[item].value
        lista.append(ws[item].value)
    return lista

listaFile=loadfile()
listaGoals=list()
# per eliminare la parte iniziale del nome che io non ho...
for f in listaFile:
    if len(f.split(":"))>2:
        listaGoals.append(f.split(":")[1].strip()+":"+f.split(":")[2].strip())

reponame="tinkerpop/gremlin"
f = open('logs\\maven\\tinkerpop_gremlin\\gremlin-184-170106235.txt', 'r')
mavenLog = maven_parser(f, MavenLog(reponame))
#controllo quali goal non sono presenti in tabella
for snap in mavenLog.getSnapshots():
    diff=set(snap.getGoals())-set(listaGoals)
    if len(diff)>0:
        # stampa
        wb = load_workbook("goalsMancanti.xlsx")
        ws = wb.active
        for item in diff:
            ws.append([item])
            print item
        wb.save("goalsMancanti.xlsx")