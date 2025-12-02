import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ---------- ДАННЫЕ ----------
def load_set():
    currents = np.array([50, 100, 150, 200, 250])
    voltages = np.array([4.3, 7.8, 13.15, 17.1, 21.35])
    dI = np.full_like(currents, 11.3)
    dU = np.full_like(voltages, 0.53)
    return currents, voltages, dI, dU


# ---------- ЛИНЕЙНАЯ РЕГРЕССИЯ ----------
def fit_linear(x, y):
    m, b, *_ = stats.linregress(x, y)
    return m, b


# ---------- ПОДГОТОВКА ОСЕЙ С ММ-СЕТКОЙ ----------
def init_axes():

    # размеры в миллиметрах
    width_mm = 164.8
    height_mm = 104.8

    # пересчёт в дюймы (1 дюйм = 25.4 мм)
    width_in = width_mm / 25.4
    height_in = height_mm / 25.4

    # создаём картинку нужного реального размера
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=300)

    ax.set_axisbelow(True)

    # основная сетка = 10 мм
    ax.grid(which="major", linestyle="--", linewidth=0.7,
            color="#505050", alpha=0.55)

    # промежуточная сетка = 1 мм
    ax.grid(which="minor", linestyle=":", linewidth=0.45,
            color="#b0b0b0", alpha=0.45)

    # интервалы осей задаём в мм
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1))

    return fig, ax


# ---------- ТОЧКИ И ПОГРЕШНОСТИ ----------
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


# ---------- ЛИНИЯ РЕГРЕССИИ ----------
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


# ---------- ОФОРМЛЕНИЕ ----------
def finalize(ax):
    ax.set_xlabel("Ток I, мкА", fontsize=12)
    ax.set_ylabel("U_x, мВ", fontsize=12)
    ax.set_title("Зависимость напряжения Холла от тока", fontsize=14)
    ax.set_xlim(35, 265)
    ax.set_ylim(2, 24)
    ax.legend()


# ---------- СБОРКА ----------
def build():
    I, U, dI, dU = load_set()
    slope, intercept = fit_linear(I, U)

    fig, ax = init_axes()
    draw_data(ax, I, U, dI, dU)
    draw_fit(ax, slope, intercept)
    finalize(ax)

    plt.tight_layout()

    # ВАЖНО: PNG при dpi=300 сохраняет реальный размер
    plt.savefig("plot_grid_mm_correct.png", dpi=300)
    plt.show()


build()
