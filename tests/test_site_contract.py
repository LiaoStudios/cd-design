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
        self.assertIn("home-nav__brand", html)
        self.assertIn("home-hero__media", html)
        self.assertIn("home-hero__content", html)
        self.assertIn("grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)", html)
        self.assertIn("is-scrolled", html)

    def test_home_cta_expands_product_navigation(self):
        html = self.read("index.html")
        self.assertIn('id="discoverProductsBtn"', html)
        self.assertIn("function openProductsMenu", html)
        self.assertIn("prodottiSubmenu.classList.remove('hidden')", html)
        self.assertIn("prodottiSubmenu.querySelector('a')", html)

    def test_home_hero_prioritizes_large_high_desktop_copy_and_compact_mobile_copy(self):
        html = self.read("index.html")
        self.assertNotIn('class="home-hero__logo"', html)
        self.assertNotIn(".home-hero__logo", html)
        self.assertIn("align-items: flex-start", html)
        self.assertIn("padding: 6rem clamp(2rem, 4vw, 5rem)", html)
        self.assertIn("font-size: clamp(5rem, 5.8vw, 5.75rem)", html)
        self.assertIn("font-size: clamp(2.35rem, 10.5vw, 3rem)", html)
        self.assertIn("transform: none", html)

    def test_home_alternates_solid_logo_palette_sections(self):
        html = self.read("index.html")
        self.assertIn("--cd-blue-deep: #081c5b", html)
        for section_class in (
            "home-section--products",
            "home-section--projects",
            "home-section--reviews",
            "contact-panel--info",
            "contact-panel--form",
            "home-footer",
        ):
            self.assertIn(section_class, html)
        self.assertIn(".home-section--products {\n    background: #e8f0ff;", html)
        self.assertIn(".home-section--reviews {\n    color: #fff;\n    background: #0a236e;", html)
        self.assertIn(".contact-panel--info { background: #0f2d83; }", html)
        self.assertIn(".contact-panel--form { background: #e8f0ff; }", html)
        self.assertNotIn("linear-gradient(145deg, #f7faff", html)
        self.assertNotIn("linear-gradient(135deg, #0f2d83", html)
        self.assertNotIn("radial-gradient(circle at 85% 0%", html)
        self.assertIn("rgba(255,255,255,0.34)", html)

    def test_product_intro_media_is_full_bleed(self):
        css = self.read("assets/product-gallery.css")
        self.assertIn("object-fit: cover", css)
        self.assertIn("object-position: var(--intro-position, center)", css)
        self.assertIn("aspect-ratio: 16 / 9", css)

    def test_falegnameria_content_is_wood_focused(self):
        html = self.read("falegnameria.html")
        for unrelated in ("Parapetti e balaustre", "Ringhiere in vetro", "Strutture in ferro"):
            self.assertNotIn(unrelated, html)
        self.assertIn("Porte in legno su misura", html)
        self.assertIn("Infissi e ripristini in legno", html)
        self.assertIn("Finiture e pannellature", html)

    def test_incorrect_wood_shutter_card_is_removed(self):
        html = self.read("infissi-legno.html")
        self.assertNotIn("Finestra con scuri in legno", html)
        self.assertNotIn('src="images/foto-080.jpg"', html)

    def test_corrected_category_images_are_used(self):
        expected = {
            "infissi-legno.html": "images/foto-167.jpg",
            "porte-blindate.html": "images/porte-blindate-intro-wide.jpg",
            "zanzariere.html": "images/zanzariere-bettio-neoscenica-wide.jpg",
            "persiane-scuri-alluminio.html": "images/persiane-alluminio-intro.jpg",
            "porte-interne.html": "images/porte-interne-intro.jpg",
            "falegnameria.html": "images/falegnameria-intro.jpg",
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
