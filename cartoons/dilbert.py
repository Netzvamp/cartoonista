import requests
import logging
from bs4 import BeautifulSoup
import time
if __name__ != "__main__":
    from .cartoonist import Cartoonist


logger = logging.getLogger(__name__)


def dilbert_scraper(years: list):
    filenames = []
    for year in years:
        logger.info(f"Scraping year {year}")
        soup = BeautifulSoup(requests.get("https://dilbert.com/search_results?page=1&sort=date_asc&year=" + str(year)).text, 'html.parser')
        max_pages = int(soup.select(".pagination a")[-2].text)

        for page in range(1, max_pages + 1):
            soup = BeautifulSoup(requests.get(f"https://dilbert.com/search_results?page={page}&sort=date_asc&year=" + str(year)).text, 'html.parser')
            for img in soup.select(".img-comic"):
                img_src = img["src"].replace("https://assets.amuniversal.com/", "")
                filenames.append(img_src)
                logger.info("Added https://assets.amuniversal.com/" + img_src)
        logger.info("Prevent getting banned from dilbert.com, so we pause for for 5 minutes after each year.")
        """
        Download only two years without breaks, or you'll get a ban!
        """
        if year != years[-1]:
            time.sleep(300)
    return filenames


def dilbert_2015_2020_scraper():
    return dilbert_scraper(years=[2015, 2016, 2017, 2018, 2019, 2020])


if __name__ != "__main__":
    dilbert_2015_2020 = Cartoonist(
        name="dilbert.com_2015-2020",
        credits="Scott Adams",
        website="https://dilbert.com",
        language="en",
        base_url="https://assets.amuniversal.com/",
        scraper=dilbert_2015_2020_scraper
    )
else:
    logging.basicConfig(level=logging.INFO)
    dilberts = dilbert_2015_2020_scraper()
    print(len(dilberts))
