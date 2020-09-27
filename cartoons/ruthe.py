import re
import requests
import logging
from bs4 import BeautifulSoup
if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def rr_scraper():
    soup = BeautifulSoup(requests.get("https://ruthe.de/").text, 'html.parser')
    match = re.search("/cartoons/strip_([0-9]*).jpg", soup.select("#wrapper_cartoon img")[0]["src"])
    if match:
        max_img_id = match.group(1)

        filenames = []

        for img_id in range(1, int(max_img_id)+1):
            img_id_str = str(img_id).zfill(4)
            req = requests.head("https://ruthe.de/cartoons/strip_" + img_id_str + ".jpg")
            if req.ok:
                filenames.append(img_id_str + ".jpg")
                logger.info("Added https://ruthe.de/cartoons/strip_" + img_id_str + ".jpg")
        return filenames


if __name__ != "__main__":
    ruthe = Cartoonist(
        name="ruthe.de",
        credits="Ralf Ruthe",
        website="https://ruthe.de",
        language="de",
        base_url="https://ruthe.de/cartoons/strip_",
        scraper=rr_scraper
    )
else:
    print(rr_scraper())
