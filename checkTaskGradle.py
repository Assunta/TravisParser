import re
import pymysql



def readDbLogin():
    f = open('C:\\Users\Assunta\\Desktop\\TESI\\TravisParser\\config\\db_login', 'r')
    host = f.readline().strip()
    username = f.readline().strip()
    password = f.readline().strip()
    return [host, username, password]

# def getTaskDb():
#     lista= list()
#     credenziali= readDbLogin()
#     connection = pymysql.connect(host=credenziali[0],
#                                  user=credenziali[1],
#                                  password=credenziali[2],
#                                  db='travisdb',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT `*`FROM `regoletaskgradle`"
#             cursor.execute(sql)
#             for r in cursor.fetchall():
#                 lista.append(r)
#     finally:
#         connection.close()
#         return lista
#
# def checkTask(lista):
#     # leggo i task classificati dal db
#     listaDB = getTaskDb()
#     #
#     # for command in listaCommand:
#     for task in lista:
#         trovato = False
#         for item in listaDB:
#             if task is not None:
#                 if re.match(item.get("EspressioneRegolare"), task.getNome().strip()) and not trovato:
#                     task.setCategoria(item.get("Categoria"))
#                     trovato = True
#             if not trovato and task is not None:
#                 task.setCategoria("other")









