import fs from 'node:fs';
import path from 'node:path';
import { getSupabase } from '../lib/merit-demo-lib.mjs';

const ROOT = path.resolve(process.cwd());

function readJson(rel) {
  const p = path.join(ROOT, rel);
  return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const consumerId = process.env.MERIT_CONSUMER_ID || 'merit-demo';
  const gate = process.env.OPERATOR_GATE_HASH_SLOT_1 || '';

  if (req.method === 'GET') {
    const plus = readJson('cfg/plus_sku.json');
    const tenant = readJson('cfg/meritstore_tenant.json');
    const supabase = getSupabase();
    let override = null;
    if (supabase) {
      const { data } = await supabase
        .from('operator_pricing')
        .select('config, updated_at')
        .eq('consumer_id', consumerId)
        .maybeSingle();
      if (data?.config) override = data;
    }
    return res.status(200).json({
      consumer_id: consumerId,
      plus_sku: plus,
      meritstore_tenant: {
        offerings_seed: tenant.offerings_seed,
        revenue_split: tenant.revenue_split,
        status: tenant.status,
      },
      override,
      note: 'POST saves to Supabase operator_pricing when configured; sync offerings to meritstore via vault after cert.',
    });
  }

  if (req.method === 'POST') {
    const auth = req.headers.authorization || '';
    if (gate && !auth.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'operator_auth_required', hint: 'MeritAdminGate session or vault hash' });
    }
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    const supabase = getSupabase();
    if (!supabase) {
      return res.status(503).json({
        error: 'supabase_required',
        hint: 'Edit cfg/plus_sku.json locally or configure Supabase for cloud admin saves',
      });
    }
    const config = {
      default: body.default || body.plus_default,
      approved_price_points: body.approved_price_points || [],
    };
    if (!config.default?.monthly_billed_usd) {
      return res.status(400).json({ error: 'default.monthly_billed_usd required' });
    }
    const { error } = await supabase.from('operator_pricing').upsert({
      consumer_id: consumerId,
      config,
      updated_at: new Date().toISOString(),
    });
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ ok: true, consumer_id: consumerId, config });
  }

  return res.status(405).json({ error: 'method not allowed' });
}
