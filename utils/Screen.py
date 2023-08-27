import tkinter as tk
from tkinter import ttk
import os

class App(tk.Tk):
    def __init__(self, window_title, capturar_cpu=None, capturar_ram=None, capturar_disco=None, plt=None):
        super().__init__()

        # Definindo Atributos
        self.__capturar_cpu = capturar_cpu
        self.__capturar_ram = capturar_ram
        self.__capturar_disco = capturar_disco
        self.__plt = plt

        # Configurando a janela
        self.title(window_title)
        self.geometry("300x400")
        self.resizable(False, False)

        # Configurando Grid
        self.columnconfigure(0, weight=1)

    def create_menu(self):
        # Criação da Label
        label_title = ttk.Label(text="Menu", font=('Arial', 18))

        # Grid Label
        label_title.grid(column=0, row=0, sticky=tk.N, padx=50, pady=10)

        # Criação dos Buttons
        button_cpu = ttk.Button(self, text='Monitorar CPU', command=self.__capturar_cpu)
        button_ram = ttk.Button(self, text='Monitorar Ram', command=self.__capturar_ram)
        button_disk = ttk.Button(self, text='Monitorar Disco', command=self.__capturar_disco)
        button_exit = ttk.Button(self, text='Sair', command=lambda: os._exit(0))

        # Grid Buttons
        button_cpu.grid(column=0, row=1, sticky=tk.EW, padx=50, pady=5)
        button_ram.grid(column=0, row=2, sticky=tk.EW, padx=50, pady=5)
        button_disk.grid(column=0, row=3, sticky=tk.EW, padx=50, pady=5)
        button_exit.grid(column=0, row=4, sticky=tk.EW, padx=50, pady=5)

    def show_info(self, title, command, divisor, format_option):
        window_show_info = tk.Toplevel(self)

        # Criação do Title
        label_title = ttk.Label(window_show_info, text=title, font=('Arial', 18))

        # Grid Title
        label_title.grid(column=0, row=0, sticky=tk.N, padx=50, pady=10)

        # Criação dos Textos
        values = command

        for i, (key, value) in enumerate(values._asdict().items()):
            label_value = ttk.Label(window_show_info, text=f"{key}: {value/divisor:{format_option}}", font=('Arial', 10))
            label_value.grid(column=0, row=i+1, sticky=tk.N, padx=50, pady=10)

