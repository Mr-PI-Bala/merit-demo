const DEFAULT_MERITSTORE = 'https://meritstore.vercel.app';

function json(res, status, body) {
  res.status(status).json(body);
}

function providerBase() {
  return (process.env.MERITSUBS_PROVIDER_BASE_URL || `${DEFAULT_MERITSTORE}/api/meritsubs`).replace(/\/$/, '');
}

function meritstoreBase() {
  return (process.env.MERITSTORE_BASE_URL || DEFAULT_MERITSTORE).replace(/\/$/, '');
}

function defaultPromo() {
  return (process.env.MERIT_DEFAULT_PROMOCODE || 'MERITAGENT').trim().toUpperCase();
}

async function proxyProvider(req, res, path) {
  const target = `${providerBase()}${path}`;
  const headers = { 'content-type': 'application/json' };
  if (req.headers.authorization) headers.authorization = req.headers.authorization;
  const init = { method: req.method, headers };
  if (!['GET', 'HEAD'].includes(req.method)) {
    init.body = typeof req.body === 'string' ? req.body : JSON.stringify(req.body || {});
  }
  const upstream = await fetch(target, init);
  const text = await upstream.text();
  res.status(upstream.status);
  res.setHeader('content-type', upstream.headers.get('content-type') || 'application/json');
  return res.send(text);
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const consumerId = process.env.MERIT_CONSUMER_ID || 'merit-demo';
  const promoCode = defaultPromo();
  const introCreditUsd = Number(process.env.MERIT_INTRO_CREDIT_USD || '25');

  const rawUrl = req.url || '/api/meritsubs';
  const path = rawUrl.replace(/^\/api\/meritsubs/, '') || '/api/v1/health';

  if (req.method === 'GET' && (path === '/' || path === '/api/v1/health')) {
    return json(res, 200, {
      service: 'meritsubs-relay',
      mode: 'hosted_provider_boundary',
      consumer_id: consumerId,
      provider_base_url: providerBase(),
      meritstore_base_url: meritstoreBase(),
      default_promocode: promoCode,
      intro_credit_usd: introCreditUsd,
      note: 'Public merit-demo does not embed meritsubs billing or entitlement source code.',
    });
  }

  if (req.method === 'GET' && path === '/api/v1/entitlements') {
    try {
      return await proxyProvider(req, res, path);
    } catch {
      return json(res, 200, {
        tier: 'guest',
        grants: {},
        mode: 'hosted_provider_unavailable_guest_only',
        default_promocode: promoCode,
      });
    }
  }

  if (req.method === 'POST' && path.includes('/checkout/meritstore')) {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    const tenant = body.tenant || consumerId;
    const plan = body.plan || 'plus-monthly';
    const affiliate = (body.affiliate_code || consumerId).toString().toUpperCase();
    const checkoutUrl =
      `${meritstoreBase()}/${encodeURIComponent(tenant)}/register?` +
      `plan=${encodeURIComponent(plan)}&promo=${encodeURIComponent(promoCode)}` +
      `&affiliate=${encodeURIComponent(affiliate)}`;
    return json(res, 200, {
      checkout_url: checkoutUrl,
      tenant,
      plan,
      promo_code: promoCode,
      affiliate_code: affiliate,
      intro_credit_usd: introCreditUsd,
      authority: 'hosted_meritstore',
    });
  }

  try {
    return await proxyProvider(req, res, path);
  } catch (err) {
    return json(res, 502, {
      error: 'hosted_meritsubs_unavailable',
      message: err instanceof Error ? err.message : 'provider request failed',
    });
  }
}
