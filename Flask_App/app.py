from flask import Flask, render_template, request, json
from domain.Build import Build
from domain.GradleLog import GradleLog

from parserGeneral import common_parse
from parserGradle import gradle_parser

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('sign_up.html')


@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    # validate the received values
    if _name:
        f=open("jfxtras-labs-245-48664144.txt", 'r')
        gradleLog = gradle_parser(f, GradleLog(_name))
        return common_parse(_name, -1).toJSON()+" "+ gradleLog.toJSON()
       #return json.dumps([(common_parse(_name, -1)).__dict__])
    else:
        return "Errore: Inserisci il nome del repository!!!"

if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)
