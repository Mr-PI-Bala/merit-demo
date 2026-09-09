(function () {
  function text(path, value) {
    document.querySelectorAll('[data-portal="' + path + '"]').forEach(function (node) {
      node.textContent = value || node.textContent;
    });
  }

  function link(label, href, secondary) {
    var a = document.createElement('a');
    a.className = 'button' + (secondary ? ' secondary' : '');
    a.href = href || '#';
    a.textContent = label || 'Open';
    return a;
  }

  function render(cfg) {
    cfg = cfg || {};
    var runtime = window.MERIT_DEMO_CONFIG || {};
    var brand = cfg.brand || {};
    text('brand.name', brand.name);
    text('brand.tagline', brand.tagline);
    text('brand.description', brand.description);
    text('footer', cfg.footer || 'MERIT Powered');
    if (brand.name) document.title = brand.name;

    var ctas = document.getElementById('portal-ctas');
    (cfg.ctas || []).forEach(function (cta, idx) {
      var href = cta.href;
      if (/workbench/i.test(cta.label || '')) href = '/play/';
      if (/register/i.test(cta.label || '')) href = runtime.meritstoreRegisterUrl || href;
      ctas.appendChild(link(cta.label, href, idx > 0));
    });

    var cards = document.getElementById('provider-cards');
    (cfg.providers || []).forEach(function (provider) {
      var card = document.createElement('article');
      card.className = 'card';
      var heading = document.createElement('h3');
      var summary = document.createElement('p');
      var anchor = document.createElement('a');
      heading.textContent = provider.name || 'MERIT provider';
      summary.textContent = provider.summary || '';
      anchor.href = provider.href || cfg.appBaseUrl || '#';
      anchor.textContent = provider.statusPath ? 'Open ' + provider.statusPath : 'Open';
      card.append(heading, summary, anchor);
      cards.appendChild(card);
    });

    var notes = document.getElementById('portal-notes');
    (cfg.notes || []).forEach(function (note) {
      var li = document.createElement('li');
      li.textContent = note;
      notes.appendChild(li);
    });
  }

  fetch('/portal/portal.json', { cache: 'no-store' })
    .then(function (res) { return res.json(); })
    .then(render)
    .catch(function () { render({}); });
})();

