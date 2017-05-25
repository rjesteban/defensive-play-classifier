"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
plt.rcdefaults()


def plot_bar_chart_comparison(lin_score, rbf_score, score):
    ind = np.arange(5)  # the x locations for the groups
    width = 0.45       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, lin_score, width, color='b')
    rects2 = ax.bar(ind + width, rbf_score, width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylim(top=1.1)
    ax.set_ylabel(score)
    ax.set_title('Kernel Score Comparison: ' + score)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('AI', 'AINV', 'AM', 'AMNV', 'RFE'))

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%.2f' % float(height * 100),
                    ha='center', va='bottom')

    ax.legend((rects1[0], rects2[0]), ('Linear Kernel', 'RBF Kernel'), loc=4)
    autolabel(rects1)
    autolabel(rects2)

    plt.show()


def plot_bar_chart(title, x_labels, scores):
    score_series = pd.Series.from_array(scores)
    # now to plot the figure...
    plt.figure(figsize=(6, 4))
    ax = score_series.plot(kind='bar', alpha=0.5, color='k')
    plt.title(title + ' scores')
    ax.set_xlabel("Experiment No.")
    plt.ylabel(title)
    ax.set_xticklabels(x_labels, rotation='horizontal')
    ax.set_ylim(top=1.1)
    matplotlib.rcParams.update({'font.size': 14})
    rects = ax.patches
    # Now make some labels
    labels = ['%.2f' % (score * 100) for score in scores]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')
    plt.show()
