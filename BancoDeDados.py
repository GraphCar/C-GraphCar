import mysql.connector
import psutil
import time
from datetime import datetime

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
        "core": psutil.cpu_count(),
        "threds": psutil.cpu_count(logical=False),
        "CPUAtual": psutil.cpu_percent(interval=None),
        "CPUDelay": psutil.cpu_percent(interval=2)
    }
    

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

    print("Tempo usuário: " + str(round(CPU["tempoUsuario"],0)) + "S")
    print("Tempo sistema: " + str(round(CPU["tempoSistema"],0)) + "S")
    print("Tempo ocioso: " + str(round(CPU["tempoOcioso"],0)) + "S")
    print("Frequência atual: " + str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz")
    print("Frequência máxima: " + str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Núcleos: " + str(CPU["threds"]))
    print("Threds: " + str(CPU["core"]))
    print("Porcentagem da CPU atual: " + str(CPU["CPUAtual"]) + "%")
    print("Delay da CPU: " + str(CPU["CPUDelay"]) + "%")

    print("=======================>-----------<=========================\n")


def capturaRam():

    print("=======================>   Memória RAM   <==========================\n")
    
    ValoresRAM = {
        
        "espacoTotalRAM" : psutil.virtual_memory().total,
        "espacoDisponivelRAM" : psutil.virtual_memory().available,
        "espacoUsadoRAM" : psutil.virtual_memory().used,
        "porcentagemUsoRAM" : psutil.virtual_memory().percent,
        "espacoLivreRAM" : psutil.virtual_memory().free
    
    }


    comando = "INSERT INTO Dados (idDados, dado, dateDado, fkMedida, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados = (ValoresRAM["espacoTotalRAM"], data_e_hora, 3, 2) 
    cursor.execute(comando, dados)

    dados = (ValoresRAM["espacoDisponivelRAM"], data_e_hora, 3, 2) 
    cursor.execute(comando, dados)

    dados = (ValoresRAM["espacoUsadoRAM"], data_e_hora, 3, 2)
    cursor.execute(comando, dados)

    dados = (ValoresRAM["porcentagemUsoRAM"], data_e_hora, 2, 2)
    cursor.execute(comando, dados)

    dados = (ValoresRAM["espacoLivreRAM"], data_e_hora, 3, 2)
    cursor.execute(comando, dados)


    con.commit()
    # print(cursor.rowcount, "Dados da RAM inseridos na tabela!")
    
    print("Espaço total de RAM: " + str(round(ValoresRAM["espacoTotalRAM"]/1e9,2)) + " Gb")
    print("Espaço disponível de RAM: " + str(round(ValoresRAM["espacoDisponivelRAM"]/1e9,2)) + " Gb")
    print("Espaço usado de RAM: " + str(round(ValoresRAM["espacoUsadoRAM"]/1e9,2)) + " Gb")
    print("Porcentagem de RAM: " + str(round(ValoresRAM["porcentagemUsoRAM"])) + " %")
    print("Espaço livre de RAM:" + str(round(ValoresRAM["espacoLivreRAM"]/1e9,2)) + " Gb")

    print("=======================>-----------------<==========================\n")

    time.sleep(1)

def CapturaDisco():

    print("==========================>   Disco   <=============================\n")
    
    disk_usage = psutil.disk_usage('C:\\')

    valoresDisco = {
        "TotalDisco" : disk_usage.total,
        "TotalDiscoUsado" : disk_usage.used,
        "TotalDiscoLivre" : disk_usage.free,
        "PercentualDisco" : disk_usage.percent
    }


    comando = "INSERT INTO Dados (idDados, dado, dateDado, fkMedida, fkComponentes) VALUES (NULL, %s, %s, %s, %s)"
    dados = (valoresDisco["TotalDisco"], data_e_hora, 1, 3)
    cursor.execute(comando, dados)

    dados = (valoresDisco["TotalDiscoUsado"], data_e_hora, 1, 3)
    cursor.execute(comando, dados)

    dados = (valoresDisco["TotalDiscoLivre"], data_e_hora, 1, 3)
    cursor.execute(comando, dados)
    
    dados = (valoresDisco["PercentualDisco"], data_e_hora, 2, 3)
    cursor.execute(comando, dados)

    
    con.commit()
    # print(cursor.rowcount, "Dados do Disco inseridos na tabela!")
    
    print("Total de Disco: " + str(round(valoresDisco["TotalDisco"]/1e9,2)) + " GHz")
    print("Total de Disco usado: " + str(round(valoresDisco["TotalDiscoUsado"]/1e9,2)) + " GHz")
    print("Total de Disco livre: " + str(round(valoresDisco["TotalDiscoLivre"]/1e9,2)) + " GHz")
    print("Percentual de Disco: " + str(valoresDisco["PercentualDisco"]) + " %")

    print("=======================>-----------------<==========================\n")

    time.sleep(1)


    
def load_menu():
    print(f"""
    ==========================>   Menu   <=============================
    Digite uma opção

    1- Monitoramento de CPU
    2- Monitoramento de Disco
    3- Monitoramento de Memória RAM
    4- Todos
    0- Sair

    {'='*68}
    """)
    return input(': ')

menu_keys = [1,2,3,4,0]
opcao_escolhida = int(load_menu())

while True:
    if opcao_escolhida in menu_keys:
        if opcao_escolhida == 1:
            #CPU
            capturaCPU()

        elif opcao_escolhida == 2:
            #Disco
            CapturaDisco()

        elif opcao_escolhida == 3:
            #mRam
            capturaRam()

        elif opcao_escolhida == 4:
            #all
            capturaCPU()
            CapturaDisco()
            capturaRam()

        elif opcao_escolhida == 0:
            #exit
            exit()
    else:
        opcao_escolhida = load_menu()