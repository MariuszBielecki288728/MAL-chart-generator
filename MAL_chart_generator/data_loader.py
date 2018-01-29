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
        else:
            time.sleep(retry_interval)

    raise response.raise_for_status()
    # raise Exception("Unhandled response: " + response.status_code)


def create_manga_dict(item):
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

    dict_ = {'name': name,
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

    return (db_id, dict_)


def create_anime_dict(item):
    db_id = item.series_animedb_id.string
    name = item.series_title.string

    start_date = item.series_start.string
    end_date = item.series_end.string
    image = item.series_image.string

    user_start_date = item.my_start_date.string
    user_end_date = item.my_finish_date.string
    user_score = item.my_score.string

    url = 'https://myanimelist.net/includes/ajax.inc.php'
    params = {'t': '64',
              'id': db_id}
    title_data_soup = request_retryer(url, params=params)
    spans = title_data_soup.find_all('span')

    genres_str = spans[0].next_sibling.string
    genres_list = genres_str.strip().split(', ')

    avg_score = spans[4].next_sibling.string.strip()
    ranked = spans[5].next_sibling.string.strip()
    popularity = spans[6].next_sibling.string.strip()

    dict_ = {'name': name,
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

    return (db_id, dict_)


def gather_titles_info(user_name, user_passwd='', **kwargs):
    """
        Gathers information about user and mangas (from list) to (soup, dict)
        shows progress bar in console

        Arguments:
            user_name - username used to log in myanimelist.net
            user_passwd - password used to log in myanimelist.net

        Optional arguments:
            list_type - type of list (manga or anime)
            custom_user    - user whose list will be downloaded

    """

    user = kwargs.get('custom_user', user_name)
    list_type = kwargs.get('list_type', 'manga')

    if list_type not in ['manga', 'anime']:
        raise ValueError("list_type must be 'anime' or 'manga'")

    url = 'http://myanimelist.net/malappinfo.php'
    params = {'u': user,
              'status': 'all',
              'type': list_type}

    list_soup = request_retryer(url, params=params)
    user_info_soup = list_soup.myinfo
    entries = list_soup.find_all(list_type)
    # 1/watching, 2/completed, 3/onhold, 4/dropped, 6/plantowatch

    id_dict = dict()

    titles_num = len(entries)
    bar = progressbar.ProgressBar(max_value=titles_num)

    if list_type == 'manga':
        create_dict = create_manga_dict
    else:
        create_dict = create_anime_dict

    for count, item in enumerate(entries):
        bar.update(count)

        # only watching and completed
        if item.my_status.string not in ['1', '2']:
            continue
        db_id, dict_ = create_dict(item)
        id_dict[db_id] = dict_
        time.sleep(random.randint(4, 6))

    bar.update(titles_num)
    bar.finish()

    return (user_info_soup, id_dict)
