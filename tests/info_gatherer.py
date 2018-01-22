
import os
import sys
import pickle
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
from MAL_chart_generator import DataLoader
from MAL_chart_generator import plots_generator


sys.setrecursionlimit(100000)


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


user = 'MariuszB'
passwd = 'tCa7osGcXkkQTUCB'

user_info, manga_dict = DataLoader.gather_mangas_info(user, passwd, 'manga')
# plots_generator.draw_genres_pie(manga_dict)
save_obj(manga_dict, 'test_cache')
print(load_obj('test_cache'))
