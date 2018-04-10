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


def f(x, k=1):
    return k**3/2 * x**2 * math.e**(-k*x)


def F(x, k=1):
    return 1 - (1 + k*x + (k*x)**2/2)*math.e**(-k*x)


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Задание 2")

        self.hist_width = 600
        self.hist_height = 400

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        row = 0
        for frame in (InputFrame, SelectorFrame):
            self.frames[frame] = frame(self.container, self)
            self.frames[frame].grid(row=row, column=0, sticky="ewns", padx=2, pady=4)
            self.showFrame(frame)
            row += 1

        self.engines = {}
        for engine in (RawGenerator, StatGenerator):
            self.engines[engine] = engine(self)

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def update_input(self, value):
        frame = self.frames[SelectorFrame].frames[RecycleFrame][0]
        frame.clear()

        try:
            value = int(value)
        except ValueError:
            value = 'Error: Wrong input value - int needed'
            frame.addValue(value)
        engine = self.engines[RawGenerator]
        engine.generateRaw(value)
        for i in range(len(engine.raw)):
            frame.addValue('X[{0}] - {1}'.format(i, engine.raw[i]))

        frame = self.frames[SelectorFrame].frames[StatFrame][0]
        engine = self.engines[StatGenerator]
        engine.compute(self.engines[RawGenerator].raw)
        frame.update(engine.values)

        frame = self.frames[SelectorFrame].frames[HistFrame][0]
        try:
            value = int(frame.getCountBins())
        except ValueError:
            value = 0
        frame.draw(self.engines[RawGenerator].raw, value)

        frame = self.frames[SelectorFrame].frames[StatFunFrame][0]
        frame.draw(self.engines[RawGenerator].raw)

    def redrawHist(self, value):
        frame = self.frames[SelectorFrame].frames[RecycleFrame][0]
        frame.clear()

        try:
            value = int(value)
        except ValueError:
            value = 0

        frame = self.frames[SelectorFrame].frames[HistFrame][0]
        frame.draw(self.engines[RawGenerator].raw, value)

    def saveRaw(self, type):
        engine = self.engines[RawGenerator]
        if (type == 'byte'):
            with open('raw.txt', 'wb') as fout:
                for i in range(len(engine.raw)):
                    fout.write(bytes(engine.raw[i]))
        elif (type == 'string'):
            with open('raw.txt', 'w') as fout:
                for i in range(len(engine.raw)):
                    fout.write('{}\n'.format(engine.raw[i]))


class InputFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.entry = tk.Entry(self, width=10)
        self.entry.pack(side="left", fill="x", expand=True, padx=2)
        self.entry.focus()
        self.entry.bind('<Return>', self.notifyParent)

        self.button = ttk.Button(self, text="Запустить")
        self.button.pack(side="left", padx=2)

    def notifyParent(self, event):
        self.controller.update_input(self.entry.get())


class SelectorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.container = tk.Frame(self)
        self.container.pack(side="bottom", fill="both", expand=True)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {RecycleFrame: [None, "ewns"], StatFrame: [None, "wn"], HistFrame: [None, "ewns"], StatFunFrame: [None, "ewns"]}

        self.radioButtons = {}
        self.selector = tk.StringVar(self)
        for (key, _) in self.frames.items():
            self.radioButtons[key] = tk.Radiobutton(self, text=key.__name__, variable=self.selector, value=key.__name__, command=self.select)
            self.radioButtons[key].pack(side="left")

        for frame in self.frames:
            self.frames[frame][0] = frame(self.container, controller)

        self.selector.set(RecycleFrame.__name__)
        self.showFrame(RecycleFrame)

    def select(self):
        for (key, val) in self.frames.items():
            if key.__name__ == self.selector.get():
                self.showFrame(key)
            else:
                self.hideFrame(key)

    def showFrame(self, container):
        frame = self.frames[container][0]
        frame.grid(row=1, column=0, sticky=self.frames[container][1], padx=2, pady=4)
        frame.tkraise()

    def hideFrame(self, container):
        frame = self.frames[container][0]
        frame.grid_remove()


class RecycleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.scrollbar = tk.Scrollbar(self)

        self.frameList = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.frameList.yview)

        self.rawTypeSaving = tk.StringVar(self, "string")

        self.radioButton1 = tk.Radiobutton(self, text="byte", variable=self.rawTypeSaving, value="byte")
        self.radioButton2 = tk.Radiobutton(self, text="string", variable=self.rawTypeSaving, value="string")

        self.saveButton = ttk.Button(self, text="Save raw", command=lambda: controller.saveRaw(self.rawTypeSaving.get()))

        self.scrollbar.pack(side="right", fill="y")
        self.frameList.pack(side="top", fill="both", expand=True)
        self.radioButton1.pack(side="left", fill="y")
        self.radioButton2.pack(side="left", fill="y")
        self.saveButton.pack(side="right", fill="y")

    def addValue(self, value):
        self.frameList.insert("end", value)

    def clear(self):
        self.frameList.delete(0, "end")


class StatFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.vars = {}
        for title in ("E^[X]", "Var^[X]", "σ^[X]", "ɣ^[X]", "æ^[X]"):
            self.vars[title] = tk.StringVar(self, title + ': None')
            label = tk.Label(self, textvariable=self.vars[title])
            label.pack(side="top", anchor="w")

    def update(self, values):
        for (key, value) in self.vars.items():
            self.vars[key].set('\t' + key + ': None')
        for _, (key, value) in zip(self.vars.items(), values.items()):
            if (key in self.vars):
                self.vars[key].set(key + ': ' + str(value))


class HistFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
# New
        topFrame = tk.Frame(self, parent)
        topFrame.pack(side="top", fill="x", anchor="n")

        self.controller = controller

        self.entry = tk.Entry(topFrame, width=10)
        self.entry.pack(side="left", fill="x", expand="true", padx=2)
        self.entry.focus()
        self.entry.bind('<Return>', self.notifyParent)

        self.button = ttk.Button(topFrame, text="Перерисовать")
        self.button.pack(side="left", padx=2)
# Was
        bottomFrame = tk.Frame(self, parent)
        bottomFrame.pack(side="top", fill="both", expand=True)
        self.canvas = tk.Canvas(
            bottomFrame,
            width=controller.hist_width,
            height=controller.hist_height
        )
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind('<Configure>', self.resize)
        self.figure = None

    def getCountBins(self):
        return self.entry.get()

    def notifyParent(self, event):
        self.controller.redrawHist(self.entry.get())

    def resize(self, event):
        w, h = event.width-100, event.height-100
        self.canvas.config(width=w, height=h)

    def draw(self, raw, count_bins=0):
        _len = max(raw) - min(raw)
        minRaw = min(raw)
        if count_bins == 0:
            N = len(raw)
            dx = 4 / math.sqrt(N)
            count_bins = math.ceil(_len / dx)

        fig = mpl.figure.Figure(figsize=(16, 6), dpi=80)

        ax = fig.add_subplot(111)

        ax.set_xticks(numpy.arange(0, math.ceil(max(raw))+0.5, 0.5))
        maxCountIn = 0
        for i in range(count_bins):
            countIn = self.getCountIn(
                raw,
                _len / count_bins * i + minRaw,
                _len / count_bins * (i+1) + minRaw
            )
            if (maxCountIn < countIn):
                maxCountIn = countIn
        ax.set_ylim(0, maxCountIn + maxCountIn / 10)

        for i in range(count_bins):
            self.drawBins(
                ax,
                _len / count_bins * i + minRaw,
                _len / count_bins,
                self.getCountIn(
                    raw,
                    _len / count_bins * i + minRaw,
                    _len / count_bins * (i+1) + minRaw
                )
            )

        ax.grid(True)
        self.figure = self.drawFigure(fig)

    def drawBins(self, ax, x, width, height):
        ax.add_patch(
            patches.Rectangle(
                (x, 0),
                width,
                height,
                fill=None,
                alpha=1,
            )
        )

    def getCountIn(self, raw, _min, _max):
        N = len(raw)
        return sum(
            elem < _max for elem in raw
        ) / N - sum(
            elem < _min for elem in raw
        ) / N

    def drawFigure(self, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas

        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=self.canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        self.canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo


class StatFunFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=controller.hist_width, height=controller.hist_height)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind('<Configure>', self.resize)
        self.figure = None

    def resize(self, event):
        w, h = event.width-100, event.height-100
        self.canvas.config(width=w, height=h)

    def draw(self, raw):
        n = max(raw) - min(raw)
        N = len(raw)
        dk = 1 / math.sqrt(N)

        fig = mpl.figure.Figure(figsize=(16, 6), dpi=80)
        ax = fig.add_subplot(111)
        x = numpy.linspace(0, n, n * 1000)
        ax.set_xticks(numpy.arange(min(raw), max(raw)+1, 1))
        ax.set_yticks(numpy.arange(0, 1.05, 0.05))
        ax.plot(x, self.F(x, raw), '-', lw=2)
        ax.grid(True)
        self.figure = self.drawFigure(fig)

    def F(self, x, raw):
        N = len(raw)
        return sum(elem < x for elem in raw) / N

    def drawFigure(self, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas

        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=self.canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        self.canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo


class RawGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.raw = []

    def generateRaw(self, N):
        self.raw.clear()
        counter = 0
        const = 30
        while counter < N:
            X = random.random() * const
            Y = random.random()
            if (Y <= f(X)):
                self.raw.append(X)
                counter += 1
        return self.raw


class StatGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.values = {}

    def compute(self, raw):
        N = len(raw)
        self.values['E^[X]'] = sum(raw) / N
        self.values['Var^[X]'] = sum([(raw[i] - self.values['E^[X]'])**2 for i in range(N)]) / N
        self.values['σ^[X]'] = math.sqrt(self.values['Var^[X]'])
        self.values['ɣ^[X]'] = sum([(raw[i] - self.values['E^[X]'])**3 for i in range(N)]) / N / self.values['σ^[X]']**3
        self.values['æ^[X]'] = sum([(raw[i] - self.values['E^[X]'])**4 for i in range(N)]) / N / self.values['σ^[X]']**4 - 3
        return self.values


app = MainFrame()
app.geometry("640x480")
app.mainloop()
