from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import plots_generator


def load_obj(name):
    with open(name + '.json', 'r') as f:
        return json.loads(f.read())


env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('result_template2.html')
manga_dict = load_obj('test_save')
link = 'https://myanimelist.net/manga/'
masterpieces = [{'image': dict_['image'],
                 'link': link + str(id_),
                 'name': dict_['name']}
                for id_, dict_ in manga_dict.items()
                if dict_['user_score'] == '10']
# plots_generator.draw_genres_pie(manga_dict, '')
masterpieces_dif_img = 'mastepieces_dif.png'
plots_generator.draw_avg_vs_u10_stem(manga_dict, masterpieces_dif_img)
big_dif_img = 'big_dif.png'
plots_generator.draw_biggest_dif_stem(manga_dict, big_dif_img)
small_dif_img = 'small_dif.png'
plots_generator.draw_biggest_dif_stem(manga_dict, small_dif_img, rev=True)
oldest_img = 'oldest.png'
plots_generator.draw_oldest_chart(manga_dict, oldest_img)
youngest_img = 'youngest.png'
plots_generator.draw_oldest_chart(manga_dict, youngest_img, rev=True)
rendered = template.render(user_name='MariuszB',
                           titles_num=20,
                           masterpiece_list=masterpieces,
                           masterpieces_dif_img=masterpieces_dif_img,
                           big_dif_img=big_dif_img,
                           small_dif_img=small_dif_img,
                           oldest_img=oldest_img,
                           youngest_img=youngest_img
                           )

with open('result.html', 'w') as f:
    f.write(rendered)
