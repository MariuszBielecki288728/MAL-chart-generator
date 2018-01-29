import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from datetime import datetime
from dateutil.parser import parse


def adjust(name):
    triggered = False
    while len(name) > 21:
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
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()


def draw_oldest_chart(manga_dict, file_path, rev=False):

    plt.ioff()

    def strip_date(date):
        if date[-5:] == '00-00':
            return date[:-6] + '-01-01'
        elif date[-2:] == '00':
            return date[:-3] + '-01'
        else:
            return date

    def sort_key(x):
        start_date = parse(strip_date(x[1]['start_date']))
        if x[1]['end_date'] == '0000-00-00':
            end_date = datetime.now()
        else:
            end_date = parse(strip_date(x[1]['end_date']))
        return abs(end_date - start_date)

    items = ((id_, dict_)  # throw away all titles without valid start dates
             for id_, dict_ in manga_dict.items()
             if dict_['start_date'] != '0000-00-00')

    sorted_dates = sorted(items, key=sort_key, reverse=(not rev))[:10]

    plt.rcdefaults()

    labels = [adjust(dict_['name'])
              for id_, dict_ in sorted_dates]

    today = datetime.now()

    start_dates = [parse(strip_date(dict_["start_date"]))
                   for id_, dict_ in sorted_dates]
    end_dates = [(parse(strip_date(dict_["end_date"]))
                  if dict_["end_date"] != '0000-00-00'
                  else today.date())
                 for id_, dict_ in sorted_dates]

    my_range = range(1, len(labels) + 1)

    plt.hlines(y=my_range,
               xmin=start_dates,
               xmax=end_dates,
               color='silver',
               alpha=0.4)

    plt.scatter(start_dates,
                my_range,
                color='deepskyblue',
                alpha=1,
                label='Start date')

    plt.scatter(end_dates,
                my_range,
                color='red',
                alpha=0.4,
                label='Finish date')
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    if rev:
        interval = 2
    else:
        interval = 5
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(interval))
    plt.legend()

    plt.yticks(my_range, labels)
    # plt.title("title", loc='left')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()


def draw_dif_stem(avg_score, user_score, labels, file_path, **kwargs):
    plt.ioff()

    plot_title = kwargs.get('plot_title',
                            'Comparison of the avarage score and your score')

    df = pd.DataFrame({'group': labels,
                       'avg_score': avg_score,
                       'user_score': user_score})

    ordered_df = df
    my_range = range(1, len(df.index) + 1)

    plt.hlines(y=my_range,
               xmin=ordered_df['avg_score'],
               xmax=ordered_df['user_score'],
               color='silver',
               alpha=0.4)
    plt.scatter(ordered_df['avg_score'],
                my_range,
                color='deepskyblue',
                alpha=1,
                label='Avarage score')

    plt.scatter(ordered_df['user_score'],
                my_range,
                color='red',
                alpha=0.4,
                label='Your score')
    plt.gca().invert_yaxis()
    plt.legend()

    # Add title and axis names
    plt.yticks(my_range, ordered_df['group'])
    plt.title(plot_title, loc='left')
    plt.xlabel('Score')
    plt.tight_layout()

    plt.savefig(file_path, bbox_inches='tight')
    plt.close()


def draw_avg_vs_u10_stem(mangas_dict, file_path):
    masterpieces = [{'name': dict_['name'],
                     'avg_score': dict_['avg_score']}
                    for id_, dict_ in mangas_dict.items()
                    if dict_['user_score'] == '10']

    labels = [adjust(dict_['name']) for dict_ in masterpieces]
    avg_score = [float(dict_['avg_score']) for dict_ in masterpieces]
    user_score = [10.0 for i in range(len(avg_score))]

    draw_dif_stem(avg_score,
                  user_score,
                  labels,
                  file_path)


def draw_biggest_dif_stem(mangas_dict, file_path, rev=False):

    items = (dict_  # throw away all titles without valid scores
             for id_, dict_ in mangas_dict.items()
             if (dict_['user_score'] != '0'
                 and dict_['avg_score'] != '0'))

    def sort_key(x):
        return abs(float(x['avg_score']) - float(x['user_score']))

    sorted_items = sorted(items, key=sort_key, reverse=(not rev))[:15]

    labels = [adjust(dict_['name']) for dict_ in sorted_items]
    avg_score = [float(dict_['avg_score']) for dict_ in sorted_items]
    user_score = [float(dict_['user_score']) for dict_ in sorted_items]

    draw_dif_stem(avg_score,
                  user_score,
                  labels,
                  file_path)
