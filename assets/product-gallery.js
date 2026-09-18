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
  const figure = overlay.querySelector('.cd-lightbox__figure');
  const caption = overlay.querySelector('.cd-lightbox__caption');
  const closeButton = overlay.querySelector('.cd-lightbox__close');

  function open(image) {
    activeTrigger = image;
    figure.className = 'cd-lightbox__figure';
    if (image.dataset.lightboxCrop) {
      figure.classList.add(`cd-lightbox__figure--${image.dataset.lightboxCrop}`);
    }
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
    figure.className = 'cd-lightbox__figure';
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
