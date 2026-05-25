// Dynamic Portfolio Loader
// This script dynamically populates the portfolio cards based on the centralized PORTFOLIO_DATA database.
// It executes instantly when loaded at the bottom of the body, before script.js initializes animations.

(function() {
  function renderIndexGrids() {
    const categories = ['exterior', 'interior', 'events', 'exhibition'];
    
    categories.forEach(cat => {
      const grid = document.getElementById(`${cat}-grid`);
      if (!grid) return;
      
      grid.innerHTML = '';
      const items = (PORTFOLIO_DATA[cat] || []).filter(item => item.featured);
      
      items.forEach((item, index) => {
        const card = document.createElement('article');
        card.className = 'project-card reveal';
        
        // Preserve original layout design:
        // - First card of Exterior and Interior sections gets the 'large' size class
        // - First and fourth cards of Events and Exhibition sections get the 'wide' size class
        if (cat === 'exterior' || cat === 'interior') {
          if (index === 0) card.classList.add('large');
        } else if (cat === 'events' || cat === 'exhibition') {
          if (index === 0 || index === 3) card.classList.add('wide');
        }
        
        // Respect any custom sizeClass overridden in the database
        if (item.sizeClass) {
          card.classList.add(item.sizeClass);
        }
        
        // Image Crop/Fit Mode
        if (item.cropMode === 'contain') {
          card.classList.add('contain-fit');
        }
        
        card.innerHTML = `
          <img src="${item.image}" alt="${item.title}" />
          <div class="shine ${cat === 'events' || cat === 'exhibition' ? 'slow' : ''}"></div>
          <div>
            <small>${item.category}</small>
            <h3>${item.title}</h3>
          </div>
        `;
        
        grid.appendChild(card);
      });
    });
  }

  function renderGalleryGrid() {
    const grid = document.getElementById('gallery-grid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    // Determine category from file name in URL
    let cat = '';
    const path = window.location.pathname.toLowerCase();
    if (path.includes('exterior')) cat = 'exterior';
    else if (path.includes('interior')) cat = 'interior';
    else if (path.includes('events')) cat = 'events';
    else if (path.includes('exhibition')) cat = 'exhibition';
    
    if (!cat || !PORTFOLIO_DATA[cat]) return;
    
    const items = PORTFOLIO_DATA[cat];
    items.forEach(item => {
      const card = document.createElement('article');
      card.className = 'project-card reveal';
      
      if (item.sizeClass) {
        card.classList.add(item.sizeClass);
      }
      
      // Image Crop/Fit Mode
      if (item.cropMode === 'contain') {
        card.classList.add('contain-fit');
      }
      
      card.innerHTML = `
        <img src="${item.image}" alt="${item.title}" />
        <div class="shine slow"></div>
        <div>
          <small>${item.category}</small>
          <h3>${item.title}</h3>
        </div>
      `;
      
      grid.appendChild(card);
    });
  }

  // Run dynamic loads
  if (typeof PORTFOLIO_DATA !== 'undefined') {
    renderIndexGrids();
    renderGalleryGrid();
  } else {
    console.error("PORTFOLIO_DATA is not defined. Ensure portfolio-data.js is loaded first.");
  }
})();
