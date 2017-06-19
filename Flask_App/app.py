from flask import Flask, render_template, request, json
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('home.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('sign_up.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    # validate the received values
    if _name:
        return json.dumps({'html': '<span>All fields good !!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ == "__main__":
    #debug=true mi evita di spegnere e riaccendere il server quando faccio modifiche in fase di sviluppo
    #TODO togliero per il rilascio
    app.run(debug=True)
