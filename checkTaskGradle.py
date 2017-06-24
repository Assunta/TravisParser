import re
import pymysql


def readDbLogin():
    f = open('db_login', 'r')
    host = f.readline().strip()
    username = f.readline().strip()
    password = f.readline().strip()
    return [host, username, password]

def getTaskDb():
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
            sql = "SELECT `*`FROM `regoletaskgradle`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                lista.append(r)
    finally:
        connection.close()
        return lista

def checkTask(gradleLog):
    # leggo i task classificati dal db
    listaDB = getTaskDb()
    for task in gradleLog.getTask():
        trovato = False
        for item in listaDB:
            if re.match(item.get("EspressioneRegolare"), task.getNome().strip()) and not trovato:
                task.setCategoria(item.get("Categoria"))
                trovato = True
        if not trovato:
            task.setCategoria("other")

# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\gradle\\jakenjarvis_Android-OrmLiteContentProvider\\Android-OrmLiteContentProvider-161-42820687.txt', 'r')
# reponame="square/picasso"
# f = open('logs\\gradle\\square_picasso\\picasso-1351-174648005.txt', 'r')
# gradleLog = gradle_parser(f, GradleLog(reponame))
# checkTask(gradleLog)







