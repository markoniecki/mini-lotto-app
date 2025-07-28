import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import os


def create_heatmap(output_path='static/chart_data/mapa.png'):
    df = pd.read_csv('mini_lotto.csv')
    df.columns = ['losowanie_nr', 'data', 'liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']
    df['data'] = pd.to_datetime(df['data'], format='%d.%m.%Y')

    ostatnie_50 = df.sort_values('data', ascending=False).head(50)
    siatka = pd.DataFrame(0, index=ostatnie_50['data'].dt.strftime('%d.%m.%Y'),
                          columns=[f"{i:02}" for i in range(1, 43)])

    for _, row in ostatnie_50.iterrows():
        for liczba in row[['liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']]:
            siatka.at[row['data'].strftime('%d.%m.%Y'), f"{liczba:02}"] = 1

    siatka = siatka.iloc[::-1]
    num_rows, num_cols = siatka.shape
    numerowane_komorki = pd.DataFrame(
        [[j + 1 for j in range(num_cols)] for _ in range(num_rows)],
        index=siatka.index,
        columns=siatka.columns
    )

    custom_cmap = ListedColormap(["#e0e0e0", "darkturquoise"])

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        siatka,
        cmap=custom_cmap,
        linewidths=0.5,
        linecolor='gray',
        cbar=False,
        square=True,
        annot=numerowane_komorki,
        fmt='d',
        annot_kws={"size": 5}
    )

    plt.yticks(
        ticks=range(0, len(siatka.index), 2),
        labels=siatka.index[::2],
        rotation=0,
        fontsize=6
    )

    plt.title('Mapa losowań Mini Lotto – cyan dla wylosowanych, szary dla pozostałych', fontsize=8)
    plt.xlabel('Liczby (1–42)', fontsize=4)
    plt.ylabel('Data losowania', fontsize=7)
    plt.xticks(rotation=0, fontsize=6)
    plt.tick_params(left=False, bottom=False)
    plt.gca().spines[:].set_visible(False)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()