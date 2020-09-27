import re
import requests
import logging
from bs4 import BeautifulSoup
if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def schoenescheisse_scraper():
    nextpage_link = True
    nextpage = "https://www.schoenescheisse.de/category/cartoons/page/1/"
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')

        imgs = soup.select("article img")
        for img in imgs:
            img = img["src"].replace("https://www.schoenescheisse.de/wp-content/uploads/", "")
            filenames.append(img)
            logger.info("Added https://www.schoenescheisse.de/wp-content/uploads/" + img)

        nextpage_link = soup.select(".nav-previous a")
        if nextpage_link:
            nextpage = nextpage_link[0]["href"]
        else:
            nextpage = False
    return filenames


if __name__ != "__main__":
    schoenescheisse = Cartoonist(
        name="schoenescheisse.de",
        credits="Piero Masztalerz",
        website="https://www.schoenescheisse.de/",
        language="de",
        base_url="https://www.schoenescheisse.de/wp-content/uploads/",
        scraper=schoenescheisse_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    cartoons = schoenescheisse_scraper()
    print(cartoons)
    print(len(cartoons))
