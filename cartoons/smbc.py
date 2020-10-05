import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def commitstrip_scraper():
    """
    Filenames are in an javascript object on the mainpage.
    """
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. "
                           "This can be done with 'pip install cartoonista[scraping]'")
    nextpage_link = True
    nextpage = "https://www.smbc-comics.com/comic/2002-09-05"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Brave Chrome/85.0.4183.121 Safari/537.36'
    }
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage, headers=headers).text, 'html.parser')

        img = soup.select_one("#cc-comicbody img")

        if img:
            img_src = img["src"].replace("https://www.smbc-comics.com/comics/", "")

            filenames.append({"img": img_src, "txt": img["title"]})
            logger.info("Added https://www.smbc-comics.com/comics/" + img_src + " Text: " + img["title"])
        else:
            raise CartoonError("loadingartist.com: Couldn't find cartoon on page: " + nextpage)

        nextpage = soup.select_one(".cc-next")
        if nextpage:
            nextpage = nextpage["href"]
        else:  # we reached the last page
            break
    return nextpage


if __name__ != "__main__":
    smbc_comics = Cartoonist(
        name="smbc_comics",
        credits="Zach Weinersmith",
        website="https://www.smbc-comics.com",
        language="en",
        base_url="https://www.commitstrip.com/wp-content/uploads/",
        scraper=commitstrip_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(commitstrip_scraper())
