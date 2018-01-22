import requests
from bs4 import BeautifulSoup
import progressbar
import time
import random


def request_retryer(url, user_name='', user_passwd='', **kwargs):
    """
        sends request and (if response is wrong) trying again few more times

        Arguments:
            url - link to send request
            user_name - username used to log in myanimelist.net
            user_passwd - password used to log in myanimelist.net

        Optional arguments:
            retries_number - number of retries to get list from MAL server
            retry_interval - time beetwen consecutive retries
            retry_timeout  - timeout of single retry
            params - params for GET request

    """

    retries = kwargs.get('retries_number', 5)
    retry_interval = kwargs.get('retry_interval', 5)
    timeout = kwargs.get('retry_timeout', 10)
    params = kwargs.get('params', None)

    for retry in range(1, retries):
        if user_name == '':
            response = requests.get(
                url,
                params=params,
                timeout=timeout)
        else:
            response = requests.get(
                url,
                params=params,
                auth=(user_name, user_passwd),
                timeout=timeout)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        elif response.status_code == 204:
            raise Exception("Couldn't find manga: " + url)
        else:
            time.sleep(retry_interval)

    raise response.raise_for_status()
    # raise Exception("Unhandled response: " + response.status_code)


def gather_mangas_info(user_name, user_passwd, list_type, **kwargs):
    """
        Gathers information about mangas (from list) to (soup, dict)
        shows progress bar in console

        Arguments:
            user_name - username used to log in myanimelist.net
            user_passwd - password used to log in myanimelist.net
            list_type - type of list (manga or anime)

        Optional arguments:
            retries_number - number of retries to get list from MAL server
            retry_interval - time beetwen consecutive retries
            retry_timeout  - timeout of single retry
            custom_user    - user whose list will be downloaded

    """

    user = kwargs.get('custom_user', user_name)

    url = 'http://myanimelist.net/malappinfo.php'
    params = {'u': user,
              'status': 'all',
              'type': list_type}

    manga_list_soup = request_retryer(url, params=params)
    user_info_soup = manga_list_soup.myinfo
    mangas = manga_list_soup.find_all('manga')

    manga_dict = dict()

    mangas_num = len(mangas)
    bar = progressbar.ProgressBar(max_value=mangas_num)

    for count, item in enumerate(mangas):

        db_id = item.series_mangadb_id.string
        name = item.series_title.string

        start_date = item.series_start.string
        end_date = item.series_end.string
        image = item.series_image.string

        user_start_date = item.my_start_date.string
        user_end_date = item.my_finish_date.string
        user_score = item.my_score.string

        url = 'https://myanimelist.net/includes/ajax.inc.php'
        params = {'t': '65',
                  'id': db_id}
        title_data_soup = request_retryer(url, params=params)

        divs = title_data_soup.find_all('div')

        genres_str = divs[2].span.next_sibling.string
        genres_list = genres_str.strip().split(', ')

        avg_score = divs[5].span.next_sibling.string.strip()
        ranked = divs[6].span.next_sibling.string.strip()
        popularity = divs[7].span.next_sibling.string.strip()

        """url = 'https://myanimelist.net/api/manga/search.xml'
        params = {'q': name}
        title_ext_data_soup = request_retryer(url, params, user, passwd)

        entry = title_ext_data_soup.manga.entry
        start_date = title_ext_data_soup.start_date.string
        end_date = title_ext_data_soup.end_date.string
        image = title_ext_data_soup.image.string"""

        manga_dict[db_id] = {'name': name,
                             'genres': genres_list,
                             'avg_score': avg_score,
                             'ranked': ranked[1:],
                             'popularity': popularity[1:],
                             'start_date': start_date,
                             'end_date': end_date,
                             'image': image,

                             'user_start_date': user_start_date,
                             'user_end_date': user_end_date,
                             'user_score': user_score}
        bar.update(count)
        time.sleep(random.randint(4, 6))

    bar.update(mangas_num)
    bar.finish()

    return (user_info_soup, manga_dict)
