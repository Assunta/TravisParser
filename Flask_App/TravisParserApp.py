import random

from flask import Flask, render_template, request, json

from utility import dbUtility

app = Flask(__name__)

@app.route("/home")
def main():
    return render_template('TravisParserHome.html')

@app.route("/results", methods=['POST'])
def results():
    reponame = request.form['reponame']
    return render_template('Builds_results.html', reponame=reponame)

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
    return json.dumps([{
    "Branch": "master",
    "Commit": "fix 92 issue https://github.com/Mashape/unirest-java/issues/92",
    "CommitData": "",
    "Duration": "03:11",
    "FinishDate": "2017-05-29",
    "FinishHour": "06:22:17",
    "Language": "java",
    "NumJobs": 4,
    "PullId": "205",
    "Sha": "4e46ec83085547545e5f575045437ce092156e47",
    "StartDate": "2017-05-29",
    "StartHour": "06:21:27",
    "TitlePull": "fix 92 issue https://github.com/Mashape/unirest-java/issues/92",
    "author": "\u0412\u0430\u0434\u0438\u043c \u0410\u043d\u0434\u0440\u0435\u0435\u0432\u0438\u0447 \u0413\u0430\u0443\u0437\u044f\u043a",
    "buildNumber": "455",
    "commitData": "2017-05-25",
    "commitHour": "06:42:52",
    "commitId": 68694757,
    "description": "Unirest in Java: Simplified, lightweight HTTP client library.",
    "email": "VAGauzyak.SBT@sberbank.ru",
    "idBuild": "455",
    "isPullRequest": True,
    "status": "failed"
},
        {
            "Branch": "master",
            "Commit": "fix 92 issue https://github.com/Mashape/unirest-java/issues/92",
            "CommitData": "",
            "Duration": "03:11",
            "FinishDate": "2017-05-29",
            "FinishHour": "06:22:17",
            "Language": "java",
            "NumJobs": 4,
            "PullId": "205",
            "Sha": "4e46ec83085547545e5f575045437ce092156e47",
            "StartDate": "2017-05-29",
            "StartHour": "06:21:27",
            "TitlePull": "fix 92 issue https://github.com/Mashape/unirest-java/issues/92",
            "author": "\u0412\u0430\u0434\u0438\u043c \u0410\u043d\u0434\u0440\u0435\u0435\u0432\u0438\u0447 \u0413\u0430\u0443\u0437\u044f\u043a",
            "buildNumber": "454",
            "commitData": "2017-05-24",
            "commitHour": "06:42:52",
            "commitId": 68694757,
            "description": "Unirest in Java: Simplified, lightweight HTTP client library.",
            "email": "xxx@sberbank.ru",
            "idBuild": "454",
            "isPullRequest": True,
            "status": "failed"
        }
    ])

@app.route("/getStatStatus", methods=['GET'])
def getStatStatus():
    #TODO calcolare questi valori
    return json.dumps([
        {
            "num": 40,
            "status": "passed"
        },
        {
        "num": 35,
        "status":"failed"
        },
        {
        "num":25,
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