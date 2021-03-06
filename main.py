#!/usr/bin/env python

__version__ = 0.3
__author__ = 'Nicolas Palacio-Escat'

import tkinter as tk
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# TODO: Add menus


class Application(tk.Frame):
    init_running = False
    init_step = 0
    init_xdim = 50
    init_ydim = 50
    init_ncells = 1000
    init_rule_b = 3
    init_rule_s = 23
    init_speed = 500

    def __init__(self, root=None, **options):
        super().__init__(root)
        self.root = root
        self.root.title('CApy v%.1f' % __version__)

        self.root.rowconfigure(1, weight=1)

        for i in range(6):
            self.root.columnconfigure(i, weight=1)

        self.header = tk.StringVar(master=self.root,
                                   value='Step %d' % Application.init_step)
        self.label_header = tk.Label(self.root, textvariable=self.header)
        self.label_header.grid(columnspan=6, row=0)

        # Generate figure and canvas with toolbar
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        toolbar = NavigationToolbar2Tk(self.canvas, self.root,
                                       pack_toolbar=False)
        toolbar.update()
        toolbar.grid(columnspan=6, row=2)
        self.canvas.get_tk_widget().grid(columnspan=6, row=1, sticky='nsew')

        # Parameter entries
        self.label_xdim = tk.Label(self.root, text='X size: ', width=10,
                                   anchor='e')
        self.label_xdim.grid(column=0, row=3, sticky='e')
        self.entry_xdim = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_xdim.insert('end', Application.init_xdim)
        self.entry_xdim.grid(column=1, row=3, sticky='w')

        self.label_ydim = tk.Label(self.root, text='Y size: ', width=10,
                                   anchor='e')
        self.label_ydim.grid(column=2, row=3, sticky='e')
        self.entry_ydim = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_ydim.insert('end', Application.init_ydim)
        self.entry_ydim.grid(column=3, row=3, sticky='w')

        self.label_ncells = tk.Label(self.root, text='N cells: ', width=10,
                                     anchor='e')
        self.label_ncells.grid(column=4, row=3, sticky='e')
        self.entry_ncells = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_ncells.insert('end', Application.init_ncells)
        self.entry_ncells.grid(column=5, row=3, sticky='w')

        self.label_rule_b = tk.Label(self.root, text='B rule: ', width=10,
                                     anchor='e')
        self.label_rule_b.grid(column=0, row=4, sticky='e')
        self.entry_rule_b = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_rule_b.insert('end', Application.init_rule_b)
        self.entry_rule_b.grid(column=1, row=4, sticky='w')

        self.label_rule_s = tk.Label(self.root, text='S rule: ', width=10,
                                     anchor='e')
        self.label_rule_s.grid(column=2, row=4, sticky='e')
        self.entry_rule_s = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_rule_s.insert('end', Application.init_rule_s)
        self.entry_rule_s.grid(column=3, row=4, sticky='w')

        self.label_speed = tk.Label(self.root, text='Speed (ms): ', width=10,
                                     anchor='e')
        self.label_speed.grid(column=4, row=4, sticky='e')
        self.entry_speed = tk.Entry(self.root, relief='ridge', width=10)
        self.entry_speed.insert('end', Application.init_speed)
        self.entry_speed.grid(column=5, row=4, sticky='w')

        # Buttons
        self.button_new = tk.Button(self.root,  text='New',
                                    command=self.new_setup)
        self.button_new.grid(column=0, columnspan=3, row=5, sticky='nsew')

        self.button_playpause = tk.Button(self.root,  text='Play',
                                          command=self.playpause)
        self.button_playpause.grid(column=3, columnspan=3, row=5, sticky='nsew')

        self.new_setup()

    def new_setup(self):
        # Stop running
        self.running = Application.init_running
        self.button_playpause.configure(text='Play')

        # Assert and set/update parameters
        # Checking for non-integer values
        try:
            assert self.entry_xdim.get().isnumeric()
            assert self.entry_ydim.get().isnumeric()
            assert self.entry_ncells.get().isnumeric()
            assert self.entry_rule_b.get().isnumeric() \
                    or not self.entry_rule_b.get()
            assert self.entry_rule_s.get().isnumeric() \
                    or not self.entry_rule_s.get()
            assert self.entry_speed.get().isnumeric()

        except AssertionError:
            msg = 'Some of the parameters provided are not integers!'

            return tk.messagebox.showerror(title='Input error', message=msg)

        self.xdim = int(self.entry_xdim.get())
        self.ydim = int(self.entry_ydim.get())
        self.ncells = int(self.entry_ncells.get())
        self.rule_b = set(int(i) for i in self.entry_rule_b.get())
        self.rule_s = set(int(i) for i in self.entry_rule_s.get())
        self.speed = int(self.entry_speed.get())

        # Checking for valid parameter values
        if self.ncells > self.xdim * self.ydim:
            msg = 'Number of cells exceeds the available grid space!'

            return tk.messagebox.showerror(title='Input error', message=msg)

        if 9 in self.rule_s | self.rule_b:
            msg = 'Moore\'s neighbourhood cannot be greater than 8!'
            tk.messagebox.showwarning(title='Please note', message=msg)

        # Generating initial conditions
        self.step = Application.init_step
        self.matrix = np.zeros([self.ydim, self.xdim], dtype=bool)
        choice = np.random.choice(self.xdim * self.ydim, size=self.ncells,
                                  replace=False)
        np.put(self.matrix, choice, True)

        self.update_canvas()

    def update_canvas(self):
        self.header.set('Step %d' % self.step)
        self.ax.clear()
        self.ax.imshow(self.matrix, interpolation=None, aspect='auto',
                       cmap='binary', vmin=0, vmax=1)
        self.canvas.draw()

    def playpause(self):
        if self.running:
           self.running = False
           self.button_playpause.configure(text='Play')

        else:
            self.running = True
            self.button_playpause.configure(text='Pause')
            self.iterate()

    def iterate(self):
        if self.running:
            self.evaluate()
            self.root.after(self.speed, self.iterate)

    def evaluate(self):
        self.step += 1
        pad = np.pad(self.matrix.astype(np.uint8), 1, 'wrap')
        neighbors = (pad[1:-1, 2:] + pad[1:-1, :-2] + pad[2:, 1:-1]
                     + pad[:-2, 1:-1] + pad[2:, 2:] + pad[2:, :-2]
                     + pad[:-2, 2:] + pad[:-2, :-2])
        alive = self.matrix.copy()

        # Applying conditions
        survive = reduce(np.logical_or, [neighbors == i for i in self.rule_s]) \
                      if self.rule_s else np.zeros(neighbors.shape, dtype=bool)
        born = reduce(np.logical_or, [neighbors == i for i in self.rule_b]) if \
                   self.rule_b else np.zeros(neighbors.shape, dtype=bool)

        np.putmask(self.matrix, alive & ~survive, False)
        np.putmask(self.matrix, born & ~alive, True)

        self.update_canvas()


#==============================================================================#

if __name__ == '__main__':
    root = tk.Tk()

    app = Application(root=root)
    app.mainloop()
