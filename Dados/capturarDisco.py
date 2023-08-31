#!/home/aluno/anaconda3/bin/python
import mysql.connector
import psutil
from datetime import datetime
import os
import time
import subprocess
import platform

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

def CapturaDisco():

    lista_discos = psutil.disk_partitions()

    for disco in lista_discos:

        print(f"==========================>   Disco: {disco.device}  <=============================\n")

        uso_disco = psutil.disk_usage(disco.device)

        valoresDisco = {
            "TotalDiscoLivre": uso_disco.free,
            "TotalMemoriaDisco": uso_disco.total
        }
        saida_comando = subprocess.check_output(["df", "--output=pcent", disco.device],text=True)
        saida_comando = saida_comando.split('\n')


        info = saida_comando[1].strip()

        
        intPercent = int(info.replace('%', ''))


        comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
        dados = (round(valoresDisco["TotalMemoriaDisco"]/1e9,2), 'Gb', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (intPercent, '%', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (round(valoresDisco["TotalDiscoLivre"]/1e9,2), 'Gb', data_e_hora, 3)
        cursor.execute(comando, dados)
        
        con.commit()
    
        print("Total de Memória do Disco: " + str(round(valoresDisco["TotalMemoriaDisco"]/1e9,2)) + " G")
        print("Total de Disco livre: " + str(round(valoresDisco["TotalDiscoLivre"]/1e9,2)) + " G")
        print("Porcentagem de uso do disco: " + str(intPercent) + " %")

        print("=======================>-----------------<==========================\n")


while True:

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    time.sleep(60)
    CapturaDisco()