'use strict';
const canvas = document.querySelector('#preview');
const ctx = canvas.getContext('2d');
const play = document.querySelector('#play');
const restart = document.querySelector('#restart');
const speed = document.querySelector('#speed');
const timeline = document.querySelector('#timeline');
const status = document.querySelector('#status');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let playing = !reducedMotion.matches, current = 0, last = null, elapsed = 0, ready = false;
const sheet = new Image();
function draw() {
  ctx.drawImage(sheet, (current % 8) * 480, Math.floor(current / 8) * 480, 480, 480, 0, 0, 480, 480);
  timeline.value = current;
}
function update() {
  play.textContent = playing ? 'Pause' : 'Play';
  play.setAttribute('aria-label', playing ? 'Pause animation' : 'Play animation');
  status.textContent = playing ? 'Playing · seamless preview loop' : 'Paused · choose a frame or press Play';
}
function tick(now) {
  if (last !== null && playing && !document.hidden) {
    elapsed += (now - last) * Number(speed.value);
    if (elapsed >= 60) {
      current = (current + Math.floor(elapsed / 60)) % 48;
      elapsed %= 60;
      draw();
    }
  }
  last = now;
  requestAnimationFrame(tick);
}
sheet.onload = () => {
  if (!ctx) { status.textContent = 'Preview unavailable. Open or download the GIF below.'; return; }
  ready = true; draw();
  for (const control of [play, restart, speed, timeline]) control.disabled = false;
  update(); requestAnimationFrame(tick);
};
sheet.onerror = () => { status.textContent = 'Preview could not load. Try reloading, or open the original GIF below.'; };
play.addEventListener('click', () => { playing = !playing; last = null; update(); });
restart.addEventListener('click', () => { current = 0; elapsed = 0; last = null; draw(); update(); });
timeline.addEventListener('input', () => { playing = false; current = Number(timeline.value); elapsed = 0; draw(); update(); });
document.addEventListener('visibilitychange', () => { last = null; });
reducedMotion.addEventListener('change', () => { if (reducedMotion.matches && ready) { playing = false; update(); } });
sheet.src = './assets/frames.png';
