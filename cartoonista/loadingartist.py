import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def la_scraper():
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
    nextpage = "https://loadingartist.com/comic/born/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Brave Chrome/85.0.4183.121 Safari/537.36'
    }
    filenames = []
    while nextpage_link:
        soup = BeautifulSoup(requests.get(nextpage, headers=headers).text, 'html.parser')

        img = soup.select(".comic img")
        for i in img:
            if "/wp-content/uploads/" in i["src"]:
                img = i
                break
        if img:
            img_src = img["src"].replace("https://loadingartist.com/wp-content/uploads/", "")
            filenames.append({"img": img_src, "txt": img["title"]})
            logger.info("Added https://loadingartist.com/wp-content/uploads/" + img_src + " Text: " + img["title"])
        else:
            raise CartoonError("loadingartist.com: Couldn't find cartoon on the page")

        nextpage = soup.select_one(".next")
        if nextpage:
            nextpage = nextpage["href"]
        else:  # we reached the last page
            break
    return filenames


if __name__ != "__main__":
    loadingartist = Cartoonist(
        name="LoadingArtist_com",
        credits="LoadingArtist.com",
        website="https://loadingartist.com",
        language="en",
        base_url="https://loadingartist.com/wp-content/uploads/",
        scraper=la_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(la_scraper())
