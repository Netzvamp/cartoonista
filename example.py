from pprint import pprint
from cartoons import Cartoons

# Get a list of all cartoon cartoonists and there infos
print("All cartoonists and there infos:")
pprint(Cartoons.get_all_cartoonists())
print("Nr of cartoonists:", len(Cartoons.get_all_cartoonists()))

print("Random without filter", Cartoons.get_random_cartoon())
print("Only ruthe.de or xkcd.com", Cartoons.get_random_cartoon(cartoonists=["xkcd.com", "ruthe.de"]))
print("Only english", Cartoons.get_random_cartoon(languages=["en"]))
print("Filter given cartoonists list by language", Cartoons.get_random_cartoon(
    cartoonists=["xkcd.com", "ruthe.de", "nichtlustig.de"], languages=["en"]))
print("Single Cartoonist", Cartoons.get_random_cartoon(cartoonists=["schoenescheisse.de"]))
