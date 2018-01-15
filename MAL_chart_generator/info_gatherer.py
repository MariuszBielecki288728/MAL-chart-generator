import DataLoader
import matplotlib
import requests
from bs4 import BeautifulSoup
import progressbar
import time, random

user = 'chart_gen_tester'
passwd = ''

manga_list_soup = DataLoader.load_list_soup(user, passwd, 'manga')
mangas = manga_list_soup.find_all('manga')
mangas_num = len(mangas)
manga_dict = dict()

bar = progressbar.ProgressBar(max_value=mangas_num)
for count, item in enumerate(mangas):

    db_id = item.series_mangadb_id.string
    url = 'https://myanimelist.net/includes/ajax.inc.php?t=65&id=' + db_id

    for retry in range(1, 5):
        try:
            response = requests.get(
                url,
                timeout=10)
        except requests.HTTPError: #TODO czy aby na pewno raisuje error?
            time.sleep(5)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            break
    else:
        raise response.raise_for_status()

    divs = soup.find_all('div')


    name =  divs[0].string

    genres_str =  divs[2].span.next_sibling.string
    genres_list = genres_str.strip().split(', ')

    avg_score =   divs[5].span.next_sibling.string.strip()
    ranked =      divs[6].span.next_sibling.string.strip()
    popularity =  divs[7].span.next_sibling.string.strip()

    manga_dict[db_id]= {
                            'name': name,
                            'genres': genres_list,
                            'avg_score': avg_score,
                            'ranked': ranked[1:],
                            'popularity': popularity[1:]
                        }
    bar.update(count)
    time.sleep(random.randint(4, 5))
bar.update(mangas_num)
bar.finish()
print(manga_dict)
