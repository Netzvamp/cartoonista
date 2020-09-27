import re
import json
import requests
import logging
from bs4 import BeautifulSoup

if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def nl_scraper():
    """
    Filenames are in an javascript object on the mainpage.
    """
    soup = BeautifulSoup(requests.get("https://joscha.com/nichtlustig").text, 'html.parser')
    script = soup.findAll('script')[3].string

    if "var cartoonList" in script:
        matches = re.search(".*cartoonList = (.*)\;.*", script)
        if matches:
            nl = matches.group(1).replace("'", "\"")
            nl = re.sub("[\}],\s*[\]]", "}]", nl)

            nl = json.loads(nl)
            filenames = []
            logger.info("Found cartoonList on joscha.com")
            for img in nl:
                filenames.append(img["image"])

            return filenames
    else:
        raise Exception("Couldn't grab nichtlustig.de filenames: Script tag doesn't contain 'cartoonList'.")


if __name__ != "__main__":
    nichtlustig = Cartoonist(
        name="nichtlustig.de",
        credits="Joscha Sauer",
        website="https://joscha.com/nichtlustig",
        language="de",
        base_url="https://joscha.com/data/media/cartoons/",
        scraper=nl_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    print(nl_scraper())
