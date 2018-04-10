import math
import random
import numpy as np
from helpers import rename


# 1
@rename('задержанный единичный импульс')
def u0(n, n0=0):
    return 1 if n == n0 else 0


# 2
@rename('задержанный единичный скачок')
def u1(n, n0=0):
    return 1 if n >= n0 else 0


# 3
@rename('дискретизированная убывающая экспонента')
def gexp(n, a=0.5):
    if (n < 0 or a < 0 or a > 1):
        raise ValueError
    return a**n


# 4
@rename('дискретизированная синусоида')
def gsin(n, a=1, omega=math.pi, phi=0):
    return a*math.sin(n*omega + phi)


# 5
@rename('«меандр»')
def gmeandr(n, L=1):
    return 1 if math.fmod(n, L) < L/2 else -1


# 6
@rename('«пила»')
def gsaw(n, L=2):
    return math.fmod(n, L)/L


# 7
@rename('сигнал с экспоненциальной огибающей')
def xexp(n, a=1, tau=1, omega=math.pi, phi=0):
    return a * math.exp(-t/tau)*math.cos(omega*t + phi)


# 8
@rename('cигнал с балансной огибающей')
def xbcos(n, a=1, u=math.pi, omega=math.pi, phi=0):
    return a * math.cos(u*t) * math.cos(omega*t + phi)


# 9
@rename('cигнал с тональной огибающей')
def xton(n, a=1, m=1, u=math.pi, omega=math.pi, phi=0):
    if (m < 0 or m > 1):
        raise ValueError
    return a * (1 + m * math.cos(u * t)) * math.cos(omega*t + phi)


# 10
@rename('сигнал равномерно распределенного белого шума')
def gmis(a=0, b=1):
    return random.random() * (b-a) + a


# 11
@rename('сигнал белого шума, распределенного по нормальному закону')
def gmisnorm(a=0, sigma=1):
    return np.random.normal(a, sigma)


# 12
@rename('«АРСС»')
def autoregress(n, a=[], b=[], x=[], y=[]):
    sum_y = 0
    for i in range(count(a)):
        sum_y += a[i] * y[n-i-2]
    sum_x = 0
    for i in range(count(b)):
        sum_x += b[i] * x[n-i-2]
    return x[n-1] + sum_x + sum_y
