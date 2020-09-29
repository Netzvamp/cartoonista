import re
import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def explosm_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. "
                           "This can be done with 'pip install cartoonista[scraping]'")
    nextpage_link = True
    nextpage = "http://explosm.net/comics/15/"
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage).text, 'html.parser')
        
        img = soup.select_one("#main-comic")
        if img:
            img = img["src"].replace("//files.explosm.net/comics/", "")
            author = soup.select_one("#comic-area #comic-author").text.strip("\n").replace("\n", " ").strip("\n")
            filenames.append({"img": img, "txt": author})
            logger.info("Added https://files.explosm.net/comics/" + img + " Text: " + author)
        if soup.find_all("a", class_="nav-next disabled"):  # detect last page
            break

        nextpage = soup.select(".nav-next")
        if nextpage:
            nextpage = "http://explosm.net" + nextpage[0]["href"]

    return filenames


if __name__ != "__main__":
    explosm = Cartoonist(
        name="explosm.net",
        credits="Explosm, LLC.",
        website="http://explosm.net/",
        language="en",
        base_url="https://files.explosm.net/comics/",
        scraper=explosm_scraper,
        tags=["offensive", "nsfw"]
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(explosm_scraper())
