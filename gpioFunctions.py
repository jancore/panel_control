import time

def ciclo():
    time.sleep(1)
    print("Adelante\n")
    time.sleep(1)
    print("Atras\n")

def startCiclosConsole(n_ciclos = 0):    
    for i in range(n_ciclos):
        ciclo()

def stopConsole(arg = []):
    print("Parado\n")

def resetConsole(arg = []):
    print("Reset\n")