-- merit-demo: daily AMA activity for freemium cap enforcement (ask / vote / respond).
create table if not exists ama_daily_activity (
  id uuid primary key default gen_random_uuid(),
  consumer_id text not null,
  subscriber_id text not null,
  action text not null check (action in ('ask', 'vote', 'respond')),
  question_id uuid,
  created_at timestamptz default now()
);

create index if not exists idx_ama_activity_daily
  on ama_daily_activity (consumer_id, subscriber_id, action, created_at desc);

-- Optional: operator pricing overrides (admin UI → Supabase; sync to meritstore via vault).
create table if not exists operator_pricing (
  consumer_id text primary key,
  config jsonb not null,
  updated_at timestamptz default now()
);
