"""
=============================================================
ESTRUCTURAS AEROESPACIALES - UNII | Clase 3 | 09 Julio 2026
SCRIPT DE PRACTICA
Tema: Seccion C idealizada - flujo de cortante y centro de cortadura
=============================================================
Ejecuta este script con el entorno .venv activo.
Genera la salida numerica en terminal y una imagen PNG para clase.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_IMAGE = BASE_DIR / "resultado_clase3.png"


def shear_arrow(ax, start, end, color, label, label_offset=(0.0, 0.0), ms=18):
    """Dibuja una flecha simple y su etiqueta."""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=2.0,
        color=color,
    )
    ax.add_patch(arrow)
    mid_x = (start[0] + end[0]) / 2.0 + label_offset[0]
    mid_y = (start[1] + end[1]) / 2.0 + label_offset[1]
    ax.text(
        mid_x,
        mid_y,
        label,
        fontsize=9,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, alpha=0.92),
    )


def draw_open_section(ax, b, h, q_b, x_sc):
    """Seccion abierta tipo C."""
    ax.plot([b, 0], [h / 2, h / 2], color="black", linewidth=4)
    ax.plot([0, 0], [h / 2, -h / 2], color="black", linewidth=4)
    ax.plot([0, b], [-h / 2, -h / 2], color="black", linewidth=4)

    shear_arrow(ax, (0.88 * b, h / 2 + 10), (0.12 * b, h / 2 + 10), "#1f77b4",
                f"q12 = {q_b[0]:.2f} N/mm", label_offset=(0, 12))
    shear_arrow(ax, (-10, 0.42 * h), (-10, -0.42 * h), "#d62728",
                f"q23 = {q_b[1]:.2f} N/mm", label_offset=(-36, 0))
    shear_arrow(ax, (0.12 * b, -h / 2 - 10), (0.88 * b, -h / 2 - 10), "#1f77b4",
                f"q34 = {q_b[2]:.2f} N/mm", label_offset=(0, -12))

    ax.scatter([x_sc], [0], s=80, color="#9467bd", zorder=5)
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.text(x_sc, 15, f"S.C. = {x_sc:.1f} mm", color="#9467bd",
            ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.annotate(
        "",
        xy=(x_sc, 0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", linestyle="--", color="#9467bd", lw=1.5),
    )

    ax.text(
        0.5 * b,
        0.82 * h,
        "Seccion abierta\nEl flujo se acumula y la seccion tiende a girar",
        ha="center",
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#999999"),
    )


def draw_closed_section(ax, b, h, q_s, q0):
    """Seccion cerrada tipo cajon."""
    ax.plot([0, b], [h / 2, h / 2], color="black", linewidth=4)
    ax.plot([0, b], [-h / 2, -h / 2], color="black", linewidth=4)
    ax.plot([0, 0], [h / 2, -h / 2], color="black", linewidth=4)
    ax.plot([b, b], [h / 2, -h / 2], color="black", linewidth=4)

    shear_arrow(ax, (0.88 * b, h / 2 + 10), (0.12 * b, h / 2 + 10), "#2ca02c",
                f"q12 = {q_s[0]:.2f} N/mm", label_offset=(0, 12))
    shear_arrow(ax, (-10, 0.42 * h), (-10, -0.42 * h), "#d62728",
                f"q23 = {q_s[1]:.2f} N/mm", label_offset=(-36, 0))
    shear_arrow(ax, (0.12 * b, -h / 2 - 10), (0.88 * b, -h / 2 - 10), "#2ca02c",
                f"q34 = {q_s[2]:.2f} N/mm", label_offset=(0, -12))
    shear_arrow(ax, (b + 10, -0.42 * h), (b + 10, 0.42 * h), "#d62728",
                f"q41 = {q_s[3]:.2f} N/mm", label_offset=(36, 0))

    ax.scatter([b / 2], [0], s=60, color="#111111", zorder=5)
    ax.text(
        0.5 * b,
        0.82 * h,
        f"Seccion cerrada\nq0 = {q0:.2f} N/mm\nLas alas dejan de cargar cortante vertical",
        ha="center",
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#999999"),
    )


def save_visualization(b, h, q_b, x_sc, q0, q_s):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    draw_open_section(axes[0], b, h, q_b, x_sc)
    draw_closed_section(axes[1], b, h, q_s, q0)

    for ax in axes:
        ax.set_aspect("equal")
        ax.set_xlim(-80, b + 80)
        ax.set_ylim(-h / 2 - 70, h / 2 + 70)
        ax.axis("off")

    fig.suptitle(
        "Clase 3: flujo de cortante en seccion abierta y cerrada",
        fontsize=15,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.02,
        "Comparacion didactica: seccion abierta = flujo irregular y giro; seccion cerrada = flujo de cierre y mejor distribucion.",
        ha="center",
        fontsize=10,
    )
    fig.savefig(OUTPUT_IMAGE, dpi=200, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def main():
    # Datos de la seccion idealizada
    Vy = 15000.0
    b, h = 120.0, 240.0
    A = 150.0

    # Coordenadas (x, y) de los booms 1, 2, 3, 4
    booms = np.array([[b, h / 2], [0, h / 2], [0, -h / 2], [b, -h / 2]])

    # Inercia Ix = sum(A * y^2)
    Ix = np.sum(A * booms[:, 1] ** 2)
    print(f"Inercia Ix = {Ix:,.1f} mm^4")

    # Flujo de cortante: seccion abierta
    q_b = np.zeros(4)
    q_current = 0.0
    for i in range(3):
        y_i = booms[i, 1]
        q_current = q_current - (Vy / Ix) * A * y_i
        q_b[i] = q_current

    print(
        f"Flujos Abiertos [N/mm]: q12={q_b[0]:.2f}, q23={q_b[1]:.2f}, q34={q_b[2]:.2f}"
    )

    # Centro de cortadura
    e = (abs(q_b[0]) * b * h) / Vy
    x_sc = -e
    print(f"Centro de cortadura x_sc = {x_sc:.1f} mm")

    # Seccion cerrada
    ds_lengths = np.array([b, h, b, h])
    integral_qb_ds = np.sum(q_b * ds_lengths)
    integral_ds = np.sum(ds_lengths)
    q_0 = -integral_qb_ds / integral_ds
    print(f"\nFlujo de cierre q_0 = {q_0:.2f} N/mm")

    q_s = q_b + q_0
    print("Flujos Cerrados [N/mm]:")
    print(
        f"q12={q_s[0]:.2f}, q23={q_s[1]:.2f}, q34={q_s[2]:.2f}, q41={q_s[3]:.2f}"
    )

    Vy_int = q_s[1] * h - q_s[3] * h
    print(f"Cortante interno total = {abs(Vy_int):.1f} N")

    save_visualization(b, h, q_b, x_sc, q_0, q_s)
    print(f"Imagen generada en: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
