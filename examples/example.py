"""A simple example of cartoonista to show all possible options."""
from pprint import pprint
from cartoonista import Cartoons

# Get a list of all cartoon include and there infos
cartoonists = Cartoons.get_all_cartoonists()
print("All include and there infos:")
print(cartoonists)
print("Nr of include:", len(cartoonists))
nr = 0
for c in cartoonists:
    nr = nr + c["cartoon_count"]
print("Nr of cartoons:", nr)

print("Random without filter", Cartoons.get_random_cartoon())
print("Only ruthe.de or xkcd.com", Cartoons.get_random_cartoon(include=["xkcd.com", "ruthe.de"]))
print("Only english", Cartoons.get_random_cartoon(languages=["en"]))
print("Filter given include list by language: xkcd.com, ruthe.de, nichtlustig.de and en", Cartoons.get_random_cartoon(
    include=["xkcd.com", "ruthe.de", "nichtlustig.de"], languages=["en"]))
print("Single Cartoonist: schoenescheisse.de", Cartoons.get_random_cartoon(include=["schoenescheisse.de"]))

print(
    "Filter by tag: exclude offensive",
    Cartoons.get_random_cartoon(
        include=["xkcd.com", "explosm.net", "martin-perscheid.de"], exclude_tags=["offensive"]
    )
)  # returns only xkcd, cause they aren't offensive (to me ;) )

print("Unweighted random", Cartoons.get_random_cartoon(weighted=False))