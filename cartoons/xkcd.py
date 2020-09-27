import requests
import logging
from bs4 import BeautifulSoup

if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def xkcd_scraper():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Brave Chrome/85.0.4183.121 Safari/537.36'
    }
    soup = BeautifulSoup(requests.get("https://xkcd.com/archive/", headers=headers).text, 'html.parser')
    pages = soup.select("#middleContainer a")

    filenames = []

    for page in pages:
        page_soup = BeautifulSoup(requests.get("https://xkcd.com" + page["href"], headers=headers).text, 'html.parser')
        try:
            img = page_soup.select("#comic img")[0]["src"].replace("//imgs.xkcd.com/comics/", "")
            filenames.append(img)
            logger.info("Added https://imgs.xkcd.com/comics/" + img)
        except IndexError:
            pass
            # filters out interactive commics / comics without image

    return filenames


if __name__ != "__main__":
    xkcd = Cartoonist(
        name="xkcd.com",
        credits="Randall Munroe",
        website="https://xkcd.com",
        language="en",
        base_url="https://imgs.xkcd.com/comics/",
        scraper=xkcd_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(xkcd_scraper())