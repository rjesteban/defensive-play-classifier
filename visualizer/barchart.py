"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt


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
