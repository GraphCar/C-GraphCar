from threading import Thread

MAX_GRAPH_AXES = 100


class Graph(Thread):
    def __init__(self, plt=None, title=None, command_x=None, command_y=None):
        Thread.__init__(self)
        self.daemon = False

        # Inic Atributos
        self.plt = plt
        self.__title = title
        self.__command_x = command_x
        self.__command_y = command_y

        self.__logger = {
            'x': [],
            'y': [],
        }

        self.__ax = None
        self.__fig = None
        self.__line = None

    def generate_graph(self):
        self.__fig = self.plt.figure()
        self.__fig.suptitle(self.__title)
        self.__ax = self.__fig.add_subplot(111)

        y = list(range(0, MAX_GRAPH_AXES))
        x = list(range(0, MAX_GRAPH_AXES))

        self.__line, = self.__ax.plot(x, y, c='blue')

    def update_graph(self):
        x = self.__command_x()
        y = self.__command_y()

        self.__logger['x'].append(x)
        self.__logger['y'].append(y)

        self.__line.set_xdata(self.__logger['x'])
        self.__line.set_ydata(self.__logger['y'])

        self.__ax.relim()
        self.__ax.autoscale_view()

        self.__fig.canvas.draw()
        self.__fig.canvas.flush_events()

        if len(self.__logger['x']) > 100:
            self.__logger['x'] = self.__logger['x'][1:]
            self.__logger['y'] = self.__logger['y'][1:]

    def graph_start(self):
        self.start()

    def run(self):
        self.generate_graph()

        while True:
            self.update_graph()
