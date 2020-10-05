import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def schoenescheisse_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. T"
                           "his can be done with 'pip install cartoonista[scraping]'")
    nextpage_link = True
    nextpage = "https://www.schoenescheisse.de/category/cartoons/page/1/"
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')

        for article in soup.select("article"):
            if article.img:
                src = article.img["src"].replace("https://www.schoenescheisse.de/wp-content/uploads/", "")
                filenames.append({"img": src, "title": article.h2.a.text})
                logger.info("Added https://www.schoenescheisse.de/wp-content/uploads/" + src)

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
        scraper=schoenescheisse_scraper,
        tags=["offensive"]
    )
else:
    logging.basicConfig(level=logging.INFO)
    cartoons = schoenescheisse_scraper()
    print(cartoons)
    print(len(cartoons))
