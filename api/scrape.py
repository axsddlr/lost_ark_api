import re

import httpx

from utils.utils import headers, get_soup, get_status


def get_la_forums():
    url = (
        "https://forums.playlostark.com/c/official-news/official-news/53/l/latest.json?ascending=false"
    )
    response = httpx.get(url, headers=headers)
    return response.json()


class LostA:
    @staticmethod
    def news(tag):
        URL = f"https://www.playlostark.com/en-us/news?tag={tag}"
        status = get_status(URL)
        response = get_soup(URL)

        la_base = response.find(id="ags-NewsLandingPage-renderBlogList")
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
            r = get_soup(url)

            article = r.find("article", {"class": "ags-NewsArticlePage-contentWrapper-articlePane-article"})

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

        return data

    @staticmethod
    def la_playercount():
        url = (
            "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=1599340"
        )
        response = httpx.get(url, headers=headers)
        obj = response.json()
        status = response.status_code

        player_count = obj["response"]["player_count"]
        api = {
            "player_count": player_count
        }
        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def la_forums_v1():
        apiResponse = get_la_forums()
        base = apiResponse["topic_list"]["topics"]

        api = []
        for each in base:
            post_id = each["id"]

            URL = f"https://forums.playlostark.com/t/{post_id}.json"
            response = httpx.get(URL)
            responseJSON = response.json()
            status = response.status_code

            title = responseJSON["title"]
            created_at = responseJSON["created_at"]
            # post contents
            post_content = responseJSON["post_stream"]["posts"][0]["cooked"]
            # remove html tags from post content json string
            post_content = re.sub(r"<.*?>", "", post_content)
            # remove new lines from post content
            post_content = re.sub(r"\n", " ", post_content)
            # remove extra spaces from post content
            post_content = re.sub(r"\s{2,}", " ", post_content)

            # check if post is pinned
            pinned = responseJSON["pinned"]
            staff = responseJSON["post_stream"]["posts"][0]["staff"]

            # author of post
            author = responseJSON["post_stream"]["posts"][0]["username"]

            # url to post
            slug = responseJSON["slug"]
            url = f"https://forums.playlostark.com/t/{slug}/{post_id}"

            if not pinned and staff:
                # if title.__contains__("Downtime"):
                api.append(
                    {
                        "title": title,
                        "post_body": post_content,
                        "created_at": created_at,
                        "url": url,
                        "author": author,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def la_forums_v2(category):
        apiResponse = get_la_forums()
        base = apiResponse["topic_list"]["topics"]

        api = []
        for each in base:
            post_id = each["id"]

            URL = f"https://forums.playlostark.com/t/{post_id}.json"
            response = httpx.get(URL)
            responseJSON = response.json()
            status = response.status_code

            title = responseJSON["title"]
            created_at = responseJSON["created_at"]
            # post contents
            post_content = responseJSON["post_stream"]["posts"][0]["cooked"]
            # remove html tags from post content json string
            post_content = re.sub(r"<.*?>", "", post_content)
            # remove new lines from post content
            post_content = re.sub(r"\n", " ", post_content)
            # remove extra spaces from post content
            post_content = re.sub(r"\s{2,}", " ", post_content)

            # check if post is pinned
            pinned = responseJSON["pinned"]
            staff = responseJSON["post_stream"]["posts"][0]["staff"]

            # author of post
            author = responseJSON["post_stream"]["posts"][0]["username"]

            # url to post
            slug = responseJSON["slug"]
            url = f"https://forums.playlostark.com/t/{slug}/{post_id}"

            if not pinned and staff:
                if title.__contains__(f"{category}"):
                    api.append(
                        {
                            "title": title,
                            "post_body": post_content,
                            "created_at": created_at,
                            "url": url,
                            "author": author,
                        }
                    )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    print(LostA.news("updates"))
