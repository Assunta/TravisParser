import random

from flask import Flask, render_template, request, json

from Flask_App.utilityClasses.ErrorStat import ErrorStat
from Flask_App.utilityClasses.GoalRow import GoalRow
from Flask_App.utilityClasses.Row import Row
from Flask_App.utilityClasses.TestRow import TestRow
from analisys.advancedStats import countStatStatus, countReason
from analisys.completeParser import completeAnalysis, getBuilds
from utility import dbUtility
from utility.storeObject import store, restore


builds = []
INTERNET=False
app = Flask(__name__)


@app.route("/home")
def main():
    return render_template('TravisParserHome.html')

@app.route("/results", methods=['POST'])
def results():
    reponame = request.form['reponame']
    global builds
    if(INTERNET):
        builds = completeAnalysis(reponame, 0)
        #TODO da testare ancora connessione permettendo
        # builds=getBuilds(reponame)
        store(builds, "backupfatfreecrm")
    else:
         builds=restore("backupspringside")
    return render_template('Builds_results.html', reponame=reponame, buildNum=builds.__len__())

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
        rows.append(Row(b))
    return json.dumps(rows,default=lambda o: o.__dict__)

@app.route("/getBuild/<idBuild>", methods=['GET'])
def getSpecificBuild(idBuild):
    if(INTERNET):
        index=int(builds[0].getBuildID())-int(idBuild)
    else:
        index=int(builds[0]["idBuild"])-int(idBuild)
    return json.dumps(builds[index],default=lambda o: o.__dict__)

@app.route("/getStatStatus", methods=['GET'])
def getStatStatus():
    stats=countStatStatus(builds)
    print(stats)
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
        }
    ])

@app.route("/getStatErrors", methods=['GET'])
def getStatErrors():
    #TODO calcolare questi valori
    result=countReason(builds)
    data=[]
    for key, v in result.iteritems():
        e=ErrorStat(key, v)
        data.append(e)

    return json.dumps(data,default=lambda o: o.__dict__)


@app.route("/mavenLog")
def showMavenLog():
    return render_template('MavenLog.html')

@app.route("/getSnapshot", methods=['GET'])
def getSnapshot():
    builds = restore("backup3")
    logs= builds[1]["Logs"]
    data=logs[0]["snapshotList"]
    return json.dumps(data,default=lambda o: o.__dict__)

@app.route("/getGoalList", methods=['GET'])
def getGoalList():
    builds = restore("backup3")
    logs= builds[1]["Logs"]
    result = []
    i=0
    for s in logs[0]["snapshotList"]:
        data=s["goalList"]
        for goal in data:
            result.append(GoalRow(goal,i))# snapshot[0]["name"]))
        i=i+1
    return json.dumps(result,default=lambda o: o.__dict__)

@app.route("/getTestsList", methods=['GET'])
def getTestsList():
    builds = restore("backup3")
    logs= builds[1]["Logs"]
    result = []
    i=0
    for s in logs[0]["snapshotList"]:
        data=s["test"]
        for test in data:
            result.append(TestRow(test,i))# snapshot[0]["name"]))
        i=i+1
    return json.dumps(result,default=lambda o: o.__dict__)

if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)

