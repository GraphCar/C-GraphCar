import mysql.connector
import pyodbc
import psutil
from datetime import datetime
import os
import time
import platform
import requests
import json

data_e_hora = datetime.now()
con_mysql = mysql.connector.connect(host='localhost', database='GraphCar', user='GraphUser', password='Graph2023')
cursor_mysql = con_mysql.cursor()

con_mssql = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=44.211.199.205;DATABASE=GraphCar;UID=sa;PWD=urubu100;TrustServerCertificate=yes')
cursor_mssql = con_mssql.cursor()

temporizadorAberturaChamado = 0
alertasEmSequencia = 0
skiparTemporizador = True
alertaCPU = "CPU se encontra em normalidade."
tempoEmAlerta = 0


def capturaTodos():

    global temporizadorAberturaChamado
    global skiparTemporizador
    global alertasEmSequencia
    global alertaCPU
    global alertaRAM
    global alertaDisco
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

    ValoresRAM = {
        "espacoTotalRAM" : psutil.virtual_memory().total,
        "espacoDisponivelRAM" : psutil.virtual_memory().available,
        "espacoUsadoRAM" : psutil.virtual_memory().used,
        "porcentagemUsoRAM" : psutil.virtual_memory().percent,
        "espacoLivreRAM" : psutil.virtual_memory().free
    }

    print("Tempo usuário: " + str(round(CPU["tempoUsuario"]/3600,1)) + "H", "             Tempo sistema: " + str(round(CPU["tempoSistema"]/3600,1)) + "H")
    print("Frequência atual: " + str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz", "       Frequência máxima: " + str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Porcentagem da CPU atual: " + str(CPU["CPUAtual"]) + "%", "  Delay da CPU: " + str(CPU["CPUDelay"]) + "%")
    print("Núcleos: " + str(CPU["core"]), "                     Threads: " + str(CPU["threds"]))
    print("Tempo ocioso: " + str(round(CPU["tempoOcioso"]/3600,1)) + "H")
    
    if platform.system() != 'Windows':
        Temperatura = None #str(psutil.sensors_temperatures()['coretemp'][0].current)
        print("Temperatura da CPU: " + Temperatura + "°C")

    print("Espaço total de RAM: " + str(round(ValoresRAM["espacoTotalRAM"]/1e9,2)) + " Gb")
    print("Espaço disponível de RAM: " + str(round(ValoresRAM["espacoDisponivelRAM"]/1e9,2)) + " Gb")
    print("Espaço usado de RAM: " + str(round(ValoresRAM["espacoUsadoRAM"]/1e9,2)) + " Gb")
    print("Porcentagem de uso da RAM: " + str(round(ValoresRAM["porcentagemUsoRAM"])) + " %")
    print("Espaço livre de RAM: " + str(round(ValoresRAM["espacoLivreRAM"]/1e9,2)) + " Gb")

    ValoresBateria = {
        "nivel": psutil.sensors_battery().percent,
        "tempo_restante": psutil.sensors_battery().secsleft,
    }

    if ValoresBateria["tempo_restante"] < 0:
        ValoresBateria["tempo_restante"] = -1

    if ValoresBateria["tempo_restante"] > 4000000000:
        ValoresBateria["tempo_restante"] = -1

    print("Nível da bateria: " + str(ValoresBateria["nivel"]))
    print("Tempo Restante: " + str(round(ValoresBateria["tempo_restante"])))

    comando_mysql = "INSERT INTO Dados (idDados, cpuUso, cpuTemperatura, gpuUso, gpuTemperatura, memoria, bateriaNivel, bateriaTaxa, bateriaTempoRestante , dateDado, fkCarro) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s)"
    comando_mssql = "INSERT INTO Dados (cpuUso, cpuTemperatura, gpuUso, gpuTemperatura, memoria, bateriaNivel, bateriaTaxa, bateriaTempoRestante , dateDado, fkCarro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)"
    print(ValoresBateria["tempo_restante"])
    if platform.system() != 'Windows':
        dados = (CPU["CPUAtual"], Temperatura, None, None, round(ValoresRAM["porcentagemUsoRAM"], 1), round(ValoresBateria["nivel"], 1), None, ValoresBateria["tempo_restante"], 2)
        cursor_mysql.execute(comando_mysql,dados)
        cursor_mssql.execute(comando_mssql, dados)
    else:
        dados = (CPU["CPUAtual"], None, None, None, round(ValoresRAM["porcentagemUsoRAM"], 1), round(ValoresBateria["nivel"], 1), None, ValoresBateria["tempo_restante"], 2)
        cursor_mysql.execute(comando_mysql,dados)
        cursor_mssql.execute(comando_mssql, dados)

    # temporizadorAberturaChamado = temporizadorAberturaChamado+1
    # if temporizadorAberturaChamado == 60 or skiparTemporizador:

    #     if CPU["CPUAtual"] > 50:

    #         alertasEmSequencia = alertasEmSequencia + 1
            
    #         if alertasEmSequencia >= 2 :

    #             alertaCPU = {"text": f"""
    #             🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 50% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "{tempoEmAlerta}min e até agora não houve melhoras!!"
    #             """}

    #             # requests.post(chatEscolhido, data=json.dumps(alertaCPU))

    #             alertaCPU = "🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 50% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"

    #         else:
    #             alertaCPU = {"text": f""" 
    #             🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 50% De utilização.
    #             """} 
    #             # requests.post(chatEscolhido, data=json.dumps(alertaCPU))

    #             alertaCPU = "🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 30% De utilização."

    #         skiparTemporizador = False
    #         temporizadorAberturaChamado = 0
    #         tempoEmAlerta = tempoEmAlerta + 5

    #     elif CPU["CPUAtual"] > 30:
            
    #         alertasEmSequencia = alertasEmSequencia + 1

    #         if alertasEmSequencia >= 2 :
    #             alertaCPU = {"text": f"""
    #             🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 30% De utilização. Essa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "{tempoEmAlerta}min e até agora não houve melhoras!!"
    #             """}

    #             # requests.post(chatEscolhido, data=json.dumps(alertaCPU))

    #             alertaCPU = "🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 30% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"
                
    #         else:
    #             alertaCPU = {"text": f"""
    #             🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 30% De utilização.
    #             """}

    #             # requests.post(chatEscolhido, data=json.dumps(alertaCPU))
                
    #             alertaCPU = "🚨ALERTA DA CPU🚨 Detectamos que a CPU está com mais de 30% De utilização.\nEssa não é a primeira vez emitimos um alerta a respeito dela, já se passaram "+ str(tempoEmAlerta) +" min e até agora...\n...não houve melhoras!!"

    #         skiparTemporizador = False
    #         temporizadorAberturaChamado = 0
    #         tempoEmAlerta = tempoEmAlerta + 5

    #     else:
    #         skiparTemporizador = True
    #         alertaCPU = "CPU se encontra em normalidade."
    #         alertasEmSequencia = 0
    #         tempoEmAlerta = 0

    #     if temporizadorAberturaChamado == 60:
    #         temporizadorAberturaChamado = 0

#     print("\n" + alertaCPU + "\n")
#     print(">> Temporizador para abertura de chamado caso necessário: (",temporizadorAberturaChamado*5, "s / 5 min)")
#     print("""
# ________________________________________________________________________________________
# |OBS: Alertas no terminal e o envio deles para o Slack / Jira serão realizados somente |
# |quando o temporizador reiniciar caso tenha sido enviado um alerta anteriormente, porém|
# |se for capturado um dado alarmante enquanto a CPU estiver em normalidade, então o...  |
# |...temporizador será ignorado.                                                        |
# |______________________________________________________________________________________|
#     """)

    print("==========================================>-----------------<=============================================\n")

    con_mysql.commit()
    con_mssql.commit()
    

while True:
    
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    
    capturaTodos()   
    time.sleep(5)
