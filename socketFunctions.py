from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from random import random
import socket
import fins.udp

thread_stop_event = Event()
var_socketio = SocketIO()

stop_thread = False
HOST = '192.168.1.212'
DEST_NODE = 212
ORIG_NODE = 79

class Commands:   
    def __init__(self):         
        self.fins_instance = fins.udp.UDPFinsConnection() 
        self.fins_instance.dest_node_add=DEST_NODE
        self.fins_instance.srce_node_add=ORIG_NODE

    def StartCiclosConsole(self, n_cycles=0):
        global stop_thread, current_cycle     

        self.fins_instance.fins_socket.close()                       
        self.fins_instance = fins.udp.UDPFinsConnection() 
        self.fins_instance.dest_node_add=DEST_NODE
        self.fins_instance.srce_node_add=ORIG_NODE                    
        self.fins_instance.connect(HOST)                      
        var_socketio.emit('newcycle', {'current_cycle': '{0}'.format(0), 'n_cycles': '{0}'.format(n_cycles)})
        try:
            for cicle in range(n_cycles):
                if stop_thread:
                        self.fins_instance.fins_socket.close()
                        break
                self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
                mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                byte_initial_pose = mem_area[-1:]
                while byte_initial_pose != b'\x02':                
                    if stop_thread:
                        self.fins_instance.fins_socket.close()
                        break
                    mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                    byte_initial_pose = mem_area[-1:]

                self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x02',1)
                mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                byte_initial_pose = mem_area[-1:]
                while byte_initial_pose != b'\x01':
                    if stop_thread:
                        self.fins_instance.fins_socket.close()
                        break
                    mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                    byte_initial_pose = mem_area[-1:]
                    
                self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)
                current_cycle = cicle + 1                
                var_socketio.emit('newcycle', {'current_cycle': '{0}'.format(current_cycle), 'n_cycles': '{0}'.format(n_cycles)})
        except:
            self.StartCiclosConsole(n_cycles)

    def StopConsole(self, n_cycles):
        global stop_thread

        stop_thread = True
        self.fins_instance.fins_socket.close()       
        self.fins_instance = fins.udp.UDPFinsConnection() 
        self.fins_instance.dest_node_add=DEST_NODE
        self.fins_instance.srce_node_add=ORIG_NODE    
        self.fins_instance.connect(HOST)

        try:
            self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
            mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
            byte_initial_pose = mem_area[-1:]
            while byte_initial_pose != b'\x01':    
                mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                byte_initial_pose = mem_area[-1:]
            self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)
            self.fins_instance.fins_socket.close()
        except:
            self.StopConsole(n_cycles)
        
        stop_thread = False

    def ResetConsole(self, n_cycles):
        global stop_thread
        
        n_cycles = 0       
        stop_thread = True
        self.fins_instance.fins_socket.close() 
        self.fins_instance = fins.udp.UDPFinsConnection() 
        self.fins_instance.dest_node_add=DEST_NODE
        self.fins_instance.srce_node_add=ORIG_NODE   
        self.fins_instance.connect(HOST) 

        try:
            self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x01',1)
            mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
            byte_initial_pose = mem_area[-1:]
            while byte_initial_pose != b'\x01':
                mem_area = self.fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x00\x00')
                byte_initial_pose = mem_area[-1:]
            self.fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00',b'\x00\x00',1)
            var_socketio.emit('newcycle', {'current_cycle': '{0}'.format(0), 'n_cycles': '{0}'.format(n_cycles)})
            self.fins_instance.fins_socket.close()
        except:
            self.ResetConsole(0)

        stop_thread = False         
