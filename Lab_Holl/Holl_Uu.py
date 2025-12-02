import matplotlib.pyplot as plt
import numpy as np


# ---------------- ДАННЫЕ ----------------
def load_input():
    u = np.array([4.3, 7.8, 13.2, 17.1, 21.4])
    rh = np.array([0.43, 0.40, 0.44, 0.43, 0.43])
    du = np.full_like(u, 0.67)
    dr = np.full_like(rh, 0.05)
    return u, rh, du, dr


# ---------------- СРЕДНЕЕ ----------------
def calc_average(values):
    return float(np.mean(values))


# ---------------- ФИЗИЧЕСКАЯ ММ-СЕТКА ----------------
def draw_physical_mm_grid(fig, ax, width_mm=164.8, height_mm=104.8, dpi=300):
    """
    Рисует сетку в физических миллиметрах поверх axes.
    width_mm, height_mm — размеры рисунка в мм (включая поля figure->axes).
    dpi — разрешение при котором была создана фигура.
    """

    # Нужен рендер, чтобы трансформации были корректны
    fig.canvas.draw()

    # bbox оси в координатах окна (pixels)
    bbox = ax.get_window_extent()

    # шаг в пикселях для 1 mm
    px_per_mm = dpi / 25.4

    # вертикальные линии (по ширине фигуры)
    for x_mm in np.arange(0, width_mm + 0.1, 1.0):
        display_x = bbox.x0 + x_mm * px_per_mm
        # Преобразуем точку из display -> data
        xdata, _ = ax.transData.inverted().transform((display_x, bbox.y0))
        # большой штрих через каждые 10 мм
        if (x_mm % 10) == 0:
            ax.axvline(xdata, linewidth=0.8, linestyle='--', color="#505050", alpha=0.7, zorder=0)
        else:
            ax.axvline(xdata, linewidth=0.35, linestyle=':', color="#b0b0b0", alpha=0.45, zorder=0)

    # горизонтальные линии (по высоте фигуры)
    for y_mm in np.arange(0, height_mm + 0.1, 1.0):
        display_y = bbox.y0 + y_mm * px_per_mm
        _, ydata = ax.transData.inverted().transform((bbox.x0, display_y))
        if (y_mm % 10) == 0:
            ax.axhline(ydata, linewidth=0.8, linestyle='--', color="#505050", alpha=0.7, zorder=0)
        else:
            ax.axhline(ydata, linewidth=0.35, linestyle=':', color="#b0b0b0", alpha=0.45, zorder=0)


# ---------------- ОСЬ И СЕТКА В ЕДИНИЦАХ ДАННЫХ ----------------
def make_axes():
    # размеры в мм (физические)
    width_mm = 164.8
    height_mm = 104.8

    # перевод в дюймы для figsize
    width_in = width_mm / 25.4
    height_in = height_mm / 25.4

    # создаём фигуру нужного физического размера и dpi
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=300)
    ax.set_axisbelow(True)

    # НЕ используем ax.grid для физической мм-сетки.
    # Оставим стили отображения данных как раньше (major/minor в единицах данных),
    # но реальную миллиметровую сетку мы дорисуем функцией draw_physical_mm_grid.
    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.02))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.01))

    return fig, ax, width_mm, height_mm


# ---------------- ТОЧКИ ----------------
def draw_points(ax, u, rh, du, dr):
    ax.errorbar(
        u, rh,
        xerr=du, yerr=dr,
        fmt='s', markersize=7,
        markerfacecolor="#0072B2",
        markeredgecolor="#003f5c",
        ecolor="#404040",
        elinewidth=1.6, capsize=4,
        label="Эксперимент",
        zorder=5
    )


# ---------------- ЛИНИЯ СРЕДНЕГО ----------------
def draw_mean_line(ax, mean_val):
    ax.axhline(
        mean_val,
        color="#CC79A7",
        linestyle="-.",
        linewidth=2.3,
        label="Среднее значение",
        zorder=4
    )


# ---------------- ОФОРМЛЕНИЕ ----------------
def finalize_layout(ax, u, rh, du, dr):
    ax.set_xlabel("U, мВ", fontsize=12)
    ax.set_ylabel("R_H, м³/Кл", fontsize=12)
    ax.set_title("Экспериментальная зависимость коэффициента Холла", fontsize=14)

    ax.set_xlim(min(u) - du[0] - 4, max(u) + du[0] + 4)
    ax.set_ylim(min(rh) - dr[0] - 0.05, max(rh) + dr[0] + 0.05)
    ax.legend()


# ---------------- СБОРКА ----------------
def build_plot():
    u, rh, du, dr = load_input()
    mean_val = calc_average(rh)

    fig, ax, width_mm, height_mm = make_axes()
    draw_points(ax, u, rh, du, dr)
    draw_mean_line(ax, mean_val)
    finalize_layout(ax, u, rh, du, dr)

    # рисуем физическую миллиметровую сетку ПОСЛЕ установки лимитов и прорисовки данных
    # (фигуру нужно предварительно отрисовать, поэтому вызываем canvas.draw внутри функции)
    draw_physical_mm_grid(fig, ax, width_mm=width_mm, height_mm=height_mm, dpi=300)

    plt.tight_layout(pad=0.2)
    plt.savefig("plot_RH_mm_true_grid.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    build_plot()
