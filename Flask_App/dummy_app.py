import random

from flask import Flask, render_template, request, json, url_for
from werkzeug.utils import redirect

app = Flask(__name__)

# @app.route("/reponame", methods=['POST'])
# def reponame():
#     reponame = request.form['reponame']
#     return redirect(url_for('results', reponame=reponame), code=200)
#     # return render_template('job_tabs.html', numJobs=numJobs, reponame=reponame)

@app.route("/results", methods=['POST'])
def results():
    reponame = request.form['reponame']
    numJobs = json.dumps(random.randrange(15, 20))
    return render_template('job_tabs.html', numJobs=numJobs, reponame=reponame)

@app.route("/")
def main():
    return render_template('home_dummy.html')




if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)
