/** Small consumer-owned session bridge for the public meritsubs contract. */
(function meritSession() {
  const root = document.getElementById('merit-session');
  if (!root || !window.MERIT_API) return;
  const cfg = window.MERIT_DEMO_CONFIG || {};
  const registerUrl = cfg.meritstoreRegisterUrl || '#';

  function esc(value) {
    const node = document.createElement('span');
    node.textContent = String(value || '');
    return node.innerHTML;
  }

  function subscriberLabel(session) {
    const sub = session?.subscriber || {};
    return sub.handle || sub.email || sub.subscriber_id || 'member';
  }

  function renderSignedIn(session) {
    root.innerHTML = `<div class="session-copy"><strong>Member session ready</strong><span>Signed in as ${esc(subscriberLabel(session))}. Cloud actions can use the provider session.</span></div><button type="button" class="secondary-button" data-session-action="signout">Sign out</button>`;
    root.dataset.state = 'ready';
    root.querySelector('[data-session-action="signout"]').onclick = () => {
      window.MERIT_API.clearSession();
      render();
    };
  }

  function render() {
    const session = window.MERIT_API.getSession();
    if (session) return renderSignedIn(session);
    root.dataset.state = 'anonymous';
    root.innerHTML = `<div class="session-copy"><strong>Try this app as a member</strong><span>Register free on MERIT, then continue here with the email you used. A guest preview stays local.</span><a href="${esc(registerUrl)}" target="_blank" rel="noreferrer">Open hosted registration</a></div><form class="session-form"><label><span>Email</span><input name="email" type="email" autocomplete="email" required placeholder="you@example.com"></label><button type="submit" class="primary-button">Continue with email</button></form><details class="session-guest"><summary>Preview as a guest</summary><form class="session-form"><label><span>Guest handle</span><input name="handle" minlength="2" maxlength="32" required placeholder="your-handle"></label><button type="submit" class="secondary-button">Start guest preview</button></form></details><p class="session-note" data-session-note>Cloud session is optional; local demo mode remains available.</p>`;
    const [emailForm, guestForm] = root.querySelectorAll('form');
    async function submit(form, mode) {
      const button = form.querySelector('button');
      const field = form.querySelector('input');
      button.disabled = true;
      root.dataset.state = 'checking';
      root.querySelector('[data-session-note]').textContent = 'Connecting to the MERIT identity service…';
      try {
        const session = await window.MERIT_API.onboard(mode, mode === 'guest' ? { handle: field.value } : { email: field.value });
        renderSignedIn(session);
        window.dispatchEvent(new CustomEvent('merit-session-ready', { detail: session }));
      } catch (error) {
        root.dataset.state = 'error';
        root.querySelector('[data-session-note]').textContent = `The provider session is unavailable (${error.message}). You can continue in local demo mode.`;
      } finally {
        button.disabled = false;
      }
    }
    emailForm.onsubmit = (event) => { event.preventDefault(); submit(emailForm, 'email'); };
    guestForm.onsubmit = (event) => { event.preventDefault(); submit(guestForm, 'guest'); };
  }

  render();
})();
