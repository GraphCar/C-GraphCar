#!/home/aluno/anaconda3/bin/python
import mysql.connector
import psutil
from datetime import datetime
import os
import time
import platform

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost', database='GraphCar', user='GraphUser', password='Graph2023')
cursor = con.cursor()

def capturaCPU():

    print("=======================>   CPU   <==========================\n")

    CPU = {
        "tempoUsuario": psutil.cpu_times().user,
        "tempoSistema": psutil.cpu_times().system,
        "tempoOcioso": psutil.cpu_times().idle,
        "frequenciaAtual": psutil.cpu_freq().current,
        "frequenciaMaxima": psutil.cpu_freq().max,
        "core": psutil.cpu_count(logical=False),
        "threds": psutil.cpu_count(logical=True),
        "CPUAtual": psutil.cpu_percent(interval=None),
        "CPUDelay": psutil.cpu_percent(interval=None)
    }
    

    comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    if platform.system() != 'windows':
        dados = (Temperatura, '°C', data_e_hora, 1)
        cursor.execute(comando,dados)
    else:
        dados = (CPU["CPUAtual"], '%', data_e_hora, 1)
        cursor.execute(comando,dados)


    con.commit()

    print("Tempo usuário: " + str(round(CPU["tempoUsuario"]/3600,1)) + "H")
    print("Tempo sistema: " + str(round(CPU["tempoSistema"]/3600,1)) + "H")

    # if CPU["tempoOcioso"] < 70:
    #     print()
    # elif CPU["tempoOcioso"] >= 70 and CPU["tempoOcioso"] < 80:
    #     print()
    # else:
    #     p

    
    # if CPU["frequenciaAtual"]:
    #     print()
    
    # if CPU["frequenciaMaxima"]:
    #     print()
    
    # if CPU["core"]:
    #     print()
    
    # if CPU["threds"]:
    #     print()
    
    # if CPU["CPUAtual"]:
    #     print()
    
    # if CPU["CPUDelay"]:
    #     print()
    
    # if CPU["Temperatura"]:
    #    print()

    print("Tempo ocioso: " + str(round(CPU["tempoOcioso"]/3600,1)) + "H")
    print("Frequência atual: " + str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz")
    print("Frequência máxima: " + str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Núcleos: " + str(CPU["core"]))
    print("Threads: " + str(CPU["threds"]))
    print("Porcentagem da CPU atual: " + str(CPU["CPUAtual"]) + "%")
    print("Delay da CPU: " + str(CPU["CPUDelay"]) + "%")

    if platform.system() != 'windows':
        Temperatura = psutil.sensors_temperatures()['coretemp'][0].current
        print("Temperatura da CPU: " + Temperatura + "°C")

    print("=======================>-----------<=========================\n")

    

while True:
    time.sleep(1)
    os.system('clear')
    capturaCPU()