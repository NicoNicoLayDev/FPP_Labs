import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Загружает исходные данные
def load_data_Ux_I():
    I = np.array([50, 100, 150, 200, 250])
    U_x = np.array([4.3, 7.8, 13.15, 17.1, 21.35])
    delta_I = np.full_like(I, 11.3)
    delta_U = np.full_like(U_x, 0.53)
    return I, U_x, delta_I, delta_U


# Строит линейную аппроксимацию
def compute_regression(I, U_x):
    slope, intercept, *_ = stats.linregress(I, U_x)
    return slope, intercept


# Создаёт фигуру и настраивает миллиметровку
def create_mm_axes():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_axisbelow(True)

    ax.grid(True, which='major', linestyle='-', linewidth=0.6,
            color='#6b6b6b', alpha=0.55)
    ax.grid(True, which='minor', linestyle='-', linewidth=0.35,
            color='#b3b3b3', alpha=0.35)

    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
    return fig, ax


# Добавление точкек с погрешностями
def plot_points(ax, I, U_x, dI, dU):
    ax.errorbar(I, U_x, xerr=dI, yerr=dU,
                fmt='o', color='#d53e4f',
                markersize=8, capsize=4,
                elinewidth=1.4, alpha=0.9,
                label='Эксперимент', zorder=5)


# Добавление линии регрессии
def plot_regression_line(ax, slope, intercept):
    I_line = np.linspace(30, 270, 200)
    U_line = slope * I_line + intercept
    ax.plot(I_line, U_line, color='#3288bd',
            linewidth=2.2, label='Линейная аппроксимация')


# Настройка подписей, рамки и оформления
def setup_layout_Ux_I(ax):
    ax.set_xlabel('Ток I, мкА', fontsize=13)
    ax.set_ylabel('Напряжение Холла U_x, мВ', fontsize=13)
    ax.set_title('Зависимость напряжения Холла от тока', fontsize=15)
    ax.set_xlim(30, 270)
    ax.set_ylim(2, 24)
    ax.legend()


# Собирает график целиком
def build_plot_Ux_I():
    I, U_x, dI, dU = load_data_Ux_I()
    slope, intercept = compute_regression(I, U_x)
    fig, ax = create_mm_axes()
    plot_points(ax, I, U_x, dI, dU)
    plot_regression_line(ax, slope, intercept)
    setup_layout_Ux_I(ax)
    plt.tight_layout()
    plt.savefig('hall_voltage_mm_style.png', dpi=300)
    plt.show()


# ---- Запуск ----
build_plot_Ux_I()