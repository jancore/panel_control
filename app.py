"""
Created on Mon Dec  9 13:29:34 2019

@author: antoniojavier.perez
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, Markup
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db, User
import forms
from socketFunctions import Commands, var_socketio

app =  Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

n_cycles = 0
current_cycle = 0  
commands = Commands()

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint == 'login':
        return redirect(url_for('main'))
    # elif 'username' in session and request.endpoint == 'login':

@app.route("/", methods = ['GET', 'POST'])
def main():
    global n_cycles, current_cycle, stop_thread

    panel_form = forms.PanelForms(request.form)

    success_message = Markup('<h5>Bienvenido ' + session['username'] + '</h5>')
    flash(success_message)

    return render_template('bench_control/panel.html', form = panel_form, admin = session['admin'], cycles=n_cycles, current_cycle=current_cycle)

@app.after_request
def after_request(response):
    return response

@app.route('/command/<c>')
def send_command(c):
    global stop_thread, n_cycles, commands
    aux = request.args.get('n_cycles')
    print(aux)
    if len(aux) == 0:
        aux = 0
    n_cycles = int(aux)
    if(c == 'start'):
        commands.StartCiclosConsole(c, n_cycles)
    if(c == 'stop'):
        stop_thread = True
        commands.StopConsole(c, n_cycles)
        stop_thread = False
    if(c == 'reset'):
        stop_thread = True
        commands.ResetConsole(c, 0)
        stop_thread = False
    
    return ''

@app.route('/login', methods = ['GET', 'POST'])
def login():    
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            session['username'] = username
            session['admin'] = user.admin
            return redirect(url_for('main'))
        else:
            error_message = Markup('<div class="alert alert-danger" role="alert">¡Usuario o contraseña no validos!</div>')
            flash(error_message) 

    return render_template('bench_control/login.html', form = login_form)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User(
            create_form.admin.data,
            create_form.username.data,
            create_form.password.data
        )
        db.session.add(user)
        db.session.commit()

        success_message = Markup('<div class="alert alert-success alert-dismissible fade show" role="alert"> \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"> \
                                        <span aria-hidden="true">&times;</span> \
                                    </button>¡Usuario registrado con exito! \
                                </div>')
        flash(success_message)
        return redirect(url_for('main'))
    
    return render_template('bench_control/create.html', form = create_form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        user = User.query.filter_by(username = 'admin').first()
        if user == None:
            user = User(
                True,
                'admin',
                'Innovations2019'
            )
            db.session.add(user)
            db.session.commit()
    var_socketio.init_app(app, async_mode='threading', logger=True, engineio_logger=True)
    var_socketio.run(app, host='0.0.0.0', port=8000)