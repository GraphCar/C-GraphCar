import psutil
import time

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

    print(str(round(CPU["tempoUsuario"],0)) + "S")
    print(str(round(CPU["tempoSistema"],0)) + "S")
    print(str(round(CPU["tempoOcioso"],0)) + "S")
    print(str(round((CPU["frequenciaAtual"]/1e3),2)) + " GHz")
    print(str(round((CPU["frequenciaMaxima"]/1e3),2)) + " GHz")
    print("Núcleos: " + str(CPU["core"]))
    print("Threds: " + str(CPU["threds"]))
    print(str(CPU["CPUAtual"]) + "%")
    print(str(CPU["CPUDelay"]) + "%")

    print("=======================>-----------<=========================\n")



def capturaRam():

    print("=======================>   Memória RAM   <==========================\n")
    
    ValoresRAM = {
        
    "espacoTotalRAM" : psutil.virtual_memory().total,
    "espacoDisponivelRAM" : psutil.virtual_memory().available,
    "espacoUsadoRAM" : psutil.virtual_memory().used,
    "porcentagemUsoRAM" : psutil.virtual_memory().percent,
    "espacoLivreRAM" : psutil.virtual_memory().free,
    
    }
    
    print(str(round(ValoresRAM["espacoTotalRAM"]/1e3,2)) + "Gb")
    print(str(round(ValoresRAM["espacoDisponivelRAM"]/1e3,2)) + "Gb")
    print(str(round(ValoresRAM["espacoUsadoRAM"]/1e3,2)) + "Gb")
    print(str(round(ValoresRAM["porcentagemUsoRAM"])) + "%")
    print(str(round(ValoresRAM["espacoLivreRAM"]/1e3,2)) + "Gb")

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
    
    
    print(str(valoresDisco["TotalDisco"]/1000) + "Gb")
    print(str(valoresDisco["TotalDiscoUsado"]/1000) + "Gb")
    print(str(valoresDisco["PercentualDisco"]) + "%")

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

