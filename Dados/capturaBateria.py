import psutil
import os
import time

def capturaTodos():
    try:
        # Obtém as informações da bateria
        bateria = psutil.sensors_battery()

        # Verifica se a bateria está presente
        if bateria is not None:
            # Obtém o tempo restante de duração da bateria em segundos
            tempo_restante_segundos = bateria.secsleft

            ValoresBateria = {
                "nivel": psutil.sensors_battery().percent,
            }

            print("Nível da bateria: " + str(round(ValoresBateria["nivel"]))  + "%")

            # Converte o tempo restante para horas e minutos
            if tempo_restante_segundos < 0:
                print("Bateria na fonte de alimentação...")
            else:
                horas_restantes, minutos_restantes = divmod(tempo_restante_segundos // 60, 60)
                print(f'Tempo restante de duração da bateria: {horas_restantes} h e {minutos_restantes} min')

        else:
            print('Informações da bateria não disponíveis.')

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chama a função para obter o tempo restante da bateria
    try:
        # Obtém informações sobre a bateria
        bateria = psutil.sensors_battery()

        # Verifica se a bateria está presente
        if bateria is not None:
            # Obtém informações sobre a energia
            info_energia = psutil.cpu_freq(percpu=False)

            # Verifica se as informações estão disponíveis
            if info_energia is not None:
                consumo_energia_mhz = info_energia.current  # Obtém a frequência atual da CPU

                print(f'Consumo de energia da bateria: {consumo_energia_mhz:.2f} MHz')
            else:
                print('Informações de energia não disponíveis.')
        else:
            print('Informações da bateria não disponíveis.')

    except Exception as e:
        print(f"Ocorreu um erro: {e}")



while True:
    os.system('cls')   
    capturaTodos()   
    time.sleep(2)