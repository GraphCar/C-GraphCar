import mysql.connector
import psutil
from datetime import datetime
import os
import time
import subprocess

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

def CapturaDisco():

    lista_discos = psutil.disk_partitions()

    for disco in lista_discos:

        print(f"==========================>   Disco: {disco.device}  <=============================\n")

        valoresDisco = {
            
        }
        uso_disco = subprocess.check_output(["df", "-h", disco.device],text=True)
        uso_disco = uso_disco.split('/n')
        infos = uso_disco[1]
        infos = infos.split('')
        intPercent = int(infos[9].replace('%', ''))
        percentual += intPercent/lista_discos


        comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
        dados = (round(valoresDisco["TotalMemoriaDisco"]/1e9,2), 'GHz', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (round(valoresDisco["PorcentagemUsoDisco"]), '%', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (round(valoresDisco["TotalDiscoLivre"]/1e9,2), 'GHz', data_e_hora, 3)
        cursor.execute(comando, dados)
        
        con.commit()
    
        print("Total de Memória do Disco: " + str(round(valoresDisco["TotalMemoriaDisco"]/1e9,2)) + " GHz")
        print("Total de Disco livre: " + str(round(valoresDisco["TotalDiscoLivre"]/1e9,2)) + " GHz")
        print("Porcentagem de uso do disco: " + str(valoresDisco["PorcentagemUsoDisco"]) + " %")

        print("=======================>-----------------<==========================\n")

        time.sleep(1)

while True:
    time.sleep(1)
    os.system('cls')
    CapturaDisco()