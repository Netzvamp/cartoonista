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
    nextpage = "https://www.commitstrip.com/en/2012/02/22/interview/?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Brave Chrome/85.0.4183.121 Safari/537.36'
    }
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage, headers=headers).text, 'html.parser')

        img = soup.select_one(".entry-content img")

        if img and "commitstrip.com/wp-content/uploads" in img["src"]:
            img_src = img["src"].\
                replace("https://www.commitstrip.com/wp-content/uploads/", "").\
                replace("//www.commitstrip.com/wp-content/uploads/", "")

            title = soup.select_one(".entry-title").text

            filenames.append({"img": img_src, "txt": title})
            logger.info("Added https://www.commitstrip.com/wp-content/uploads/" + img_src + " Text: " + title)

        nextpage = soup.select_one(".nav-next a")
        if nextpage:
            nextpage = nextpage["href"]
        else:  # we reached the last page
            break
    return filenames


if __name__ != "__main__":
    commitstrip = Cartoonist(
        name="commitstrip_com",
        credits="CommitStrip.com",
        website="https://www.commitstrip.com",
        language="en",
        base_url="https://www.commitstrip.com/wp-content/uploads/",
        scraper=commitstrip_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(commitstrip_scraper())
