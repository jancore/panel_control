"""
Created on Mon Dec  9 13:29:34 2019

@author: antoniojavier.perez
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Markup
from flask_wtf import CSRFProtect
from flask_socketio import emit, SocketIO
from flask_restful import Resource, Api
from asyncThreads import var_socketio, RandomThread
from config import DevelopmentConfig
from models import db, User
import forms, json
import gpioFunctions

app =  Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
api = Api(app)

n_cycles = 0
current_cycle = 0

class CurrentCycles(Resource):
    def get(self):
        return {'cycle': current_cycle}

    def put(self):
        current_cycle = request.form['data']
        return {'cycle': current_cycle}

api.add_resource(CurrentCycles, '/<string>')

funcionesPanel = {
    "start" : gpioFunctions.startCiclosConsole,
    "stop" : gpioFunctions.stopConsole,
    "reset" : gpioFunctions.resetConsole,
}

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint == 'login':
        return redirect(url_for('main'))

@app.route("/", methods = ['GET', 'POST'])
def main():
    global n_cycles, current_cycle

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
    
    success_message = Markup('<h5>Bienvenido ' + session['username'] + '</h5>')
    flash(success_message)
    
    return render_template('bench_control/panel.html', form = panel_form, admin = session['admin'], cycles=n_cycles, current_cycle=current_cycle)

@var_socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')
    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@var_socketio.on('my_event', namespace='/test')
def test_message(message):                        # test_message() is the event callback function.
    emit('my response', {'data': 'got it!'})      # Trigger a new event called "my response"


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

if __name__ == "__main__":
    csrf.init_app(app)
    #var_socketio.init_app(app)
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

    app.run(port = 8000)