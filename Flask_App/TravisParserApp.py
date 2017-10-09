import os
from datetime import datetime

from flask import Flask, render_template, request, json, session
from github import Github
from travispy import TravisPy

from Flask_App.utilityClasses.AppConfiguration import getLogger, configureScheduler, getLoggerScheduler
from Flask_App.utilityClasses.ErrorStat import ErrorStat
from Flask_App.utilityClasses.Row import Row
from Flask_App.utilityClasses.TestRow import TestRow
from Flask_App.utilityClasses.storeObject import store, restore
from analisys.advancedStats import countStatStatus, countReason, getAuthors, countStatStatusFilter, countReasonFilter
from analisys.completeParser import getBuilds, getRefreshBuilds
from utility import dbUtility
from utility.dbUtility import addUser, getUserProjects, getCategories, addTaskRule, deleteTaskRule, getTaskUser, \
    getGoalUser, addGoalRule, deleteGoalRule, getResultRubyUser, deleteResultRubyRule, addResultRubyRule, getToolUser, \
    addToolRule, deleteToolRule, addProjectUser, addErrorRubyRule, deleteErrorRubyRule, getErrorRubyUser, updateToken, \
    deleteProjectUser

#set logger
log= getLogger()

#set job scheduler
scheduler=configureScheduler()
builds = []
app = Flask(__name__)
app.secret_key = 'lodmdmncdvnjnjksdcnkwcw'      #session work only with secret key

#set logger for APSCHEDULER
logAps=getLoggerScheduler()


@app.route("/home",  methods=['POST', 'GET'])
def main():
    return render_template('TravisParserHome.html')

@app.route("/registration")
def registration():
    return render_template('registration.html')

@app.route("/settings")
def settings():
    c=getCategories()
    return render_template('customization.html', categories=json.dumps(c))

@app.route("/editProfile")
def editProfile():
    user=session['username']
    token = dbUtility.findUser(user)
    projects = getUserProjects(user)
    return render_template('editProfile.html', projects=json.dumps(projects), token=token)


