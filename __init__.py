from utils import get_daily_events, create_template 

MAIN_URL = "https://en.wikipedia.org/wiki/Main_Page"
parser = "html.parser"


if __name__ == "__main__":
    daily_events = get_daily_events(MAIN_URL, parser)
    html_str = create_template(daily_events)
    with open("preview.html", "w") as f:
        f.write(html_str)
