from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import sys
from multiprocessing import Process
import plots_generator
import data_loader


def render_page(titles_dict, user_name, list_type):
    link = 'https://myanimelist.net/' + list_type + '/'
    masterpieces = [{'image': dict_['image'],
                     'link': link + str(id_),
                     'name': dict_['name'].encode('utf-8')}
                    for id_, dict_ in titles_dict.items()
                    if dict_['user_score'] == '10']
    masterpieces_dif_img = 'mastepieces_dif.png'
    big_dif_img = 'big_dif.png'
    small_dif_img = 'small_dif.png'
    oldest_img = 'oldest.png'
    youngest_img = 'youngest.png'
    genres_pie_img = 'genres_pie.png'
    processes = []

    processes.append(Process(target=plots_generator.draw_avg_vs_u10_stem,
                             args=(titles_dict, masterpieces_dif_img)))
    processes.append(Process(target=plots_generator.draw_biggest_dif_stem,
                             args=(titles_dict, big_dif_img)))
    processes.append(Process(target=plots_generator.draw_biggest_dif_stem,
                             args=(titles_dict, small_dif_img),
                             kwargs={'rev': True}))
    processes.append(Process(target=plots_generator.draw_oldest_chart,
                             args=(titles_dict, oldest_img)))
    processes.append(Process(target=plots_generator.draw_oldest_chart,
                             args=(titles_dict, youngest_img),
                             kwargs={'rev': True}))
    processes.append(Process(target=plots_generator.draw_genres_pie,
                             args=(titles_dict, genres_pie_img)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    rendered = template.render(list_type=list_type,
                               user_name=user_name,
                               titles_num=len(titles_dict.items()),
                               masterpiece_list=masterpieces,
                               masterpieces_dif_img=masterpieces_dif_img,
                               big_dif_img=big_dif_img,
                               small_dif_img=small_dif_img,
                               oldest_img=oldest_img,
                               youngest_img=youngest_img,
                               genres_pie_img=genres_pie_img
                               )
    return rendered


"""def save_obj(obj, name):
    with open(name + '.json', 'w') as f:
        f.write(json.dumps(obj))


def load_obj(name):
    with open(name + '.json', 'r') as f:
        return json.loads(f.read())"""


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('result_template.html')
    if len(sys.argv) == 1:
        print("Welcome to MAL chart generator")
        user_name = input("Please, enter your myanimelist.net username")
        os.system('cls')
    else:
        user_name = sys.argv[1]

    manga_dict = data_loader.gather_titles_info(user_name)[1]
    print("Generating manga.html done!")
    # manga_dict = load_obj('test_save')
    result = render_page(manga_dict, user_name, 'manga')
    os.system('cls')

    with open('manga.html', 'w') as f:
        f.write(result)

    manga_dict = data_loader.gather_titles_info(user_name,
                                                list_type='anime')[1]
    print("Generating anime.html done!")
    result = render_page(manga_dict, user_name, 'anime')
    with open('anime.html', 'w') as f:
        f.write(result)
