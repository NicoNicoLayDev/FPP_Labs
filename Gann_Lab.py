import matplotlib.pyplot as plt
import numpy as np


# Загружает данные
def load_data_RH():
    U_exp = np.array([4.3, 7.8, 13.2, 17.1, 21.4])
    R_H = np.array([0.43, 0.4, 0.44, 0.43, 0.43])
    dU = np.full_like(U_exp, 0.67)
    dR = np.full_like(R_H, 0.05)
    return U_exp, R_H, dU, dR


# Вычисляет среднее значение
def compute_RH_stats(R_H):
    return np.mean(R_H)


# Создаёт миллиметровку
def create_mm_axes_RH():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_axisbelow(True)

    # Крупная сетка — идентична первой
    ax.grid(True, which='major',
            linestyle='-', linewidth=0.6,
            color='#6b6b6b', alpha=0.55)

    # Мелкая сетка — идентична первой
    ax.grid(True, which='minor',
            linestyle='-', linewidth=0.35,
            color='#b3b3b3', alpha=0.35)

    # СВОИ деления для второй задачи
    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.02))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.01))
    return fig, ax


# Добавляет точки с погрешностями
def plot_points_RH(ax, U_exp, R_H, dU, dR):
    ax.errorbar(U_exp, R_H, xerr=dU, yerr=dR,
                fmt='o', color='red', markersize=8,
                capsize=5, capthick=2, elinewidth=2,
                alpha=0.8, label='Эксперимент')


# Добавляет линию среднего значения
def plot_mean_RH(ax, RH_mean):
    ax.axhline(RH_mean, color='blue', linewidth=2.5,
               label='Среднее значение')


# Оформляет график
def setup_layout_RH(ax, U_exp, R_H, dU, dR):
    ax.set_xlabel('U, мВ', fontsize=12)
    ax.set_ylabel('R_H, м³/Кл', fontsize=12)
    ax.set_title('Зависимость коэффициента Холла от напряжения', fontsize=14)

    x_margin = dU[0] + 5
    y_margin = dR[0] + 0.08

    ax.set_xlim(min(U_exp) - x_margin, max(U_exp) + x_margin)
    ax.set_ylim(min(R_H) - y_margin, max(R_H) + y_margin)
    ax.legend()


# Собирает график целиком
def build_plot_RH():
    U_exp, R_H, dU, dR = load_data_RH()
    RH_mean = compute_RH_stats(R_H)
    fig, ax = create_mm_axes_RH()
    plot_points_RH(ax, U_exp, R_H, dU, dR)
    plot_mean_RH(ax, RH_mean)
    setup_layout_RH(ax, U_exp, R_H, dU, dR)
    plt.tight_layout()
    plt.savefig('hall_coefficient_vs_voltage_mm.png', dpi=300)
    plt.show()


# ---- Запуск второй версии ----
build_plot_RH()