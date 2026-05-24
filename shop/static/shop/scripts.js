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