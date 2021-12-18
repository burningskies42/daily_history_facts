from typing import List
import requests
import bs4

from daily_events import DailyEvent


def get_daily_events(main_url: str, parser: str) -> List[DailyEvent]:
    """Extract all promoted top historical events from wikipedia main page

    Returns:
        list: event list
    """
    data = requests.get(main_url)
    soup = bs4.BeautifulSoup(data.content, parser)
    daily_event_objects_list = soup.find_all(id="mp-otd")[0].find("ul").find_all("li")

    daily_events = []
    for each in daily_event_objects_list:

        de = DailyEvent(each)
        daily_events.append(de)
        print(de.link)
        print(de.text)

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
        subtitle.string = article.text#[:300] + "..."

        link = article_template.a
        link["href"] = article.link  # urls[i]
        link.string = article.link  # urls[i]
        article_template.a.replace_with(link)

        newsletter_content += str(article_template).replace("\n", "")

    email_content = html_start + newsletter_content + html_end
    return bs4.BeautifulSoup(email_content, features="lxml").prettify()