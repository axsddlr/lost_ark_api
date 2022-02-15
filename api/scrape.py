import time

import requests
from bs4 import BeautifulSoup

from utils.utils import headers


class LostA:
    @staticmethod
    def news(tag):
        URL = f"https://www.playlostark.com/en-us/news?tag={tag}"

        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        status = r.status_code

        la_base = soup.find(id="ags-NewsLandingPage-renderBlogList")
        la_module = la_base.find_all(
            "div",
            {
                "class": "ags-SlotModule ags-SlotModule--blog ags-SlotModule--threePerRow"
            },
        )

        api = []
        for module in la_module:

            # url of articles
            url_parent = module.find("a")["href"]
            url = f"https://www.playlostark.com{url_parent}"

            # date of articles
            date = module.find(
                "span", {"class": "ags-SlotModule-contentContainer-date"}
            ).text.strip()

            # title of articles
            title = module.find(
                "span",
                {"class": "ags-SlotModule-contentContainer-heading"},
            ).text.strip()

            # description of articles
            try:
                description = module.find(
                    "div",
                    {
                        "class": "ags-SlotModule-contentContainer-text ags-SlotModule-contentContainer-text--blog ags-SlotModule-contentContainer-text"
                    },
                ).text.strip()

            except:
                description = "No description"

            # scrape each paragraph from url
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')

            article = soup.find("article", {"class": "ags-NewsArticlePage-contentWrapper-articlePane-article"})

            excerpt = []
            for text in article.find_all("p", {"class": "ags-rich-text-p"}):
                excerpt.append(text.select_one("span").text)

            thumbnail = []
            for thumb in article.find_all("div", {"class": "ags-MediaGalleryEmbed-container-gallery-box-thumbnail"}):
                thumbnail.append(
                    thumb.find("img", {"class": "ags-MediaGalleryEmbed-container-gallery-box-thumbnail-image"})["src"])

            api.append(
                {
                    "title": title,
                    "description": description.split("\n")[0],
                    "thumbnail": "https:" + thumbnail[0],
                    "url": url,
                    "publishDate": date,
                    "excerpt": excerpt[2],
                }
            )
        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def get_server_status(monitored_servers):
        """Checks whether a server is full or not. Default server to check is Una.
        A specific server can be set in the function argument."""
        True

        url = "https://www.playlostark.com/en-us/support/server-status"
        html = requests.get(url, headers=headers)
        try:
            soup = BeautifulSoup(html.content, "lxml")
            status = html.status_code

        except:
            print("An error occurred. Trying again in 5 seconds")
            time.sleep(5)

        server_list = soup.find_all('div',
                                    class_='ags-ServerStatus-content-responses-response-server')

        new_status = {}

        for server in server_list:
            server_name = server.find('div',
                                      class_='ags-ServerStatus-content-responses-response-server-name').text.strip()
            if server_name in monitored_servers:
                if server.find('div',
                               class_='ags-ServerStatus-content-responses-response-server-status '
                                      'ags-ServerStatus-content-responses-response-server-status--good'):
                    new_status[server_name] = '✅'
                if server.find('div',
                               class_='ags-ServerStatus-content-responses-response-server-status '
                                      'ags-ServerStatus-content-responses-response-server-status--busy'):
                    new_status[server_name] = '❌'
                if server.find('div',
                               class_='ags-ServerStatus-content-responses-response-server-status '
                                      'ags-ServerStatus-content-responses-response-server-status--maintenance'):
                    new_status[server_name] = '🛠️'
                if server.find('div',
                               class_='ags-ServerStatus-content-responses-response-server-status '
                                      'ags-ServerStatus-content-responses-response-server-status--full'):
                    new_status[server_name] = '⚠️'

        data = {"status": status, "data": new_status}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
        # return new_status

    @staticmethod
    def get_server_list_status():
        """gets all servers into one list"""
        True

        url = "https://www.playlostark.com/en-us/support/server-status"
        html = requests.get(url, headers=headers)
        try:
            soup = BeautifulSoup(html.content, "lxml")
            status = html.status_code

        except:
            print("An error occurred. Trying again in 5 seconds")
            time.sleep(5)

        server_list = soup.find_all('div',
                                    class_='ags-ServerStatus-content-responses-response-server')

        new_status = {}

        for server in server_list:
            server_name = server.find('div',
                                      class_='ags-ServerStatus-content-responses-response-server-name').text.strip()
            if server.find('div',
                           class_='ags-ServerStatus-content-responses-response-server-status '
                                  'ags-ServerStatus-content-responses-response-server-status--good'):
                new_status[server_name] = '✔️ Ok'
            if server.find('div',
                           class_='ags-ServerStatus-content-responses-response-server-status '
                                  'ags-ServerStatus-content-responses-response-server-status--busy'):
                new_status[server_name] = '❌ Busy'
            if server.find('div',
                           class_='ags-ServerStatus-content-responses-response-server-status '
                                  'ags-ServerStatus-content-responses-response-server-status--maintenance'):
                new_status[server_name] = '🛠️ Maintenance ️'
            if server.find('div',
                           class_='ags-ServerStatus-content-responses-response-server-status '
                                  'ags-ServerStatus-content-responses-response-server-status--full'):
                new_status[server_name] = '⚠️ Full'

        data = {"status": status, "data": new_status}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
        # return new_status


if __name__ == '__main__':
    print(LostA.news("updates"))
