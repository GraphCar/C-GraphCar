import mysql.connector
import psutil
from datetime import datetime
import os
import time
import platform
import requests
import json

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost',database='GraphCar',user='GraphUser',password='Graph2023')
cursor = con.cursor()

temporizadorAberturaChamado = 0
alertasEmSequencia = 0
skiparTemporizador = True
tempoEmAlerta = 999 

alertaDisco = {"text": f""" 
🚨ALERTA🚨 Detectamos que o Disco está com mais de 80% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "{tempoEmAlerta}min e até agora não houve melhoras!!
"""} 

chatEscolhido = "https://hooks.slack.com/services/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"

def capturaRam():
    global temporizadorAberturaChamado
    global alertasEmSequencia
    global skiparTemporizador
    global alertaRAM
    global tempoEmAlerta


    print("===========================================>   Memória RAM   <============================================\n")
    
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

    comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados = (round(ValoresRAM["espacoTotalRAM"]/1e9,2), 'Gb', data_e_hora, 2)
    cursor.execute(comando,dados)

    dados = (round(ValoresRAM["porcentagemUsoRAM"]), '%', data_e_hora, 2)
    cursor.execute(comando,dados)
    
    con.commit()

    temporizadorAberturaChamado = temporizadorAberturaChamado+1 
    if temporizadorAberturaChamado == 60 or skiparTemporizador:

        if ValoresRAM["porcentagemUsoRAM"] > 75:

            alertasEmSequencia = alertasEmSequencia + 1
            
            if alertasEmSequencia >= 2 :
                alertaRAM = {"text": f""" 
                🚨ALERTA🚨 Detectamos que a RAM está com mais de 75% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "{tempoEmAlerta}min e até agora não houve melhoras!!
                """} 

                requests.post(chatEscolhido, data=json.dumps(alertaRAM))

                alertaRAM = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"

            else:
                alertaRAM = alertaRAM = {"text": f""" 
                🚨ALERTA🚨 Detectamos que a RAM está com mais de 75% De utilização.
                """} 
                requests.post(chatEscolhido, data=json.dumps(alertaRAM))

                alertaRAM = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 75% De utilização."

            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia

        elif ValoresRAM["porcentagemUsoRAM"] > 50:
            
            alertasEmSequencia = alertasEmSequencia + 1

            if alertasEmSequencia >= 2 :

                alertaRAM = {"text": f""" 
                🚨ALERTA🚨 Detectamos que a RAM está com mais de 50% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "{tempoEmAlerta}min e até agora não houve melhoras!!
                """} 

                requests.post(chatEscolhido, data=json.dumps(alertaRAM))

                alertaRAM = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"
                
            else:
                alertaRAM = {"text": f""" 
                🚨ALERTA🚨 Detectamos que a RAM está com mais de 50% De utilização.
                """} 

                requests.post(chatEscolhido, data=json.dumps(alertaRAM))

                alertaRAM = "🚨ALERTA🚨 Detectamos que o Disco está com mais de 50% De utilização."

            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia

        else:
            skiparTemporizador = True
            alertaRAM = "RAM se encontra em normalidade."
            alertasEmSequencia = 0
            tempoEmAlerta = 0

        if temporizadorAberturaChamado == 60:
            temporizadorAberturaChamado = 0

    print("\n" + alertaRAM + "\n")
    print(">> Temporizador para abertura de chamado caso necessário: (",temporizadorAberturaChamado, "s / 1min)")

    print("""
________________________________________________________________________________________
|OBS: Alertas no terminal e o envio deles para o Slack / Jira serão realizados somente |
|quando o temporizador reiniciar caso tenha sido enviado um alerta anteriormente, porém|
|se for capturado um dado alarmante enquanto a RAM estiver em normalidade, então o...  |
|...temporizador será ignorado.                                                        |
|______________________________________________________________________________________|
    """)

    print("==========================================>-----------------<=============================================\n")


while True:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    capturaRam()
    time.sleep(1)