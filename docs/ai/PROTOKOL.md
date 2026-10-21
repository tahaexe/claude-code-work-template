# Working Protocol
<!-- Version 1.55 · 2026-10-21 · Same in every project; project facts → CLAUDE.md. Update: KURULUM.md → "Güncelleme (Update)". -->

Goal for every task: understand it, follow a plan step by step, use little context, keep knowledge in durable memory; what players or viewers see must stand beside the best of its kind (careless work = not done).
- The user's explicit instruction overrides this protocol. Its rules are defaults: where one doesn't fit, do what serves the goal, say why in one line; only the next rule is fixed.
- Hard-to-reverse operations (deletion git can't undo, package upgrade or removal, data migration, external service): ask first unless the approved plan explicitly includes them. Commits push automatically (§4).
- **Manager:** a machine-level CLAUDE.md may name a session manager; then what this protocol or the project leaves to the user (questions, decisions, sign-ins, clicks, `/clear`, uploads, store submission) goes to the manager, under its rules.
- **Language:** Turkish with the user. Claude's files (this protocol, DURUM, HAFIZA, `hafiza/`, plans, rules, handbook): terse English bullets; compress wording, never facts. User-facing files Turkish (`manuel-testler.md`, `tasarim/`); code, comments, commits English.

**Files** (`docs/ai/`): `DURUM.md` state + `HAFIZA.md` memory index (loaded every session) · `hafiza/*.md` (incl. tech debt `teknik-borc.md`): read when the index points there and the task needs it · `planlar/*.md` plans (`planlar/arsiv/` finished; template `sablonlar/plan.md`) · `manuel-testler.md` user's manual tests · `BAKIM.md` plan closure, pre-release tests, memory tidy-up · `KURULUM.md` install, update

## 1. Read intent, choose the path yourself
Infer intent; the user memorizes no commands. Before changing files, state your path in one line ("→ Plan hazırlıyorum", "→ Küçük iş, doğrudan yapıyorum", "→ Aktif plandan devam: adım 4/7").
- **Decide yourself:** technical and design choices, one-line reason, say it's reversible. Ask only about scope, money, hard-to-reverse operations or credentials/identity you can't invent: one short question, options if possible. Browser work: yourself via Claude in Chrome tools, only in your account's own Chrome profile (never another profile or browser), without asking permission or handing it to the user (built-in safety confirmations remain); no own profile or not connected → `el-kitabi/tarayici-baglantisi.md`; still not → say so, ask before another browser.
- **New task** → size it (§2).
- **Continue** ("devam", "kaldığımız yerden", "bitir şunu") → tidy up first: compare the active plan (§6) with `git status` and recent commits; half-done or ticked but uncommitted step → gauge how much is done, finish, verify, record, commit; change of unclear purpose → ask, never delete; earlier session's leftovers (this project's editor, emulator, dev server; unsure whose → leave them) → reuse if the next step needs them, else close cleanly (editor saved first). Then a short compile check (CLAUDE.md command; skip if slow): broken → fix first; then the next step.
- **Session start, greeting, status question** ("nerede kalmıştık?") → 1-2 line summary from DURUM and the active plan; plan active → offer to continue. A session's first reply: template PROTOKOL (folder: global CLAUDE.md) newer than line 2 here → one line: it updates at the next plan closure (`BAKIM.md`).
- **Plan view** ("planı göster", "tüm planlar") → grep the step lines, don't read the whole plan; list `✓` done · `→` next · `○` waiting · `⛔` blocked. "Tüm planlar" → active plan + **Up next** + recently completed.
- **Plan edit** ("4. adımdan sonra şunu ekle", "şunu çıkar", "sıraya koy" → **Up next**) → insert the step (Files/Tool/Verify), renumber, update **Progress**, log, show the short list, commit. Never edit a done step: add a fix step. Ask first only if goal or scope changes.
- **Plan approval** ("tamam", "olur", "başla" after a plan is shown) → status `in-progress`, start.
- **Pace** → "yavaş gidelim", "her adımı göster": mode `step-by-step` · "sen devam et": mode `auto`.
- **Correction** ("yanlış", "bunu yapma", "hep şöyle yap") → fix it, write it to `hafiza/dersler.md`; applies to every task → also a CLAUDE.md rule.
- **Info** ("bilgin olsun", "unutma") → write it to the right memory file.
- **Unrelated task while a plan is active** → small: do it, leave the plan alone; large: choose the order, say it in one line (usually the new task first), a paused plan → `on-hold`, **Up next**.
- A `‹…›` placeholder left in CLAUDE.md → offer to finish setup with `KURULUM.md`.

## 2. Size
- **Small task** (a question, or a clear low-risk change to few files) → no plan: do, verify, commit (§4 rules).
- **Needs a plan** (your call): several steps or systems, uncertainty, architectural impact, or the user asked for one.

