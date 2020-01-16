"""
Created on Mon Dec  9 13:29:34 2019

@author: antoniojavier.perez
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Markup
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db, User
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from socketFunctions import var_socketio, getCurrentCycle, startCiclosConsole, stopConsole, resetConsole, stop_thread
import forms, json
from time import sleep

app =  Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

n_cycles = 0
current_cycle = 0

funcionesPanel = {
    "start" : startCiclosConsole,
    "stop" : stopConsole,
    "reset" : resetConsole,
}


thread = Thread()
thread_bench = Thread(target = funcionesPanel['reset'])
# thread_bench.daemon = True

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint == 'login':
        return redirect(url_for('main'))

@app.route("/", methods = ['GET', 'POST'])
def main():
    global n_cycles, current_cycle, thread_bench, stop_thread

    panel_form = forms.PanelForms(request.form)
    
    if request.method == 'POST':
        if panel_form.action() == 'start':
            if panel_form.cyclesForm.cycles.validate(request.form):
                n_cycles = panel_form.cyclesForm.cycles.data
                if n_cycles == None:
                        n_cycles = 0
                
                thread_bench = Thread(target = funcionesPanel[panel_form.action()], args = (n_cycles,))

        elif panel_form.action() == 'stop' or panel_form.action() == 'reset':
            stop_thread = True
            # thread_bench.join()
            thread_bench = Thread(target = funcionesPanel[panel_form.action()])
            stop_thread = False      
    
    
    # if not thread_bench.isAlive():
    thread_bench.start()
    success_message = Markup('<h5>Bienvenido ' + session['username'] + '</h5>')
    flash(success_message)
    
    return render_template('bench_control/panel.html', form = panel_form, admin = session['admin'], cycles=n_cycles, current_cycle=current_cycle)

@app.after_request
def after_request(response):
    return response

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

@var_socketio.on('connect')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Server connected')
    
    if not thread.isAlive():
        print("Starting Thread")
        thread = var_socketio.start_background_task(getCurrentCycle)

@var_socketio.on('disconnect')
def test_disconnect():
    print('Server disconnected')

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
    var_socketio.init_app(app, async_mode=None, logger=True, engineio_logger=True)
    var_socketio.run(app, host='0.0.0.0', port=8000)