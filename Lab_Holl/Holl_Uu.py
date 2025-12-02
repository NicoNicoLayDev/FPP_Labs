import matplotlib.pyplot as plt
import numpy as np


# Загружает экспериментальные точки и погрешности
def load_input():
    u = np.array([4.3, 7.8, 13.2, 17.1, 21.4])
    rh = np.array([0.43, 0.40, 0.44, 0.43, 0.43])
    du = np.full_like(u, 0.67)
    dr = np.full_like(rh, 0.05)
    return u, rh, du, dr


# Возвращает среднее значение величины
def calc_average(values):
    return float(np.mean(values))


# Создаёт поле графика с миллиметровкой
def make_axes():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_axisbelow(True)

    # Основная сетка
    ax.grid(which="major", linestyle="--", linewidth=0.7,
            color="#4a4a4a", alpha=0.55)

    # Мелкая сетка
    ax.grid(which="minor", linestyle=":", linewidth=0.45,
            color="#9e9e9e", alpha=0.45)

    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.02))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.01))

    return fig, ax


# Строит экспериментальные точки с погрешностями
def draw_points(ax, u, rh, du, dr):
    ax.errorbar(
        u, rh,
        xerr=du, yerr=dr,
        fmt='s', markersize=7,
        markerfacecolor="#0072B2",
        markeredgecolor="#003f5c",
        ecolor="#404040",
        elinewidth=1.6, capsize=4,
        label="Эксперимент"
    )


# Рисует линию среднего значения
def draw_mean_line(ax, mean_val):
    ax.axhline(
        mean_val,
        color="#CC79A7",
        linestyle="-.",
        linewidth=2.3,
        label="Среднее"
    )


# Подписывает оси и задаёт рамки
def finalize_layout(ax, u, rh, du, dr):
    ax.set_xlabel("U, мВ", fontsize=12)
    ax.set_ylabel("R_H, м³/Кл", fontsize=12)
    ax.set_title("Экспериментальная зависимость коэффициента Холла", fontsize=14)

    ax.set_xlim(min(u) - du[0] - 4, max(u) + du[0] + 4)
    ax.set_ylim(min(rh) - dr[0] - 0.05, max(rh) + dr[0] + 0.05)
    ax.legend()


# Собирает график целиком
def build_plot():
    u, rh, du, dr = load_input()
    mean_val = calc_average(rh)

    fig, ax = make_axes()
    draw_points(ax, u, rh, du, dr)
    draw_mean_line(ax, mean_val)
    finalize_layout(ax, u, rh, du, dr)

    plt.tight_layout()
    plt.savefig("plot_RH_modified_visual.png", dpi=300)
    plt.show()


build_plot()