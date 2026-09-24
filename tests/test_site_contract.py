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
    "tapparelle-alluminio.html",
    "tende-caduta-sole.html",
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
        self.assertIn("font-size: clamp(2.75rem, 12vw, 3.5rem)", html)
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

    def test_product_cards_use_larger_full_bleed_media(self):
        css = self.read("assets/product-gallery.css")
        self.assertIn(".product-card-media", css)
        self.assertIn("height: 18rem", css)
        self.assertIn("object-fit: cover", css)
        self.assertIn("padding: 0", css)

    def test_product_navigation_links_look_like_buttons(self):
        for page in PRODUCT_PAGES:
            html = self.read(page)
            self.assertIn("product-back-button", html, page)
            self.assertEqual(html.count("product-pager__button"), 2, page)
        css = self.read("assets/product-gallery.css")
        self.assertIn(".product-back-button", css)
        self.assertIn("background: #0f2d83", css)
        self.assertIn(".product-pager__button", css)

    def test_correct_product_photos_match_wood_windows_and_security_products(self):
        wood = self.read("infissi-legno.html")
        security = self.read("porte-blindate.html")
        self.assertRegex(wood, r'foto-167\.jpg[^>]+alt="Finestre in legno"')
        self.assertRegex(wood, r'foto-121\.jpg[^>]+alt="Finestre ad arco"')
        self.assertRegex(security, r'foto-117\.jpg[^>]+alt="Grata di sicurezza a doppia anta"')
        self.assertNotIn("Ingresso con vetrata", security)

    def test_armored_door_catalog_copy_matches_the_selected_images(self):
        html = self.read("porte-blindate.html")
        expected = {
            "images/foto-019.jpg": ("Porta blindata moderna", "Pannello rosso con inserti geometrici"),
            "images/porta-blindata-intro.jpg": ("Porta effetto legno", "Ingresso installato con pannello coordinato"),
            "images/foto-151.jpg": ("Pannelli personalizzabili", "Modelli e finiture effetto legno"),
            "images/foto-192.jpg": ("Struttura della porta", "Vista esplosa dei componenti interni"),
            "images/foto-067.jpg": ("Cilindro di sicurezza", "Dettaglio della chiusura con defender"),
            "images/foto-117.jpg": ("Grata di sicurezza a doppia anta", "Protezione esterna apribile in metallo verniciato"),
        }
        for image, (title, copy) in expected.items():
            self.assertIn(f'src="{image}"', html)
            self.assertIn(title, html)
            self.assertIn(copy, html)
        for stale_image in ("images/foto-028.jpg", "images/foto-041.jpg", "images/foto-159.jpg"):
            self.assertNotIn(stale_image, html)
        self.assertIn("Soluzioni per ogni ingresso", html)
        self.assertIn("security-product-card", html)

    def test_arched_window_photo_has_no_embedded_heading(self):
        from PIL import Image
        html = self.read("infissi-legno.html")
        self.assertRegex(html, r'foto-121\.jpg[^>]+alt="Finestre ad arco"')
        self.assertNotIn("data-lightbox-crop", html)
        with Image.open(ROOT / "images/foto-121.jpg") as image:
            self.assertEqual(image.size, (1296, 1200))

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
        }
        for page, image in expected.items():
            self.assertIn(f'src="{image}"', self.read(page), page)

    def test_supplier_names_appear_in_page_titles(self):
        self.assertIn("Zanzariere Bettio</h1>", self.read("zanzariere.html"))
        self.assertIn("Porte Interne Tecnoporte</h1>", self.read("porte-interne.html"))

    def test_pvc_products_use_requested_names(self):
        html = self.read("infissi-pvc.html")
        self.assertIn("PVC a 6 camere", html)
        self.assertIn("3 guarnizioni", html)
        self.assertIn("Salamander Green Evolution 76", html)
        self.assertNotIn("Gealan", html)

    def test_tapparelle_have_their_own_section_before_tende(self):
        tapparelle = self.read("tapparelle-alluminio.html")
        tende = self.read("tende-caduta-sole.html")
        self.assertIn("Tapparelle in Alluminio</h1>", tapparelle)
        self.assertIn('href="tende-caduta-sole.html"', tapparelle)
        self.assertNotIn("Tapparelle", tende.replace("Tapparelle in Alluminio", ""))
        for page in ["index.html", *PRODUCT_PAGES]:
            html = self.read(page)
            self.assertLess(html.index('href="tapparelle-alluminio.html"'), html.index('href="tende-caduta-sole.html"'), page)

    def test_home_offers_turnkey_renovation_service(self):
        html = self.read("index.html")
        self.assertIn("Ristrutturazione completa chiavi in mano", html)

    def test_nav_logo_is_enlarged_and_always_centered(self):
        for page in ["index.html", *PRODUCT_PAGES]:
            html = self.read(page)
            self.assertIn("h-[3.75rem] md:h-12 w-auto", html, page)
            if page != "index.html":
                self.assertIn("absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2", html, page)

    def test_falegnameria_section_is_removed(self):
        self.assertFalse((ROOT / "falegnameria.html").exists())
        for page in ["index.html", *PRODUCT_PAGES]:
            self.assertNotIn("falegnameria", self.read(page).lower(), page)

    def test_section_is_named_tende_da_sole(self):
        for page in ["index.html", *PRODUCT_PAGES]:
            self.assertNotIn("Tende a Caduta e da Sole", self.read(page), page)
        self.assertIn("Tende da Sole</h1>", self.read("tende-caduta-sole.html"))

    def test_shop_gallery_photo_is_removed(self):
        self.assertNotIn("Serramenti per negozio", self.read("index.html"))

    def test_wood_page_has_several_photos_and_no_brand_caption(self):
        html = self.read("infissi-legno.html")
        self.assertNotIn("Immagine prodotto Pavanello", html)
        for image in ("legno-vetrate-luminose", "legno-portefinestre-scorrevoli", "legno-porta-finestra-tapparella", "legno-vetrate-tutta-altezza"):
            self.assertIn(f"images/{image}.jpg", html)

    def test_dropdown_menu_scrolls_instead_of_clipping_the_product_list(self):
        for page in ["index.html", *PRODUCT_PAGES]:
            html = self.read(page)
            self.assertIn("#prodottiSubmenu { flex-shrink: 0; }", html, page)
            self.assertIn("#dropdownMenu { max-height", html, page)

    def test_aluminium_page_does_not_claim_wood_products(self):
        html = self.read("persiane-scuri-alluminio.html")
        self.assertNotIn("Scuri in legno", html)
        self.assertIn("lamelle", html)
        self.assertIn("pannello pieno", html)


if __name__ == "__main__":
    unittest.main()
