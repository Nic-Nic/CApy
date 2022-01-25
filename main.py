import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler


__version__ = 0.1
__author__ = 'Nicolas Palacio-Escat'

class Application(tk.Frame):
    def __init__(self, master=None, **options):
        super().__init__(master)
        self.master = master
        self.master.title('CApy v%.1f' % __version__)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(1, weight=1)

        # Initial configuration
        self.ncells = 100
        self.xdim = 50
        self.ydim = 50

        header = tk.Label(self.master, text='CApy')
        header.grid(columnspan=2, row=0)

        # Generate figure and canvas with toolbar
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        toolbar = NavigationToolbar2Tk(self.canvas, self.master,
                                       pack_toolbar=False)
        toolbar.update()
        toolbar.grid(columnspan=2, row=2)
        self.canvas.get_tk_widget().grid(columnspan=2, row=1, sticky='nsew')

        # Buttons
        self.new = tk.Button(self.master,  text='New', command=self.new_grid)
        self.new.grid(column=0, row=3, sticky='nsew')

        self.playpause = tk.Button(self.master,  text='Play',
                                   command=self.play)
        self.playpause.grid(column=1, row=3, sticky='nsew')

        self.new_grid()

    def new_grid(self):
        self.running = False
        self.playpause.configure(text='Play')

        self.grid = np.zeros([self.xdim, self.ydim], dtype=bool)
        choice = np.random.choice(self.xdim * self.ydim, size=self.ncells,
                                  replace=False)
        np.put(self.grid, choice, True)
        self.update_grid()

    def update_grid(self):
        self.ax.imshow(self.grid, interpolation=None, aspect='auto',
                       cmap='binary')
        self.canvas.draw()

    def play(self):
        if self.running:
           self.running = False
           self.playpause.configure(text='Play')

        else:
            self.running = True
            self.playpause.configure(text='Pause')
            self.iterate()

    def iterate(self):
        if self.running:
            self.evaluate()

        self.master.after(1000, self.iterate)

    def evaluate(self):
        pad = np.pad(self.grid.astype(int), 1, 'wrap')
        neighbors = (pad[1:-1, 2:] + pad[1:-1, :-2] + pad[2:, 1:-1]
                     + pad[:-2, 1:-1] + pad[2:, 2:] + pad[2:, :-2]
                     + pad[:-2, 2:] + pad[:-2, :-2])

        # Conditions
        alive = set(np.where(self.grid.flat)[0])
        nis2 = set(np.where(neighbors.flat == 2)[0])
        nis3 = set(np.where(neighbors.flat == 3)[0])

        # Updating grid
        np.put(self.grid, list(alive - (nis2 | nis3)), False)
        np.put(self.grid, list(nis3 - alive), True)
        self.update_grid()

#==============================================================================#

root = tk.Tk()

app = Application(master=root)
app.mainloop()
