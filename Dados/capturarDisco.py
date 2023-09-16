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
alertaDisco = "Disco se encontra em normalidade."
tempoEmAlerta = 0

chatEscolhido = "https://hooks.slack.com/services/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"


def CapturaDisco():
    
    global temporizadorAberturaChamado
    global skiparTemporizador
    global alertasEmSequencia
    global alertaDisco
    global tempoEmAlerta

    lista_discos = psutil.disk_partitions()

    for disco in lista_discos:

        print(f"===========================================>   Disco: {disco.device}  <==============================================\n")

        uso_disco = psutil.disk_usage(disco.device)

        valoresDisco = {
            "TotalDiscoLivre": uso_disco.free,
            "TotalMemoriaDisco": uso_disco.total
        }

        porcentagemUsoDisco = uso_disco.percent+20

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

        if porcentagemUsoDisco > 75:
            alertasEmSequencia = alertasEmSequencia + 1
            
            if alertasEmSequencia >= 2 :

                alertaDisco = {"text": f"""
                🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram {tempoEmAlerta}min e até agora não houve melhoras!!
                """}

                requests.post(chatEscolhido, data=json.dumps(alertaDisco))
                
                alertaDisco = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dele, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"

            else:
                alertaDisco = {"text": f"""
                🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização.
                """}

                requests.post(chatEscolhido, data=json.dumps(alertaDisco))

                alertaDisco = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização."
            

            
            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = tempoEmAlerta + 5

        elif porcentagemUsoDisco > 50:
            
            alertasEmSequencia = alertasEmSequencia + 1

            if alertasEmSequencia >= 2 :
                alertaDisco = {"text": f"""
                🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram {tempoEmAlerta}min e até agora não houve melhoras!!
                """}

                requests.post(chatEscolhido, data=json.dumps(alertaDisco))
                
                alertaDisco = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dele, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"
                
            else:
                alertaDisco = {"text": f"""
                🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização.
                """}

                requests.post(chatEscolhido, data=json.dumps(alertaDisco))

                alertaDisco = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização."

            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = tempoEmAlerta + 5

        else:
            skiparTemporizador = True
            alertaDisco = "Disco se encontra em normalidade."
            alertasEmSequencia = 0
            tempoEmAlerta = 0

        if temporizadorAberturaChamado == 5:
            temporizadorAberturaChamado = 0

    print("\n" + alertaDisco + "\n")
    print(">> Temporizador para abertura de chamado caso necessário: (",temporizadorAberturaChamado, "min / 5 min)")
    print("""
________________________________________________________________________________________
|OBS: Alertas no terminal e o envio deles para o Slack / Jira serão realizados somente |
|quando o temporizador reiniciar caso tenha sido enviado um alerta anteriormente, porém|
|se for capturado um dado alarmante enquanto o Disco estiver em normalidade, então o...|
|...temporizador será ignorado.                                                        |
|______________________________________________________________________________________|
    """)

    print("==========================================>-----------------<=============================================\n")

while True:

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    CapturaDisco()
    time.sleep(60)