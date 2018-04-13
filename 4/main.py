#!/usr/bin/python

from sys import argv
import random
import math
import tkinter as tk
from tkinter import ttk
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import spectrum

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

        self.fun_list = dict([f for f in getmembers(gen)
                             if isfunction(f[1]) and f[0] != 'rename'])

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
        for engine in (RawGenerator, StatGenerator):
            self.engines[engine] = engine(self)

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def update(self):
        print('update!')
        frame = self.frames[CenterFrame].frames[ParametersFrame]
        values = frame.getParameters()
        del values['L_SPM']
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        engine = self.engines[RawGenerator]
        raw = engine.generate(funName, values)
        frame = self.frames[CenterFrame].frames[RawFrame]
        frame.clear()
        for i in range(len(raw)):
            frame.addValue('x[{0}]: {1}'.format(i, raw[i]))
        frame = self.frames[CenterFrame].frames[SelectorFrame].frames[StatFrame]
        engine = self.engines[StatGenerator]
        frame.update(engine.compute(raw))

    def saveRaw(self):
        engine = self.engines[RawGenerator]
        with open('raw.txt', 'w') as fout:
            for i in range(len(engine.raw)):
                fout.write('{}\n'.format(engine.raw[i]))

    def plotLinear(self):
        engine = self.engines[RawGenerator]
        x = numpy.arange(0, len(engine.raw), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()
        plt.xlabel(u'n')
        plt.ylabel(u'X(n)')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'Функция "{}"'.format(self.fun_list[funName].__name__))
        plt.plot(x, engine.raw, '-', lw=2)
        plt.grid(True)
        plt.show()

    def plotLines(self):
        engine = self.engines[RawGenerator]
        x = numpy.arange(0, len(engine.raw), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()

        plt.xlabel(u'n')
        plt.ylabel(u'X(n)')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'Функция "{}"'.format(self.fun_list[funName].__name__))

        plt.plot(x, engine.raw, '.', lw=2)
        plt.vlines(x, [0], engine.raw)
        plt.grid(True)
        plt.show()

    def plotFFTAm(self):
        engine = self.engines[RawGenerator]
        fun = numpy.abs(numpy.fft.rfft(engine.raw))
        x = numpy.arange(0, len(fun), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()

        plt.xlabel(u'n')
        plt.ylabel(u'FFT(X(n)) -> Am(n)')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'ДПФ. Амплитудный спектр. ({})'.format(self.fun_list[funName].__name__))

        plt.plot(x, fun, '-', lw=2)
        plt.grid(True)
        plt.show()

    def plotFFTLogAm(self):
        engine = self.engines[RawGenerator]
        lg = numpy.vectorize(lambda x: 20 * numpy.log10(x))
        fun = lg(numpy.abs(numpy.fft.rfft(engine.raw)))
        x = numpy.arange(0, len(fun), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()

        plt.xlabel(u'n')
        plt.ylabel(u'FFT(X(n)) -> Am(n)')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'ДПФ. Амплитудный спектр (Log10). ({})'.format(self.fun_list[funName].__name__))

        plt.plot(x, fun, '-', lw=2)
        plt.grid(True)
        plt.show()

    def plotFFTMoment(self):
        engine = self.engines[RawGenerator]
        fun = numpy.angle(numpy.fft.rfft(engine.raw))
        x = numpy.arange(0, len(fun), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()

        plt.xlabel(u'n')
        plt.ylabel(u'FFT(X(n)) -> Phase(n)')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'ДПФ. Частотный спектр. ({})'.format(self.fun_list[funName].__name__))

        plt.plot(x, fun, '-', lw=2)
        plt.grid(True)
        plt.show()

    def plotSPM(self):
        frame = self.frames[CenterFrame].frames[ParametersFrame]
        values = frame.getParameters()

        engine = self.engines[RawGenerator]
        psd = spectrum.DaniellPeriodogram(engine.raw, values['L_SPM'])
        psd_plot_data = numpy.sqrt(numpy.power(psd[0], 2.0) + numpy.power(psd[1], 2.0))
        x = numpy.arange(0, len(psd_plot_data), 1)
        fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
        ax = fig.gca()

        plt.xlabel(u'n')
        plt.ylabel(u'SPM(X(n))')
        frame = self.frames[CenterFrame].frames[SelectorFrame]
        funName = frame.getFunction()
        plt.title(u'СПМ. ({})'.format(self.fun_list[funName].__name__))

        plt.plot(x, psd_plot_data, '-', lw=2)
        plt.grid(True)
        plt.show()


class CenterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        column = 0
        for frame in (SelectorFrame, ParametersFrame, RawFrame):
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

        self.frames = {}
        self.frames[StatFrame] = StatFrame(self, controller)
        self.frames[StatFrame].pack(side="left")
        self.showFrame(StatFrame)

    def showFrame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def notifyParent(self):
        self.controller.setFunction(self.selector.get())

    def getFunction(self):
        return self.selector.get()


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
        parameters.append('L_SPM')

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

    def getParameters(self):
        res = {}
        for key, val in self.entries.items():
            try:
                if (key == 'n' or key == 'n0' or key == 'L_SPM'):
                    res[key] = int(val.get())
                elif (key == 'aMass' or key == 'bMass'):
                    res[key] = list(map(float, val.get().split(',')))
                else:
                    res[key] = float(val.get())
            except ValueError:
                print('Bad value at {}'.format(key))
                if (key == 'aMass' or key == 'bMass'):
                    res[key] = []
                else:
                    res[key] = 0
        return res


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
        self.plotLinearButton = ttk.Button(self,
                                           text='Plot (linear inter.)',
                                           command=lambda: controller.plotLinear())
        self.plotLinearButton.pack(side="left", padx=2)

        self.plotLinesButton = ttk.Button(self,
                                          text='Plot (vetical lines)',
                                          command=lambda: controller.plotLines())
        self.plotLinesButton.pack(side="left", padx=2)

        self.plotFFTAmButton = ttk.Button(self,
                                          text='Plot (FFT Amplitude)',
                                          command=lambda: controller.plotFFTAm())
        self.plotFFTAmButton.pack(side="left", padx=2)

        self.plotFFTLogAmButton = ttk.Button(self,
                                             text='Plot (20Log FFT Amplitude)',
                                             command=lambda: controller.plotFFTLogAm())
        self.plotFFTLogAmButton.pack(side="left", padx=2)

        self.plotFFTMomentButton = ttk.Button(self,
                                          text='Plot (FFT Phase)',
                                          command=lambda: controller.plotFFTMoment())
        self.plotFFTMomentButton.pack(side="left", padx=2)

        self.plotSPMButton = ttk.Button(self,
                                          text='Plot (SPM)',
                                          command=lambda: controller.plotSPM())
        self.plotSPMButton.pack(side="left", padx=2)

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
        self.raw = self.fun_list[fun](**parameters)
        return self.raw


class StatFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.vars = {}
        for title in ("Среднее", "Дисперсия", "CKO", "Коэффициент вариации", "Коэффициент асимметрии", "Коэффициент эксцесса"):
            self.vars[title] = tk.StringVar(self, title + ': None')
            label = tk.Label(self, textvariable=self.vars[title])
            label.pack(side="top", anchor="w")

    def update(self, values):
        for (key, value) in self.vars.items():
            self.vars[key].set('\t' + key + ': None')
        for _, (key, value) in zip(self.vars.items(), values.items()):
            if (key in self.vars):
                self.vars[key].set(key + ': ' + str(value))


class StatGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.values = {}

    def compute(self, raw):
        N = len(raw)
        self.values['Среднее'] = sum(raw) / N
        self.values['Дисперсия'] = sum([(raw[i] - self.values['Среднее'])**2 for i in range(N)]) / N
        self.values['CKO'] = math.sqrt(self.values['Дисперсия'])
        self.values['Коэффициент вариации'] = self.values['CKO'] / self.values['Среднее']
        self.values['Коэффициент асимметрии'] = sum([(raw[i] - self.values['Среднее'])**3 for i in range(N)]) / N / self.values['CKO']**3
        self.values['Коэффициент эксцесса'] = sum([(raw[i] - self.values['Среднее'])**4 for i in range(N)]) / N / self.values['CKO']**4 - 3
        return self.values


app = MainFrame()
app.geometry("900x600")
# app.resizable(width=False, height=False)
app.mainloop()
