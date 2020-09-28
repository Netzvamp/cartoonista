import json
import random
import os
import logging
from .exceptions import CartoonError


logger = logging.getLogger(__name__)


class Cartoonist:
    data = {}
    __objects = {}
    
    def __init__(self, name: str, credits: str, website: str, language: str, base_url: str, scraper: callable):
        self.name: str = name
        self.credits: str = credits
        self.website: str = website
        self.language: str = language
        self.base_url: str = base_url
        self.scraper: callable = scraper
        Cartoonist.__objects[self.name] = self

        logger.debug(f"Added {self.name}.")

    @classmethod
    def save(cls):
        with open(os.path.join(os.path.dirname(__file__), "cartoons.json"), "w") as j:
            json.dump(cls.data, j, indent=4, sort_keys=True)
            logger.info("Saved scraped data to json file")

    @classmethod
    def load(cls):
        try:
            with open(os.path.join(os.path.dirname(__file__), "cartoons.json")) as j:
                cls.data = json.load(j)
        except FileNotFoundError:
            logger.info("No json savefile found, need to scrape everything.")
            pass  # The scraper get some work

    @classmethod
    def get_random_cartoon(cls, cartoonists: list = None, languages: list = None):
        if not languages:
            languages = ["de", "en"]
        if not cartoonists:
            cartoonists = [_art for _art in Cartoonist.data]

        # choose cartoonists weighted with the number of cartoons
        weights = []
        arts = []

        for _art in Cartoonist.data:
            if (cartoonists and _art in cartoonists) and (languages and cls.__objects[_art].language in languages):
                weights.append(len(cls.data[_art]["filenames"]))
                arts.append(_art)

        if len(arts):
            art = random.choices(arts, weights=weights, k=1)[0]
            img = cls.data[art]["filenames"][random.randrange(0, len(cls.data[art]["filenames"]) - 1)]
            if isinstance(img, str):
                return {"img": cls.__objects[art].base_url + img, "credits": cls.__objects[art].credits, "website": cls.__objects[art].website}
            elif isinstance(img, dict):
                img["img"] = cls.__objects[art].base_url + img["img"]
                return {**img, "credits": cls.__objects[art].credits, "website": cls.__objects[art].website}
        else:
            raise CartoonError("Oh noes! No cartoonists with that names found!")

    @classmethod
    def get_all_cartoonists(cls):
        cartoonists = []
        for obj in cls.__objects:
            cartoonists.append({"name": cls.__objects[obj].name, "credits": cls.__objects[obj].credits, "website": cls.__objects[obj].website, "language": cls.__objects[obj].language})
        return cartoonists

    @classmethod
    def start_scraping(cls, cartoonists: list = None):
        if not cartoonists:
            cartoonists = []
            for obj in cls.__objects:
                cartoonists.append(obj)
        for obj in cartoonists:
            cls.data[cls.__objects[obj].name] = {"filenames": cls.__objects[obj].scraper()}
            cls.save()

    @property
    def filenames(self):
        if self.name:
            if Cartoonist.data.get(self.name, False):
                return Cartoonist.data[self.name]["filenames"]
            else:
                Cartoonist.data[self.name] = {"filenames": []}
                return Cartoonist.data[self.name]
        else:
            return None

    @filenames.setter
    def filenames(self, value):
        if self.name:
            if Cartoonist.data.get(self.name, False):
                Cartoonist.data[self.name]["filenames"] = value
            else:
                Cartoonist.data[self.name] = {"filenames": value}


Cartoonist.load()
