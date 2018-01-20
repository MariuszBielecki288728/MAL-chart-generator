import DataLoader
import requests
from bs4 import BeautifulSoup
import progressbar
import time, random


user = 'chart_gen_tester'
passwd = ''

user_info, manga_dict = DataLoader.gather_mangas_info(user, passwd, 'manga')
print(user_info.prettify())
print()
print(manga_dict)
