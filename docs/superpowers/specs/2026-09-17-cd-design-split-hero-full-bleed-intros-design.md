# CD Design Split Hero and Product Imagery Design

## Objective

Refine the existing site so the home page presents a clear editorial split on desktop, a legible image-led hero on mobile, and commercially coherent category imagery throughout the product pages.

## Home page

- At widths of 768px and above, the hero is divided into two equal columns: copy and calls to action on the left, a full-height photographic panel on the right.
- The desktop photo uses `object-fit: cover`, without blurred side fills or excessive zoom. Its crop is controlled with `object-position`.
- The fixed navigation remains transparent at the top and becomes white after scrolling.
- The brand is visually centered in the viewport; the menu trigger stays at the top right.
- The “Scopri i Prodotti” control opens the existing menu, expands the Prodotti submenu, and moves keyboard focus to the first product link.
- Below 768px, the photograph becomes the hero background. Copy and buttons sit in a compact lower overlay protected by a neutral gradient, leaving a meaningful portion of the photo unobstructed.
- Motion and keyboard behavior continue to respect accessibility requirements already present in the site.

## Product pages

- Every introductory category image fills its media slot using `object-fit: cover`.
- Intro media uses a consistent 4:3 ratio on small screens and 16:9 on larger screens.
- Each page may set a focal point with the shared `--intro-position` custom property rather than adding page-specific layout code.
- Images are chosen for commercial relevance and suitability for a landscape crop. Existing suitable photographs are retained; unsuitable portrait renders or unrelated imagery are replaced with better local assets.
- The Falegnameria page is rewritten around wood doors, windows, finishes, and restoration. Glass railings and iron structures are removed because they do not match the category.
- Product gallery enlargement and the existing accessible close button remain unchanged.

## Verification

- Contract tests cover the desktop/mobile hero hooks, product-menu action, full-bleed intro media, and Falegnameria category coherence.
- The full test suite must pass.
- Home and representative product pages are visually checked at desktop and mobile viewport sizes, including menu expansion and image crops.

