from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from random import random

thread = Thread()
thread_stop_event = Event()
var_socketio = SocketIO()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random.r()*10, 3)
            print(number)
            var_socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)
    def run(self):
        self.randomNumberGenerator()