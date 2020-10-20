import unittest
from cartoonista import Cartoons, CartoonError


class TestCartoonista(unittest.TestCase):
    def test_random(self):
        """
        We should get a dict with random cartoon values.
        """
        for x in range(0, 99):
            c = Cartoons.get_random_cartoon()
            self.assertIsInstance(c, dict)
            self.assertTrue(
                all(item in list(c.keys()) for item in ['img', 'credits', 'website']),
                msg="Every cartoon should contain this keys + some optional" + str(['img', 'credits', 'website'])
            )

    def test_cartoonists_include_filter(self):
        """
        Test whitelisting.
        """
        cartoonists_filter = ["xkcd_com", "smbc_comics_com"]
        got_cartoonists = []

        for x in range(0, 99):
            c = Cartoons.get_random_cartoon(include=cartoonists_filter)
            self.assertIsInstance(c, dict)
            self.assertTrue(
                all(item in list(c.keys()) for item in ['img', 'credits', 'website']),
                msg="Every cartoon should contain this keys + some optional: " + str(['img', 'credits', 'website'])
            )
            self.assertTrue(c["name"] in cartoonists_filter, msg="only filtered cartoonists")

            if c["name"] not in got_cartoonists:
                got_cartoonists.append(c["name"])

        self.assertTrue(all(item in got_cartoonists for item in cartoonists_filter),
                        msg="Not all Cartoonists in filter showed a cartoon:" + str(got_cartoonists))
        self.assertTrue(len(cartoonists_filter) == len(got_cartoonists))

    def test_cartoonists_exclude_filter(self):
        """
        Test blacklisting.
        """
        exclude_filter = ["xkcd_com", "smbc_comics_com"]

        for x in range(0, 99):
            c = Cartoons.get_random_cartoon(exclude=exclude_filter)
            self.assertTrue(
                all(item in list(c.keys()) for item in ['img', 'credits', 'website']),
                msg="Every cartoon should contain this keys + some optional: " + str(['img', 'credits', 'website'])
            )
            self.assertTrue(c["name"] not in exclude_filter, msg=c["name"] + " shouldn't be in " + str(exclude_filter))

    def test_cartoonists_include_exclude_filter(self):
        """
        Test combined black/whitelisting. Exclude has priority.
        """
        exclude_filter = ["xkcd_com"]
        include_filter = ["ruthe_de", "nichtlustig_de", "xkcd_com"]
        got_cartoonists = []

        for x in range(0, 99):
            c = Cartoons.get_random_cartoon(include=include_filter, exclude=exclude_filter)
            self.assertTrue(
                all(item in list(c.keys()) for item in ['img', 'credits', 'website']),
                msg="Every cartoon should contain this keys + some optional: " + str(['img', 'credits', 'website'])
            )
            self.assertTrue(c["name"] not in exclude_filter, msg="no excluded cartoonists")
            if c["name"] not in got_cartoonists:
                got_cartoonists.append(c["name"])

        asserted_cartoonists = ["ruthe_de", "nichtlustig_de"]

        self.assertTrue(all(item in got_cartoonists for item in asserted_cartoonists),
                        msg="Not all Cartoonists in filter showed a cartoon:" + str(got_cartoonists))
        self.assertTrue(len(got_cartoonists) == len(asserted_cartoonists))

    def test_language_filter(self):
        """
        Test language filtering.
        """

        for x in range(0, 99):
            languages = ["en"]
            c = Cartoons.get_random_cartoon(languages=languages)
            self.assertTrue(c["language"] == languages[0], msg="Language en:" + str(c))

            languages = ["de"]
            c = Cartoons.get_random_cartoon(languages=languages)
            self.assertTrue(c["language"] == languages[0], msg="Language en:" + str(c))

            with self.assertRaises(CartoonError):
                c = Cartoons.get_random_cartoon(languages=languages, include=["xkcd_com"])

    def alternative_import(self):
        import cartoonista
        for x in range(0, 99):
            c = cartoonista.get_random_cartoon()
            self.assertIsInstance(c, dict)
            self.assertTrue(
                all(item in list(c.keys()) for item in ['img', 'credits', 'website']),
                msg="Every cartoon should contain this keys + some optional" + str(['img', 'credits', 'website'])
            )

if __name__ == '__main__':
    unittest.main()
