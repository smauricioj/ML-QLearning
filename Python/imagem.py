import matplotlib.pyplot as plt
from math import log2, factorial
from itertools import cycle

def beta(o,n):
    return (factorial(int(log2(o))))/(factorial(int(log2(o))-n))

def q_size(o,n):
    return (2**(4*(n+1)))*(3**n)*(beta(o,n))

def full_size(o):
    return (log2(o)-1)**16

x, y, y2 = [], [], []
marker = cycle(('.', 'x', 'd', 'o', '^', 'v')) 

for n in range(2,8):
    for o in [2**x for x in range(4,12)]:
        if log2(o)-n >= 0:
            x.append(o)
            y.append(q_size(o, n)/full_size(o))
            print(n, ', ', o, ', ', q_size(o, n))
    plt.plot(x, y, marker=next(marker), label=f'n = {n}')
    x.clear()
    y.clear()

# for o in [2**x for x in range(4,12)]:
#     x.append(o)
#     y2.append(1-log2(o))
# plt.plot(x, y2, 'r--', label='min(r)')

plt.gca().set_xscale("log", base=2)
plt.gca().set_yscale("log")

plt.axhline(y=1, linestyle='--')
plt.grid()
plt.legend()
plt.xlabel('Objetivo')
plt.ylabel('|E|/|S|')
plt.show()