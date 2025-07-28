import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import get_cmap

def generate_trend_plot():
    # Wczytaj dane
    df = pd.read_csv("mini_lotto.csv", header=None)
    df = df.iloc[:, -5:].astype(int)
    df_last20 = df.tail(20).reset_index(drop=True)

    x = list(range(1, 21))
    colors = get_cmap('tab10').colors

    # Tworzenie wykresu
    plt.figure(figsize=(10, 6))
    for i in range(5):
        plt.plot(x, df_last20.iloc[:, i], marker='o', label=f'Liczba {i + 1}', color=colors[i])

    plt.title("TREND – Ostatnie 20 losowań")
    plt.xlabel("Losowanie")
    plt.ylabel("Liczba")
    plt.xticks(x)
    plt.yticks(range(1, 43, 1))
    plt.legend(title="Pozycja w losowaniu")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/chart_data/wykres.png")
    plt.close()
