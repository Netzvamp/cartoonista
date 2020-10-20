import json
import random
import os
import logging
from .exceptions import CartoonError


logger = logging.getLogger(__name__)


class Cartoonist:
    data = {}
    __objects = {}
    
    def __init__(self, name: str, credits: str, website: str, language: str, base_url: str, scraper: callable, tags: list = None):
        self.name: str = name
        self.credits: str = credits
        self.website: str = website
        self.language: str = language
        self.base_url: str = base_url
        self.scraper: callable = scraper
        if not tags:
            self.tags: list = []
        else:
            self.tags: list = tags
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
    def get_random_cartoon(cls, include: list = None, exclude: list = None, languages: list = None,
                           exclude_tags: list = None, weighted: bool = True):
        """
        :param include:
        :type include: list
        :param exclude:
        :type exclude: list
        :param languages:
        :type languages: list
        :param exclude_tags:
        :type exclude_tags: list
        :param weighted:
        :type weighted: bool
        :return:
        :rtype:

        """
        weights = []
        filtered_cartoonists = []

        for c in Cartoonist.data:
            # print("to filter", c)
            if exclude_tags and isinstance(exclude_tags, list) and cls.__objects[c].tags in exclude_tags:
                # print("Exclude by tag:", c)
                continue
            if exclude and isinstance(exclude, list) and c in exclude:
                # print("Exclude:", c)
                continue
            if include and isinstance(include, list) and c not in include:
                # print("Is not in include:", c)
                continue
            if languages and isinstance(languages, list) and cls.__objects[c].language not in languages:
                continue
            # print("Added:", c)
            filtered_cartoonists.append(c)

        # print("filtered_cartoonists", filtered_cartoonists)

        weights = [len(cls.data[_art]["filenames"]) for _art in filtered_cartoonists]

        if len(filtered_cartoonists):
            if weighted:  # choose cartoonist weighted by the number of cartoons
                cartoonist = random.choices(filtered_cartoonists, weights=weights)[0]
            else:
                cartoonist = random.choices(filtered_cartoonists)[0]

            img = cls.data[cartoonist]["filenames"][random.randrange(0, len(cls.data[cartoonist]["filenames"]) - 1)]

            if isinstance(img, str):
                return {
                    "name": cartoonist,
                    "img": cls.__objects[cartoonist].base_url + img,
                    "language": cls.__objects[cartoonist].language,
                    "credits": cls.__objects[cartoonist].credits,
                    "website": cls.__objects[cartoonist].website
                }
            elif isinstance(img, dict):
                src = cls.__objects[cartoonist].base_url + img["img"]
                return {
                    **img,
                    "name": cartoonist,
                    "img": src,
                    "language": cls.__objects[cartoonist].language,
                    "credits": cls.__objects[cartoonist].credits,
                    "website": cls.__objects[cartoonist].website
                }
        else:
            raise CartoonError("Oh noes! No cartoonists with that names and criteria found!")

    @classmethod
    def get_all_cartoonists(cls):
        cartoonists = []
        for obj in cls.__objects:
            cartoonists.append(
                {
                    "name": cls.__objects[obj].name,
                    "credits": cls.__objects[obj].credits,
                    "website": cls.__objects[obj].website,
                    "language": cls.__objects[obj].language,
                    "tags": cls.__objects[obj].tags,
                    "cartoon_count": len(cls.data[cls.__objects[obj].name]["filenames"])
                }
            )
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
