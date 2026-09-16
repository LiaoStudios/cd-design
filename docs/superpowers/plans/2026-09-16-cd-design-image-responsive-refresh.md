# CD Design Image and Responsive Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rendere la home più fotografica e leggibile su desktop/mobile, correggere le immagini prodotto non pertinenti e aggiungere una lightbox accessibile a tutte le pagine di categoria.

**Architecture:** Il sito resta composto da pagine HTML statiche con Tailwind CDN. La home riceve classi e JavaScript locali per hero e navigazione; le pagine prodotto condividono `assets/product-gallery.css` e `assets/product-gallery.js`, così proporzioni e lightbox hanno una sola implementazione. Le immagini esterne vengono importate, orientate e ottimizzate nella cartella `images/`.

**Tech Stack:** HTML5, CSS, JavaScript browser senza framework, Tailwind CSS CDN, Python `unittest` per i controlli statici, browser locale per la verifica responsive.

## Global Constraints

- Conservare lo stile e la struttura generale del sito esistente.
- Non modificare contenuti legali, comportamento del modulo contatti o modifiche utente non pertinenti.
- Non referenziare `/Users/feng/Desktop/ cd design immagini/` dal sito finale.
- Usare testi alternativi veritieri e specifici.
- Garantire target tattili di almeno 44 px, focus visibile e funzionamento da tastiera.
- Nessun overflow orizzontale a 320 px.
- Rispettare `prefers-reduced-motion`.
- Caricare prioritariamente soltanto hero e immagini introduttive; mantenere `loading="lazy"` sulle card.

---

## File Map

- `index.html`: hero responsive, overlay neutro, stato trasparente/bianco della barra.
- `assets/product-gallery.css`: proporzioni comuni delle introduzioni e stile della lightbox.
- `assets/product-gallery.js`: attivazione immagini, dialogo, focus, chiusura e blocco scroll.
- `tests/test_site_contract.py`: controlli statici su pagine, asset, testi rimossi e integrazione lightbox.
- `infissi-pvc.html`, `infissi-alluminio.html`, `infissi-legno.html`, `porte-blindate.html`, `zanzariere.html`, `persiane-scuri-alluminio.html`, `porte-interne.html`, `tende-caduta-sole.html`, `falegnameria.html`: classe condivisa del dettaglio, risorse lightbox e correzioni fotografiche specifiche.
- `images/infissi-legno-intro.jpg`: fotografia orientata e ottimizzata da `20260623_122415.jpg`.
- `images/porta-blindata-intro.jpg`: fotografia orientata e ottimizzata da `20260429_130806.jpg`.
- `images/zanzariere-bettio-neoscenica.jpg`: immagine ufficiale Bettio da `https://www.bettio.it/media/207805/slide-neoscenica.jpg`.
- `images/persiana-alluminio-grigia.jpg`: fotografia orientata e ottimizzata da `IMG_1427.JPG`.
- `images/persiana-alluminio-verde.jpg`: fotografia ottimizzata da `Rif. Landi.jpg`.
- `images/scuro-alluminio-effetto-legno.jpg`: fotografia orientata e ottimizzata da `20260721_164159.jpg`; l'ispezione della Task 3 decide in modo esplicito se includerla nella pagina.
- `images/porte-interne-intro.jpg`: fotografia ottimizzata da `laccato bianca legno tranciato.jpg`.

---

### Task 1: Static Contract Tests

**Files:**
- Create: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: file HTML e asset presenti nella root del progetto.
- Produces: suite `python3 -m unittest tests.test_site_contract -v` che rileva immagini mancanti, integrazioni mancanti e regressioni sui requisiti principali.

- [ ] **Step 1: Write the failing site-contract tests**

Creare `tests/test_site_contract.py` con questa struttura:

```python
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
```

- [ ] **Step 2: Run the tests and verify the expected failures**

Run:

```bash
python3 -m unittest tests.test_site_contract -v
```

Expected: image-reference test passes; gallery, home, category-image and incorrect-copy tests fail because implementation is not present yet.

