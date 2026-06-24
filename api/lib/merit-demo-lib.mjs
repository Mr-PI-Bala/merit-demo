import { createClient } from '@supabase/supabase-js';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.cwd());

function loadLimits() {
  try {
    const raw = fs.readFileSync(path.join(ROOT, 'cfg/freemium_limits.json'), 'utf8');
    return JSON.parse(raw).guest_and_free || {};
  } catch {
    return {
      journal_entries_per_day: 2,
      ama_questions_per_day: 2,
      ama_votes_per_day: 2,
      ama_responses_per_day: 2,
      ama_leaderboard_visible: 25,
    };
  }
}

export function getSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;
  if (!url || !key) return null;
  return createClient(url, key);
}

export function tierFromRequest(req) {
  const auth = req.headers.authorization || '';
  if (auth.startsWith('Bearer ') && auth.length > 20) return 'subscriber';
  return 'guest';
}

export function subscriberIdFromRequest(req, body = {}) {
  return body.subscriber_id || req.headers['x-subscriber-id'] || 'guest';
}

export function startOfDay() {
  const d = new Date();
  d.setUTCHours(0, 0, 0, 0);
  return d.toISOString();
}

/** Vercel geo headers (state/region); null when not on Vercel or unavailable. */
export function geoFromRequest(req) {
  const region = req.headers['x-vercel-ip-country-region'] || req.headers['x-vercel-ip-country'];
  const city = req.headers['x-vercel-ip-city'];
  if (!region && !city) return null;
  const regionGeo = region ? String(region) : String(city);
  return { region_geo: regionGeo, region_fine: city ? String(city) : null };
}

export async function countDailyActivity(supabase, { consumerId, subscriberId, action }) {
  const { count, error } = await supabase
    .from('ama_daily_activity')
    .select('id', { count: 'exact', head: true })
    .eq('consumer_id', consumerId)
    .eq('subscriber_id', subscriberId)
    .eq('action', action)
    .gte('created_at', startOfDay());
  if (error) throw new Error(error.message);
  return count || 0;
}

export async function recordDailyActivity(supabase, { consumerId, subscriberId, action, questionId }) {
  const row = {
    consumer_id: consumerId,
    subscriber_id: subscriberId,
    action,
    question_id: questionId || null,
  };
  const { error } = await supabase.from('ama_daily_activity').insert(row);
  if (error) throw new Error(error.message);
}

export async function checkFreemiumCap(supabase, { tier, limits, consumerId, subscriberId, action, capKey }) {
  if (tier === 'subscriber') return null;
  const cap = limits[capKey];
  if (!cap) return null;
  try {
    const count = await countDailyActivity(supabase, { consumerId, subscriberId, action });
    if (count >= cap) {
      return { status: 402, error: 'freemium_cap', message: `Daily ${action} limit reached; upgrade to Plus` };
    }
  } catch {
    // Table may not exist until 002 migration — fall through
  }
  return null;
}

export { loadLimits };
