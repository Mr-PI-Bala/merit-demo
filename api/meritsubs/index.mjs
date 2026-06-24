import fs from 'node:fs';
import path from 'node:path';

function loadPlus() {
  try {
    const raw = fs.readFileSync(path.join(process.cwd(), 'cfg/plus_sku.json'), 'utf8');
    return JSON.parse(raw).default || {};
  } catch {
    return { monthly_billed_usd: 10.79, name: 'Plus' };
  }
}

export default async function handler(req, res) {
  const consumerId = process.env.MERIT_CONSUMER_ID || 'merit-demo';
  const url = new URL(req.url || '', 'http://localhost');
  const pathname = url.pathname.replace(/\/$/, '') || '/api/meritsubs';

  if (req.method === 'GET' && (pathname.endsWith('/health') || pathname === '/api/meritsubs')) {
    return res.status(200).json({
      consumer_id: consumerId,
      mode: 'merit-demo-stub',
      version: '0.3.0',
      note: 'Wire vendor/meritsubs for production OAuth; guest tier active',
    });
  }

  if (pathname.includes('/entitlements') || pathname.includes('/api/v1/entitlements')) {
    const auth = req.headers.authorization || '';
    const tier = auth.startsWith('Bearer ') ? 'subscriber' : 'guest';
    const plus = loadPlus();
    return res.status(200).json({
      consumer_id: consumerId,
      tier,
      features: {
        journal_uncapped: tier !== 'guest',
        ama_uncapped: tier !== 'guest',
        par_pin: tier !== 'guest' ? 'merit_workbench@1.0.x' : 'merit_workbench@0.4.0',
      },
      upgrade_url: `https://meritstore.vercel.app/${consumerId}/register`,
      plus_sku_usd_monthly: plus.monthly_billed_usd,
    });
  }

  if (pathname.includes('/legal/terms') || pathname.endsWith('/terms')) {
    return res.status(200).json({ terms_url: '/legal.html', consumer_id: consumerId });
  }

  return res.status(404).json({ error: 'meritsubs route not implemented in demo stub', consumer_id: consumerId });
}
