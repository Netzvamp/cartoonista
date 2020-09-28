# Cartoonista - A python cartoon library

An extendable framework to get (random) cartoons image links from these websites:

English:
* https://xkcd.com
* https://dilbert.com

German:
* https://joscha.com/nichtlustig
* https://ruthe.de
* https://martin-perscheid.de
* https://islieb.de
* https://www.schoenescheisse.de/

Thats more than 11.000 cartoons and it's relative easy to add more...

This lib includes all scrapers for these sites, but it ships with all data, so these are only needed for manual updating.

## Install

```pip install cartoonista```

## Examples / Documentation

```python
from cartoons import Cartoons

print("Random without filter", Cartoons.get_random_cartoon())
# >>> Random without filter {'img': 'https://imgs.xkcd.com/comics/code_quality_3.png', 'credits': 'Randall Munroe', 'website': 'https://xkcd.com'}
print("Only ruthe.de or xkcd.com", Cartoons.get_random_cartoon(cartoonists=["xkcd.com", "ruthe.de"]))
# >>> Only ruthe.de or xkcd.com {'img': 'https://ruthe.de/cartoons/strip_0716.jpg', 'credits': 'Ralf Ruthe', 'website': 'https://ruthe.de'}
print("Only english", Cartoons.get_random_cartoon(languages=["en"]))
# >>> Only english {'img': 'https://imgs.xkcd.com/comics/old_game_worlds.png', 'credits': 'Randall Munroe', 'website': 'https://xkcd.com'}
print("Filter given cartoonist list by language", Cartoons.get_random_cartoon(cartoonists=["xkcd.com", "ruthe.de", "nichtlustig.de"], languages=["en"]))
# >>>  Filter given cartoonist list by language {'img': 'https://imgs.xkcd.com/comics/tab_explosion.png', 'credits': 'Randall Munroe', 'website': 'https://xkcd.com'}

# Get a list of all cartoonists and there infos
print("All cartoonists and there infos:")
print(Cartoons.get_all_cartoonists())
# >>>  [{'credits': 'Joscha Sauer',
# >>>   'language': 'de',
# >>>   'name': 'nichtlustig.de',
# >>>   'website': 'https://joscha.com/nichtlustig'},
# >>>  {'credits': 'Ralf Ruthe',
# >>>   'language': 'de',
# >>>   'name': 'ruthe.de',
# >>>   'website': 'https://ruthe.de'},...
print("Nr of cartoonists:", len(Cartoons.get_all_cartoonists()))
# >>>  Nr of cartoonists: 9
```

## Manual updating

Manual updating isn't strictly needed, cause the lib ships with all data, but it's possible.

Run the ```scrape.py``` or start scraping by running ```Cartoons.start_scraping()``` in the IDLE. It's also possible to update only some cartoonist with ```Cartoons.start_scraping(cartoonists=["islieb.de", "xkcd.com"])``` cartoonists

This takes a long time (1h+), cause we have to do some sleeps on delbert.com, to not get banned.