@app.route("/changeToken/<token>", methods=['GET'])
def changeToken(token):
    user=session['username']
    try:
        updateToken(user,token)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        log.info("Successfully update github's token for user %s ",user)
    except Exception, e:
        log.error("Error during update github's token for user %s : %s",user, e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteProjects", methods=['POST'])
def deleteProjects():
    user=session['username']
    try:
        #TODO lo dovresti fare transazionale!
        project=request.form['project']
        filename=session['username'].encode('ascii', 'ignore') + "_" + project.replace("/", "_")+".json"
        os.remove(filename)
        deleteProjectUser(project, user)
        #check if there is an associate job running
        jobNameToCheck=session['username']+"_"+project
        if(scheduler.get_job(jobNameToCheck) is not None):
            scheduler.remove_job(jobNameToCheck)
        log.info("Successfully deleted projects for user %s ", user)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        log.error("Error during delete projects for user %s : %s",user, e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/homeUser" , methods=['POST','GET'])
def homeUser():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        try:
            g = Github(username, password, 'https://api.github.com')
            print g.get_user(login=username)
            #session
            session['username'] = request.form['username']
            #find project to display
            user = session['username']
            projects = getUserProjects(user)
            log.debug("Show home for %s", username)
            return render_template('homeUser.html', username=session['username'], projects=projects)
        except Exception, e:
            log.error("Error show home for %s : %s", username, e.message)
            return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
    else:
        if 'username' in session:
            user = session['username']
            projects = getUserProjects(user)
            return render_template('homeUser.html', username=session['username'], projects=projects)
        else:
            log.warning("Try to acces without login; Redirect to login page")
            return render_template('TravisParserHome.html')

@app.route('/logout', methods=['GET'])
def logout():
    # remove the username from the session if it is there
    log.debug("Logout %s", session['username'])
    session.pop('username', None)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route("/signUp", methods=['POST'])
def signUp():
    username = request.form['username']
    password= request.form['password']
    token= request.form['gitkey']
    g = Github(username, password, 'https://api.github.com')
    try:
        #check if userame and password are correct
        print g.get_user(login=username)
    except Exception, e:
        log.error("Username and password not correct %s", e.message)
        return json.dumps({'error': "Username or password are not correct, please retry"}), 400
        # gToken = Github(token)
        # print gToken.get_user(login=token)
    try:
        # TODO da testare!
        t = TravisPy.github_auth(str(token))
        #da inserire un eventuale controllo sul token che appartiene effettivamente a quell'utente e non a qualcun altro
        print(t.user())
    except Exception ,e:
        log.error("Failed to create new user: token is incorrect %s %s", token, e.message)
        return json.dumps({'error': "Your token is not correct! "}), 400
    try:
        addUser(username, token)
    except Exception ,e:
        log.error("Failed to create new user: %s",e.message)
        return json.dumps({'error': "Duplicate username "+username+"<BR>this user is still registered"}), 400
    log.info("New user correct created %s", username)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



@app.route("/results", methods=['POST'])
def results():
    reponame = request.form['reponame']
    reponame= reponame.replace("\'", "")
    session['reponame'] = reponame
    global builds
    fileName = session['username'].encode('ascii', 'ignore') + "_" + reponame.replace("/", "_")
    builds=restore(fileName)
    return render_template('header.html', reponame=reponame, buildNum=builds.__len__())

@app.route("/results/<reponame>", methods=['GET'])
def resultsReponame(reponame):
    global builds
    filename=session['username'].encode('ascii','ignore')+"_"+reponame;
    builds=restore(filename)
    return render_template('header.html', reponame=session['reponame'], buildNum=builds.__len__())

@app.route("/newAnalysis", methods=['POST'])
def newAnalysis():
    reponame = request.form['reponame']
    reponame= reponame.replace("\'", "")
    try:
        global builds
        session['reponame'] = reponame.replace("_","/")
        builds=getBuilds(session['username'],reponame)
        fileName=session['username'].encode('ascii','ignore')+"_"+reponame.replace("/","_")
        store(builds, fileName)
        addProjectUser(reponame,session['username'])
        builds=restore(fileName)
        log.info("New analysis performed for project %s", reponame)
        return render_template('header.html', reponame=session['reponame'], buildNum=builds.__len__())
    except Exception,e:
        log.error("Error during new analysis for project: %s: %s", reponame, e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

#this method allow to restart the analysis
@app.route("/force", methods=['GET'])
def force():
    reponame = session['reponame']
    try:
        global builds
        builds=getBuilds(session['username'],reponame)
        fileName=session['username'].encode('ascii','ignore')+"_"+reponame.replace("/","_")
        store(builds, fileName)
        builds=restore(fileName)
        log.info("repeated analysis for project %s", reponame)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error during repeating the analysis for project %s: %s", reponame, e.message)
        if (str(e.message).find("403")>0):
            return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}



# @app.route("/validateKey", methods=['POST'])
# def validateKey():
#     userName = request.form['userName']
#     result=dbUtility.findUser(userName)
#     print result[0]
#     if(result[0] is "no_key"):
#         return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
#     else:
#         return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route("/getBuild", methods=['GET'])
def getBuild():
    rows=[]
    for b in builds:
        rows.append(Row(b))
    return json.dumps(rows,default=lambda o: o.__dict__)

@app.route("/getBuild/<idBuild>", methods=['GET'])
def getSpecificBuild(idBuild):
    # if(INTERNET):
    #     index=int(builds[0].getBuildID())-int(idBuild)
    # else:
    i=int(builds[0]["idBuild"])
    index=0;
    while(builds[index]["idBuild"]!=idBuild):
        i=i-1
        index=index+1
    # index=int(builds[0]["idBuild"])-int(idBuild)
    return json.dumps(builds[index],default=lambda o: o.__dict__)

@app.route("/queryStats", methods=['POST'])
def queryStats():
    start = request.form['StartDate']
    finish= request.form['FinishDate']
    items= request.form['Authors']
    try:
        stats=countStatStatusFilter(builds,  datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(finish, '%Y-%m-%d'), items)
        return json.dumps([
            {
                "num": stats[0],
                "status": "passed"
            },
            {
                "num": stats[1],
                "status": "failed"
            },
            {
                "num": stats[2],
                "status": "errored"
            },
            {
                "num": stats[3],
                "status": "canceled"
            }
        ])
    except Exception, e:
        log.error("exception during calculating status statistics: %s", e.message)
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}




@app.route("/getStatStatus", methods=['GET'])
def getStatStatus():
    stats=countStatStatus(builds)
    return json.dumps([
        {
            "num": stats[0],
            "status": "passed"
        },
        {
            "num": stats[1],
            "status":"failed"
        },
        {
            "num":stats[2],
            "status":"errored"
        },
        {
            "num": stats[3],
            "status": "canceled"
        }
    ])

@app.route("/getStatErrors", methods=['GET'])
def getStatErrors():
    result=countReason(builds)
    data=[]
    for key, v in result.iteritems():
        e=ErrorStat(key, v)
        data.append(e)

    return json.dumps(data,default=lambda o: o.__dict__)

@app.route("/queryStatErrors", methods=['POST'])
def queryStatErrors():
    start = request.form['StartDate']
    finish = request.form['FinishDate']
    items = request.form['Authors']
    try:
        result=countReasonFilter(builds,  datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(finish, '%Y-%m-%d'), items)
        data=[]
        for key, v in result.iteritems():
            e=ErrorStat(key, v)
            data.append(e)
        if data.__len__()> 0:
            return json.dumps(data,default=lambda o: o.__dict__)
        else:
            return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("exception during calculating type of error statistics: %s", e.message)
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}

