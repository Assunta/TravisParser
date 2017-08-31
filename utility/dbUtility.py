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
def getRubyTools(user):
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubytools` where `configuration`=\"default\" or `configuration`=%s"
            cursor.execute(sql, user)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

#get all the items in table rubytestmessags
def getRubyTestMessages(user):
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubytestmessages` where`configuration`=\"default\" or `configuration`=%s"
            cursor.execute(sql,user)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

#get all the items in table rubyerror
def getRubyErrors(user):
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `rubyerror` where`configuration`=\"default\" or `configuration`=%s"
            cursor.execute(sql, user)
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

def getGradleTaskRules(user):
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `taskgradlerules` where`configuration`=\"default\" or `configuration`=%s"
            cursor.execute(sql,user)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

def getGradleErrorsRules():
    connection= getConnection()
    records= list()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*`FROM `gradleerrors`"
            cursor.execute(sql)
            for r in cursor.fetchall():
                records.append(r)
    finally:
        connection.close()
        return records

def findCategory(user,name):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `goalmaven` WHERE `Goal`LIKE %s AND (`configuration`=\"default\" OR `configuration`=%s)"
            if cursor.execute(sql, (("%"+name+"%"),user)) >0:
                result = cursor.fetchone()
                category=(result.get("Category"))
            else:
                category = "other"
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
                # config=(result.get("configuration"))
            else:
                key="no_key"
                # config="default"
    finally:
        connection.close()
        return [key]

#this method allow to add new user
def addUser(username, key):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`Git_name`,  `key`) VALUES (%s, %s)"
            cursor.execute(sql, (username, key))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()


#this method allows to get all projects linked to one user
def getUserProjects(name):
    connection=getConnection()
    projects=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `user_projects` WHERE `user`= %s"
            if cursor.execute(sql, (name)) >0:
                for r in cursor.fetchall():
                    project=(r.get("project")).encode('ascii','ignore')
                    projects.append(project)
    finally:
        connection.close()
        return projects


#this method allows to get all categories
def getCategories():
    connection=getConnection()
    c=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `category`"
            if cursor.execute(sql) >0:
                for r in cursor.fetchall():
                    category=(r.get("CategoryName")).encode('ascii','ignore')
                    c.append(category.strip())
    finally:
        connection.close()
        return c

#this method allow to add new task gradle rule
def addTaskRule(username, task, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `taskgradlerules` (`regex`,  `category`,`configuration`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (task, category.strip(), username))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#DELETE FROM `travisdb`.`taskgradlerules` WHERE  `ID`=81;
#this method allow to delete a customized task
def deleteTaskRule(username, task, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `taskgradlerules`  WHERE `regex`=%s AND`category`=%s AND`configuration`=%s LIMIT 1"
            cursor.execute(sql, (task, category, username))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#this method allows to get all task customized of user
def getTaskUser(username):
    connection=getConnection()
    c=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `taskgradlerules`  WHERE `configuration`=%s"
            if cursor.execute(sql, username) >0:
                for r in cursor.fetchall():
                    task_name=(r.get("regex"))
                    category_name=(r.get("category"))
                    c.append({'task':task_name, 'category': category_name})
    finally:
        connection.close()
        return c


#this method allow to add new goal maven rule
def addGoalRule(username, goal, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `goalmaven` (`Goal`,  `Category`,`configuration`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (goal, category, username))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()


#this method allow to delete a customized task
def deleteGoalRule(username, goal, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `goalmaven`  WHERE `Goal`=%s AND`Category`=%s AND`configuration`=%s LIMIT 1"
            cursor.execute(sql, (goal, category, username))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#this method allows to get all task customized of user
def getGoalUser(username):
    connection=getConnection()
    c=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `goalmaven`  WHERE `configuration`=%s"
            if cursor.execute(sql, username) >0:
                for r in cursor.fetchall():
                    goal_name=(r.get("Goal"))
                    category_name=(r.get("Category"))
                    c.append({'goal':goal_name, 'category': category_name})
    finally:
        connection.close()
        return c


#this method allow to add new result message ruby
def addResultRubyRule(username, result, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `rubytestmessages` (`regex`,  `category`,`configuration`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (result, category, username))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()


#this method allow to delete a message result customized
def deleteResultRubyRule(username, result, category):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `rubytestmessages`  WHERE `regex`=%s AND`category`=%s AND`configuration`=%s LIMIT 1"
            cursor.execute(sql, (result, category, username))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#this method allows to get all result message customized of user
def getResultRubyUser(username):
    connection=getConnection()
    c=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `rubytestmessages`  WHERE `configuration`=%s"
            if cursor.execute(sql, username) >0:
                for r in cursor.fetchall():
                    goal_name=(r.get("regex"))
                    category_name=(r.get("category"))
                    c.append({'result':goal_name, 'category': category_name})
    finally:
        connection.close()
        return c

# this method allow to add new error message ruby
def addErrorRubyRule(username, result, category):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `rubyerror` (`regex`,  `category`,`configuration`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (result, category, username))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

# this method allow to delete a message error customized
def deleteErrorRubyRule(username, result, category):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `rubyerror`  WHERE `regex`=%s AND`category`=%s AND`configuration`=%s LIMIT 1"
            cursor.execute(sql, (result, category, username))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

# this method allows to get all error messages customized of user
def getErrorRubyUser(username):
    connection = getConnection()
    c = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `rubyerror`  WHERE `configuration`=%s"
            if cursor.execute(sql, username) > 0:
                for r in cursor.fetchall():
                    goal_name = (r.get("regex"))
                    category_name = (r.get("category"))
                    c.append({'regex': goal_name, 'category': category_name})
    finally:
        connection.close()
        return c


#this method allow to add new result message ruby
def addToolRule(username, tool, regex):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `rubytools` (`tool`,  `regex`,`configuration`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (tool, regex, username))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()


#this method allow to delete a customized task
def deleteToolRule(username, tool, regex):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `rubytools`  WHERE `regex`=%s AND`tool`=%s AND`configuration`=%s LIMIT 1"
            cursor.execute(sql, (regex, tool, username))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#this method allows to get all task customized of user
def getToolUser(username):
    connection=getConnection()
    c=[]
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `rubytools`  WHERE `configuration`=%s"
            if cursor.execute(sql, username) >0:
                for r in cursor.fetchall():
                    tool_name=(r.get("tool"))
                    regex=(r.get("regex"))
                    c.append({'tool':tool_name, 'regex': regex})
    finally:
        connection.close()
        return c

#add project to user
def addProjectUser(project, user):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user_projects` (`user`,  `project`) VALUES (%s, %s)"
            cursor.execute(sql, (user, project))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        connection.close()

#this method allow to delete a user's project
def deleteProjectUser(project,username):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `user_projects`  WHERE `user`=%s AND`project`=%s"
            cursor.execute(sql, (username,project))
        connection.commit()
    finally:
        connection.close()

#this method allows to update user's token
def updateToken(username, token):
    connection=getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `users` SET `key`=%s WHERE `Git_name`=%s"
            cursor.execute(sql, (token, username))
        connection.commit()
    finally:
        connection.close()

#this method allows to get user's token
def getToken(username):
    connection=getConnection()
    token="no_key"
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users`  WHERE `Git_name`=%s"
            cursor.execute(sql, (username))
            r=cursor.fetchone()
            token = (r.get("key"))
        connection.commit()
    finally:
        connection.close()
    return token
