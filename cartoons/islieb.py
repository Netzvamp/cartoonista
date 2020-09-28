import re
import logging
from .exceptions import CartoonError
if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def islieb_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. T"
                           "his can be done with 'pip install cartoonista[scraping]'")
    soup = BeautifulSoup(requests.get("https://islieb.de/").text, 'html.parser')

    match = re.search("/page/([0-9]*)/", soup.select(".archive-pagination a")[3]["href"])
    if match:
        max_page_id = int(match.group(1))
        filenames = []
        for page_id in range(1, max_page_id + 1):
            imgs = BeautifulSoup(requests.get(f"https://islieb.de/page/{page_id}/").text, 'html.parser').select(".comic-post img")
            for img in imgs:
                    img = img["src"].replace("http://", "https://").replace("https://islieb.de/blog/wp-content/uploads/", "")
                    if not "https://islieb.de" in img:  # filter paths
                        filenames.append(img)
                        logger.info("Added https://islieb.de/blog/wp-content/uploads/" + img)
        return filenames


if __name__ != "__main__":
    islieb = Cartoonist(
        name="islieb.de",
        credits="Alexander Brückner",
        website="https://islieb.de",
        language="de",
        base_url="https://islieb.de/blog/wp-content/uploads/",
        scraper=islieb_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(islieb_scraper())
