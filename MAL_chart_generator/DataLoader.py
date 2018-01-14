import requests
import time
from bs4 import BeautifulSoup

def load_list_soup(user_name, user_passwd, list_type, **kwargs):
    """
        Creates soup of anime or manga xml list got from
        http://myanimelist.net/malappinfo.php

        Arguments:
            user_name - username used to log in myanimelist.net
            user_passwd - password used to log in myanimelist.net
            list_type - type of list (manga or anime)

        Optional arguments:
            retries_number - number of retries to get list from MAL server
            retry_interval - time beetwen consecutive retries
            retry_timeout  - timeout of single retry

    """

    retries =        kwargs.get('retries_number', 5)
    retry_interval = kwargs.get('retry_interval', 3)
    timeout  =       kwargs.get('retry_timeout', 10)


    url = ('http://myanimelist.net/malappinfo.php'
           + '?u='    + user_name
           + '&status=all'
           + '&type=' + list_type)

    for time in range(1, retries):
        try:
            response = requests.get(url,
                                    auth=(user_name, user_passwd),
                                    timeout=timeout)
        except handled_exceptions:
            time.sleep(retry_interval)
        else:
            return BeautifulSoup(response.content, "html.parser")
    else:
        raise response.raise_for_status()
