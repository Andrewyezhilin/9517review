"""Figures for the elevator-pitch deck (whole-project video pitch)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

DARK = "#1a2744"
BLUE = "#2f6fb3"
RED = "#c0392b"
GOLD = "#b8860b"
GREY = "#8a94a6"
GREEN = "#2e7d52"
LIGHT = "#f2f4f8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.edgecolor": GREY,
    "axes.linewidth": 0.8,
})


def hook_figure(path):
    """The blind spot: history-only forecast misses an incident collapse."""
    rng = np.random.default_rng(11)
    t = np.linspace(0, 120, 145)  # minutes

    actual = 100 + rng.normal(0, 1.5, t.size)
    collapse = 58 / (1 + np.exp(-(t - 62) / 5))
    recover = 40 / (1 + np.exp(-(t - 108) / 6))
    actual = actual - collapse + recover
    forecast = 100 + 0 * t  # history-only model keeps predicting normal

    fig, ax = plt.subplots(figsize=(9.8, 4.5), dpi=200)

    ax.fill_between(t, actual, forecast, where=(forecast > actual + 4),
                    color=RED, alpha=0.14, linewidth=0)
    ax.plot(t, forecast, ls="--", lw=2.6, color=GREY,
            label="History-only forecast: \"everything looks normal\"")
    ax.plot(t, actual, lw=2.8, color=BLUE, label="What actually happens")

    ax.axvline(55, color=RED, lw=1.6, ls=":")
    ax.annotate("Crash reported\n(or rain cell / stadium crowd)",
                xy=(55, 96), xytext=(12, 66),
                fontsize=12.5, color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax.text(88, 74, "THE BLIND SPOT\nbiggest errors exactly when\nearly warning matters most",
            fontsize=13, color=RED, fontweight="bold", ha="center")

    ax.set_xlim(0, 120)
    ax.set_ylim(30, 112)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Speed (km/h)")
    ax.legend(loc="lower left", fontsize=11.5, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, tc="white", fs=12.5, bold=True, ec=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                linewidth=1.5 if ec else 0,
                                edgecolor=ec or fc, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, color=DARK, lw=2.2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle="-|>", mutation_scale=18,
                                 linewidth=lw, color=color))


def architecture_figure(path):
    fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=200)

    # Left column: inputs
    box(ax, 0.15, 3.55, 3.1, 0.85, "TRAFFIC SENSORS\n60-min speed / flow", BLUE, fs=10.5)
    box(ax, 0.15, 2.45, 3.1, 0.85, "INCIDENTS\ntype, distance, time", "#8e44ad", fs=10.5)
    box(ax, 0.15, 1.35, 3.1, 0.85, "WEATHER\nrain, visibility, wind", GREEN, fs=10.5)
    box(ax, 0.15, 0.25, 3.1, 0.85, "EVENT SCHEDULES\nvenue, start / end", GOLD, fs=10.5)

    # Middle: encoders
    box(ax, 4.1, 3.55, 3.0, 0.85, "Graph WaveNet\nbackbone (baseline)", DARK, fs=10.5)
    box(ax, 4.1, 1.1, 3.0, 2.0, "Three compact\ncontext encoders\n+ availability masks", LIGHT, tc=DARK, ec=GREY, fs=10.5)

    # Fusion
    box(ax, 7.7, 2.0, 1.9, 1.5, "GATED\nATTENTION\nfusion", RED, fs=11)

    # Output
    box(ax, 10.15, 2.0, 2.5, 1.5, "30-MINUTE\nNETWORK\nFORECAST", DARK, fs=11.5)

    arrow(ax, 3.25, 3.97, 4.1, 3.97, BLUE)
    arrow(ax, 3.25, 2.87, 4.1, 2.55, "#8e44ad")
    arrow(ax, 3.25, 1.77, 4.1, 2.05, GREEN)
    arrow(ax, 3.25, 0.67, 4.1, 1.55, GOLD)
    arrow(ax, 7.1, 3.97, 8.4, 3.5, DARK)
    arrow(ax, 7.1, 2.1, 7.7, 2.5, GREY)
    arrow(ax, 9.6, 2.75, 10.15, 2.75, RED)

    ax.text(6.4, 4.85, "Only information available at forecast time - no future data, ever",
            fontsize=12, color=RED, style="italic", ha="center")
    ax.text(11.4, 1.35, "Target: reliability gap cut by >= 20%,\nroutine traffic protected within 1%",
            fontsize=10, color=GREY, ha="center")

    ax.set_xlim(0, 12.9)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    hook_figure("presentation/fig_pitch_blindspot.png")
    architecture_figure("presentation/fig_pitch_architecture.png")
    print("pitch figures written")
