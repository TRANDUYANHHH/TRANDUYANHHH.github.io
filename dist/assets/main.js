(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  menu?.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    nav.classList.toggle('is-open', expanded);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu) {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }
  });

  const grid = document.querySelector('[data-article-grid]');
  if (grid) {
    const search = document.querySelector('#search');
    const filters = [...document.querySelectorAll('[data-filter]')];
    const categorySelect = document.querySelector('#category');
    const cards = [...grid.querySelectorAll('.post-card')];
    const empty = document.querySelector('.empty-state');
    const status = document.querySelector('#search-status');
    let category = categorySelect.value;
    const normalize = text => text.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
    document.querySelector('[data-search-box]').hidden = false;
    document.querySelector('[data-filter-tools]').hidden = false;
    const update = () => {
      const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const matches = (!category || card.dataset.category === category) && terms.every(term => normalize(card.dataset.search).includes(term));
        card.hidden = !matches;
        if (matches) visible++;
      });
      empty.hidden = visible > 0;
      status.textContent = `${visible} bài viết được tìm thấy`;
      filters.forEach(filter => {
        const active = filter.dataset.filter === category;
        filter.classList.toggle('active', active);
        if (active) filter.setAttribute('aria-current', 'true');
        else filter.removeAttribute('aria-current');
      });
    };
    filters.forEach(filter => filter.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      category = filter.dataset.filter;
      update();
    }));
    search.addEventListener('input', update);
    categorySelect.addEventListener('change', () => { category = categorySelect.value; update(); });
    document.querySelector('[data-reset]').addEventListener('click', () => { category = ''; categorySelect.value = ''; search.value = ''; update(); search.focus(); });
    document.addEventListener('keydown', event => {
      if (event.key === '/' && !event.ctrlKey && !event.metaKey && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName) && !document.activeElement?.isContentEditable) {
        event.preventDefault(); search.focus();
      }
    });
    update();
    window.addEventListener('pageshow', () => { category = categorySelect.value; update(); });
  }

  const toast = document.querySelector('.toast');
  let timer;
  function notify(text) {
    toast.textContent = text;
    toast.classList.add('visible');
    clearTimeout(timer);
    timer = setTimeout(() => toast.classList.remove('visible'), 2400);
  }
  document.querySelectorAll('.codehilite').forEach(block => {
    const code = block.querySelector('pre');
    if (!code || !navigator.clipboard?.writeText) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-code';
    button.textContent = 'Sao chép';
    button.setAttribute('aria-label', 'Sao chép đoạn mã');
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(code.textContent); notify('Đã sao chép đoạn mã'); }
      catch { notify('Bạn có thể chọn đoạn mã và sao chép thủ công.'); }
    });
    block.append(button);
  });
  const copyLink = document.querySelector('[data-copy-link]');
  if (copyLink && navigator.clipboard?.writeText) {
    copyLink.hidden = false;
    copyLink.addEventListener('click', async () => {
      const status = document.querySelector('.copy-status');
      try { await navigator.clipboard.writeText(location.href); status.textContent = 'Đã sao chép!'; }
      catch { status.textContent = 'Hãy sao chép địa chỉ trên thanh trình duyệt.'; }
    });
  }
})();
