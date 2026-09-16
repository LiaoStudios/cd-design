# CD Design Split Hero and Full-Bleed Intros Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a 50/50 desktop home hero, an image-led mobile hero, a product-expanding CTA, and commercially coherent full-bleed category imagery.

**Architecture:** Keep the current static HTML/CSS/JavaScript structure. Extend the existing home hero and menu state helpers in `index.html`, centralize category image fitting in `assets/product-gallery.css`, and correct category content within the existing product pages.

**Tech Stack:** Static HTML5, CSS custom properties and media queries, vanilla JavaScript, Python `unittest` contract tests.

## Global Constraints

- Preserve the transparent-at-top and white-on-scroll navigation behavior.
- Do not add external runtime dependencies.
- Use local, category-appropriate imagery and preserve existing accessible lightbox behavior.
- Do not discard unrelated worktree changes.

---

### Task 1: Lock the responsive and content contracts

**Files:**
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: existing static pages and shared gallery stylesheet.
- Produces: contract tests for `discoverProductsBtn`, `openProductsMenu`, `--intro-position`, full-bleed media, and coherent Falegnameria content.

- [ ] **Step 1: Write the failing tests**

```python
def test_home_cta_expands_product_navigation(self):
    html = self.read("index.html")
    self.assertIn('id="discoverProductsBtn"', html)
    self.assertIn("function openProductsMenu", html)
    self.assertIn("prodottiSubmenu.classList.remove('hidden')", html)

def test_product_intro_media_is_full_bleed(self):
    css = self.read("assets/product-gallery.css")
    self.assertIn("object-fit: cover", css)
    self.assertIn("var(--intro-position, center)", css)

def test_falegnameria_content_is_wood_focused(self):
    html = self.read("falegnameria.html")
    for unrelated in ("Parapetti e balaustre", "Ringhiere in vetro", "Strutture in ferro"):
        self.assertNotIn(unrelated, html)
    self.assertIn("Porte in legno su misura", html)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_site_contract -v`
Expected: failures for the missing CTA behavior, `object-fit: cover`, and Falegnameria copy.

- [ ] **Step 3: Keep the failures as the implementation target**

No production files are changed in this task.

### Task 2: Implement the desktop split hero and mobile image hero

**Files:**
- Modify: `index.html`
- Test: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: current `.home-hero__media`, `.home-hero__content`, `openMenu()`, and submenu nodes.
- Produces: `#discoverProductsBtn` and `openProductsMenu({ focusFirst = true } = {})`.

- [ ] **Step 1: Add the behavior hook**

Add `id="discoverProductsBtn"` to the existing secondary hero CTA and bind it to a function that opens the menu, removes `hidden` from the product submenu, updates `aria-expanded`, rotates the plus icon, and focuses the first submenu link.

- [ ] **Step 2: Implement the responsive layout**

At 768px and above, use `grid-template-columns: minmax(0, 1fr) minmax(0, 1fr)` with content on the left and cover imagery on the right. Below 768px, absolutely position the media as the background and use a bottom-weighted neutral gradient behind compact white copy.

- [ ] **Step 3: Center the brand and preserve scroll state**

Center the logo with `left: 50%` and `transform: translateX(-50%)`; keep the menu trigger right-aligned and retain `.home-nav.is-scrolled` styling.

- [ ] **Step 4: Run the focused tests**

Run: `python3 -m unittest tests.test_site_contract.SiteContractTests.test_home_has_scroll_aware_navigation_and_split_hero tests.test_site_contract.SiteContractTests.test_home_cta_expands_product_navigation -v`
Expected: PASS.

### Task 3: Make category intros full-bleed and correct imagery

**Files:**
- Modify: `assets/product-gallery.css`
- Modify: `infissi-pvc.html`
- Modify: `infissi-alluminio.html`
- Modify: `infissi-legno.html`
- Modify: `porte-blindate.html`
- Modify: `zanzariere.html`
- Modify: `persiane-scuri-alluminio.html`
- Modify: `porte-interne.html`
- Modify: `tende-caduta-sole.html`
- Test: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: `.product-intro-media img`.
- Produces: `object-fit: cover` and `object-position: var(--intro-position, center)` with per-page focal positions.

- [ ] **Step 1: Implement shared fitting rules**

Use 4:3 for narrow screens and 16:9 from 768px, with the image filling the slot and honoring `--intro-position`.

- [ ] **Step 2: Review and update category images**

Retain wide, relevant images; replace technical diagrams or unsuitable portrait renders with local landscape photographs where available. Set a focal position on remaining portrait sources so the product stays visible after cropping.

- [ ] **Step 3: Run image and reference contracts**

Run: `python3 -m unittest tests.test_site_contract.SiteContractTests.test_all_local_image_references_exist tests.test_site_contract.SiteContractTests.test_product_intro_media_is_full_bleed -v`
Expected: PASS.

### Task 4: Rebuild Falegnameria as a coherent commercial category

**Files:**
- Modify: `falegnameria.html`
- Create: `images/falegnameria-porta-legno.jpg`
- Create: `images/falegnameria-finiture-legno.jpg`
- Test: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: the existing product-card and gallery-lightbox markup.
- Produces: wood-focused intro copy and product cards while preserving `product-detail` lightbox hooks.

- [ ] **Step 1: Prepare optimized local assets**

Create web-sized JPEG copies from the supplied wood-door photography, keeping the source crop and using the shared focal-position mechanism.

- [ ] **Step 2: Replace unrelated content**

Replace glass railing and iron structure cards with “Porte in legno su misura”, “Infissi e ripristini in legno”, and “Finiture e pannellature”, using precise commercial copy without unsupported manufacturing claims.

- [ ] **Step 3: Run focused category contracts**

Run: `python3 -m unittest tests.test_site_contract.SiteContractTests.test_falegnameria_content_is_wood_focused tests.test_site_contract.SiteContractTests.test_every_product_page_loads_shared_gallery -v`
Expected: PASS.

### Task 5: Verify interaction and responsive presentation

**Files:**
- Modify only if verification reveals a defect.

**Interfaces:**
- Consumes: completed static site.
- Produces: verified desktop and mobile behavior.

- [ ] **Step 1: Run the full suite**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 2: Serve the site locally**

Run: `python3 -m http.server 4173 --bind 127.0.0.1`
Expected: the site is reachable at `http://127.0.0.1:4173/`.

- [ ] **Step 3: Inspect representative viewports**

Inspect the home page at 1440×900, 390×844, and 320×700; inspect Falegnameria and at least two other category pages at desktop and mobile widths. Confirm the CTA opens the full product list, the logo is centered, text does not consume the whole mobile image, and intro crops fill their slots.

- [ ] **Step 4: Re-run tests after visual adjustments**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

