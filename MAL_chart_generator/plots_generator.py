import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def adjust(name):
    triggered = False
    while len(name) > 18:
        triggered = True
        name = name.rsplit(' ', 1)[0]
    return name + ('...' if triggered else '')


def draw_genres_pie(mangas_dict, file_path):
    plt.ioff()
    sns.set_style("dark")
    appear_freq_dict = dict()
    count = 0
    for title_id, info_dict in mangas_dict.items():
        for genre in info_dict['genres']:
            try:
                appear_freq_dict[genre] = appear_freq_dict[genre] + 1
            except KeyError:
                appear_freq_dict[genre] = 1
            count += 1
    sorted_genres = sorted(appear_freq_dict.items(),
                           key=lambda x: x[1],
                           reverse=True)[:9]

    labels = [item[0] for item in sorted_genres]
    labels.append('Other')
    labels = tuple(labels)

    fracs = [round((item[1] / count) * 100, 2) for item in sorted_genres]
    fracs.append(100 - sum(fracs))
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(fracs,
            labels=labels,
            wedgeprops={'linewidth': 7, 'edgecolor': 'white'})
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.show()
    # fig.savefig(file_path)
    # plt.close(fig)


def draw_oldest_chart(mangas_dict, file_path):

    def strip_date(date):
        if date[-5:] == '00-00':
            return date[:-6]
        elif date[-2:] == '00':
            return date[:-3]
        else:
            return date

    def sort_key(x):
        return parse(strip_date(x[1]['start_date']))

    items = ((id_, dict_)  # throw away all titles without valid dates
             for id_, dict_ in mangas_dict.items()
             if dict_['start_date'] != '0000-00-00')
    sorted_dates = sorted(items, key=sort_key)[:10]

    plt.rcdefaults()
    sns.set_style("dark")
    fig, ax = plt.subplots()

    """ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)"""

    titles = tuple(adjust(dict_['name'])
                   for id_, dict_ in sorted_dates)
    y_pos = range(len(titles))

    today = datetime.now()
    performance = [relativedelta(today,
                                 parse(strip_date(dict_['start_date']))).years
                   for id_, dict_ in sorted_dates]

    ax.barh(y_pos, performance,
            color='blue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(titles)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Years')
    ax.set_title('The oldest titles in your list')
    plt.tight_layout()
    plt.show()
    # plt.close(fig)


def draw_dif_stem(avg_score, user_score, labels, file_path, **kwargs):

    plot_title = kwargs.get('plot_title',
                            'Comparison of the avarage score and your score')

    df = pd.DataFrame({'group': labels,
                       'avg_score': avg_score,
                       'user_score': user_score})

    # Reorder it following the values of the first value:
    ordered_df = df.sort_values(by='user_score')
    #ordered_df = df
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
                color='purple',
                alpha=1,
                label='Avarage score')

    plt.scatter(ordered_df['user_score'],
                my_range,
                color='blue',
                alpha=0.4,
                label='Your score')
    plt.legend()

    # Add title and axis names
    plt.yticks(my_range, ordered_df['group'])
    plt.title(plot_title, loc='left')
    plt.xlabel('Score')
    plt.tight_layout()
    # plt.ylabel('Group')

    plt.show()


def draw_avg_vs_u10_stem(manga_dict, file_path):
    masterpieces = [{'name': dict_['name'],
                     'avg_score': dict_['avg_score']}
                    for id_, dict_ in manga_dict.items()
                    if dict_['user_score'] == '10']

    labels = [adjust(dict_['name']) for dict_ in masterpieces]
    avg_score = [float(dict_['avg_score']) for dict_ in masterpieces]
    user_score = [10.0 for i in range(len(avg_score))]
    draw_dif_stem(avg_score,
                  user_score,
                  labels,
                  '')
