import { getSupabase, loadLimits, tierFromRequest, startOfDay } from '../lib/merit-demo-lib.mjs';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const consumerId = process.env.MERIT_CONSUMER_ID || 'merit-demo';
  const limits = loadLimits();
  const tier = tierFromRequest(req);
  const supabase = getSupabase();

  if (req.method === 'GET') {
    if (!supabase) return res.status(200).json({ entries: [], mode: 'local_only' });
    const { data, error } = await supabase
      .from('journal_entries')
      .select('id, body, created_at')
      .eq('consumer_id', consumerId)
      .order('created_at', { ascending: false })
      .limit(50);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ entries: data || [], tier });
  }

  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    if (!supabase) {
      return res.status(503).json({ error: 'Supabase not configured; use local-only mode in browser' });
    }
    const cap = tier !== 'subscriber' ? limits.journal_entries_per_day : null;
    if (cap) {
      const { count } = await supabase
        .from('journal_entries')
        .select('id', { count: 'exact', head: true })
        .eq('consumer_id', consumerId)
        .gte('created_at', startOfDay());
      if ((count || 0) >= cap) {
        return res.status(402).json({ error: 'freemium_cap', message: 'Journal daily limit reached; upgrade to Plus' });
      }
    }
    const { data, error } = await supabase
      .from('journal_entries')
      .insert({ consumer_id: consumerId, subscriber_id: body.subscriber_id || 'guest', body: body.text })
      .select()
      .single();
    if (error) return res.status(500).json({ error: error.message });
    return res.status(201).json({ entry: data });
  }

  return res.status(405).json({ error: 'method not allowed' });
}