@app.route("/getAllAuthors", methods=['GET'])
def getAllAuthors():
    result=getAuthors(builds)
    return json.dumps(result,default=lambda o: o.__dict__)

@app.route("/getMinData", methods=['GET'])
def getMinData():
    # if(INTERNET):
    #     date=builds[-1].setStart()
    # else:
    date=builds[-1]["StartDate"]
    #dateObject= datetime.strptime(date, '%Y-%m-%d')
    return json.dumps(date,default=lambda o: o.__dict__)



@app.route("/getTestsList", methods=['GET'])
def getTestsList():
    builds = restore("backup3")
    logs= builds[2]["Logs"]
    result = []
    i=0
    for s in logs[0]["snapshotList"]:
        data=s["test"]
        for test in data:
            result.append(TestRow(test,i))# snapshot[0]["name"]))
        i=i+1
    return json.dumps(result,default=lambda o: o.__dict__)

@app.route("/getInfoLog/<idLog>", methods=['GET'])
def getInfoLog(idLog):
    builds = restore("backup3")
    logs = builds[0]["Logs"]
    return json.dumps(logs[0], default=lambda o: o.__dict__)


#function to customization:
@app.route("/addTask", methods=['POST'])
def addTask():
    task = request.form['task']
    category = request.form['category']
    username=session['username']
    try:
        addTaskRule(username,task,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        log.error("Error adding customized Task Gradle Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteTask", methods=['POST'])
def deleteTask():
    task = request.form['task']
    category = request.form['category']
    username=session['username']
    try:
        deleteTaskRule(username,task,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error deleting customized Task Gradle Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getTask", methods=['GET'])
def getTask():
    username=session['username']
    try:
        result=getTaskUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        log.error("Error during get Task Gradle Rules %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}


@app.route("/addGoal", methods=['POST'])
def addGoal():
    task = request.form['goal']
    category = request.form['category']
    username=session['username']
    try:
        addGoalRule(username,task,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error adding customized Goal Maven Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteGoal", methods=['POST'])
def deleteGoal():
    goal = request.form['goal']
    category = request.form['category']
    username=session['username']
    try:
        deleteGoalRule(username,goal,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error deleting customized Goal Maven Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getGoal", methods=['GET'])
def getGoal():
    username=session['username']
    try:
        result=getGoalUser(username)
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        log.error("Error get customized Goal Maven Rules %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}



@app.route("/addResultRuby", methods=['POST'])
def addResultRuby():
    result = request.form['result']
    category = request.form['category']
    username=session['username']
    try:
        addResultRubyRule(username,result,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        log.error("Error adding customized Result Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteResultRuby", methods=['POST'])
def deleteResultRuby():
    result = request.form['result']
    category = request.form['category']
    username=session['username']
    try:
        deleteResultRubyRule(username,result,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error deleting customized Result Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getResultRuby", methods=['GET'])
def getResultRuby():
    username=session['username']
    try:
        result=getResultRubyUser(username)
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        log.error("Error get customized Result Ruby Rules %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/addErrorRuby", methods=['POST'])
def addErrorRuby():
    result = request.form['regex']
    category = request.form['category']
    username=session['username']
    try:
        addErrorRubyRule(username,result,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error adding customized Error Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteErrorRuby", methods=['POST'])
def deleteErrorRuby():
    result = request.form['regex']
    category = request.form['category']
    username=session['username']
    try:
        deleteErrorRubyRule(username,result,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error deleting customized Error Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getErrorRuby", methods=['GET'])
def getErrorRuby():
    username=session['username']
    try:
        result=getErrorRubyUser(username)
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        log.error("Error get customized Error Ruby Rules %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}


@app.route("/addToolRuby", methods=['POST'])
def addToolRuby():
    tool = request.form['tool']
    regex = request.form['regex']
    username=session['username']
    try:
        addToolRule(username,tool,regex)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error adding customized Tool Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/deleteToolRuby", methods=['POST'])
def deleteToolRuby():
    tool = request.form['tool']
    regex = request.form['regex']
    username=session['username']
    try:
        deleteToolRule(username,tool,regex)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        log.error("Error deleting customized Tool Ruby Rule %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getToolRuby", methods=['GET'])
def getToolRuby():
    username=session['username']
    try:
        result=getToolUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        log.error("Error get customized Tool Ruby Rules %s", e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getOption", methods=['GET'])
def getOption():
    job=scheduler.get_job(session['username']+"_"+session['reponame'])
    if (job == None):
        ret= False
    else:
        ret=True
    return json.dumps([
        {
            "name":session['reponame'],
            "numBuilds": builds.__len__(),
            "backgroundProcess": ret
        }
    ])



@app.route("/addBackgroundProcess", methods=['GET'])
def addBackgroundProcess():
    try:
        username=session['username']
        reponame=session['reponame']
        fileName = session['username'].encode('ascii', 'ignore') + "_" + session['reponame']
        scheduler.add_job('utilityClasses.Job:addBackgroundFunction', 'interval', hours=24,args=(username,reponame),  id=fileName )
        log.info("Add background process for project %s and username %s", session['reponame'], session['username'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        # log.error("Error adding background process for project %s and username %s: %s",reponame, username, e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/removeBackgroundProcess", methods=['GET'])
def removeBackgroundProcess():
    try:
        scheduler.remove_job(session['username']+"_"+session['reponame'])
        log.info("Deleted background process for project %s and username %s", session['reponame'], session['username'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        # log.error("Error deleting background process for project %s and username %s: %s", session['reponame'], session['username'], e.message)
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
#
@app.route("/refresh", methods=['GET'])
def refresh():
    global builds
    try:
        fileName = session['username'].encode('ascii', 'ignore') + "_" + session['reponame'].replace("/", "_")
        result=getRefreshBuilds(session["username"],session['reponame'], builds)
        #remove duplicate if present
        all=result
        if result.__len__()==0:
            return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}
        index=result[-1].getBuildID()
        for item in builds:
            if int(item["idBuild"])<int(index):
                result.append(item)
        store(all, fileName)
        builds = restore(fileName)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception,e:
        #TODO da testare bene perche' non si e' capito qual e' la condizione esatta per farlo verificare
        log.error("Error during refresh %s: %s", fileName, e.message)
        if(str(e.message).find("403")>0):
            return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
        elif (str(e.message).find("Max retries exceeded")>0):
            return json.dumps({'success': False}), 402, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    scheduler.start()
    app.run(debug=True, threaded=True)

