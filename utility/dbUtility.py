import pymysql

#read db username and password in file db_login
def readDbLogin():
    f = open('C:\\Users\Assunta\\Desktop\\TESI\\TravisParser\\config\\db_login', 'r')
    host = f.readline().strip()
    username = f.readline().strip()
    password = f.readline().strip()
    return [host, username, password]

#get an object connection
#after the use remamber to close the connection
def getConnection():
    credenziali= readDbLogin()
    connection = pymysql.connect(host=credenziali[0],
                                 user=credenziali[1],
                                 password=credenziali[2],
                                 db='travisdb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


#get all the items in table rubystatusmessage
def getRubyStatusMessages():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubystatusmessages`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

#get all the items in table rubytools
def getRubyTools():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubytools`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

#get all the items in table rubytestmessags
def getRubyTestMessages():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubytestmessages`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

#get all the items in table rubyerror
def getRubyErrors():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubyerror`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records


#get all the items in table mavenerrors
def getMavenErrors():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `mavenerrors`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records