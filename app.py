"""
Created on Mon Dec  9 13:29:34 2019

@author: antoniojavier.perez
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_wtf import CSRFProtect
import forms, json
import gpioFunctions

app =  Flask(__name__)
app.secret_key = 'innovations'
csrf = CSRFProtect(app)

n_cycles = 0
current_cycle = 0

funcionesPanel = {
    "start" : gpioFunctions.startCiclosConsole,
    "stop" : gpioFunctions.stopConsole,
    "reset" : gpioFunctions.resetConsole,
}

@app.before_request
def before_request():
    pass

@app.route("/", methods = ['GET', 'POST'])
def main():
    global n_cycles, current_cycle
    if 'username' not in session:
        return redirect(url_for('login'))
    
    success_message = 'Bienvenido ' + session['username']
    flash(success_message)

    panel_form = forms.PanelForms(request.form)
    
    if request.method == 'POST':
        if panel_form.action() == 'start':
            if panel_form.cyclesForm.cycles.validate(request.form):
                n_cycles = panel_form.cyclesForm.cycles.data
                if n_cycles == None:
                        n_cycles = 0

                funcionesPanel[panel_form.action()](n_cycles)       
                return redirect(url_for('main'))
        else:
            funcionesPanel[panel_form.action()](n_cycles)       
            return redirect(url_for('main'))
    
    return render_template('bench_control/panel.html', form = panel_form, cycles=n_cycles)

@app.after_request
def after_request(response):
    return response

@app.route('/login', methods = ['GET', 'POST'])
def login():    
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        session['username'] = username
        return redirect(url_for('main'))

    return render_template('bench_control/login.html', form = login_form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/ajax-login', methods = ['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    session['username'] = username
    response = { 'status':200, 'username':username, 'id':1}
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug = True, port = 8000)