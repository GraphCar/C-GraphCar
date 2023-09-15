import mysql.connector
import psutil
from datetime import datetime
import os
import time
import subprocess
import platform
import requests
import json

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

temporizadorAberturaChamado = 0
alertasEmSequencia = 0
skiparTemporizador = True
alertaTerminal = "Disco se encontra em normalidade."
tempoEmAlerta = 999

chatEscolhido = "https://hooks.slack.com/services/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"


def CapturaDisco():
    
    global temporizadorAberturaChamado
    global skiparTemporizador
    global alertasEmSequencia
    global alertaTerminal
    global tempoEmAlerta

    alertasDisco = {
        "50percent": "🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização.",
        "80percent": "🚨ALERTA🚨 Detectamos que o Disco está com mais de 80% De utilização.",
        "frequente": f" Essa não é a primeira vez que captamos esse dado, já se passaram {tempoEmAlerta} min e até agora não houve melhoras!!"
    }

    lista_discos = psutil.disk_partitions()

    for disco in lista_discos:

        print(f"===========================================>   Disco: {disco.device}  <==============================================\n")

        uso_disco = psutil.disk_usage(disco.device)

        valoresDisco = {
            "TotalDiscoLivre": uso_disco.free,
            "TotalMemoriaDisco": uso_disco.total
        }

        porcentagemUsoDisco = uso_disco.percent

        if platform.system() != 'Windows':
            saida_comando = subprocess.check_output(["df", "--output=pcent", disco.device],text=True)
            saida_comando = saida_comando.split('\n')


            info = saida_comando[1].strip()

            
            porcentagemUsoDisco = int(info.replace('%', ''))


        comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
        dados = (round(valoresDisco["TotalMemoriaDisco"]/1e9,2), 'Gb', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (porcentagemUsoDisco, '%', data_e_hora, 3)
        cursor.execute(comando, dados)

        dados = (round(valoresDisco["TotalDiscoLivre"]/1e9,2), 'Gb', data_e_hora, 3)
        cursor.execute(comando, dados)
        
        con.commit()
    
        print("Total de Memória do Disco: " + str(round(valoresDisco["TotalMemoriaDisco"]/1e9,2)) + " G")
        print("Total de Disco livre: " + str(round(valoresDisco["TotalDiscoLivre"]/1e9,2)) + " G")
        print("Porcentagem de uso do disco: " + str(porcentagemUsoDisco) + " %")

    temporizadorAberturaChamado = temporizadorAberturaChamado+1
    if temporizadorAberturaChamado == 5 or skiparTemporizador:

        if porcentagemUsoDisco > 80:

            alertasEmSequencia = alertasEmSequencia + 1
            
            if alertasEmSequencia >= 2 :
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertasDisco["80percent"] + alertasDisco["frequente"]))
                alertaTerminal = (alertasDisco["80percent"] +"..\n..."+ alertasDisco["frequente"])

            else:
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertasDisco["80percent"]))
                alertaTerminal = (alertasDisco["80percent"])

            print(postMsg.status_code)
            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia*5

        elif porcentagemUsoDisco > 50:
            
            alertasEmSequencia = alertasEmSequencia + 1

            if alertasEmSequencia >= 2 :
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertasDisco["50percent"] + alertasDisco["frequente"]))
                alertaTerminal = (alertasDisco["50percent"] +"...\n..."+ alertasDisco["frequente"])
                
            else:
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertasDisco["50percent"]))
                alertaTerminal = (alertasDisco["50percent"])

            print(postMsg.status_code)
            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia*5

        else:
            skiparTemporizador = True
            alertaTerminal = "Disco se encontra em normalidade."
            alertasEmSequencia = 0

        if temporizadorAberturaChamado == 5:
            temporizadorAberturaChamado = 0

    print("\n" + alertaTerminal + "\n")
    print(">> Temporizador para abertura de chamado caso necessário: ",temporizadorAberturaChamado, " min")
    print("OBS: Alertas no terminal são atualizados somente quando o temporizador reiniciar")

    print("==========================================>-----------------<=============================================\n")


while True:

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    CapturaDisco()
    time.sleep(5)