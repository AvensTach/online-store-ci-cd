// Simple interactions: add a small click animation for product cards
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      // if click lands on a link, let it navigate
      if (e.target.closest('a')) return;
      const link = card.querySelector('a');
      if (link) {
        // quick visual effect then navigate
        card.style.transition = 'transform .12s ease';
        card.style.transform = 'scale(.99)';
        setTimeout(function () {
          window.location = link.href;
        }, 120);
      }
    });
  });
});
// gallery carousel
document.addEventListener('DOMContentLoaded', function () {
  const gallery = document.querySelector('.gallery');
  if (!gallery) return;

  const images = Array.from(gallery.querySelectorAll('.gallery-image'));
  const thumbs = Array.from(gallery.querySelectorAll('.thumb'));
  const prevBtn = gallery.querySelector('.gallery-btn.prev');
  const nextBtn = gallery.querySelector('.gallery-btn.next');

  let active = images.findIndex(img => img.classList.contains('active'));
  if (active < 0) active = 0;

  function show(index) {
    if (index < 0) index = images.length - 1;
    if (index >= images.length) index = 0;
    images.forEach((img, i) => img.classList.toggle('active', i === index));
    thumbs.forEach((t, i) => t.classList.toggle('active', i === index));
    active = index;
  }

  if (prevBtn) prevBtn.addEventListener('click', () => show(active - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => show(active + 1));

  thumbs.forEach(t => {
    t.addEventListener('click', () => {
      const i = parseInt(t.dataset.index, 10) || 0;
      show(i);
    });
  });

  // keyboard
  document.addEventListener('keydown', function (e) {
    if (!gallery.contains(document.activeElement)) {
      if (e.key === 'ArrowLeft') show(active - 1);
      if (e.key === 'ArrowRight') show(active + 1);
    }
  });

  // simple touch swipe
  let startX = 0;
  gallery.addEventListener('touchstart', function (e) {
    startX = e.touches[0].clientX;
  }, {passive: true});
  gallery.addEventListener('touchend', function (e) {
    const dx = e.changedTouches[0].clientX - startX;
    if (dx > 40) show(active - 1);
    else if (dx < -40) show(active + 1);
  });
});

// Sidebar toggle
document.addEventListener('DOMContentLoaded', function () {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarClose = document.getElementById('sidebarClose');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', openSidebar);
  }

  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }

  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  // Close sidebar on category link click
  document.querySelectorAll('.category-list a').forEach(link => {
    link.addEventListener('click', closeSidebar);
  });

  // Gallery carousel (existing code)
  const gallery = document.querySelector('.gallery');
  if (!gallery) return;

  const images = Array.from(gallery.querySelectorAll('.gallery-image'));
  const thumbs = Array.from(gallery.querySelectorAll('.thumb'));
  const prevBtn = gallery.querySelector('.gallery-btn.prev');
  const nextBtn = gallery.querySelector('.gallery-btn.next');

  let active = images.findIndex(img => img.classList.contains('active'));
  if (active < 0) active = 0;

  function show(index) {
    if (index < 0) index = images.length - 1;
    if (index >= images.length) index = 0;
    images.forEach((img, i) => img.classList.toggle('active', i === index));
    thumbs.forEach((t, i) => t.classList.toggle('active', i === index));
    active = index;
  }

  if (prevBtn) prevBtn.addEventListener('click', () => show(active - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => show(active + 1));

  thumbs.forEach(t => {
    t.addEventListener('click', () => {
      const i = parseInt(t.dataset.index, 10) || 0;
      show(i);
    });
  });

  document.addEventListener('keydown', function (e) {
    if (!gallery.contains(document.activeElement)) {
      if (e.key === 'ArrowLeft') show(active - 1);
      if (e.key === 'ArrowRight') show(active + 1);
    }
  });

  let startX = 0;
  gallery.addEventListener('touchstart', function (e) {
    startX = e.touches[0].clientX;
  }, {passive: true});
  gallery.addEventListener('touchend', function (e) {
    const dx = e.changedTouches[0].clientX - startX;
    if (dx > 40) show(active - 1);
    else if (dx < -40) show(active + 1);
  });
});