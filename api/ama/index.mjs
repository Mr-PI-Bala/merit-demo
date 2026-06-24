import {
  getSupabase,
  loadLimits,
  tierFromRequest,
  subscriberIdFromRequest,
  geoFromRequest,
  checkFreemiumCap,
  recordDailyActivity,
} from '../lib/merit-demo-lib.mjs';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Subscriber-Id');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const consumerId = process.env.MERIT_CONSUMER_ID || 'merit-demo';
  const limits = loadLimits();
  const tier = tierFromRequest(req);
  const supabase = getSupabase();

  if (req.method === 'GET') {
    const top = limits.ama_leaderboard_visible || 25;
    if (!supabase) {
      return res.status(200).json({ questions: [], mode: 'local_only', top, tier });
    }
    const { data, error } = await supabase
      .from('ama_questions')
      .select('id, body, votes, handle, region_geo, region_profile, anonymous_leaderboard, show_fine_area, created_at')
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
    const subId = subscriberIdFromRequest(req, body);

    if (action === 'vote') {
      const capErr = await checkFreemiumCap(supabase, {
        tier,
        limits,
        consumerId,
        subscriberId: subId,
        action: 'vote',
        capKey: 'ama_votes_per_day',
      });
      if (capErr) return res.status(capErr.status).json(capErr);

      const { data: q } = await supabase.from('ama_questions').select('votes').eq('id', body.question_id).single();
      if (!q) return res.status(404).json({ error: 'not found' });
      await supabase.from('ama_questions').update({ votes: (q.votes || 0) + 1 }).eq('id', body.question_id);
      try {
        await recordDailyActivity(supabase, {
          consumerId,
          subscriberId: subId,
          action: 'vote',
          questionId: body.question_id,
        });
      } catch {
        /* activity table optional until migration */
      }
      return res.status(200).json({ ok: true });
    }

    if (action === 'respond') {
      const capErr = await checkFreemiumCap(supabase, {
        tier,
        limits,
        consumerId,
        subscriberId: subId,
        action: 'respond',
        capKey: 'ama_responses_per_day',
      });
      if (capErr) return res.status(capErr.status).json(capErr);

      const { error } = await supabase.from('ama_responses').insert({
        question_id: body.question_id,
        subscriber_id: subId,
        body: body.text,
      });
      if (error) return res.status(500).json({ error: error.message });
      try {
        await recordDailyActivity(supabase, {
          consumerId,
          subscriberId: subId,
          action: 'respond',
          questionId: body.question_id,
        });
      } catch {
        /* optional */
      }
      return res.status(201).json({ ok: true });
    }

    const capErr = await checkFreemiumCap(supabase, {
      tier,
      limits,
      consumerId,
      subscriberId: subId,
      action: 'ask',
      capKey: 'ama_questions_per_day',
    });
    if (capErr) return res.status(capErr.status).json(capErr);

    const geo = geoFromRequest(req);
    const regionGeo = body.region_geo || geo?.region_geo || null;
    const regionProfile = body.region_profile || null;
    const showFine = !!body.show_fine_area && !!geo?.region_fine;
    const regionFine = showFine ? geo.region_fine : null;

    const { data, error } = await supabase
      .from('ama_questions')
      .insert({
        consumer_id: consumerId,
        subscriber_id: subId,
        body: body.text,
        handle: body.handle || null,
        region_geo: regionGeo,
        region_profile: regionProfile || regionFine,
        show_fine_area: showFine,
        anonymous_leaderboard: !!body.anonymous_leaderboard,
      })
      .select()
      .single();
    if (error) return res.status(500).json({ error: error.message });

    try {
      await recordDailyActivity(supabase, {
        consumerId,
        subscriberId: subId,
        action: 'ask',
        questionId: data.id,
      });
    } catch {
      /* optional */
    }
    return res.status(201).json({ question: data });
  }

  return res.status(405).json({ error: 'method not allowed' });
}
