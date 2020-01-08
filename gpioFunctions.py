import time

def ciclo():
    time.sleep(1)
    print("Adelante\n")
    time.sleep(1)
    print("Atras\n")

def startCiclosConsole(n_ciclos = 0):
    i = 0  
    for i in range(n_ciclos):
        ciclo()
    return i

def stopConsole(arg = []):
    print("Parado\n")
    return arg

def resetConsole(arg = []):
    print("Reset\n")
    return 0