- [ ] **Step 3: Commit the tests**

```bash
git add tests/test_site_contract.py
git commit -m "test: define responsive gallery contracts"
```

---

### Task 2: Shared Product Gallery and Accessible Lightbox

**Files:**
- Create: `assets/product-gallery.css`
- Create: `assets/product-gallery.js`
- Modify: `infissi-pvc.html`
- Modify: `infissi-alluminio.html`
- Modify: `infissi-legno.html`
- Modify: `porte-blindate.html`
- Modify: `zanzariere.html`
- Modify: `persiane-scuri-alluminio.html`
- Modify: `porte-interne.html`
- Modify: `tende-caduta-sole.html`
- Modify: `falegnameria.html`

**Interfaces:**
- Consumes: immagini contenute in una sezione `.product-detail`.
- Produces: `window.CDProductGallery` con metodi `open(image)`, `close()` e inizializzazione automatica su `DOMContentLoaded`.

- [ ] **Step 1: Add the shared stylesheet**

Creare `assets/product-gallery.css` con:

```css
.product-intro-media {
  width: min(100%, 48rem);
  aspect-ratio: 4 / 3;
  margin-inline: auto;
  overflow: hidden;
  border-radius: 1.5rem;
  background: #f5f7fa;
}

.product-intro-media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-detail img[data-gallery-ready="true"] {
  cursor: zoom-in;
}

.product-detail img[data-gallery-ready="true"]:focus-visible,
.cd-lightbox__close:focus-visible {
  outline: 3px solid #fff;
  outline-offset: 4px;
}

.cd-lightbox {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: rgba(2, 6, 23, 0.92);
  opacity: 0;
  visibility: hidden;
  transition: opacity 180ms ease, visibility 180ms ease;
}

.cd-lightbox.is-open {
  opacity: 1;
  visibility: visible;
}

.cd-lightbox__figure {
  display: grid;
  gap: 0.75rem;
  max-width: min(92vw, 90rem);
  max-height: 90vh;
  margin: 0;
}

.cd-lightbox__image {
  display: block;
  max-width: 100%;
  max-height: 80vh;
  margin: auto;
  object-fit: contain;
  border-radius: 1rem;
}

.cd-lightbox__caption {
  color: #fff;
  text-align: center;
  font-size: 0.95rem;
}

.cd-lightbox__close {
  position: absolute;
  top: max(1rem, env(safe-area-inset-top));
  right: max(1rem, env(safe-area-inset-right));
  width: 3rem;
  height: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.72);
  color: #fff;
  font-size: 1.75rem;
  line-height: 1;
}

body.cd-lightbox-open { overflow: hidden; }

@media (min-width: 768px) {
  .product-intro-media { aspect-ratio: 3 / 2; }
}

@media (prefers-reduced-motion: reduce) {
  .cd-lightbox { transition: none; }
}
```

- [ ] **Step 2: Add the shared JavaScript**

Creare `assets/product-gallery.js` con una IIFE che:

