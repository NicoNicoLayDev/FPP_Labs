import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Загружает эксперимент
def load_set():
    currents = np.array([50, 100, 150, 200, 250])
    voltages = np.array([4.3, 7.8, 13.15, 17.1, 21.35])
    dI = np.full_like(currents, 11.3)
    dU = np.full_like(voltages, 0.53)
    return currents, voltages, dI, dU


# Строит коэффициенты линейной аппроксимации
def fit_linear(x, y):
    m, b, *_ = stats.linregress(x, y)
    return m, b


# Формирует поле графика с миллиметровкой
def init_axes():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_axisbelow(True)

    ax.grid(which="major", linestyle="--", linewidth=0.7,
            color="#505050", alpha=0.55)

    ax.grid(which="minor", linestyle=":", linewidth=0.45,
            color="#b0b0b0", alpha=0.45)

    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))

    return fig, ax


# Рисует экспериментальные точки и погрешности
def draw_data(ax, I, U, dI, dU):
    ax.errorbar(
        I, U,
        xerr=dI, yerr=dU,
        fmt="D",
        markersize=7,
        markerfacecolor="#009E73",
        markeredgecolor="#004d40",
        ecolor="#444444",
        linewidth=1.5,
        capsize=4,
        label="Эксперимент"
    )


# Рисует прямую регрессии
def draw_fit(ax, slope, intercept):
    x_vals = np.linspace(40, 260, 250)
    y_vals = slope * x_vals + intercept

    ax.plot(
        x_vals, y_vals,
        color="#D55E00",
        linewidth=2.4,
        linestyle="-",
        label="Линейная аппроксимация"
    )


# Подписывает оси и оформляет
def finalize(ax):
    ax.set_xlabel("Ток I, мкА", fontsize=12)
    ax.set_ylabel("U_x, мВ", fontsize=12)
    ax.set_title("Зависимость напряжения Холла от тока", fontsize=14)
    ax.set_xlim(35, 265)
    ax.set_ylim(2, 24)
    ax.legend()


# Сборка графика
def build():
    I, U, dI, dU = load_set()
    slope, intercept = fit_linear(I, U)

    fig, ax = init_axes()
    draw_data(ax, I, U, dI, dU)
    draw_fit(ax, slope, intercept)
    finalize(ax)

    plt.tight_layout()
    plt.savefig("plot_UxI_modified_visual.png", dpi=300)
    plt.show()


build()
