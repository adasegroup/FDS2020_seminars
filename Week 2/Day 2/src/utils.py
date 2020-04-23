import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def result2dataframe(result):
    words = list(result.keys())
    counts = list(result.values())

    # TURNING THE DICTIONARY INTO A DATAFRAME, SORTING & SELECTING FOR RELEVANCE
    df = pd.DataFrame.from_dict({
        "words": words,
        "counts": counts,
    })

    df2 = df.set_index("words")
    df_sorted = df2.sort_values("counts", ascending=True)
    return df_sorted


def plot_horizontal_bar(x, count, title, save=None,  color="#C19A6B"):
    # PLOTTING
    plt.barh(x, count, color=color)
    plt.title(title)
    if save:
        plt.savefig(save)
    plt.close()
