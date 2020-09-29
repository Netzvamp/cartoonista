import logging
from cartoons import Cartoons

logging.basicConfig(level=logging.INFO)  # without you don't see the progress

Cartoons.start_scraping(cartoonists=["explosm.net"])
