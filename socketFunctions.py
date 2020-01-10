from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from random import random
import socket

thread_stop_event = Event()
var_socketio = SocketIO()

def startCiclosConsole(n_ciclos = 0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 9999))
    s.listen(1)
    clientsocket, address = s.accept()
    msg =  "{0} Ciclos enviados a {1}".format(n_ciclos, address)
    clientsocket.send(bytes('{0}'.format(n_ciclos), "utf-8"))
    clientsocket.close()
    return msg

def stopConsole(arg = []):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 9999))
    s.listen(1)
    clientsocket, address = s.accept()
    msg =  "Parar a {0}".format(address)
    clientsocket.send(bytes('-1', "utf-8"))
    clientsocket.close()
    return msg, arg

def resetConsole(arg = []):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 9999))
    s.listen(1)
    clientsocket, address = s.accept()
    msg =  "Reiniciar a {0}".format( address)
    clientsocket.send(bytes('0', "utf-8"))
    clientsocket.close()
    return msg, 0
    
def getCurrentCycle():
    while not thread_stop_event.isSet():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5000))
        number = s.recv(1024)
        number = number.decode('utf-8')
        s.close()
        print(number)
        var_socketio.emit('newnumber', {'number': number})
        var_socketio.sleep(1)