```javascript
(function () {
  let activeTrigger = null;
  const overlay = document.createElement('div');
  overlay.className = 'cd-lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Anteprima immagine');
  overlay.innerHTML = `
    <button class="cd-lightbox__close" type="button" aria-label="Chiudi immagine">&times;</button>
    <figure class="cd-lightbox__figure">
      <img class="cd-lightbox__image" alt="">
      <figcaption class="cd-lightbox__caption"></figcaption>
    </figure>`;

  const fullImage = overlay.querySelector('.cd-lightbox__image');
  const caption = overlay.querySelector('.cd-lightbox__caption');
  const closeButton = overlay.querySelector('.cd-lightbox__close');

  function open(image) {
    activeTrigger = image;
    fullImage.src = image.currentSrc || image.src;
    fullImage.alt = image.alt || '';
    caption.textContent = image.alt || '';
    overlay.classList.add('is-open');
    document.body.classList.add('cd-lightbox-open');
    closeButton.focus();
  }

  function close() {
    if (!overlay.classList.contains('is-open')) return;
    overlay.classList.remove('is-open');
    document.body.classList.remove('cd-lightbox-open');
    fullImage.removeAttribute('src');
    if (activeTrigger) activeTrigger.focus();
    activeTrigger = null;
  }

  function initialize() {
    document.body.appendChild(overlay);
    document.querySelectorAll('.product-detail img').forEach((image) => {
      image.dataset.galleryReady = 'true';
      image.tabIndex = 0;
      image.setAttribute('role', 'button');
      image.setAttribute('aria-label', `Apri immagine: ${image.alt || 'prodotto'}`);
      image.addEventListener('click', () => open(image));
      image.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open(image);
        }
      });
    });
    closeButton.addEventListener('click', close);
    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) close();
    });
    document.addEventListener('keydown', (event) => {
      if (!overlay.classList.contains('is-open')) return;
      if (event.key === 'Escape') close();
      if (event.key === 'Tab') {
        event.preventDefault();
        closeButton.focus();
      }
    });
  }

  window.CDProductGallery = { open, close };
  document.addEventListener('DOMContentLoaded', initialize);
})();
```

- [ ] **Step 3: Integrate the shared files into every product page**

In ciascuna delle nove pagine:

1. aggiungere `<link rel="stylesheet" href="assets/product-gallery.css">` nel `<head>`;
2. aggiungere la classe `product-detail` alla sezione `<!-- DETTAGLIO -->`;
3. sostituire il contenitore introduttivo `h-64 md:h-96` con `product-intro-media`;
4. aggiungere `<script src="assets/product-gallery.js"></script>` prima di `</body>`.

- [ ] **Step 4: Run the focused tests**

```bash
python3 -m unittest tests.test_site_contract.SiteContractTests.test_every_product_page_loads_shared_gallery -v
```

Expected: PASS.

- [ ] **Step 5: Commit the shared gallery**

```bash
git add assets/product-gallery.css assets/product-gallery.js *.html
git commit -m "feat: add accessible product lightbox"
```

---

### Task 3: Import and Optimize Correct Product Images

**Files:**
- Create: `images/infissi-legno-intro.jpg`
- Create: `images/porta-blindata-intro.jpg`
- Create: `images/zanzariere-bettio-neoscenica.jpg`
- Create: `images/persiana-alluminio-grigia.jpg`
- Create: `images/persiana-alluminio-verde.jpg`
- Create: `images/scuro-alluminio-effetto-legno.jpg`
- Create: `images/porte-interne-intro.jpg`

**Interfaces:**
- Consumes: fotografie sorgente locali e URL ufficiale Bettio.
- Produces: JPEG orientati correttamente, profilo sRGB, lato lungo massimo 2000 px, qualità web circa 82–86%.

- [ ] **Step 1: Import the local candidates into a temporary directory**

Usare percorsi espliciti e non modificare i file sorgente:

```bash
mkdir -p /tmp/cd-design-assets
cp '/Users/feng/Desktop/ cd design immagini/20260623_122415.jpg' /tmp/cd-design-assets/infissi-legno-intro.jpg
cp '/Users/feng/Desktop/ cd design immagini/20260429_130806.jpg' /tmp/cd-design-assets/porta-blindata-intro.jpg
cp '/Users/feng/Desktop/ cd design immagini/IMG_1427.JPG' /tmp/cd-design-assets/persiana-alluminio-grigia.jpg
cp '/Users/feng/Desktop/ cd design immagini/Rif. Landi.jpg' /tmp/cd-design-assets/persiana-alluminio-verde.jpg
cp '/Users/feng/Desktop/ cd design immagini/20260721_164159.jpg' /tmp/cd-design-assets/scuro-alluminio-effetto-legno.jpg
cp '/Users/feng/Desktop/ cd design immagini/laccato bianca legno tranciato.jpg' /tmp/cd-design-assets/porte-interne-intro.jpg
```

- [ ] **Step 2: Download the official Bettio hero**

