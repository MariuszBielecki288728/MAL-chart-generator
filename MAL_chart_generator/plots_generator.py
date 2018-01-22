import matplotlib.pyplot as plt


def draw_genres_pie(mangas_dict):
    appear_freq_dict = dict()
    count = 0
    for title_id, info_dict in mangas_dict.items():
        for genre in info_dict['genres']:
            try:
                appear_freq_dict[genre] = appear_freq_dict[genre] + 1
            except KeyError:
                appear_freq_dict[genre] = 1
            count += 1
    sorted_genres = sorted(appear_freq_dict.items(), key=lambda x: x[1])[:5]

    labels = [item[0] for item in sorted_genres]
    labels.append('Other')
    labels = tuple(labels)
    print(sorted_genres)
    print(count)
    fracs = [round((item[1] / count) * 100, 2) for item in sorted_genres]
    fracs.append(100 - sum(fracs))
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.show()
