-- merit-demo Supabase schema (consumer-scoped). Run in consumer Supabase project.
create table if not exists journal_entries (
  id uuid primary key default gen_random_uuid(),
  consumer_id text not null,
  subscriber_id text,
  body text not null,
  created_at timestamptz default now()
);

create table if not exists ama_questions (
  id uuid primary key default gen_random_uuid(),
  consumer_id text not null,
  subscriber_id text,
  handle text,
  region_geo text,
  region_profile text,
  show_fine_area boolean default false,
  anonymous_leaderboard boolean default false,
  body text not null,
  votes int default 0,
  created_at timestamptz default now()
);

create table if not exists ama_responses (
  id uuid primary key default gen_random_uuid(),
  question_id uuid references ama_questions(id) on delete cascade,
  subscriber_id text,
  body text not null,
  created_at timestamptz default now()
);

create index if not exists idx_ama_votes on ama_questions (consumer_id, votes desc);
