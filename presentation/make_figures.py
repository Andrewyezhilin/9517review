"""Generate the two diagrams embedded in the presentation slides."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DARK = "#1a2744"
BLUE = "#2f6fb3"
RED = "#c0392b"
GOLD = "#b8860b"
GREY = "#8a94a6"
GREEN = "#2e7d52"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.edgecolor": GREY,
    "axes.linewidth": 0.8,
})


def episode_figure(path):
    rng = np.random.default_rng(7)
    t = np.linspace(0, 24, 289)  # 5-min steps over 24 h

    # Expected weekly profile: morning peak stays above threshold, evening peak
    # dips below it so the plot shows a *recurring* congestion episode too.
    profile = 105 - 22 * np.exp(-((t - 8.0) / 1.3) ** 2) - 38 * np.exp(-((t - 17.5) / 1.4) ** 2)

    # Observed speed: follows profile, plus an incident-induced collapse ~13:00-15:00
    obs = profile + rng.normal(0, 1.8, t.size)
    incident = 62 * np.exp(-((t - 14.0) / 0.85) ** 4)
    obs = obs - incident
    obs = np.clip(obs, 8, None)

    free_flow = 106.0
    threshold = 0.7 * free_flow

    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=200)

    below = obs < threshold
    ax.fill_between(t, 0, 130, where=below, color=RED, alpha=0.08, linewidth=0)

    ax.plot(t, profile, ls="--", lw=1.8, color=GREY, label="Expected time-of-week profile (training median)")
    ax.plot(t, obs, lw=2.2, color=BLUE, label="Observed 5-min speed")
    ax.axhline(free_flow, color=GREEN, lw=1.4, ls="-.")
    ax.axhline(threshold, color=RED, lw=1.4, ls=":")

    ax.text(0.3, free_flow + 3.0, "Free-flow speed (85th pct of overnight training obs)",
            color=GREEN, fontsize=11)
    ax.text(0.3, threshold + 2.5, "70% of free-flow: episode starts when below for >= 15 min",
            color=RED, fontsize=11)

    ax.annotate("Incident reported\n(<= 5 km, <= 90 min\nbefore forecast origin)",
                xy=(13.2, 40), xytext=(8.6, 22),
                fontsize=10.5, color=DARK, ha="center",
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.3))

    # Deviation arrow at the centre of the incident dip
    i = int(14.35 / 24 * 288)
    ax.annotate("", xy=(14.35, obs[i] + 2), xytext=(14.35, profile[i] - 2),
                arrowprops=dict(arrowstyle="<->", color=GOLD, lw=2.2))
    ax.text(14.9, 48, ">= 20% or 15 km/h\nbelow expected + disruption\n= NON-RECURRING",
            color=GOLD, fontsize=10.5, fontweight="bold", va="center")

    ax.annotate("Ordinary evening peak,\nno anomaly, no exposure\n= RECURRING",
                xy=(18.1, 62), xytext=(21.2, 12),
                fontsize=10.5, color=GREY, ha="center", style="italic",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))

    ax.set_xlim(0, 24)
    ax.set_ylim(0, 128)
    ax.set_xticks(range(0, 25, 4))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 4)])
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Speed (km/h)")
    ax.legend(loc="lower left", fontsize=10, framealpha=0.95)
    ax.set_title("Separating recurring from non-recurring congestion (all thresholds from training data only)",
                 fontsize=13.5, color=DARK, pad=10)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def split_figure(path):
    fig, ax = plt.subplots(figsize=(9.6, 3.0), dpi=200)

    segments = [
        ("Training  ~21 mo", 21, BLUE, 12),
        ("", 1.4, GOLD, 0),
        ("Validation ~7 mo", 7, GREEN, 10.5),
        ("", 1.4, GOLD, 0),
        ("Test ~7 mo", 7, RED, 10.5),
    ]
    x = 0.0
    embargo_centres = []
    for label, w, color, fs in segments:
        ax.barh(0.55, w, left=x, height=0.55, color=color,
                edgecolor="white", linewidth=1.5)
        if label:
            ax.text(x + w / 2, 0.55, label, ha="center", va="center", color="white",
                    fontsize=fs, fontweight="bold")
        else:
            embargo_centres.append(x + w / 2)
        x += w

    for cx in embargo_centres:
        ax.annotate("7-day\nembargo", xy=(cx, 0.83), xytext=(cx, 1.12),
                    fontsize=10, color=GOLD, ha="center", fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))

    ax.text(x / 2, 1.52, "Chronological 60 / 20 / 20 split of the 2022-2024 study period",
            ha="center", fontsize=13.5, color=DARK, fontweight="bold")

    ax.annotate("No congestion episode may cross a boundary;\nall preprocessing statistics fitted on training data only",
                xy=(21.7, 0.27), xytext=(11.0, -0.42),
                fontsize=10.5, color=DARK, ha="center",
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))
    ax.annotate("Test set untouched until analysis code\nand decision rules are frozen",
                xy=(33.3, 0.27), xytext=(31.0, -0.42),
                fontsize=10.5, color=RED, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

    ax.set_xlim(-0.3, 38.4)
    ax.set_ylim(-0.75, 1.75)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    episode_figure("presentation/fig_episode_definition.png")
    split_figure("presentation/fig_chronological_split.png")
    print("figures written")
