import { createClient } from '@supabase/supabase-js';
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
    const top = limits.ama_leaderboard_visible || 25;
    if (!supabase) {
      return res.status(200).json({ questions: [], mode: 'local_only', top });
    }
    const { data, error } = await supabase
      .from('ama_questions')
      .select('id, body, votes, handle, region_geo, region_profile, anonymous_leaderboard, created_at')
      .eq('consumer_id', consumerId)
      .order('votes', { ascending: false })
      .limit(top);
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json({ questions: data || [], tier, top });
  }

  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    const action = body.action || 'ask';
    if (!supabase) {
      return res.status(503).json({ error: 'Supabase not configured; use local-only mode in browser' });
    }
    const subId = body.subscriber_id || req.headers['x-subscriber-id'] || 'guest';

    if (action === 'vote') {
      if (tier === 'guest' && limits.ama_votes_per_day) {
        const { count } = await supabase
          .from('ama_questions')
          .select('id', { count: 'exact', head: true })
          .eq('consumer_id', consumerId);
        void count;
      }
      const { data: q } = await supabase.from('ama_questions').select('votes').eq('id', body.question_id).single();
      if (!q) return res.status(404).json({ error: 'not found' });
      await supabase.from('ama_questions').update({ votes: (q.votes || 0) + 1 }).eq('id', body.question_id);
      return res.status(200).json({ ok: true });
    }

    if (action === 'respond') {
      const { error } = await supabase.from('ama_responses').insert({
        question_id: body.question_id,
        subscriber_id: subId,
        body: body.text,
      });
      if (error) return res.status(500).json({ error: error.message });
      return res.status(201).json({ ok: true });
    }

    const cap = tier === 'guest' ? limits.ama_questions_per_day : null;
    if (cap) {
      const { count } = await supabase
        .from('ama_questions')
        .select('id', { count: 'exact', head: true })
        .eq('consumer_id', consumerId)
        .gte('created_at', startOfDay());
      if ((count || 0) >= cap) {
        return res.status(402).json({ error: 'freemium_cap', message: 'AMA question daily limit reached; upgrade to Plus' });
      }
    }

    const { data, error } = await supabase
      .from('ama_questions')
      .insert({
        consumer_id: consumerId,
        subscriber_id: subId,
        body: body.text,
        handle: body.handle || null,
        region_geo: body.region_geo || null,
        region_profile: body.region_profile || null,
        show_fine_area: !!body.show_fine_area,
        anonymous_leaderboard: !!body.anonymous_leaderboard,
      })
      .select()
      .single();
    if (error) return res.status(500).json({ error: error.message });
    return res.status(201).json({ question: data });
  }

  return res.status(405).json({ error: 'method not allowed' });
}
