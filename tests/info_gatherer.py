
import os
import sys
import json
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
from MAL_chart_generator import data_loader
from MAL_chart_generator import plots_generator


sys.setrecursionlimit(1000000)


def save_obj(obj, name):
    with open(name + '.json', 'w') as f:
        f.write(json.dumps(obj))


def load_obj(name):
    with open(name + '.json', 'r') as f:
        return json.loads(f.read())


user = 'MariuszB'
passwd = ''

# user_info, manga_dict = DataLoader.gather_mangas_info(user, passwd, 'manga')

# save_obj(manga_dict, 'test_cache')
manga_dict = load_obj('test_save')
plots_generator.draw_oldest(manga_dict, '', rev=True)
# plots_generator.draw_biggest_dif_stem(manga_dict, 'big_dif.png')
# plots_generator.draw_oldest_chart(manga_dict, '')
