import sys
import numpy
import matplotlib.pyplot as plt
import math
import random
import argparse

plot_f_path = 'fun_2.png'
plot_F_path = 'Fun_2.png'


def f(x, k=1):
    return k**3/2 * x**2 * math.e**(-k*x)


def F(x, k=1):
    return 1 - (1 + k*x + (k*x)**2/2)*math.e**(-k*x)


x = numpy.arange(0, 15, 0.5)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, 15, 1))
ax.set_yticks(numpy.arange(0, 1 + 0.05, 0.05))
plt.plot(x, F(x), '-', lw=2)
plt.grid(True)
plt.savefig(plot_F_path)

x = numpy.arange(0, 15, 0.05)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, 15, 1))
ax.set_yticks(numpy.arange(0, 1 + 0.05, 0.05))
plt.plot(x, f(x), '-', lw=2)
plt.grid(True)
plt.savefig(plot_f_path)
