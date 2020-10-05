import re
import logging
if __name__ != "__main__":
    from .exceptions import CartoonError
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def perscheid_scraper():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        raise CartoonError("Packages for scraping not installed. Install requests and beautifulsoup4. T"
                           "his can be done with 'pip install cartoonista[scraping]'")
    soup = BeautifulSoup(requests.get("https://martin-perscheid.de/").text, 'html.parser')
    match = re.search("/cartoon/([0-9]*).gif", soup.select("#cartoon img")[0]["src"])
    if match:
        max_img_id = int(match.group(1))
        min_img_id = 3035

        filenames = []

        for img_id in range(min_img_id, max_img_id + 1):
            img_id_str = str(img_id).zfill(4)
            req = requests.head("https://martin-perscheid.de/image/cartoon/" + img_id_str + ".gif")
            if req.ok:
                filenames.append(img_id_str + ".gif")
                logger.info("Added https://martin-perscheid.de/image/cartoon/" + img_id_str + ".gif")
        return filenames


if __name__ != "__main__":
    perscheid = Cartoonist(
        name="martin-perscheid.de",
        credits="Martin Perscheid",
        website="https://martin-perscheid.de",
        language="de",
        base_url="https://martin-perscheid.de/image/cartoon/",
        scraper=perscheid_scraper,
        tags=["offensive"]
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(perscheid_scraper())
