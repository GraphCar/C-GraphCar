import psutil
import matplotlib.pyplot as plt

from utils import Logger
from utils.Screen import App
from utils.Graph import Graph

DEFAULT_INTERVAL = 0  # s


def capturar_cpu():
    graph_use_cpu = Graph(plt, 'Uso CPU',
                          lambda: psutil.cpu_times().user,  # Axes X
                          lambda: psutil.cpu_percent(interval=DEFAULT_INTERVAL))  # Axes Y

    graph_use_cpu.graph_start()

    # cat /sys/class/hwmon/hwmonX/in0_input


def capturar_ram():
    graph_use_ram = Graph(plt, 'Uso Ram',
                           lambda: psutil.cpu_times().user,  # Axes X
                           lambda: psutil.virtual_memory().percent)  # Axes Y

    graph_use_ram.graph_start()


def capturar_disco():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        device = partition.device

        try:
            device_infos = psutil.disk_usage(device)

            app.show_info(f"Disco - {device}", device_infos, 1e9, '.2f')

        except Exception as e:
            Logger.warning(f"Erro ao Ler Disco - {e}")


if __name__ == "__main__":
    plt.ion()
    app = App("C-GraphCar", capturar_cpu, capturar_ram, capturar_disco, plt)
    app.create_menu()
    app.mainloop()

