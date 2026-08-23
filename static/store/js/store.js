(function () {
  const openModal = (name) => {
    const modal = document.querySelector(`[data-modal="${name}"]`);
    if (!modal) return;
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
  };

  const closeModals = () => {
    document.querySelectorAll('.modal.is-open').forEach((modal) => {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
    });
    document.body.classList.remove('modal-open');
  };

  document.addEventListener('click', (event) => {
    const openSearch = event.target.closest('[data-open-search]');
    const openCallback = event.target.closest('[data-open-callback]');
    const closeModal = event.target.closest('[data-close-modal]');
    if (openSearch) openModal('search');
    if (openCallback) openModal('callback');
    if (closeModal) closeModals();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeModals();
  });
})();
