// ==========================================
// starfield.js — Animated star canvas
// ==========================================

(function() {
  const canvas = document.getElementById('starfield');
  const ctx = canvas.getContext('2d');
  let stars = [];
  let animFrame;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function initStars() {
    stars = [];
    const count = Math.floor((canvas.width * canvas.height) / 6000);
    for (let i = 0; i < count; i++) {
      stars.push({
        x:     Math.random() * canvas.width,
        y:     Math.random() * canvas.height,
        r:     Math.random() * 1.3 + 0.15,
        o:     Math.random() * 0.7 + 0.1,
        speed: Math.random() * 0.012 + 0.002,
        phase: Math.random() * Math.PI * 2,
        hue:   Math.random() < 0.15 ? 'teal' : 'white',
      });
    }
  }

  function drawStars(t) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const s of stars) {
      const opacity = s.o * (0.5 + 0.5 * Math.sin(t * s.speed + s.phase));
      if (s.hue === 'teal') {
        ctx.fillStyle = `rgba(20,168,174,${opacity * 0.6})`;
      } else {
        ctx.fillStyle = `rgba(240,244,248,${opacity})`;
      }
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fill();
    }
    animFrame = requestAnimationFrame(drawStars);
  }

  resize();
  initStars();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { resize(); initStars(); }, 150);
  });

  requestAnimationFrame(drawStars);
})();
