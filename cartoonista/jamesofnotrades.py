import re
import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def jamesofnotrades_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. "
                           "This can be done with 'pip install cartoonista[scraping]'")
    nextpage_link = True
    nextpage = "https://jamesofnotrades.com/comic/soraka-bullies-aurelion-sol/"
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        
        img = soup.select_one("#comic img")
        if img:
            img_src = img["src"].replace("https://jamesofnotrades.com/comics/", "")
            title = soup.select_one("title").text.replace(" – James of No Trades", "")
            txt = img["title"]
            filenames.append({"img": img_src, "txt": txt, "title": title})
            logger.info("Added https://jamesofnotrades.com/comics/" + img_src + " Text: " + txt + " Title: " + title)
        if not soup.select_one(".navi-next").get("href"):  # detect last page
            break

        nextpage = soup.select_one(".navi-next")
        if nextpage:
            nextpage = nextpage["href"]

    return filenames


if __name__ != "__main__":
    jamesofnotrades = Cartoonist(
        name="jamesofnotrades_com",
        credits="JamesOfNoTrades.com",
        website="https://jamesofnotrades.com/",
        language="en",
        base_url="https://jamesofnotrades.com/comics/",
        scraper=jamesofnotrades_scraper,
        tags=[]
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(jamesofnotrades_scraper())
