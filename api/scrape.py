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
            thumbnail = module.find("img")["src"]
            thumbnail_url = f"https:{thumbnail}"

            # url of articles
            url_parent = module.find("a")["href"]
            url = f"https://www.playlostark.com/{url_parent}"

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
            api.append(
                {
                    "title": title,
                    "description": description.split("\n")[0],
                    "thumbnail": thumbnail_url,
                    "url": url,
                    "publishDate": date,
                    # "excerpt": remove_tags(summary_full),
                }
            )
        # #
        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    print(LostA.news())
