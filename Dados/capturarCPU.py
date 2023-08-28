import mysql.connector
import psutil
from datetime import datetime
import os
import time

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
        "CPUDelay": psutil.cpu_percent(interval=None)
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

    print("=======================>-----------<=========================\n")

    comando = "INSERT INTO Dados (idDados, dado, dateDado, fkMedida, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados =( CPU["tempoUsuario"], data_e_hora, 4, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["tempoSistema"], data_e_hora, 4, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["tempoOcioso"], data_e_hora, 4, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["frequenciaAtual"], data_e_hora, 1, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["frequenciaMaxima"], data_e_hora, 1, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["core"], data_e_hora, 5, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["threds"], data_e_hora, 5, 1)
    cursor.execute(comando, dados)
    
    dados = (CPU["CPUAtual"], data_e_hora, 2, 1)
    cursor.execute(comando, dados)

    dados = (CPU["CPUDelay"], data_e_hora, 2, 1)
    cursor.execute(comando, dados)
    

    con.commit()
    # print(cursor.rowcount, "Dados da CPU inseridos na tabela!")

    

while True:
    time.sleep(1)
    os.system('cls')
    capturaCPU()