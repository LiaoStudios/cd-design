import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PAGES = [
    "infissi-pvc.html",
    "infissi-alluminio.html",
    "infissi-legno.html",
    "porte-blindate.html",
    "zanzariere.html",
    "persiane-scuri-alluminio.html",
    "porte-interne.html",
    "tende-caduta-sole.html",
    "falegnameria.html",
]


class SiteContractTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_all_local_image_references_exist(self):
        for page in ["index.html", *PRODUCT_PAGES]:
            html = self.read(page)
            for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
                if not src.startswith(("http://", "https://", "data:")):
                    self.assertTrue((ROOT / src).is_file(), f"{page}: missing {src}")

    def test_every_product_page_loads_shared_gallery(self):
        for page in PRODUCT_PAGES:
            html = self.read(page)
            self.assertIn('href="assets/product-gallery.css"', html, page)
            self.assertIn('src="assets/product-gallery.js"', html, page)
            self.assertIn("product-detail", html, page)

    def test_home_has_scroll_aware_navigation_and_split_hero(self):
        html = self.read("index.html")
        self.assertIn('id="siteNav"', html)
        self.assertIn("home-hero__media", html)
        self.assertIn("home-hero__content", html)
        self.assertIn("is-scrolled", html)

    def test_incorrect_wood_shutter_card_is_removed(self):
        html = self.read("infissi-legno.html")
        self.assertNotIn("Finestra con scuri in legno", html)
        self.assertNotIn('src="images/foto-080.jpg"', html)

    def test_corrected_category_images_are_used(self):
        expected = {
            "infissi-legno.html": "images/infissi-legno-intro.jpg",
            "porte-blindate.html": "images/porta-blindata-intro.jpg",
            "zanzariere.html": "images/zanzariere-bettio-neoscenica.jpg",
            "porte-interne.html": "images/porte-interne-intro.jpg",
        }
        for page, image in expected.items():
            self.assertIn(f'src="{image}"', self.read(page), page)

    def test_aluminium_page_does_not_claim_wood_products(self):
        html = self.read("persiane-scuri-alluminio.html")
        self.assertNotIn("Scuri in legno", html)
        self.assertIn("lamelle", html)
        self.assertIn("pannello pieno", html)


if __name__ == "__main__":
    unittest.main()
