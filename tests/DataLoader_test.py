import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MAL_chart_generator import DataLoader

user_name = 'MariuszB'
user_passwd = ''

soup = DataLoader.load_list_soup(user_name, user_passwd, 'manga')

for item in soup.findAll('manga'):
    print(item.series_title)


soup = DataLoader.load_list_soup(user_name, user_passwd, 'anime')

for item in soup.findAll('anime'):
    print(item.series_title)
