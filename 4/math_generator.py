import math
import random
import numpy as np
from helpers import rename


# 1
@rename('задержанный единичный импульс')
def u0(n, n0=0):
    data = np.zeros(n)
    data[n0] = 1
    return data


# 2
@rename('задержанный единичный скачок')
def u1(n, n0=0):
    return np.concatenate([np.zeros(n0), np.ones(n - n0)])


# 3
@rename('дискретизированная убывающая экспонента')
def gexp(n, a=0.5):
    return np.power(a, np.arange(n))


# 4
@rename('дискретизированная синусоида')
def gsin(n, a=1, omega=math.pi, phi=0):
    return np.multiply(a, np.sin(np.multiply(np.arange(n), omega) + phi))


# 5
@rename('«меандр»')
def gmeandr(n, L=1):
    return np.array([1 if x % L < L/2 else -1 for x in np.arange(n)])


# 6
@rename('«пила»')
def gsaw(n, L=2):
    return np.divide(np.mod(np.arange(n), L), L)


# 7
@rename('сигнал с экспоненциальной огибающей')
def xexp(n, a=1, tau=1, omega=math.pi, phi=0):
    return np.multiply(np.multiply(a, np.exp(np.divide(np.arange(n), -tau))),
                       np.cos(np.multiply(omega, np.arange(n)) + phi))


# 8
@rename('cигнал с балансной огибающей')
def xbcos(n, a=1, u=math.pi, omega=math.pi, phi=0):
    return np.multiply(np.multiply(a, np.cos(np.multiply(u, np.arange(n)))),
                       np.cos(np.multiply(omega, np.arange(n)) + phi))


# 9
@rename('cигнал с тональной огибающей')
def xton(n, a=1, m=1, u=math.pi, omega=math.pi, phi=0):
    return np.multiply(np.multiply(a, 1 + np.multiply(m, np.cos(np.multiply(u, np.arange(n))))),
                       np.cos(np.multiply(omega, np.arange(n)) + phi))


# 10
@rename('сигнал равномерно распределенного белого шума')
def gmis(n, a=0, b=1):
    return np.random.uniform(a, b, n)


# 11
@rename('сигнал белого шума, распределенного по нормальному закону')
def gmisnorm(n, a=0, sigma=1):
    return np.random.normal(a, sigma, n)


# 12
@rename('«АРСС»')
def autoregress(n, sigma=1, aMass=[], bMass=[]):
    p = len(aMass)
    q = len(bMass)
    x = gmisnorm(n, 0, sigma)
    y = np.arange(n)
    for i in range(n):
        sumB = 0
        for j in range(q):
            if i - j - 1 >= 0:
                sumB += bMass[j] * x[i - j]
        sumA = 0
        for j in range(p):
            if i - j - 1 >= 0:
                sumA += aMass[j] * y[i - j - 1]
        y[i] = x[i] + sumB + sumA
    return y