```bash
curl --fail --location --output /tmp/cd-design-assets/zanzariere-bettio-neoscenica.jpg 'https://www.bettio.it/media/207805/slide-neoscenica.jpg'
```

Verificare che il file sia un JPEG valido con `file /tmp/cd-design-assets/zanzariere-bettio-neoscenica.jpg`.

- [ ] **Step 3: Normalize orientation and resize without distortion**

Eseguire questo script con Pillow per applicare l'orientamento EXIF, convertire in RGB, limitare il lato lungo a 2000 px e salvare come JPEG progressivo qualità 84:

```bash
python3 - <<'PY'
from pathlib import Path
from PIL import Image, ImageOps

source = Path('/tmp/cd-design-assets')
destination = Path('images')
destination.mkdir(exist_ok=True)

for path in sorted(source.glob('*.jpg')):
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened).convert('RGB')
        image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        image.save(
            destination / path.name,
            format='JPEG',
            quality=84,
            optimize=True,
            progressive=True,
        )
PY
```

Controllare con:

```bash
for image in images/infissi-legno-intro.jpg images/porta-blindata-intro.jpg images/zanzariere-bettio-neoscenica.jpg images/persiana-alluminio-grigia.jpg images/persiana-alluminio-verde.jpg images/scuro-alluminio-effetto-legno.jpg images/porte-interne-intro.jpg; do
  file "$image"
  sips -g pixelWidth -g pixelHeight "$image"
done
```

Expected: tutti i file sono JPEG leggibili e nessun lato supera 2000 px.

- [ ] **Step 4: Visually inspect every imported image**

Confermare:

- finestra legno: serramento completo e materiale coerente;
- porta blindata: porta completa con bordi visibili;
- Bettio: zanzariera riconoscibile e nessun elemento UI dello screenshot;
- persiane/scuro: tipologia e materiale coerenti, senza dichiarare legno;
- porta interna: ambiente interno e porta chiaramente visibile.

Registrare l'esito dell'ispezione prima dell'editing HTML: se ferramenta, profilo e superficie confermano una chiusura in alluminio effetto legno, includere `scuro-alluminio-effetto-legno.jpg`; in caso contrario escluderla e usare soltanto `persiana-alluminio-grigia.jpg` e `persiana-alluminio-verde.jpg`.

- [ ] **Step 5: Commit the optimized assets**

```bash
git add images/infissi-legno-intro.jpg images/porta-blindata-intro.jpg images/zanzariere-bettio-neoscenica.jpg images/persiana-alluminio-grigia.jpg images/persiana-alluminio-verde.jpg images/scuro-alluminio-effetto-legno.jpg images/porte-interne-intro.jpg
git commit -m "assets: add corrected product photography"
```

---

### Task 4: Correct Product Page Photography and Copy

**Files:**
- Modify: `infissi-legno.html`
- Modify: `porte-blindate.html`
- Modify: `zanzariere.html`
- Modify: `persiane-scuri-alluminio.html`
- Modify: `porte-interne.html`

**Interfaces:**
- Consumes: asset creati nella Task 3 e classi della Task 2.
- Produces: pagine con fotografia introduttiva pertinente, card corrette e descrizioni coerenti.

- [ ] **Step 1: Correct the wood windows page**

In `infissi-legno.html`:

- sostituire l'introduzione con `images/infissi-legno-intro.jpg` e alt `Finestra con finitura legno installata da CD Design`;
- eliminare interamente la card che usa `images/foto-080.jpg` e il titolo `Finestra con scuri in legno`;
- mantenere le tre card restanti e verificarne alt e descrizioni.

- [ ] **Step 2: Correct the armored-door introduction**

In `porte-blindate.html`, usare `images/porta-blindata-intro.jpg` con alt `Porta blindata completa con finitura effetto legno installata da CD Design` e `object-fit: contain` ereditato da `.product-intro-media`.

- [ ] **Step 3: Correct the Bettio introduction**

In `zanzariere.html`, usare `images/zanzariere-bettio-neoscenica.jpg` con alt `Zanzariera Neoscenica Bettio installata su una finestra` e aggiungere sotto l'immagine una didascalia discreta `Immagine prodotto Bettio`.

