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
def getStatusMessages():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `statusmessages`"
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

def getGradleTaskRules():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `taskgradlerules`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records


def findCategory(name):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `goalmaven` WHERE `Goal`LIKE %s"
            if cursor.execute(sql, ("%"+name+"%")) >0:
                result = cursor.fetchone()
                category=(result.get("Category"))
            else:
                category="other"
    finally:
        connection.close()
        return category

#this ethod allow to get user key
def findUser(name):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users` WHERE `Git_name`= %s"
            if cursor.execute(sql, (name)) >0:
                result = cursor.fetchone()
                key=(result.get("key"))
                config=(result.get("configuration"))
            else:
                key="no_key"
                config="default"
    finally:
        connection.close()
        return [key,config]