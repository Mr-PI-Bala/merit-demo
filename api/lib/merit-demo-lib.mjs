import { createClient } from '@supabase/supabase-js';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.cwd());

function loadLimits() {
  try {
    const raw = fs.readFileSync(path.join(ROOT, 'cfg/freemium_limits.json'), 'utf8');
    return JSON.parse(raw).guest_and_free || {};
  } catch {
    return { journal_entries_per_day: 2, ama_questions_per_day: 2, ama_votes_per_day: 2, ama_responses_per_day: 2, ama_leaderboard_visible: 25 };
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

export function startOfDay() {
  const d = new Date();
  d.setUTCHours(0, 0, 0, 0);
  return d.toISOString();
}

export { loadLimits };
