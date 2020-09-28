import re
import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def islieb_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. T"
                           "his can be done with 'pip install cartoonista[scraping]'")
    nextpage_link = True
    nextpage = "https://islieb.de/"
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')

        for article in soup.select("article"):
            if article.img:
                src = article.img["src"].replace("http://", "https://").replace("https://islieb.de/blog/wp-content/uploads/", "")
                title = article.header.h2.a.text
                if "https://islieb.de" not in src:  # filter paths to get only cartoons
                    filenames.append({"img": src, "title": title})
                    logger.info("Added https://islieb.de/blog/wp-content/uploads/" + src + " Title: " + title)

        nextpage_link = soup.select(".pagination-next a")
        if nextpage_link:
            nextpage = nextpage_link[0]["href"]
        else:
            nextpage = False

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
