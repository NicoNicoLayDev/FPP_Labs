import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ---------------- ДАННЫЕ ----------------
def load_set():
    currents = np.array([50, 100, 150, 200, 250])
    voltages = np.array([4.3, 7.8, 13.15, 17.1, 21.35])
    dI = np.full_like(currents, 11.3)
    dU = np.full_like(voltages, 0.53)
    return currents, voltages, dI, dU


# ---------------- ЛИНЕЙНАЯ АППРОКСИМАЦИЯ ----------------
def fit_linear(x, y):
    m, b, *_ = stats.linregress(x, y)
    return m, b


# ---------------- ФИЗИЧЕСКАЯ ММ-СЕТКА ----------------
def draw_physical_mm_grid(fig, ax, width_mm, height_mm, dpi):
    fig.canvas.draw()
    bbox = ax.get_window_extent()
    px_per_mm = dpi / 25.4

    # вертикальные линии
    for x_mm in np.arange(0, width_mm + 0.1, 1):
        display_x = bbox.x0 + x_mm * px_per_mm
        xdata, _ = ax.transData.inverted().transform((display_x, bbox.y0))
        if x_mm % 10 == 0:
            ax.axvline(xdata, linewidth=0.8, linestyle='--', color="#505050", alpha=0.7, zorder=0)
        else:
            ax.axvline(xdata, linewidth=0.35, linestyle=':', color="#b0b0b0", alpha=0.45, zorder=0)

    # горизонтальные линии
    for y_mm in np.arange(0, height_mm + 0.1, 1):
        display_y = bbox.y0 + y_mm * px_per_mm
        _, ydata = ax.transData.inverted().transform((bbox.x0, display_y))
        if y_mm % 10 == 0:
            ax.axhline(ydata, linewidth=0.8, linestyle='--', color="#505050", alpha=0.7, zorder=0)
        else:
            ax.axhline(ydata, linewidth=0.35, linestyle=':', color="#b0b0b0", alpha=0.45, zorder=0)


# ---------------- СОЗДАНИЕ ОСЕЙ ----------------
def init_axes():
    width_mm = 164.8       # 16.48 cm
    height_mm = 104.8      # 10.48 cm
    dpi = 300

    fig, ax = plt.subplots(
        figsize=(width_mm / 25.4, height_mm / 25.4),
        dpi=dpi
    )
    ax.set_axisbelow(True)

    # локаторы для данных, НЕ для миллиметровки!
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.2))

    return fig, ax, width_mm, height_mm, dpi


# ---------------- ТОЧКИ ----------------
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
        label="Эксперимент",
        zorder=5
    )


# ---------------- ЛИНИЯ РЕГРЕССИИ ----------------
def draw_fit(ax, slope, intercept):
    x_vals = np.linspace(40, 260, 250)
    y_vals = slope * x_vals + intercept

    ax.plot(
        x_vals, y_vals,
        color="#D55E00",
        linewidth=2.4,
        linestyle="-",
        label="Линейная аппроксимация",
        zorder=4
    )


# ---------------- ОФОРМЛЕНИЕ ----------------
def finalize(ax):
    ax.set_xlabel("Ток I, мкА", fontsize=12)
    ax.set_ylabel("U_x, мВ", fontsize=12)
    ax.set_title("Зависимость напряжения Холла от тока", fontsize=14)
    ax.set_xlim(35, 265)
    ax.set_ylim(2, 24)
    ax.legend()


# ---------------- СБОРКА ----------------
def build():
    I, U, dI, dU = load_set()
    slope, intercept = fit_linear(I, U)

    fig, ax, width_mm, height_mm, dpi = init_axes()
    draw_data(ax, I, U, dI, dU)
    draw_fit(ax, slope, intercept)
    finalize(ax)

    # ФИЗИЧЕСКАЯ МИЛЛИМЕТРОВКА
    draw_physical_mm_grid(fig, ax, width_mm, height_mm, dpi)

    plt.tight_layout(pad=0.2)
    plt.savefig("plot_UxI_mm_true_grid.png", dpi=dpi)
    plt.show()


if __name__ == "__main__":
    build()
