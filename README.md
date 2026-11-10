# Orarul meu (cu cont propriu, Supabase)

Site static: îl pui pe un hosting gratuit, te autentifici cu emailul și parola ta, iar orarul (schimburi de laborator, program de muncă, modificări pe săptămâni) se sincronizează între laptop și telefon.

## Pașii (≈15 minute)

1. **Proiect Supabase.** Cont gratuit pe supabase.com → *New project* (alege o parolă pentru baza de date și o regiune din Europa).
2. **Tabelul.** În proiect: *SQL Editor* → *New query* → lipești conținutul din `schema.sql` → *Run*. Asta creează tabelele `orar_data` (folosit de aplicație) și `orar_state` (vechi, citit doar la migrare) și regulile (RLS) care permit fiecărui utilizator să-și vadă doar datele.
3. **Cheile.** *Project Settings → API* (sau *API Keys*): copiezi **Project URL** și cheia **anon / publishable**. Le pui în `config.js`. Cheia anon e publică prin design; **nu pune niciodată cheia `service_role`**.
4. **Autentificare.** *Authentication → Providers → Email*: pentru uz personal poți dezactiva *Confirm email* (altfel primești un email de confirmare la crearea contului).
5. **Hosting.** Pune folderul pe un hosting static gratuit: Netlify (Drop: tragi folderul în pagină), Cloudflare Pages, Vercel sau GitHub Pages. Rezultă un link `https://…`.
6. **URL-ul site-ului.** În Supabase: *Authentication → URL Configuration* → *Site URL* = linkul de la pasul 5.
7. **Contul.** Deschizi linkul, apeși *Creează cont* (email + parolă), apoi te autentifici.
8. **Blochezi înregistrările noi** (recomandat): *Authentication → Sign In / Providers* → dezactivezi *Allow new users to sign up*. Contul tău rămâne.

## Pe telefon
Deschizi același link în browser și te autentifici cu același email și aceeași parolă. Apoi *Adaugă pe ecranul principal* (Chrome: meniu ⋮ → *Install app*; iPhone/Safari: *Share → Add to Home Screen*). Se comportă ca o aplicație.

## Cum funcționează
- Datele sunt într-un singur rând pe utilizator (`orar_data`, JSON). Ultima modificare câștigă; aplicația verifică la fiecare 20 de secunde și când revii în pagină.
- Funcționează și offline (se deschide din cache), iar modificările se trimit când ai din nou internet.
- *Exportă datele (.json)* / *Importă din fișier* pentru copii de siguranță.

## De știut
- Proiectele Supabase gratuite se pun în pauză după ~1 săptămână fără activitate; le reactivezi dintr-un click în panou. Exportul JSON e plasa ta de siguranță.
- Dacă nu completezi `config.js`, aplicația merge doar local (butonul *Continuă fără cont*).
