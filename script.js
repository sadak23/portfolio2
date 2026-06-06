const cursorGlow = document.querySelector('.cursor-glow');
window.addEventListener('mousemove', e => {
  if (!cursorGlow) return;
  cursorGlow.style.left = e.clientX + 'px';
  cursorGlow.style.top = e.clientY + 'px';
});

const particleWrap = document.getElementById('particles');
if (particleWrap) {
  for (let i = 0; i < 120; i++) {
    const p = document.createElement('span');
    p.className = 'particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.bottom = -(Math.random() * 220) + 'px';
    p.style.animationDuration = 18 + Math.random() * 28 + 's';
    p.style.animationDelay = Math.random() * 18 + 's';
    p.style.opacity = .18 + Math.random() * .65;
    particleWrap.appendChild(p);
  }
}

const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: .16 });
reveals.forEach(el => observer.observe(el));

const parallaxEls = document.querySelectorAll('.parallax');
function parallax() {
  const y = window.scrollY;
  parallaxEls.forEach(el => {
    const speed = parseFloat(el.dataset.speed || .08);
    el.style.transform = `translate3d(0,${y * speed}px,0) scale(1.04)`;
  });
}
window.addEventListener('scroll', parallax, { passive: true });
parallax();

const heroSlides = [];
if (typeof PORTFOLIO_DATA !== 'undefined') {
  const categories = ['events', 'exhibition', 'exterior', 'interior'];
  const catNames = {
    events: 'Event Design',
    exhibition: 'Exhibition',
    exterior: 'Architecture Exterior',
    interior: 'Architecture Interior'
  };

  // 1. Gather all items explicitly marked for the slideshow
  const slideshowItems = [];
  categories.forEach(cat => {
    (PORTFOLIO_DATA[cat] || []).forEach(item => {
      if (item.inSlideshow) {
        slideshowItems.push({
          src: item.image,
          category: item.slideshowCategory || item.category || catNames[cat],
          title: item.slideshowTitle || item.title || ''
        });
      }
    });
  });

  if (slideshowItems.length > 0) {
    heroSlides.push(...slideshowItems);
  } else {
    // Fallback: If no items have inSlideshow = true, use the featured images
    const featuredLists = {};
    categories.forEach(cat => {
      featuredLists[cat] = (PORTFOLIO_DATA[cat] || []).filter(item => item.featured);
    });
    const maxLen = Math.max(...categories.map(cat => featuredLists[cat].length));
    for (let i = 0; i < maxLen; i++) {
      categories.forEach(cat => {
        if (featuredLists[cat][i]) {
          const item = featuredLists[cat][i];
          heroSlides.push({
            src: item.image,
            category: item.slideshowCategory || item.category || catNames[cat],
            title: item.slideshowTitle || item.title || ''
          });
        }
      });
    }
  }
} else {
  // Fallback if PORTFOLIO_DATA is somehow not loaded
  heroSlides.push({ src: 'images/events/event-01.webp', category: 'Event Design', title: 'Qatar Airways Stage' });
}

const sliderImage = document.getElementById('heroSliderImage');
const sliderCaption = document.getElementById('heroSliderCaption');
const sliderDots = document.getElementById('heroSliderDots');
let currentSlide = 0;

