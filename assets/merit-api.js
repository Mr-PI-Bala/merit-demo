/** Public consumer request helpers. Providers remain authoritative for identity,
 * entitlements, quotas, and tenant isolation. */
(function meritApi() {
  const cfg = window.MERIT_DEMO_CONFIG || {};
  const consumerId = String(cfg.consumer_id || 'merit-demo-alpha');
  const apiBase = String(cfg.meteredApiBase || 'https://merit-prod.vercel.app').replace(/\/$/, '');
  const gatewayPrefix = String(cfg.gatewayApiPrefix || '/api/gw').replace(/\/$/, '');
  const sessionKey = `merit-demo:session:${consumerId}`;

  function readStoredSession() {
    try {
      const raw = window.sessionStorage.getItem(sessionKey);
      if (!raw) return null;
      const value = JSON.parse(raw);
      if (!value || value.consumer_id !== consumerId || !value.token) return null;
      return value;
    } catch {
      return null;
    }
  }

  function getSession() {
    return window.MERIT_SESSION || window.MeritSession || readStoredSession();
  }

  function setSession(value) {
    const session = {
      token: String(value?.token || ''),
      consumer_id: consumerId,
      subscriber: value?.subscriber || null,
      saved_at: new Date().toISOString(),
    };
    if (!session.token) throw new Error('Provider returned no session token');
    try { window.sessionStorage.setItem(sessionKey, JSON.stringify(session)); } catch { /* private browsing */ }
    window.MERIT_SESSION = session;
    return session;
  }

  function clearSession() {
    try { window.sessionStorage.removeItem(sessionKey); } catch { /* private browsing */ }
    delete window.MERIT_SESSION;
    delete window.MeritSession;
  }

  function sessionToken() {
    const session = getSession();
    if (session && typeof session === 'object') {
      return session.access_token || session.accessToken || session.token || '';
    }
    return '';
  }

  function headers(extra = {}) {
    const result = { 'X-Merit-Consumer': consumerId, ...extra };
    const token = sessionToken();
    if (token) result.Authorization = `Bearer ${token}`;
    return result;
  }

  function request(path, options = {}) {
    const requestOptions = { credentials: 'include', ...options };
    requestOptions.headers = headers(requestOptions.headers || {});
    return fetch(`${apiBase}${path}`, requestOptions);
  }

  function rail(service, suffix = '') {
    const cleanService = String(service || '').replace(/^\/+|\/+$/g, '');
    const cleanSuffix = String(suffix || '').replace(/^\/+/, '');
    return `${gatewayPrefix}/${cleanService}${cleanSuffix ? `/${cleanSuffix}` : ''}`;
  }

  async function onboard(mode, fields = {}) {
    const route = mode === 'guest' ? 'guest' : 'email';
    const body = route === 'guest'
      ? { handle: String(fields.handle || '').trim(), consumer_id: consumerId }
      : { email: String(fields.email || '').trim(), consumer_id: consumerId };
    const response = await request(rail('meritsubs', `api/v1/subscribers/onboard/${route}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(10000),
    });
    let data = null;
    try { data = await response.json(); } catch { /* provider may return text */ }
    if (!response.ok) {
      const detail = data?.detail || data?.message || data?.error || `Provider returned HTTP ${response.status}`;
      throw new Error(String(detail));
    }
    return setSession(data);
  }

  async function entitlements() {
    const response = await request(rail('meritsubs', 'api/v1/entitlements'), {
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) throw new Error(`Provider returned HTTP ${response.status}`);
    return response.json();
  }

  window.MERIT_API = Object.freeze({
    consumerId, apiBase, gatewayPrefix, headers, request, rail,
    getSession, setSession, clearSession, onboard, entitlements,
  });
})();
