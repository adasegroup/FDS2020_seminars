import argparse

import matplotlib.pyplot as plt


def save_plot(df, name, color):
    plt.barh(df.index, df.counts['counts'], color=color)
    plt.title("Most used words in {} 'New in' SS2020 Women collection".format(name))
    plt.savefig("SS2020_{}_word_frequency.jpg".format(name))


if __name__ == "__main__":
    pass