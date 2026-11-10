-- Rulează acest script în Supabase: SQL Editor → New query → lipești → Run.
-- Poate fi rulat și a doua oară (nu strică nimic și nu șterge date).

-- Tabelul vechi (versiunile dinainte de calendarul pe semestru). Aplicația îl citește o singură dată, la migrare.
create table if not exists public.orar_state (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  state      jsonb       not null,
  ts         bigint      not null default 0,
  updated_at timestamptz not null default now()
);

-- Tabelul folosit acum de aplicație.
create table if not exists public.orar_data (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  state      jsonb       not null,
  ts         bigint      not null default 0,
  updated_at timestamptz not null default now()
);

-- Fiecare utilizator vede și modifică DOAR rândul lui.
alter table public.orar_state enable row level security;
alter table public.orar_data  enable row level security;

drop policy if exists "orar: citire proprie"   on public.orar_state;
drop policy if exists "orar: inserare proprie" on public.orar_state;
drop policy if exists "orar: update propriu"   on public.orar_state;
drop policy if exists "orar: ștergere proprie" on public.orar_state;
create policy "orar: citire proprie"   on public.orar_state for select using ((select auth.uid()) = user_id);
create policy "orar: inserare proprie" on public.orar_state for insert with check ((select auth.uid()) = user_id);
create policy "orar: update propriu"   on public.orar_state for update using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "orar: ștergere proprie" on public.orar_state for delete using ((select auth.uid()) = user_id);

drop policy if exists "orar_data: citire proprie"   on public.orar_data;
drop policy if exists "orar_data: inserare proprie" on public.orar_data;
drop policy if exists "orar_data: update propriu"   on public.orar_data;
drop policy if exists "orar_data: ștergere proprie" on public.orar_data;
create policy "orar_data: citire proprie"   on public.orar_data for select using ((select auth.uid()) = user_id);
create policy "orar_data: inserare proprie" on public.orar_data for insert with check ((select auth.uid()) = user_id);
create policy "orar_data: update propriu"   on public.orar_data for update using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "orar_data: ștergere proprie" on public.orar_data for delete using ((select auth.uid()) = user_id);
