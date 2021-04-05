import datetime
import os
import re

import bs4
import requests

BASE_URL = "https://en.wikipedia.org"
MAIN_URL = os.path.join(BASE_URL, "wiki", "Main_Page")


class DailyEvent:
    def __init__(self, event_tag: bs4.element.Tag):
        """News artice wrapper object

        Args:
            event_tag (bs4.element.Tag): harvested news object
        """
        try:
            self.name = event_tag.find("b").text
        except AttributeError:
            self.name = event_tag.text

        self.text = event_tag.text
        self.link = self.extract_url(event_tag)
        self.image_url = self.get_image()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name

    def extract_url(self, event_tag):
        """get the clean url from bs4 object

        Args:
            event_tag (bs4.Tag): tag containing all data

        Returns:
            str: url
        """
        try:
            ahref_str = str(event_tag.find("b"))
        except Exception:
            ahref_str = str(event_tag.find("a"))

        part_url = bs4.BeautifulSoup(ahref_str, "html.parser").find("a").get("href")

        return "https://en.wikipedia.org" + part_url

    def get_image(self):
        # TODO: get better images. Maybe from google image search API
        """extract image from wikipedia article

        Returns:
            url: image url
        """
        data = requests.get(self.link)
        soup = bs4.BeautifulSoup(data.content, "html5lib")
        for x in soup.find_all("img")[1:]:
            try:
                image = str(x.attrs["srcset"]).split(" ")[0]
                return "https:" + image
            except Exception:
                pass


def get_daily_events():
    """Extract all promoted top historical events from wikipedia main page

    Returns:
        list: event list
    """
    data = requests.get(MAIN_URL)
    soup = bs4.BeautifulSoup(data.content, "html5lib")
    daily_event_objects_list = soup.find_all(id="mp-otd")[0].find("ul").find_all("li")

    daily_events = []
    for each in daily_event_objects_list:

        de = DailyEvent(each)
        daily_events.append(de)
        print(de.link)

    return daily_events


def create_template(event_list: list):
    """create newsletter template

    Args:
        event_list (list): parsed event list

    Returns:
        string: html of newsletter
    """
    template = open("template.html")
    soup = bs4.BeautifulSoup(template.read(), "html.parser")

    article_template = soup.find("div", attrs={"class": "columns"})
    html_start = str(soup)[: str(soup).find(str(article_template))]
    html_end = str(soup)[str(soup).find(str(article_template)) + len(str(article_template)) :]
    html_start = html_start.replace("\n", "")
    html_end = html_end.replace("\n", "")

    newsletter_content = ""
    for article in event_list:

        try:
            img = article_template.img
            img["src"] = article.image_url
            article_template.img.replace_with(img)
        except Exception():
            pass

        title = article_template.h1
        title.string = article.name[:300]

        subtitle = article_template.p
        subtitle.string = article.text[:300] + "..."

        link = article_template.a
        link["href"] = article.link  # urls[i]
        link.string = article.link  # urls[i]
        article_template.a.replace_with(link)

        newsletter_content += str(article_template).replace("\n", "")

    email_content = html_start + newsletter_content + html_end
    return bs4.BeautifulSoup(email_content, features="lxml").prettify()


if __name__ == "__main__":
    daily_events = get_daily_events()
    html_str = create_template(daily_events)
    with open("preview.html", "w") as f:
        f.write(html_str)