if (sliderImage && sliderCaption && sliderDots) {
  // Clear any existing dots first, just in case
  sliderDots.innerHTML = '';
  
  heroSlides.forEach((_, i) => {
    const dot = document.createElement('span');
    if (i === 0) dot.classList.add('active');
    sliderDots.appendChild(dot);
  });
  const dots = sliderDots.querySelectorAll('span');

  function showSlide(index) {
    if (!heroSlides[index]) return;
    sliderImage.classList.add('changing');
    setTimeout(() => {
      sliderImage.src = heroSlides[index].src;
      
      // Update individual category/title elements if they exist (new markup)
      const catEl = document.getElementById('heroSliderCategory');
      const titleEl = document.getElementById('heroSliderTitle');
      if (catEl && titleEl) {
        catEl.textContent = heroSlides[index].category;
        titleEl.textContent = heroSlides[index].title;
      } else {
        // Fallback for old single-element markup
        sliderCaption.textContent = `${heroSlides[index].category} • ${heroSlides[index].title}`;
      }
      
      dots.forEach(d => d.classList.remove('active'));
      if (dots[index]) dots[index].classList.add('active');
      sliderImage.classList.remove('changing');
    }, 500);
  }

  // Set initial content if elements exist
  const catEl = document.getElementById('heroSliderCategory');
  const titleEl = document.getElementById('heroSliderTitle');
  if (catEl && titleEl && heroSlides[0]) {
    catEl.textContent = heroSlides[0].category;
    titleEl.textContent = heroSlides[0].title;
  } else if (sliderCaption && heroSlides[0]) {
    sliderCaption.textContent = `${heroSlides[0].category} • ${heroSlides[0].title}`;
  }

  setInterval(() => {
    currentSlide = (currentSlide + 1) % heroSlides.length;
    showSlide(currentSlide);
  }, 4200);
}

const videoCards = document.querySelectorAll('.video-card');
videoCards.forEach(card => {
  const video = card.querySelector('video');
  if (!video) return;
  if (card.classList.contains('showreel-card')) return;
  video.addEventListener('loadeddata', () => video.play().catch(() => {}));
  card.addEventListener('mouseenter', () => video.play().catch(() => {}));
  card.addEventListener('mouseleave', () => { video.pause(); video.currentTime = 0; });
});

const menuButton = document.querySelector('.menu-button');
const nav = document.querySelector('.nav');
if (menuButton && nav) {
  menuButton.addEventListener('click', () => nav.classList.toggle('mobile-open'));
}

// ==========================================
// V4 ADDITION: Cinematic Fullscreen Lightbox
// ==========================================
function openLightbox(src, title, category) {
  let lightbox = document.getElementById('portfolio-lightbox');
  if (!lightbox) {
    lightbox = document.createElement('div');
    lightbox.id = 'portfolio-lightbox';
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
      <button class="lightbox-close" aria-label="Close Lightbox">✕</button>
      <div class="lightbox-content">
        <img class="lightbox-image" src="" alt="" />
        <div class="lightbox-caption">
          <small class="lightbox-category"></small>
          <h3 class="lightbox-title"></h3>
        </div>
      </div>
    `;
    document.body.appendChild(lightbox);
    
    // Bind close events
    lightbox.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', e => {
      if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
        closeLightbox();
      }
    });
    
    // Escape key listener
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && lightbox.classList.contains('open')) {
        closeLightbox();
      }
    });
  }
  
  const img = lightbox.querySelector('.lightbox-image');
  const catEl = lightbox.querySelector('.lightbox-category');
  const titleEl = lightbox.querySelector('.lightbox-title');
  
  img.src = src;
  img.alt = title || 'Sadak Kalathil Portfolio';
  catEl.textContent = category || '';
  titleEl.textContent = title || '';
  
  // Trigger open animation
  lightbox.classList.add('open');
  document.body.style.overflow = 'hidden'; // Lock scroll
}

function closeLightbox() {
  const lightbox = document.getElementById('portfolio-lightbox');
  if (lightbox) {
    lightbox.classList.remove('open');
    document.body.style.overflow = ''; // Unlock scroll
  }
}

// Global double click event listener for project cards
document.addEventListener('dblclick', e => {
  const card = e.target.closest('.project-card');
  if (!card) return;
  
  const img = card.querySelector('img');
  if (!img) return;
  
  const small = card.querySelector('small');
  const h3 = card.querySelector('h3');
  
  const src = img.src;
  const title = h3 ? h3.textContent.trim() : (img.alt ? img.alt.trim() : '');
  const category = small ? small.textContent.trim() : '';
  
  openLightbox(src, title, category);
});
