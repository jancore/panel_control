from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from random import random
import socket
import fins.udp

thread_stop_event = Event()
var_socketio = SocketIO()

stop_thread = False

class Commands:   
    def __init__(self):         
        self.fins_instance = fins.udp.UDPFinsConnection() 
        self.fins_instance.dest_node_add=212
        self.fins_instance.srce_node_add=79

    def StartCiclosConsole(self, command, n_cycles=0):
        global stop_thread, current_cycle     

        if command == 'start' and (not stop_thread):
            self.fins_instance.fins_socket.close()                       
            self.fins_instance = fins.udp.UDPFinsConnection() 
            self.fins_instance.dest_node_add=212
            self.fins_instance.srce_node_add=79                    
            self.fins_instance.connect('192.168.1.212')                      
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
                    var_socketio.emit('newcycle', {'current_cycle': '{0}'.format(cicle + 1), 'n_cycles': '{0}'.format(n_cycles)})
            except:
                self.StartCiclosConsole('start', n_cycles)

    def StopConsole(self, command, n_cycles):
        global stop_thread

        if command == 'stop':       
            stop_thread = True
            self.fins_instance.fins_socket.close()       
            self.fins_instance = fins.udp.UDPFinsConnection() 
            self.fins_instance.dest_node_add=212
            self.fins_instance.srce_node_add=79    
            self.fins_instance.connect('192.168.1.212')

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
                self.StopConsole('stop', n_cycles)
        
        stop_thread = False

    def ResetConsole(self, command, n_cycles):
        global stop_thread
        
        if command == 'reset': 
            n_cycles = 0       
            stop_thread = True
            self.fins_instance.fins_socket.close() 
            self.fins_instance = fins.udp.UDPFinsConnection() 
            self.fins_instance.dest_node_add=212
            self.fins_instance.srce_node_add=79   
            self.fins_instance.connect('192.168.1.212') 

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
                self.ResetConsole('reset',0)

        stop_thread = False         
