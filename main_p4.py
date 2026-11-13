from methods import network_search, golden_ratio, fibonacci, dichotomy

c = 0.37
r = 0.4
a, b = -2, 2

def f1(x):
    return x

def f2(x):
    return -x

def f3(x):
    return (x - c) * (x - c)

def f4(x):
    return abs(x - c)

def f5(x):
    return (x - c) ** 4

def f6(x):
    return (max(abs(x - c) - r, 0))**2

def cmp(y1, y2):
    if y1 > y2:
        return -1
    if y1 < y2:
        return 1
    return 0

def f_star(f):
    mono_type = [[], [], []]
    mono = []
    prototype = dict()
    minf = None
    def add(fx, x):
        if fx in prototype:
            prototype[fx].append(x)
        else:
            prototype[fx] = [x]
    last = None
    for i in range(a*100, b*100+1):
        x = i / 100
        fx = f(x)
        minf = fx if minf is None else min(minf, fx)
        add(fx, x)
        if last is not None:
            mono.append(cmp(last, fx))
        last = fx

    last = mono[0]
    left, right = 0, 0
    for i in range(1, len(mono)):
        if mono[i] == last:
            right += 1
        else:
            if last == -1:
                mono_type[0].append([left / 100 + a, right / 100 + a])
            elif last == 0:
                mono_type[1].append([left / 100 + a, right / 100 + a])
            else:
                mono_type[2].append([left / 100 + a, right / 100 + a])
            last = mono[i]
            left, right = i, i

    return minf, prototype[minf], mono_type
ot = f_star(f6)[1]
print(ot[0], ot[-1])
#Ex = max(0, -0.33-x, x-0.77)


def f0(x):
    return 1


def boundary_minimum(x):
    return (x - 2) ** 2

file = open("4_1.txt", "w")
eps = 1e-4
for label, f, left, right, f_min in [("Постоянная функция", f0, a, b, 1),
                                     ("Граничный минимум", boundary_minimum, b, b, 0),]:
    file.write(label)
    for method in (network_search, dichotomy, golden_ratio, fibonacci):
        x, fx, *_ = method(f, a, b, eps)
        ex = max(0, left - x, x - right)
        file.write(f"{method.__name__} x = {x} E_x = {ex}, E_f = {fx - f_min}\n")


functions = [
    (f1, a, a, a),
    (f2, b, b, -b),
    (f3, c, c, 0),
    (f4, c, c, 0),
    (f5, c, c, 0),
    (f6, c - r, c + r, 0),
]
methods = (network_search, dichotomy, golden_ratio, fibonacci)
limit = 100_000

file = open("4_2.txt", "w")
file.write("Функция | eps | Метод | N_f | L | x | E_x | E_f | Причина остановки\n")
for f, left, right, f_min in functions:
    for eps in (1e-2, 1e-4, 1e-6):
        nodes = int((b - a) / eps) + 2
        file.write("\n")
        for method in methods:
            if method is network_search and nodes + 1 > limit:
                file.write(f"{f.__name__} | {eps:.0e} | {method.__name__} | "
                      f"— | — | — | — | — | превышен лимит ({nodes} узлов)\n")
                continue

            x, fx, (lo, hi), _, nf, reason, _ = method(f, a, b, eps)
            ex = max(0, left - x, x - right)
            ef = fx - f_min
            file.write(f"{f.__name__} | {eps:.0e} | {method.__name__} | {nf} | "
                  f"{hi - lo:.6g} | {x:.10g} | {ex:.6g} | {ef:.6g} | {reason}\n")
