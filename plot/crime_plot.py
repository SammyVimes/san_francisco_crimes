# -*- coding: utf-8 -*-
import operator
from string import capwords

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from data.input_reader import load
from translator.yandex import translate

__author__ = 'Semyon'


def plot_gen(is_demo):
    # Plotting Options
    sns.set_style("whitegrid")
    sns.despine()


    def rname(old):
        return translate(old, "en", "ru")


    def plot_bar(df, title, filename):
        p = (
            'Set2', 'Paired', 'colorblind', 'husl',
            'Set1', 'coolwarm', 'RdYlGn', 'spectral'
        )
        df = df.rename(rname)
        bar = df.plot(kind='barh',
                      title=title,
                      fontsize=8,
                      figsize=(12, 8),
                      stacked=False,
                      width=1,
                      color=sns.color_palette(np.random.choice(p), len(df)),
                      )

        bar.figure.savefig(filename)

        plt.show()


    def plot_top_crimes(df, column, title, fname, items=0):
        df.columns = df.columns.map(operator.methodcaller('lower'))
        by_col = df.groupby(column)
        col_freq = by_col.size()
        col_freq.index = col_freq.index.map(capwords)

        col_freq.sort(ascending=True, inplace=True)
        plot_bar(col_freq[slice(-1, - items, -1)], title, fname)


    df = load("../data/train.csv.zip" if not is_demo else "data/train.csv.zip")

    plot_top_crimes(df, 'category', 'Количество преступлений (по типу)', 'category.png')
    plot_top_crimes(df, 'resolution', 'Результаты расследования', 'resolution.png')
    plot_top_crimes(df, 'pddistrict', 'Активность полиции', 'police.png')
    plot_top_crimes(df, 'dayofweek', 'Преступления по дням недели', 'weekly.png')
    plot_top_crimes(df, 'address', 'Адреса преступлений (топ 20)', 'location.png', items=20)
    plot_top_crimes(df, 'descript', 'Конкретные преступления (топ 20)', 'descript.png', items=20)

if __name__ == "__main__":
    plot_gen(False)