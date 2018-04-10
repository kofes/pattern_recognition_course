import sys
import numpy
import matplotlib.pyplot as plt
import math
import random
import argparse

argparser = argparse.ArgumentParser(description='Process count of series.')
argparser.add_argument('--N', metavar='N', type=int, help='set count of series')
argparser.add_argument('--file', metavar='input', help='set input binary file')
args = argparser.parse_args()

N = args.N
filename = args.file

plot_hist_path = 'custom_hist.png'
plot_gen_fun_path = 'custom_gen_fun.png'
n = 50
count_buns = 10

# if N not set, then exit
if not (type(N) is int) or not (type(filename) is str):
    sys.exit()

generated_raw = []
with open(filename, 'rb') as fin:
    for i in range(N):
        generated_raw.append(int(fin.read(1)[0]))

# task g
gen_E = sum(generated_raw) / N
gen_Var = sum([(generated_raw[i] - gen_E)**2 for i in range(N)]) / N
gen_sigma = math.sqrt(gen_Var)
gen_gamma = sum([(generated_raw[i] - gen_E)**3 for i in range(N)]) / N / gen_sigma**3
gen_ae = sum([(generated_raw[i] - gen_E)**4 for i in range(N)]) / N / gen_sigma**4 - 3
print('E^[X] = {0}\nVar^[X] = {1}\nɣ^ = {2}\næ^ = {3}'.format(gen_E, gen_Var, gen_gamma, gen_ae))
print('task G: complete\n')

# task h
dk = 50 / math.sqrt(N)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(min(generated_raw), max(generated_raw)+1, 1))
ax.set_yticks(numpy.arange(0, 1 + dk / 50, dk / 50))
plt.hist(generated_raw, normed=True, bins=(math.ceil(n / dk)))
plt.grid(True)
plt.savefig(plot_hist_path)
print('hist\'s plot saved to {0}'.format(plot_hist_path))
print('task H: complete\n')

# task i


def F(x):
    return sum(elem < x for elem in generated_raw) / N


x = numpy.linspace(min(generated_raw), max(generated_raw), (max(generated_raw) - min(generated_raw)) * 2)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(min(generated_raw), max(generated_raw)+1, 1))
ax.set_yticks(numpy.arange(0, 1 + dk / 50, dk / 50))
plt.plot(x, F(x), '-', lw=2)
plt.grid(True)
plt.savefig(plot_gen_fun_path)
print('raw\'s plot saved to {0}'.format(plot_gen_fun_path))
print('task I: complete\n')
