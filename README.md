# Cartoonista - A python cartoon library

A library to get a random cartoon image url from ~20000 cartoons. 
It also contains the scrapers for many cartoon websites.

:tada: :satisfied: :man_facepalming: **A product of the finest german overengineering to solve a non existing problem with a complicated solution.** :man_facepalming: :satisfied: :tada: 

## Sites

English:
* https://xkcd.com
* https://explosm.net
* https://loadingartist.com/
* https://www.smbc-comics.com
* https://www.commitstrip.com

German:
* https://joscha.com/nichtlustig
* https://ruthe.de
* https://martin-perscheid.de
* https://islieb.de
* https://www.schoenescheisse.de

This lib includes all scrapers for these sites, but it ships with all data, so these are only needed for manual updating.

## Install

```pip install cartoonista```

## Examples / Documentation

    from cartoons import Cartoons

    Cartoons.get_random_cartoon(
        include=["xkcd_com", "ruthe_de"],  # optional
        exclude=["loadingartist_com", "commitstrip_com"],  # optional
        languages=["en"],  # optional
        exclude_tags=["offensive"],  # optional
        weighted=False  # optional
    )

This is the main function to get a random cartoon. There are optional filter parameters:
* cartoonists: Get only from these cartoonists. You can get the names and all infos with ```Cartoons.get_all_cartoonists()```
* language: Get only in this languages. There are currently only "en" and "de" cartoons.
* exclude_tags: Exclude cartoonists by tags. Possible values: "offensive", "nsfw"
* weighted: Default is to give cartoonists a weight by the amount of there cartoons, to prevent double cartoons for cartoonists with small amounts. This can be disabled, to randomize even over all cartoonists. 
The cartoons have to match all filters.

It returns something like this:

    {
        'img': 'https://imgs.xkcd.com/comics/standard_model_changes.png', 
        'title': 'Standard Model Changes', 
        'txt': "Bugs are spin 1/2 particles, unless it's particularly windy.", 
        'credits': 'Randall Munroe', 
        'website': 'https://xkcd.com',
        'tags': []
    }

*Title/txt could be placed over/under the image and it would be fair to give credit and link to website.*

## Manual updating

Manual updating isn't strictly needed, cause the lib ships with all data, but it's possible.

Install the requirements with ```pip install pip install cartoonista[scraping]``` or manually install requests and beautifulsoup4.

Run the ```scrape.py``` from the repo (that gives you some logging output) or start scraping by running ```python -c "exec(\"from cartoons import Cartoons\nCartoons.start_scraping()\")"```. It's also possible to update only some cartoonist with ```Cartoons.start_scraping(cartoonists=["islieb.de", "xkcd.com"])```.