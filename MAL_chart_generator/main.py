from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def load_obj(name):
    with open(name + '.json', 'r') as f:
        return json.loads(f.read())


env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('result_template.html')
manga_dict = load_obj('test_save')
link = 'https://myanimelist.net/manga/'
masterpieces = [{'image': dict_['image'],
                 'link': link + str(id_),
                 'name': dict_['name']}
                for id_, dict_ in manga_dict.items()
                if dict_['user_score'] == '10']

rendered = template.render(masterpiece_list=masterpieces)

with open('result.html', 'w') as f:
    f.write(rendered)
