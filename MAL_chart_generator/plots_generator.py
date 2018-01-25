import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def draw_genres_pie(mangas_dict, file_path):
    plt.ioff()
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

    fig = plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=False)
    fig.savefig(file_path)
    plt.close(fig)


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

    def adjust(name):
        triggered = False
        while len(name) > 18:
            triggered = True
            name = name.rsplit(' ', 1)[0]
        return name + ('...' if triggered else '')

    items = ((id_, dict_)  # throw away all titles without valid dates
             for id_, dict_ in mangas_dict.items()
             if dict_['start_date'] != '0000-00-00')
    sorted_dates = sorted(items, key=sort_key)[:10]

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
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
