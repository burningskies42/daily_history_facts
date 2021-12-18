import bs4
import requests


class DailyEvent:
    def __init__(self, event_tag: bs4.element.Tag, parser: str = "html.parser"):
        """News artice wrapper object

        Args:
            event_tag (bs4.element.Tag): harvested news object
        """
        try:
            self.name = event_tag.find("b").text
        except AttributeError:
            self.name = event_tag.text

        self.parser = parser
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

        part_url = bs4.BeautifulSoup(ahref_str, self.parser).find("a").get("href")

        return "https://en.wikipedia.org" + part_url

    def get_image(self):
        # TODO: get better images. Maybe from google image search API
        """extract image from wikipedia article

        Returns:
            url: image url
        """
        data = requests.get(self.link)
        soup = bs4.BeautifulSoup(data.content, self.parser)
        for x in soup.find_all("img")[1:]:
            try:
                image = str(x.attrs["srcset"]).split(" ")[0]
                return "https:" + image
            except Exception:
                pass