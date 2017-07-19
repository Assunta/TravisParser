import random

from flask import Flask, render_template, request, json

from analisys.advancedStats import countStatStatus
from analisys.completeParser import completeAnalysis
from utility import dbUtility



builds = []
app = Flask(__name__)


@app.route("/home")
def main():
    return render_template('TravisParserHome.html')

@app.route("/results", methods=['POST'])
def results():
    reponame = request.form['reponame']
    global builds
    builds = completeAnalysis(reponame)
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
    return json.dumps(builds,default=lambda o: o.__dict__)


@app.route("/getStatStatus", methods=['GET'])
def getStatStatus():
    stats=countStatStatus(builds)
    print(stats)
    # stats=[55.75, 24.15, 30.00 ]
    #TODO calcolare questi valori
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
    return json.dumps([
        { "num": 40, "error": "testing"},
        { "num": 35, "error":"anliysis"},
        { "num":10, "error":"dependencies"},
        {"num": 15, "error": "other"}
    ])


if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)