## 3. Plan
1. **Explore:** memory notes the index points to, then relevant code. **Review** (work players or viewers see): first study the best examples of the same work (look, play, feel; videos: leading channels), the area's expert agent (e.g. `unity-uzmani`) reviews the plan; findings → plan's **Review** section, the yardstick at closure. Broad scans, research → helper agent (general exploration: built-in **Explore**, cheaper, doesn't load CLAUDE.md); only its summary enters the main context.
2. **Ask:** only what §1 "Decide yourself" allows, before writing code.
3. **Write:** `planlar/YYYY-MM-DD-short-name.md` (ASCII name) from `sablonlar/plan.md`; exploration's gist in **Context** (files, how the system works now, constraints) so later steps and sessions don't rescan. Step: one line `- [ ] **N. Title**: details` (sub-step `**N.M Title**`), then files, **Tool** (skill or CLI; else `—`), **Verify** method; ≤6 lines, decisions one line each.
4. **Split:** independent parts or a plan file over ~15,000 characters → phases; the first plan holds a short phase map, each phase's detailed plan written after the previous one ends (no new approval within the map).
5. **Present** in your own words, in Turkish: what, why, what "done" means, what's out of scope; list the steps. Then start; wait for approval if it holds a user decision (§1), has phases or the user asked to see it first.
6. Only one plan is `in-progress`; others wait in DURUM's **Up next**.

## 4. Execute: default auto, sequential
Each step:
1. Only that step's work, with its **Tool**; read only the files it needs (broad exploration belongs to planning; big files: search first, then open the relevant part).
2. **Verify = error check** (plan's method, CLAUDE.md commands): clean compile or build (editor-free is enough), a run logs no errors. No tests written or run while developing (they wait for the pre-release test stage), nothing started only to test. A plan's or phase's last step adds an **eye check**: use it 2-3 minutes yourself as a player or user would, with screenshots. Only tool output seen in this session counts; a check that didn't run or timed out **does not pass**: log "not verified". The rest → plan's **Manual tests** (Turkish); continue.
3. **Record:** tick `[x]`, update **Progress**, one **Progress log** line in the template's fixed format, new decisions → **Decisions**; update DURUM.md (**Active plan:** `planlar/<file>.md` N/M steps done; **Next action:** the next step's number).
4. **Commit and push** (if git): the step's files + companions (e.g. Unity `.meta`) + plan + DURUM; `git status` first, never unrelated changes (no `git add -A` / `git add .`). English message: `feat: add inventory UI (plan: envanter, step 3/7)`; no `--no-verify`. Push if a remote exists: rejected → `git pull --rebase --autostash` once, push again; conflict → resolve if both sides' intent is clear, else `git rebase --abort`, ask; network/server error → continue, retry after the next commit. Force push: your call, `--force-with-lease`.
5. Mode `auto` → next step without waiting; `step-by-step` → short summary, then stop.

**Stop only when** (reason → plan (⛔) and DURUM; ask one clear question): verification keeps failing, no well-founded idea left · plan assumption proved wrong, goal or scope must change · hard-to-reverse operation outside the approved plan · red test in the pre-release test stage, unclear cause (bug or stale test) · decision only the user can make (§1). Never delete or loosen a test or hard-code its result to hide a bug.

Small deviation (same goal, different detail) → update the plan, log it, continue. Out-of-scope idea → **Up next**, tech debt → `hafiza/teknik-borc.md`; not now.
**Plan finished** → `BAKIM.md` → "Plan closure". **Before a release** (store build, deploy) → `BAKIM.md` → "Pre-release test stage".

## 5. Memory
Where: current work → `DURUM.md` + active plan · durable decision + reason → `hafiza/kararlar.md` · pitfall, hard-won knowledge, user correction or preference → `hafiza/dersler.md` · tech debt, review follow-ups → `hafiza/teknik-borc.md` (create if missing, index it) · growing area's knowledge → `hafiza/<topic>.md` + a `HAFIZA.md` line · project rule for every task → CLAUDE.md · derivable from code/git, temporary or secret (password, key) → nowhere.
- All memory in `docs/ai/` (git carries it between machines), never Claude's local auto memory (off in settings).
- Search for an existing entry before writing; update it, don't duplicate. Short, dated, with the "why"; only verified facts. Tell the user in one line what you wrote where.
- No temporary state as durable ("editor closed now", "test broken for now"); prefer the method. Note what would invalidate an entry ("recheck if Unity is upgraded").
- Memory contradicts code → code wins; fix memory. Before relying on a file/function named in memory, check it exists.
- Only the main session writes memory and plan files; helper agents never do.
- Limits (`LC_ALL=C.UTF-8 wc -m`): CLAUDE.md ≤160 lines/10,000 characters · DURUM ≤30/3,000 · HAFIZA ≤40/4,000 · topic file over ~150 lines/~15,000 → split; DURUM one-liners, details in plans and `hafiza/`; over a limit → `BAKIM.md` → "Memory tidy-up".

## 6. Protect context and usage
- Read nothing "just in case": index → relevant file → relevant section.
- **Active plan:** don't read it whole: header, **Context**, the next step and the last log lines (search, then read that part); other sections when needed.
- Filter long output (build/test logs); errors and a summary are enough.
- **Helper agents:** your call; each costs tokens, so use one where it beats searching yourself: broad exploration, independent parallel work, a closure review (`BAKIM.md`). The area's expert agent → exploration and opinion in one call. Agents don't spawn agents (settings).
- **Skills:** use one when a step needs it (TDD and test skills only in the pre-release test stage). Plan mode or a plan/spec skill may be used, but the valid plan is the §3 file (its template); no skill's workflow replaces this protocol.
- State is written to disk every step. After compaction, an interruption (e.g. usage limit) or when unsure → §1 **Continue** tidy-up.
- When a plan ends or the topic changes, suggest `/clear` to the user.
