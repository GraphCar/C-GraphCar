import platform
import os 


commando_incializacao = "gnome-terminal --bash -c ./" 


if platform.system() == "Windows":
    commando_incializacao = "start "


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

    #print(opcao_escolhida, type(opcao_escolhida))

    if opcao_escolhida in menu_keys:

        if opcao_escolhida == 1:
            #CPU
            os.system(f'{commando_incializacao}Dados/capturarCPU.py')
            opcao_escolhida = -1

        elif opcao_escolhida == 2:
            #Disco
            os.system(f'{commando_incializacao}Dados/capturarDisco.py')
            opcao_escolhida = -1

        elif opcao_escolhida == 3:
            #mRam
            os.system(f'{commando_incializacao}Dados/capturarRAM.py')
            opcao_escolhida = -1

        elif opcao_escolhida == 4:
            #all
            os.system(f'{commando_incializacao}Dados/capturarCPU.py')
            os.system(f'{commando_incializacao}Dados/capturarDisco.py')
            os.system(f'{commando_incializacao}Dados/capturarRAM.py')
            opcao_escolhida = -1

        elif opcao_escolhida == 0:
            #exit
            exit() 
    else:
        opcao_escolhida = int(load_menu()) 