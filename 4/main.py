#!/usr/bin/python

from sys import argv
import random
import math
import tkinter as tk
from tkinter import ttk
import numpy
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

from inspect import getmembers, isfunction, getargspec
import math_generator as gen


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Задание 4")

        self.hist_width = 800
        self.hist_height = 640

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        row = 0
        for frame in (CenterFrame, BottomFrame):
            self.frames[frame] = frame(self.container, self)
            self.frames[frame].grid(row=row,
                                    column=0,
                                    sticky="ewns",
                                    padx=1,
                                    pady=0)
            self.showFrame(frame)
            row += 1
        self.engines = {}
        self.engines[RawGenerator] = RawGenerator(self)

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def update(self):
        print('update!')
        frame = self.frames[CenterFrame].frames[RawFrame][0]
        frame.clear()

    def saveRaw(self):
        print('Save button clicked!')

    def plot(self):
        print('Plot button clicked!')


class CenterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        column = 0
        for frame in (SelectorFrame, RawFrame, ParametersFrame):
            self.frames[frame] = frame(self.container, self)
            self.frames[frame].grid(row=0,
                                    column=column,
                                    sticky="ewns",
                                    padx=2,
                                    pady=4)
            self.showFrame(frame)
            column += 1
        self.fun_list = dict([f for f in getmembers(gen)
                             if isfunction(f[1]) and f[0] != 'rename'])

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def setFunction(self, name):
        args, _, _, defaults = getargspec(self.fun_list[name])
        print(args)
        print(defaults)
        self.frames[ParametersFrame].setParameters(args, list(defaults))


class SelectorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.radioButtons = {}
        self.selector = tk.StringVar(self)
        self.fun_list = [f for f in getmembers(gen)
                         if isfunction(f[1]) and f[0] != 'rename']
        for (key, val) in self.fun_list:
            self.radioButtons[key] = tk.Radiobutton(self,
                                                    text=val.__name__,
                                                    variable=self.selector,
                                                    value=key,
                                                    command=self.notifyParent)
            self.radioButtons[key].pack(side="top", anchor='w')

    def notifyParent(self):
        self.controller.setFunction(self.selector.get())


class RawFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.scrollbar = tk.Scrollbar(self)

        self.frameList = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.frameList.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.frameList.pack(side="top", fill="both", expand=True)

    def addValue(self, value):
        self.frameList.insert("end", value)

    def clear(self):
        self.frameList.delete(0, "end")


class ParametersFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Parameters:')
        label.pack(side="top", anchor='w')
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="x")
        self.entries = {}

    def setParameters(self, parameters, defaults=None):
        self.entries = {}
        self.container.destroy()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="x")

        i = 0
        for title in parameters:
            label = tk.Label(self.container, text='{}:'.format(title))
            label.pack(side="top", anchor='w')

            self.entries[title] = tk.Entry(self.container, width=10)
            self.entries[title].pack(side="top",
                                     anchor='w',
                                     fill="x",
                                     expand=True)
            if not(defaults is None) and title != 'n' and i < len(defaults):
                self.entries[title].insert("end", defaults[i])
                i += 1


class BottomFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.saveButton = ttk.Button(self,
                                     text='Save',
                                     command=lambda: controller.saveRaw())
        self.saveButton.pack(side="left", padx=2)
        self.plotButton = ttk.Button(self,
                                     text='Plot',
                                     command=lambda: controller.plot())
        self.plotButton.pack(side="left", padx=2)

        self.button = ttk.Button(self,
                                 text="Run",
                                 command=lambda: controller.update())
        self.button.pack(side="right", padx=2)


class RawGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.raw = []
        self.fun_list = dict([f for f in getmembers(gen)
                             if isfunction(f[1]) and f[0] != 'rename'])

    def generate(self, fun, parameters):
        self.raw.clear()


app = MainFrame()
app.geometry("800x600")
app.resizable(width=False, height=False)
app.mainloop()
