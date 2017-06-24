from flask import Flask, render_template, request, json

from parserGeneral import common_parse

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
       return str(common_parse(_name, -1))
    else:
        return "Errore: Inserisci il nome del repository!!!"

if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)
