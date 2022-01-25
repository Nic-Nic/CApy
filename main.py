import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler


__version__ = 0.0

class Application(tk.Frame):
    def __init__(self, master=None, **options):
        super().__init__(master)
        self.master = master
        self.master.title('CApy v%.1f' % __version__)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        self.ncells = 50
        self.xdim = 100
        self.ydim = 100

        header = tk.Label(self.master, text='CApy')
        header.grid(column=0, row=0)

        self.fig, self.ax = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        toolbar = NavigationToolbar2Tk(self.canvas, self.master,
                                       pack_toolbar=False)
        toolbar.update()
        toolbar.grid(column=0, row=2)
        self.canvas.get_tk_widget().grid(column=0, row=1, sticky='nsew')

        button_new = tk.Button(self.master,  text='New', command=self.new_grid)
        button_new.grid(column=0, row=3, sticky='nsew')

        self.new_grid()

    def new_grid(self):
        self.grid = np.zeros([self.xdim, self.ydim], dtype=bool)
        choice = np.random.choice(self.xdim * self.ydim, size=self.ncells,
                                  replace=False)
        np.put(self.grid, choice, True)
        self.update_grid()

    def update_grid(self):
        self.ax.imshow(self.grid, interpolation=None, aspect='auto',
                       cmap='binary')
        self.canvas.draw()
#==============================================================================#

root = tk.Tk()

app = Application(master=root)
app.mainloop()