- [ ] **Step 4: Correct aluminium shutters and explanatory copy**

In `persiane-scuri-alluminio.html`:

- usare `images/persiana-alluminio-grigia.jpg` come introduzione;
- sostituire le card non pertinenti con `images/persiana-alluminio-verde.jpg` e applicare l'esito esplicito dell'ispezione della Task 3 a `images/scuro-alluminio-effetto-legno.jpg`;
- eliminare il titolo `Scuri in legno`;
- aggiungere dopo la descrizione questo testo:

```html
<p class="text-brand-400 leading-relaxed max-w-2xl mb-10 text-base">
  La persiana utilizza lamelle inclinate per filtrare luce e aria; lo scuro è invece un pannello pieno, pensato per ottenere un oscuramento maggiore. Entrambi possono essere realizzati in alluminio, anche con finitura effetto legno.
</p>
```

- [ ] **Step 5: Correct the internal-door introduction**

In `porte-interne.html`, usare `images/porte-interne-intro.jpg` con alt `Porta interna bianca inserita in un ambiente contemporaneo`.

- [ ] **Step 6: Run category contract tests**

```bash
python3 -m unittest \
  tests.test_site_contract.SiteContractTests.test_incorrect_wood_shutter_card_is_removed \
  tests.test_site_contract.SiteContractTests.test_corrected_category_images_are_used \
  tests.test_site_contract.SiteContractTests.test_aluminium_page_does_not_claim_wood_products -v
```

Expected: PASS.

- [ ] **Step 7: Commit the category corrections**

```bash
git add infissi-legno.html porte-blindate.html zanzariere.html persiane-scuri-alluminio.html porte-interne.html
git commit -m "fix: align category photos with products"
```

---

### Task 5: Rebuild the Home Hero and Scroll-Aware Navigation

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: `images/hero.jpg`, existing menu controls and page anchors.
- Produces: `#siteNav`, `.home-hero`, `.home-hero__media`, `.home-hero__content` and scroll-driven `.is-scrolled` state.

- [ ] **Step 1: Add semantic hooks to the existing navigation and hero**

In `index.html`:

- assegnare `id="siteNav"` e classe `home-nav` al `<nav>`;
- assegnare `home-hero` alla hero;
- rinominare il blocco immagine in `.home-hero__media`;
- avvolgere il contenuto testuale in `.home-hero__content` senza cambiare link o testo.

- [ ] **Step 2: Add desktop and mobile hero CSS**

Aggiungere CSS con questi comportamenti:

```css
.home-nav {
  background: transparent;
  border-color: transparent;
  transition: background-color 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}

.home-nav.is-scrolled,
.home-nav.menu-open {
  background: rgba(255, 255, 255, 0.96);
  border-color: #eaeef4;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.home-hero { position: relative; }
.home-hero__media { position: absolute; inset: 0; overflow: hidden; background: #111827; }
.home-hero__media::before {
  content: '';
  position: absolute;
  inset: -2rem;
  background: url('images/hero.jpg') center / cover no-repeat;
  filter: blur(20px);
  opacity: 0.58;
}
.home-hero__media img { position: relative; width: 100%; height: 100%; object-fit: contain; }
.home-hero__media::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(2, 6, 23, 0.72) 0%, rgba(2, 6, 23, 0.34) 48%, rgba(2, 6, 23, 0.12) 100%);
}

@media (max-width: 767px) {
  .home-hero { display: grid; min-height: 0; padding: 0; background: #fff; }
  .home-hero__media { position: relative; height: min(62vh, 32rem); margin-top: 0; }
  .home-hero__media::after { background: linear-gradient(180deg, rgba(2,6,23,0.06), rgba(2,6,23,0.22)); }
  .home-hero__content { position: relative; background: #fff; color: #0f2d83; padding-block: 2rem 3rem; }
  .home-hero__content h1 { color: #0f2d83; font-size: clamp(2.25rem, 11vw, 3.25rem); }
  .home-hero__content p { color: #475569; }
}

@media (prefers-reduced-motion: reduce) {
  .home-nav { transition: none; }
}
```

