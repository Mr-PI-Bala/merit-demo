/** SomaTune-style header/footer + operator branding from window.MERIT_DEMO_CONFIG */
(function meritShell() {
  const cfg = window.MERIT_DEMO_CONFIG || {};
  const b = cfg.branding || {};
  const product = b.product_name || 'MERIT Demo';
  const header = document.getElementById('merit-header');
  const footer = document.getElementById('merit-footer');
  if (header) {
    header.innerHTML = `<div class="merit-header-inner"><strong>${product}</strong><nav><a href="/play/">Play</a> · <a href="/journal/">Journal</a> · <a href="/ama/">AMA</a></nav></div>`;
    if (b.primary_color) header.style.borderBottomColor = b.primary_color;
  }
  if (footer && b.footer) {
    const powered = b.footer.show_merit_powered
      ? `<a href="${b.footer.merit_powered_url || '#'}">${b.footer.merit_powered_label || 'MERIT Powered'}</a>`
      : '';
    const abuse = b.footer.abuse_report_email
      ? ` · <a href="mailto:${b.footer.abuse_report_email}?subject=Abuse%20report">Report abuse</a>`
      : '';
    footer.innerHTML = `<small>${powered}${abuse}</small>`;
  }
  document.documentElement.style.setProperty('--merit-primary', b.primary_color || '#1d4ed8');
})();
