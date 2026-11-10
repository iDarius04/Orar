-- Rulează acest script o singură dată în Supabase: SQL Editor → New query → lipești → Run.
create table if not exists public.orar_state (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  state      jsonb       not null,
  ts         bigint      not null default 0,
  updated_at timestamptz not null default now()
);

-- Fiecare utilizator vede și modifică DOAR rândul lui.
alter table public.orar_state enable row level security;
create policy "orar: citire proprie"   on public.orar_state for select using ((select auth.uid()) = user_id);
create policy "orar: inserare proprie" on public.orar_state for insert with check ((select auth.uid()) = user_id);
create policy "orar: update propriu"   on public.orar_state for update using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "orar: ștergere proprie" on public.orar_state for delete using ((select auth.uid()) = user_id);
