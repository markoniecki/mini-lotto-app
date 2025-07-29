import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import get_cmap
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10

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

def generate_trend_plot_bokeh():
    df = pd.read_csv("mini_lotto.csv", header=None)
    df = df.iloc[:, -5:].astype(int)
    df_last20 = df.tail(20).reset_index(drop=True)

    x = list(range(1, 21))
    colors = Category10[5]

    p = figure(title="TREND – Bokeh",
               x_axis_label='Losowanie', y_axis_label='Liczba',
               width=900, height=500, tools="pan,wheel_zoom,reset,save")

    for idx, col in enumerate(df_last20.columns):
        y = df_last20[col]
        source = ColumnDataSource(data={
            'x': x,
            'y': y,
            'label': [str(val) for val in y],
        })
        p.line('x', 'y', source=source, line_width=2, color=colors[idx], legend_label=f'Liczba {idx+1}')
        p.circle('x', 'y', source=source, size=6, color=colors[idx], fill_color="white")

    hover = HoverTool(tooltips=[("Losowanie", "@x"), ("Liczba", "@label")])
    p.add_tools(hover)

    p.legend.title = "Pozycja w losowaniu"
    p.legend.click_policy = "hide"
    p.legend.location = "bottom_left"

    script, div = components(p)
    return script, div