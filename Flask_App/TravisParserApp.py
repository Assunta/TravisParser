from github import Github
from datetime import datetime
from flask import Flask, render_template, request, json, session, url_for

from apscheduler.schedulers.background import BackgroundScheduler
from Flask_App.utilityClasses.ErrorStat import ErrorStat
from Flask_App.utilityClasses.Row import Row
from Flask_App.utilityClasses.TestRow import TestRow
from analisys.advancedStats import countStatStatus, countReason, getAuthors, countStatStatusFilter, countReasonFilter
from analisys.completeParser import completeAnalysis, getBuilds
from utility import dbUtility
from utility.dbUtility import addUser, getUserProjects, getCategories, addTaskRule, deleteTaskRule, getTaskUser, \
    getGoalUser, addGoalRule, deleteGoalRule, getResultRubyUser, deleteResultRubyRule, addResultRubyRule, getToolUser, \
    addToolRule, deleteToolRule, addProjectUser
from utility.storeObject import store, restore


# scheduler = BackgroundScheduler()
builds = []
INTERNET=False
app = Flask(__name__)
app.secret_key = 'lodmdmncdvnjnjksdcnkwcw'      #session work only with secret key


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
            print(projects)
            return render_template('homeUser.html', username=session['username'], projects=projects)
        except Exception, e:
            print e
            return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
    else:
        if 'username' in session:
            user = session['username']
            projects = getUserProjects(user)
            print(projects)
            return render_template('homeUser.html', username=session['username'], projects=projects)
        else:
            return render_template('TravisParserHome.html')

@app.route('/logout', methods=['GET'])
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route("/signUp", methods=['POST'])
def signUp():
    username = request.form['username']
    password= request.form['password']
    token= request.form['gitkey']
    print username
    print password
    g = Github(username, password, 'https://api.github.com')
    try:
        print g.get_user(login=username)
        # gToken = Github(token)
        # print gToken.get_user(login=token)
        #TODO check correct token
        try:
            addUser(username, token)
        except Exception ,e:
            print e
            return json.dumps({'error': "Duplicate username "+username+"<BR>this user is still registered"}), 400
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception, e:
        print e
        return json.dumps({'error': "Username or password are not correct, please retry"}), 400


@app.route("/results", methods=['POST'])
def results():
    #TODO scegliere il file giusto
    reponame = request.form['reponame']
    reponame= reponame.replace("\'", "")
    print reponame
    global builds
    builds=restore("backupGradleJFX2")
    return render_template('header.html', reponame=reponame, buildNum=builds.__len__())

@app.route("/results/<reponame>", methods=['GET'])
def resultsReponame(reponame):
    global builds
    filename=session['username'].encode('ascii','ignore')+"_"+reponame;
    builds=restore(filename)
    return render_template('header.html', reponame=reponame, buildNum=builds.__len__())

@app.route("/newAnalysis", methods=['POST'])
def newAnalysis():
    reponame = request.form['reponame']
    reponame= reponame.replace("\'", "")
    try:
        global builds
        builds=getBuilds(reponame)
        fileName=session['username'].encode('ascii','ignore')+"_"+reponame.replace("/","_")
        store(builds, fileName)
        addProjectUser(reponame,session['username'])
        return render_template('header.html', reponame=reponame, buildNum=builds.__len__())
    except Exception,e:
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/validateKey", methods=['POST'])
def validateKey():
    userName = request.form['userName']
    result=dbUtility.findUser(userName)
    print result[0]
    if(result[0] is "no_key"):
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route("/getBuild", methods=['GET'])
def getBuild():
    rows=[]
    for b in builds:
        rows.append(Row(b, INTERNET))
    return json.dumps(rows,default=lambda o: o.__dict__)

@app.route("/getBuild/<idBuild>", methods=['GET'])
def getSpecificBuild(idBuild):
    if(INTERNET):
        index=int(builds[0].getBuildID())-int(idBuild)
    else:
        index=int(builds[0]["idBuild"])-int(idBuild)
    return json.dumps(builds[index],default=lambda o: o.__dict__)

@app.route("/queryStats", methods=['POST'])
def queryStats():
    #TODO terminare e vedere perche' i grafici non si aggiustano
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
        print e
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
    print start
    print finish
    print items
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
        print e.message
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}

@app.route("/getAllAuthors", methods=['GET'])
def getAllAuthors():
    result=getAuthors(builds)
    return json.dumps(result,default=lambda o: o.__dict__)

@app.route("/getMinData", methods=['GET'])
def getMinData():
    if(INTERNET):
        #TODO check format of data
        date=builds[-1].setStart()
    else:
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
    except Exception:
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
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getTask", methods=['GET'])
def getTask():
    username=session['username']
    try:
        result=getTaskUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}


@app.route("/addGoal", methods=['POST'])
def addGoal():
    task = request.form['goal']
    category = request.form['category']
    username=session['username']
    try:
        addGoalRule(username,task,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception:
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
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getGoal", methods=['GET'])
def getGoal():
    username=session['username']
    try:
        result=getGoalUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}



@app.route("/addResultRuby", methods=['POST'])
def addResultRuby():
    result = request.form['result']
    category = request.form['category']
    username=session['username']
    try:
        addResultRubyRule(username,result,category)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception:
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
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getResultRuby", methods=['GET'])
def getResultRuby():
    username=session['username']
    try:
        result=getResultRubyUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}


@app.route("/addToolRuby", methods=['POST'])
def addToolRuby():
    tool = request.form['tool']
    regex = request.form['regex']
    username=session['username']
    try:
        addToolRule(username,tool,regex)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except Exception:
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
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

@app.route("/getToolRuby", methods=['GET'])
def getToolRuby():
    username=session['username']
    try:
        result=getToolUser(username)
        print result
        return json.dumps(result, default=lambda o: o.__dict__)
    except Exception,e:
        print e
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
#
# def myfunc():
#     scheduler.print_jobs()


if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    #il job parte due volte perche' siamo in debug
    # scheduler.add_job(myfunc, 'interval', seconds=10,  id='job_prova')
    # scheduler.start()
    app.run(debug=True, threaded=True)

