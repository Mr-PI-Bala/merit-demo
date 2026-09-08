/** Public consumer request helpers. Providers remain authoritative for identity,
 * entitlements, quotas, and tenant isolation. */
(function meritApi() {
  const cfg = window.MERIT_DEMO_CONFIG || {};
  const consumerId = String(cfg.consumer_id || 'merit-demo');
  const apiBase = String(cfg.meteredApiBase || 'https://merit-prod.vercel.app').replace(/\/$/, '');

  function sessionToken() {
    const session = window.MERIT_SESSION || window.MeritSession;
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

  window.MERIT_API = Object.freeze({ consumerId, apiBase, headers, request });
})();
