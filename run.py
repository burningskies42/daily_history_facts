from utils import get_daily_events, create_template 
from config.core import config

if __name__ == "__main__":
    daily_events = get_daily_events(config.app.main_url, config.app.parser)
    html_str = create_template(daily_events)
    with open("preview.html", "w") as f:
        f.write(html_str)
