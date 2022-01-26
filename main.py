#!/usr/bin/env python

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler


__version__ = 0.1
__author__ = 'Nicolas Palacio-Escat'

class Application(tk.Frame):
    def __init__(self, root=None, **options):
        super().__init__(root)
        self.root = root
        self.root.title('CApy v%.1f' % __version__)

        self.root.rowconfigure(1, weight=1)

        for i in range(6):
            self.root.columnconfigure(i, weight=1)

        header = tk.Label(self.root, text='CApy')
        header.grid(columnspan=6, row=0)

        # Parameters
        self.label_xdim = tk.Label(self.root, text='X size:')
        self.label_xdim.grid(column=0, row=3, sticky='e')
        self.xdim = tk.Entry(self.root, relief='ridge')
        self.xdim.insert('end', '50')
        self.xdim.grid(column=1, row=3)

        self.label_ydim = tk.Label(self.root, text='Y size:')
        self.label_ydim.grid(column=2, row=3, sticky='e')
        self.ydim = tk.Entry(self.root, relief='ridge')
        self.ydim.insert('end', '50')
        self.ydim.grid(column=3, row=3)

        self.label_ncells = tk.Label(self.root, text='N cells:')
        self.label_ncells.grid(column=4, row=3, sticky='e')
        self.ncells = tk.Entry(self.root, relief='ridge')
        self.ncells.insert('end', '1000')
        self.ncells.grid(column=5, row=3)

        # Buttons
        self.new = tk.Button(self.root,  text='New', command=self.new_canvas)
        self.new.grid(column=0, columnspan=3, row=4, sticky='nsew')

        self.playpause = tk.Button(self.root,  text='Play',
                                   command=self.play)
        self.playpause.grid(column=3, columnspan=3, row=4, sticky='nsew')

        self.new_canvas()

    def new_canvas(self):
        # Stop running
        self.running = False
        self.playpause.configure(text='Play')

        # Generate figure and canvas with toolbar
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        toolbar = NavigationToolbar2Tk(self.canvas, self.root,
                                       pack_toolbar=False)
        toolbar.update()
        toolbar.grid(columnspan=6, row=2)
        self.canvas.get_tk_widget().grid(columnspan=6, row=1, sticky='nsew')

        self.matrix = np.zeros([int(self.ydim.get()), int(self.xdim.get())],
                             dtype=bool)
        choice = np.random.choice(int(self.xdim.get()) * int(self.ydim.get()),
                                  size=int(self.ncells.get()), replace=False)
        np.put(self.matrix, choice, True)
        self.step = 0

        self.update_canvas()

    def update_canvas(self):
        self.ax.clear()
        self.ax.imshow(self.matrix, interpolation=None, aspect='auto',
                       cmap='binary')
        self.ax.set_title('Step %d' % self.step)
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
            self.root.after(500, self.iterate)

    def evaluate(self):
        self.step += 1
        pad = np.pad(self.matrix.astype(int), 1, 'wrap')
        neighbors = (pad[1:-1, 2:] + pad[1:-1, :-2] + pad[2:, 1:-1]
                     + pad[:-2, 1:-1] + pad[2:, 2:] + pad[2:, :-2]
                     + pad[:-2, 2:] + pad[:-2, :-2])

        # Conditions
        alive = set(np.where(self.matrix.flat)[0])
        nis2 = set(np.where(neighbors.flat == 2)[0])
        nis3 = set(np.where(neighbors.flat == 3)[0])

        # Updating grid
        np.put(self.matrix, list(alive - (nis2 | nis3)), False)
        np.put(self.matrix, list(nis3 - alive), True)
        self.update_canvas()

#==============================================================================#

if __name__ == '__main__':
    root = tk.Tk()

    app = Application(root=root)
    app.mainloop()
