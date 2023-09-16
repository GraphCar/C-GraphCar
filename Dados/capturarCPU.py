import mysql.connector
import psutil
from datetime import datetime
import os
import time
import platform
import requests
import json

data_e_hora = datetime.now()
con = mysql.connector.connect(host='localhost', database='GraphCar', user='GraphUser', password='Graph2023')
cursor = con.cursor()

temporizadorAberturaChamado = 0
alertasEmSequencia = 0
skiparTemporizador = True
alertaCPU = "CPU se encontra em normalidade."
tempoEmAlerta = 999

chatEscolhido = "https://hooks.slack.com/services/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"


def capturaCPU():

    global temporizadorAberturaChamado
    global skiparTemporizador
    global alertasEmSequencia
    global alertaCPU
    global tempoEmAlerta

    print("===============================================>   CPU   <================================================\n")

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

    print("Tempo usuário: " + str(round(CPU["tempoUsuario"]/3600,1)) + "H", "             Tempo sistema: " + str(round(CPU["tempoSistema"]/3600,1)) + "H")
    print("Frequência atual: " + str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz", "       Frequência máxima: " + str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Porcentagem da CPU atual: " + str(CPU["CPUAtual"]) + "%", "  Delay da CPU: " + str(CPU["CPUDelay"]) + "%")
    print("Núcleos: " + str(CPU["core"]), " Threads: " + str(CPU["threds"]))
    print("Tempo ocioso: " + str(round(CPU["tempoOcioso"]/3600,1)) + "H")

    if platform.system() != 'Windows':
        Temperatura = str(psutil.sensors_temperatures()['coretemp'][0].current)
        print("Temperatura da CPU: " + Temperatura + "°C")

    comando = "INSERT INTO Dados (idDados, dado, medida, dateDado, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"

    if platform.system() != 'Windows':
        dados = (Temperatura, '°C', data_e_hora, 1)
        cursor.execute(comando,dados)

        dados = (CPU["CPUAtual"], '%', data_e_hora, 1)
        cursor.execute(comando,dados)
    else:
        dados = (CPU["CPUAtual"], '%', data_e_hora, 1)
        cursor.execute(comando,dados)

    temporizadorAberturaChamado = temporizadorAberturaChamado+1
    if temporizadorAberturaChamado == 8 or skiparTemporizador:

        if CPU["CPUAtual"] > 8:

            alertasEmSequencia = alertasEmSequencia + 1
            
            if alertasEmSequencia >= 2 :
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 80% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora não houve melhoras!!"
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertaCPU))
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 80% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"

            else:
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 80% De utilização."
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertaCPU))

            print(postMsg.status_code)
            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia*5

        elif CPU["CPUAtual"] > 6.5:
            
            alertasEmSequencia = alertasEmSequencia + 1

            if alertasEmSequencia >= 2 :
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 50% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora não houve melhoras!!"
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertaCPU))
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 50% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"
                
            else:
                alertaCPU = "🚨ALERTA🚨 Detectamos que a CPU está com mais de 50% De utilização."
                postMsg = requests.post(chatEscolhido, data=json.dumps(alertaCPU))

            print(postMsg.status_code)
            skiparTemporizador = False
            temporizadorAberturaChamado = 0
            tempoEmAlerta = alertasEmSequencia*5

        else:
            skiparTemporizador = True
            alertaCPU = "CPU se encontra em normalidade."
            alertasEmSequencia = 0

        if temporizadorAberturaChamado == 8:
            temporizadorAberturaChamado = 0

    print("\n" + alertaCPU + "\n")
    print(">> Temporizador para abertura de chamado caso necessário: (",temporizadorAberturaChamado, " min / 8 min)")
    print("""
________________________________________________________________________________________
|OBS: Alertas no terminal e o envio deles para o Slack / Jira serão realizados somente |
|quando o temporizador reiniciar caso tenha sido enviado um alerta anteriormente, porém|
|se for capturado um dado alarmante enquanto a CPU estiver em normalidade, então o...  |
|...temporizador será ignorado.                                                        |
|______________________________________________________________________________________|
    """)

    print("==========================================>-----------------<=============================================\n")

    con.commit()
    

while True:
    
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    
    capturaCPU()   
    time.sleep(1)
    