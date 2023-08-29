#!/home/aluno/anaconda3/bin/python

import mysql.connector
import psutil
from datetime import datetime
import os
import time
import subprocess

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
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
        "CPUDelay": psutil.cpu_percent(interval=None),
        "Temperatura": psutil.sensors_temperatures()['coretemp'][0].current,
    }

    
    
    print("Tempo usuário: " + str(round(CPU["tempoUsuario"]/3600,1)) + "H")
    print("Tempo sistema: " + str(round(CPU["tempoSistema"]/3600,1)) + "H")
    print("Tempo ocioso: " + str(round(CPU["tempoOcioso"]/3600,1)) + "H")
    print("Frequência atual: " + str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz")
    print("Frequência máxima: " + str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Núcleos: " + str(CPU["core"]))
    print("Threads: " + str(CPU["threds"]))
    print("Porcentagem da CPU atual: " + str(CPU["CPUAtual"]) + "%")
    print("Delay da CPU: " + str(CPU["CPUDelay"]) + "%")
    print("Temperatura da CPU: " + str(CPU["Temperatura"]) + "°C")

    print("=======================>-----------<=========================\n")

    # comando = "INSERT INTO Dados (idDados, temperatura, utilizacao, dateDado) VALUES (NULL, %s, %s, %s)"
    # dados =( CPU["Temperatura"] ,CPU["CPUAtual"],data_e_hora,4, 1)
    # cursor.execute(comando, dados)

    comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados = (CPU["Temperatura"], '°C', data_e_hora, 1)
    cursor.execute(comando,dados)

    dados = (CPU["CPUAtual"], '%', data_e_hora, 1)
    cursor.execute(comando,dados)


    con.commit()
    # print(cursor.rowcount, "Dados da CPU inseridos na tabela!")

    

while True:
    time.sleep(1)
    os.system('cls')
    capturaCPU()