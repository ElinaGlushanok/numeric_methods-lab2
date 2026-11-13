from methods import dichotomy, fibonacci, golden_ratio, network_search
import matplotlib.pyplot as plt

def f(x):
    return (x - 0.37) * (x - 0.37)

a, b = -2, 2
eps = 1e-4
methods = [
    ("Дихотомия", dichotomy),
    ("Золотое сечение", golden_ratio),
    ("Поиск Фибоначчи", fibonacci)]

fig, (ax_lengths, ax_ratios) = plt.subplots(1, 2, figsize=(11, 4))
for name, method in methods:
    _, _, final_interval, _, _, _, history = method(f, a, b, eps)
    lengths = [right - left for left, right, c, d in history]
    final_left, final_right = final_interval
    lengths.append(final_right - final_left)
    ratios = [lengths[k + 1] / lengths[k] for k in range(len(lengths) - 1)]
    ax_lengths.plot(range(len(lengths)), lengths, marker=".", label=name)
    ax_ratios.plot(range(len(ratios)), ratios, marker=".", label=name)
    
ax_lengths.set_xlabel("Номер интервала $k$")
ax_lengths.set_ylabel("$L_k$")
ax_lengths.set_yscale("log")

ax_ratios.set_xlabel("Номер шага $k$")
ax_ratios.set_ylabel("$L_{k+1}/L_k$")

for ax in (ax_lengths, ax_ratios):
    ax.grid(True, alpha=0.3)
    ax.legend()

fig.tight_layout()
fig.savefig("graphs_p3.png", dpi=300, bbox_inches="tight")
plt.show()