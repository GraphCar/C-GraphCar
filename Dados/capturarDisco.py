import mysql.connector
import psutil
from datetime import datetime
import os
import time

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

def CapturaDisco():

    print("==========================>   Disco   <=============================\n")
    
    disk_usage = psutil.disk_usage('C:\\')

    valoresDisco = {
        "TotalDisco" : disk_usage.total,
        "TotalDiscoUsado" : disk_usage.used,
        "TotalDiscoLivre" : disk_usage.free,
        "PercentualDisco" : disk_usage.percent
    }

    #ERROR
    comando = "INSERT INTO Dados (idDados, Utilizacao, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s)"
    # dados = (valoresDisco["TotalDisco"], data_e_hora, 1, 3)
    # cursor.execute(comando, dados)

    # dados = (valoresDisco["TotalDiscoUsado"], data_e_hora, 1, 3)
    # cursor.execute(comando, dados)

    # dados = (valoresDisco["TotalDiscoLivre"], data_e_hora, 1, 3)
    # cursor.execute(comando, dados)
    
    dados = (valoresDisco["PercentualDisco"], data_e_hora, 2, 3)
    #cursor.execute(comando, dados)

    
    con.commit()
    # print(cursor.rowcount, "Dados do Disco inseridos na tabela!")
    
    print("Total de Disco: " + str(round(valoresDisco["TotalDisco"]/1e9,2)) + " GHz")
    print("Total de Disco usado: " + str(round(valoresDisco["TotalDiscoUsado"]/1e9,2)) + " GHz")
    print("Total de Disco livre: " + str(round(valoresDisco["TotalDiscoLivre"]/1e9,2)) + " GHz")
    print("Percentual de Disco: " + str(valoresDisco["PercentualDisco"]) + " %")

    print("=======================>-----------------<==========================\n")

    time.sleep(1)

while True:
    time.sleep(1)
    os.system('cls')
    CapturaDisco()