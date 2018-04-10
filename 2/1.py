import sys
import numpy
import matplotlib.pyplot as plt
import math
import random
import argparse

argparser = argparse.ArgumentParser(description='Process count of series.')
argparser.add_argument('--N', metavar='N', type=int, help='set count of series')
args = argparser.parse_args()

N = args.N
raw_path = 'raw.txt'
generated_raw_path = 'generated_raw.txt'
plot_raw_path = 'raw.png'
plot_fun_path = 'fun.png'
plot_hist_path = 'hist.png'
plot_gen_fun_path = 'gen_fun.png'
n = 50
count_buns = 10
p = 0.1
q = 1 - p


def c(n, k):
    if not(type(n) is int) or not(type(k) is int) or n < 1 or k < 0 or n < k:
        raise ValueError
    n_k = 1
    for i in range(n - k, n):
        n_k *= i+1
    for i in range(k):
        n_k /= i+1
    return int(n_k)


# task a
raw = []
for i in range(n+1):
    elem = c(n, i) * p**i * q**(n-i)
    raw.append(elem)
with open(raw_path, 'w') as fout:
    for i in range(len(raw)):
        fout.write('{0} | {1}\n'.format(i, raw[i]))
print('raw saved to {0}'.format(raw_path))
print('task A: complete\n')

# task b
x = numpy.arange(0, n+1, 1)
y = numpy.asarray(raw)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, n+1, 1))
ax.set_yticks(numpy.arange(min(raw), max(raw), (max(raw) - min(raw)) / 10))
ax.fill_between(x, 0, y)
plt.plot(x, y, '.-', lw=2)
plt.grid(True)
plt.savefig(plot_raw_path)
print('raw\'s plot saved to {0}'.format(plot_raw_path))
print('task B: complete\n')

# task c
x = numpy.arange(0, n+1, 1)
y = numpy.array([sum([raw[i] for i in range(n)]) for n in range(len(raw))])
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, n+1, 1))
ax.set_yticks(numpy.arange(min(y), max(y) + 1, (max(y) - min(y)) / 11))
plt.plot(x, y, '-', lw=2)
plt.grid(True)
plt.savefig(plot_fun_path)
print('function\'s plot saved to {0}'.format(plot_fun_path))
print('task C: complete\n')

# task d
print('P(2 <= X <= 7) = {0}'.format(sum([raw[i] for i in range(2, 7+1)])))
print('task D: complete\n')

# task e
E = sum([i * raw[i] for i in range(len(raw))])
Var = sum([(i - E)**2 * raw[i] for i in range(n)])
print('E[X] = {0},\nVar[X] = {1}'.format(E, Var))
print('task E: complete\n')

# if N not set, then exit
if not (type(N) is int):
    sys.exit()

# task f
generated_raw = []
for i in range(N):
    bun = []
    for j in range(count_buns):
        bun.append(0)
    for k in range(n):
        bun[random.randint(0, count_buns-1)] += 1
    generated_raw.append(bun[random.randint(0, count_buns-1)])
with open(generated_raw_path, 'w') as fout:
    for i in range(len(generated_raw)):
        fout.write('{0} | {1}\n'.format(i, generated_raw[i]))
print('generated raw saved to {0}'.format(generated_raw_path))
print('task F: complete\n')

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
hist_dy = math.ceil(n / dk)
if (hist_dy > 300):
    hist_dy = 300
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, n+1, 1))
ax.set_yticks(numpy.arange(0, 1.01, 0.01))
#
bin_height, bin_boundary = numpy.histogram(generated_raw, bins=hist_dy)
width = bin_boundary[1] - bin_boundary[0]
bin_height = bin_height / float(sum(bin_height))
plt.bar(bin_boundary[:-1], bin_height, width = width)
#
plt.grid(True)
plt.savefig(plot_hist_path)
print('hist\'s plot saved to {0}'.format(plot_hist_path))
print('task H: complete\n')

# task i


def F(x):
    return sum(elem < x for elem in generated_raw) / N


x = numpy.linspace(0, n+1, n * 10)
fig = plt.figure(num=None, figsize=(16, 6), dpi=80)
ax = fig.gca()
ax.set_xticks(numpy.arange(0, n+1, 1))
ax.set_yticks(numpy.arange(0, 1.05, 0.05))
plt.plot(x, F(x), '-', lw=2)
plt.grid(True)
plt.savefig(plot_gen_fun_path)
print('raw\'s plot saved to {0}'.format(plot_gen_fun_path))
print('task I: complete\n')
