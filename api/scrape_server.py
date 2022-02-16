import time

import requests
from bs4 import BeautifulSoup

from utils.utils import headers


class LostA_servers:

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
                    new_status[server_name] = '✅ Ok'
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
                new_status[server_name] = '✅ Ok'
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


if __name__ == '__main__':
    print(LostA_servers.news("updates"))
