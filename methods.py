def network_search(f, a, b, eps):
    initial_interval = (a, b)
    n = int((b - a) / eps) + 1
    h = (b - a) / n
    nodes = [a + h * i for i in range(n)] + [b]

    result = {a: f(a)}
    for node in [b] + nodes[1:-1]:
        if node not in result:
            result[node] = f(node)
    probes = list(result)

    if len(probes) == len(nodes):
        min_ind = 0
        for i in range(n + 1):
            if result[nodes[i]] < result[nodes[min_ind]]:
                min_ind = i
        a = nodes[max(min_ind - 1, 0)]
        b = nodes[min(min_ind + 1, n)]

    midpoint = (a + b) / 2
    if midpoint not in result:
        result[midpoint] = f(midpoint)
    description = "достигнута точность" if b - a <= 2 * eps else "округление"
    history = {"bounds": [initial_interval, (a, b)], "probes": probes}
    return midpoint, result[midpoint], [a, b], len(probes), len(result), description, history


def dichotomy(f, a, b, eps):
    description = "достигнута точность"
    delt = eps / 2
    history = []
    result = dict()
    def res(x):
        if x in result: return result[x]
        result[x] = f(x)
        return result[x]
    res(a)
    res(b)
    while b - a > 2 * eps:
        m = (b + a) / 2
        c = m - delt
        d = m + delt
        if not a < c < d < b:
            description = "округление"
            break
        history.append((a, b, c, d))
        if res(c) <= res(d): b = d
        else: a = c
        
    midpoint = (a + b) / 2
    value = res(midpoint)
    return midpoint, value, [a, b], len(history), len(result), description, history

def golden_ratio(f, a, b, eps):
    tau = (5 ** 0.5 - 1) / 2
    values = {}
    history = []

    def res(x):
        if x not in values:
            values[x] = f(x)
        return values[x]

    res(a)
    res(b)
    c = a + (1 - tau) * (b - a)
    d = a + tau * (b - a)
    description = "достигнута точность"

    while b - a > 2 * eps:
        if not a < c < d < b:
            description = "округление"
            break

        history.append((a, b, c, d))
        if res(c) <= res(d):
            b, d = d, c
            c = a + (1 - tau) * (b - a)
        else:
            a, c = c, d
            d = a + tau * (b - a)

    midpoint = (a + b) / 2
    value = res(midpoint)
    return midpoint, value, [a, b], len(history), len(values), description, history

def fibonacci(f, a, b, eps):

    values = {}
    history = []

    def res(x):
        if x not in values:
            values[x] = f(x)
        return values[x]

    res(a)
    res(b)
    target = 2 * eps
    delta = eps / 100
    width = b - a

    numbers = [0, 1, 1, 2]
    while width / numbers[-1] + delta > target:
        numbers.append(numbers[-1] + numbers[-2])
    m = len(numbers) - 1

    c = a + width * (numbers[m - 2] / numbers[m])
    d = a + width * (numbers[m - 1] / numbers[m])
    if m == 3:
        d = c + delta

    while b - a > target and a < c < d < b:
        history.append((a, b, c, d))
        keep_left = res(c) <= res(d)
        if keep_left:
            b = d
        else:
            a = c

        if m == 3:
            break
        m -= 1

        if keep_left:
            d = c
            c = d - delta if m == 3 else a + (b - a) * (numbers[m - 2] / numbers[m])
        else:
            c = d
            d = c + delta if m == 3 else a + (b - a) * (numbers[m - 1] / numbers[m])

    midpoint = (a + b) / 2
    value = res(midpoint)
    description = "достигнута точность" if b - a <= target else "округление"
    return midpoint, value, [a, b], len(history), len(values), description, history
