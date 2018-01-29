# libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def stem1():
    # Create a dataframe
    avg_score = [8.8, 7.5]
    user_score = [10, 10]
    df = pd.DataFrame({'group': ['anime', 'anime'],
                       'avg_score': avg_score,
                       'user_score': user_score})

    # Reorder it following the values of the first value:
    # ordered_df = df.sort_values(by='avg_score')
    ordered_df = df
    my_range = range(1, len(df.index) + 1)

    # The vertical plot is made using the hline function
    # I load the seaborn library only to benefit the nice looking feature
    import seaborn as sns
    plt.hlines(y=my_range,
               xmin=ordered_df['avg_score'],
               xmax=ordered_df['user_score'],
               color='grey',
               alpha=0.4)
    plt.scatter(ordered_df['avg_score'],
                my_range,
                color='skyblue',
                alpha=1,
                label='Avarage score')

    plt.scatter(ordered_df['user_score'],
                my_range,
                color='green',
                alpha=0.4,
                label='Your score')
    plt.legend()

    # Add title and axis names
    plt.yticks(my_range, ordered_df['group'])
    plt.title("Comparison of the avarage score and your score", loc='left')
    plt.xlabel('Score')
    # plt.ylabel('Group')

    plt.show()


def stem2():
    markerline, stemlines, baseline = plt.stem([0, 1, 2, 3],
                                               [1, 2, 1, 2], '-.', bottom=10)
    plt.setp(baseline, 'color', 'r', 'linewidth', 2)

    plt.show()


stem1()
