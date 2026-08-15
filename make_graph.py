import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

HISTORY_FILE = "history_file.csv"
OUTPUT_IMAGE = "gaaners_progressie.png"

rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "axes.edgecolor": "#cccccc",
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linestyle": "--",
    "font.size": 11,
})


def load_history():
    df = pd.read_csv(HISTORY_FILE)
    df["Day"] = pd.to_datetime(df["Day"])
    df["Totaal gaanerspunten"] = pd.to_numeric(df["Totaal gaanerspunten"], errors="coerce")
    return df


def to_pivot(df):
    pivot = df.pivot_table(
        index="Day",
        columns="Naam",
        values="Totaal gaanerspunten",
        aggfunc="last",
    ).sort_index()
    return pivot.ffill()


def plot(pivot):
    fig, ax = plt.subplots(figsize=(14, 8))
    laatste_score = pivot.iloc[-1].sort_values(ascending=False)
    top_namen = laatste_score.index.tolist()
    kleuren = plt.cm.tab20.colors

    for i, naam in enumerate(top_namen):
        kleur = kleuren[i % len(kleuren)]
        ax.plot(
            pivot.index,
            pivot[naam],
            marker="o",
            linewidth=2.2,
            markersize=5,
            color=kleur,
            label=naam,
        )
        laatste_y = pivot[naam].iloc[-1]
        if pd.notna(laatste_y):
            ax.annotate(
                f"{naam} ({int(laatste_y)})",
                xy=(pivot.index[-1], laatste_y),
                xytext=(6, 0),
                textcoords="offset points",
                va="center",
                fontsize=8,
                color=kleur,
                fontweight="bold",
            )

    ax.set_title("Gaanerspunten — voortgang per persoon", fontsize=17, fontweight="bold", pad=14)
    ax.set_xlabel("Datum", fontsize=12)
    ax.set_ylabel("Totaal gaanerspunten", fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    fig.autofmt_xdate(rotation=45)
    ax.margins(x=0.02)
    fig.subplots_adjust(right=0.88)
    fig.savefig(OUTPUT_IMAGE, dpi=150, bbox_inches="tight")
    print(f"Grafiek opgeslagen: {OUTPUT_IMAGE}")


def main():
    if not os.path.exists(HISTORY_FILE):
        print(f"Geen history gevonden ({HISTORY_FILE}). Draai eerst snapshot.py.")
        return
    df = load_history()
    pivot = to_pivot(df)
    plot(pivot)


if __name__ == "__main__":
    main()
