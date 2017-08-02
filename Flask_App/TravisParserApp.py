from github import Github
from datetime import datetime
from flask import Flask, render_template, request, json, session, url_for
from werkzeug.utils import redirect

from Flask_App.utilityClasses.ErrorStat import ErrorStat
from Flask_App.utilityClasses.Row import Row
from Flask_App.utilityClasses.TestRow import TestRow
from analisys.advancedStats import countStatStatus, countReason, getAuthors, countStatStatusFilter
from analisys.completeParser import completeAnalysis, getBuilds
from utility import dbUtility
from utility.dbUtility import addUser, getUserProjects
from utility.storeObject import store, restore


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


@app.route("/homeUser" , methods=['POST','GET'])
def homeUser():
    if request.method == 'POST':
        #TODO check username e password
        #session
        session['username'] = request.form['username']
        #find project to display
        user = session['username']
        projects = getUserProjects(user)
        print(projects)
        return render_template('homeUser.html', username=session['username'], projects=projects)
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
    reponame = request.form['reponame']
    reponame= reponame.replace("\'", "")
    #TODO cercare il file da caricare
    global builds
    if(INTERNET):
        builds=getBuilds(reponame)
        store(builds, "backupRubyWarbler")
    else:
         builds=restore("backupGradleJFX2")
    return render_template('header.html', reponame=reponame, buildNum=builds.__len__())


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
    print start
    print finish
    print items
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
    #TODO ricalcola i grafici



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


if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True, threaded=True)

