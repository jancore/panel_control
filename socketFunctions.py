from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from random import random
import socket
import fins.udp

thread_stop_event = Event()
var_socketio = SocketIO()

stop_thread = False

HOST = 'localhost'
PORT_control = 9999
PORT_cycles = 5000

def finsInstance():
    fins_instance = fins.udp.UDPFinsConnection()
    fins_instance.connect('169.254.164.212')
    fins_instance.dest_node_add=212
    fins_instance.srce_node_add=79
    return fins_instance


def startCiclosConsole(n_ciclos = 0):
    global stop_thread
    fins_instance = finsInstance()
    for cicle in range(n_ciclos):
        if stop_thread:
                break
        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
        byte_initial_pose = mem_area[-1:]
        while byte_initial_pose != b'\x02':
            if stop_thread:
                break
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
            byte_initial_pose = mem_area[-1:]

        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x02',1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
        byte_initial_pose = mem_area[-1:]
        while byte_initial_pose != b'\x01':
            if stop_thread:
                break
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
            byte_initial_pose = mem_area[-1:]
        
        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)
    stop_thread = False

def stopConsole(arg = []):
    fins_instance = finsInstance()
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
    byte_initial_pose = mem_area[-1:]
    while byte_initial_pose != b'\x01':
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
        byte_initial_pose = mem_area[-1:]
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)

def resetConsole(arg = []):
    fins_instance = finsInstance()
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
    byte_initial_pose = mem_area[-1:]
    while byte_initial_pose != b'\x01':
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
        byte_initial_pose = mem_area[-1:]
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)

def getCurrentCycle():
    while not thread_stop_event.isSet():
        global current_cycle
        # fins_instance = finsInstance()
        # mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
        # byte_initial_pose = mem_area[-1:]
        # if byte_initial_pose != b'\x01':
        #     current_cycle = current_cycle + 1
        var_socketio.emit('newnumber', {'number': '1'})
        var_socketio.sleep(1)
    pass