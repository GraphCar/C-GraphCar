#!/home/aluno/anaconda3/bin/python
import mysql.connector
import psutil
from datetime import datetime
import os
import time
import platform

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

def capturaRam():

    print("=======================>   Memória RAM   <==========================\n")
    
    ValoresRAM = {
        "espacoTotalRAM" : psutil.virtual_memory().total,
        "espacoDisponivelRAM" : psutil.virtual_memory().available,
        "espacoUsadoRAM" : psutil.virtual_memory().used,
        "porcentagemUsoRAM" : psutil.virtual_memory().percent,
        "espacoLivreRAM" : psutil.virtual_memory().free
    }

    print("Espaço total de RAM: " + str(round(ValoresRAM["espacoTotalRAM"]/1e9,2)) + " Gb")
    print("Espaço disponível de RAM: " + str(round(ValoresRAM["espacoDisponivelRAM"]/1e9,2)) + " Gb")
    print("Espaço usado de RAM: " + str(round(ValoresRAM["espacoUsadoRAM"]/1e9,2)) + " Gb")
    print("Porcentagem de uso da RAM: " + str(round(ValoresRAM["porcentagemUsoRAM"])) + " %")
    print("Espaço livre de RAM: " + str(round(ValoresRAM["espacoLivreRAM"]/1e9,2)) + " Gb")

    print("=======================>-----------------<==========================\n")

    comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados = (round(ValoresRAM["espacoTotalRAM"]/1e9,2), 'Gb', data_e_hora, 2)
    cursor.execute(comando,dados)

    dados = (round(ValoresRAM["porcentagemUsoRAM"]), '%', data_e_hora, 2)
    cursor.execute(comando,dados)
    
    con.commit()


while True:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    capturaRam()
    time.sleep(1)