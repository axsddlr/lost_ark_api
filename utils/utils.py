import httpx
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


def get_soup(url):
    re = httpx.get(url, headers=headers)
    soup = BeautifulSoup(re.content, 'lxml')
    if re.status_code == 404:
        return None
    else:
        return soup


def get_status(url):
    re = httpx.get(url, headers=headers)
    if re.status_code != 200:
        raise Exception("API response: {}".format(re.status_code))
    else:
        return re.status_code