Adattare i colori dei pulsanti mobile affinché restino leggibili sul fondo bianco, senza cambiare le destinazioni.

- [ ] **Step 3: Add scroll and menu state handling**

Nel JavaScript esistente della home:

```javascript
const siteNav = document.getElementById('siteNav');
function updateNavigationState() {
  siteNav.classList.toggle('is-scrolled', window.scrollY > 24);
}
window.addEventListener('scroll', updateNavigationState, { passive: true });
updateNavigationState();
```

Aggiornare `openMenu()` e `closeMenu()` per aggiungere/rimuovere `menu-open`, mantenendolo quando la pagina è già scrollata.

- [ ] **Step 4: Run the home contract test**

```bash
python3 -m unittest tests.test_site_contract.SiteContractTests.test_home_has_scroll_aware_navigation_and_split_hero -v
```

Expected: PASS.

- [ ] **Step 5: Commit the home refresh**

```bash
git add index.html
git commit -m "feat: improve responsive home hero"
```

---

### Task 6: Full Verification and Final Polish

**Files:**
- Modify only files that fail the checks above.

**Interfaces:**
- Consumes: completed implementation.
- Produces: verified static site with no broken images, JavaScript errors or responsive overflow.

- [ ] **Step 1: Run the complete static test suite**

```bash
python3 -m unittest tests.test_site_contract -v
```

Expected: all tests PASS.

- [ ] **Step 2: Validate HTML image paths independently**

```bash
python3 - <<'PY'
import re
from pathlib import Path
root = Path('.')
missing = []
for page in root.glob('*.html'):
    html = page.read_text(encoding='utf-8')
    for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if not src.startswith(('http://', 'https://', 'data:')) and not (root / src).is_file():
            missing.append(f'{page.name}: {src}')
if missing:
    raise SystemExit('\n'.join(missing))
print('All local image references resolve.')
PY
```

Expected: `All local image references resolve.`

- [ ] **Step 3: Verify responsive home layouts in a local browser**

Avviare `python3 -m http.server 8765 --bind 127.0.0.1` e controllare:

- 1440 × 900: fotografia intera o sensibilmente più ampia, overlay neutro, barra trasparente;
- dopo scroll: barra bianca con contrasto corretto;
- 390 × 844 e 320 × 568: immagine sopra, testo sotto, nessun overflow;
- menu aperto in cima: barra leggibile e menu non trasparente.

- [ ] **Step 4: Verify product pages and lightbox**

Su almeno una pagina breve e sulle pagine lunghe `zanzariere.html` e `porte-interne.html`:

- aprire introduzione e card con clic;
- aprire tramite `Enter` e barra spaziatrice;
- chiudere tramite X, sfondo e `Escape`;
- verificare ritorno del focus all'immagine;
- controllare che X resti visibile a 320 px;
- controllare che lo sfondo non scorra con lightbox aperta.

- [ ] **Step 5: Check browser console and reduced motion**

Expected: nessun errore JavaScript; con `prefers-reduced-motion: reduce` non sono presenti transizioni essenziali o animazioni obbligatorie.

- [ ] **Step 6: Review the final diff for unrelated changes**

```bash
git diff --check
git status --short
git diff -- index.html infissi-legno.html porte-blindate.html zanzariere.html persiane-scuri-alluminio.html porte-interne.html assets/product-gallery.css assets/product-gallery.js tests/test_site_contract.py
```

Verificare che cookie, privacy, modulo contatti e modifiche utente estranee non siano stati alterati.

- [ ] **Step 7: Commit verification fixes if needed**

```bash
git add index.html *.html assets/product-gallery.css assets/product-gallery.js tests/test_site_contract.py images/*.jpg
git commit -m "fix: polish product imagery and responsive behavior"
```

Eseguire il commit solo se la verifica ha richiesto correzioni aggiuntive.
