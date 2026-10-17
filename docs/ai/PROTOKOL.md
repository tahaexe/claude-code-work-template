# Working Protocol
<!-- Version 1.51 · 2026-10-17 · Same in every project; project facts go to CLAUDE.md. Update: KURULUM.md → "Güncelleme (Update)". -->

Goal for every task here: understand it, follow a plan step by step, use little context, keep knowledge in durable memory.
- The user's explicit instruction overrides this protocol. Its rules are defaults: where one doesn't fit, do what serves the goal and say why in one line; only the next rule is fixed.
- Hard-to-reverse operations (deletion git can't undo, package upgrade or removal, data migration, external service): ask first unless the approved plan explicitly includes them. Every commit is pushed automatically (§4).
- **Language:** Turkish with the user. Claude's own files (this protocol, DURUM, HAFIZA, `hafiza/`, plans, rules, handbook): terse English bullets; compress wording, never facts. User-facing files stay Turkish (`manuel-testler.md`, `tasarim/`). Code, comments, commit messages: English.

**Files** (`docs/ai/`): `DURUM.md` state, `HAFIZA.md` memory index (both loaded every session) · `hafiza/*.md` incl. `teknik-borc.md` (tech debt): read when the index points there and the task needs it · `planlar/*.md` plans (`planlar/arsiv/` finished), `sablonlar/plan.md` template · `manuel-testler.md` the user's manual tests · `BAKIM.md` plan closure, memory tidy-up · `KURULUM.md` install, template update

## 1. Read intent, choose the path yourself
Infer intent; the user doesn't memorize commands. Before changing files, state your path in one line ("→ Plan hazırlıyorum", "→ Küçük iş, doğrudan yapıyorum", "→ Aktif plandan devam: adım 4/7").
- **Decide yourself:** make technical and design choices; give the reason in one line, say it is reversible. Ask only about scope, money, hard-to-reverse operations, or credentials/identity you cannot invent: one short question, with options if possible. Browser work → yourself with the Claude in Chrome tools, only in your account's own Chrome profile (never another profile or browser), without asking permission or handing it to the user (built-in safety confirmations remain); no own profile yet or not connected → `el-kitabi/tarayici-baglantisi.md`; still not connected → say so, ask before another browser.
- **New task** → size it (§2).
- **Continue** ("devam", "kaldığımız yerden", "bitir şunu") → tidy up first: read the active plan (§6), compare `git status` and recent commits with it; a half-done or ticked but uncommitted step: work out how much is done, then finish, verify, record, commit; a change of unclear purpose: ask, never delete; an earlier session's leftovers (this project's editor, emulator, dev server; unsure whose → leave it): reuse if the next step needs it, else close cleanly (editor: save first). Then a short compile check (CLAUDE.md command; skip if slow): broken → fix it before the next step. Then the next step.
- **Session start, greeting, status question** ("nerede kalmıştık?") → 1-2 line summary from DURUM and the active plan; if a plan is active, offer to continue. In a session's first reply: template PROTOKOL (folder: global CLAUDE.md) newer than line 2 here → one line suggesting "şablonu güncelle".
- **Plan view** ("planı göster", "tüm planlar") → don't read the whole plan; grep the step lines, list: `✓` done · `→` next · `○` waiting · `⛔` blocked. "Tüm planlar" → active plan + **Up next** + recently completed.
- **Plan edit** ("4. adımdan sonra şunu ekle", "şunu çıkar", "sıraya koy") → insert the step (Files/Tool/Verify), renumber, update **Progress**, log, show the short list, commit. Never edit a done step; add a fix step. Ask first only if goal or scope changes. "Sıraya koy" → **Up next**.
- **Plan approval** ("tamam", "olur", "başla" after a plan is shown) → status `in-progress`, start.
- **Pace** → "yavaş gidelim", "her adımı göster": mode `step-by-step` · "sen devam et": mode `auto`.
- **Correction** ("yanlış", "bunu yapma", "hep şöyle yap") → fix it, write it to `hafiza/dersler.md`; if it applies to every task, add a CLAUDE.md rule.
- **Info** ("bilgin olsun", "unutma") → write it to the right memory file.
- **Unrelated task while a plan is active** → small: do it, leave the plan alone. Large: choose the order, say it in one line (usually the new task first); a paused plan becomes `on-hold` and goes to **Up next**.
- A `‹…›` placeholder left in CLAUDE.md → offer to finish setup with `KURULUM.md`.

## 2. Size
- **Small task** (a question, or a clear low-risk change to few files) → no plan: do, verify, commit (§4 rules).
- **Needs a plan** (your call): several steps or systems, uncertainty, architectural impact, or the user asked for one.

## 3. Plan
1. **Explore:** memory notes the index points to, then relevant code. Broad scans and research → a helper agent (general exploration: the built-in **Explore** agent, cheaper, doesn't load CLAUDE.md); only its summary enters the main context.
2. **Ask:** only what §1 "Decide yourself" allows, before writing code.
3. **Write:** `planlar/YYYY-MM-DD-short-name.md` from `sablonlar/plan.md` (ASCII file name). Gist of exploration in **Context** (files, how the system works now, constraints) so later steps and sessions don't rescan. Each step: files, **Tool** (skill or CLI; else `—`), **Verify** method; ≤6 lines per step, decisions one line each.
4. **Split:** independent parts or a plan file over ~15,000 characters → phases. The first plan holds a short phase map; write each phase's detailed plan after the previous one ends (no new approval within the map).
5. **Present:** in your own words, in Turkish: what, why, what "done" means, what is out of scope; list the steps. Then start; wait for approval if it holds a user decision (§1), has phases or the user asked to see it first.
6. Only one plan is `in-progress`; others wait in DURUM's **Up next**.

## 4. Execute: default auto, sequential
Each step:
1. Only that step's work, with its **Tool**; read only the files needed (big files: search first, then open the relevant part).
2. **Verify:** the plan's method and CLAUDE.md commands. Only tool output seen in this session counts; a check that didn't run or timed out **does not pass**: log "not verified". What can't be verified automatically → the plan's **Manual tests** (Turkish); continue.
3. **Record:** tick `[x]`, update **Progress**, one **Progress log** line in the template's fixed format (date · step · what · tool · verify: command run and short result), new decisions to **Decisions**, update DURUM.md.
4. **Commit and push** (if git): the step's files + companions (e.g. Unity `.meta`) + plan + DURUM; check `git status` first, never add unrelated changes (no `git add -A` / `git add .`). English message: `feat: add inventory UI (plan: envanter, step 3/7)`; no `--no-verify`. Push if a remote exists: rejected → `git pull --rebase --autostash` once, push again; conflict → resolve it if both sides' intent is clear, else `git rebase --abort`, ask; network/server error → continue, retry after the next commit. Force push: your call, with `--force-with-lease`.
5. Mode `auto` → next step without waiting; `step-by-step` → short summary, then stop.

**Stop only when** (write the reason to the plan (⛔) and DURUM, ask one clear question):
- Verification keeps failing, no well-founded idea left.
- A plan assumption proved wrong; goal or scope must change.
- A hard-to-reverse operation outside the approved plan.
- A test looks wrong and the plan doesn't include changing it. Never delete or loosen a test or hard-code its result to make it pass.
- A decision only the user can make (§1).

Small deviation (same goal, different detail) → update the plan, log it, continue. Out-of-scope idea → **Up next**, tech debt → `hafiza/teknik-borc.md`; not now.
**Plan finished** → `BAKIM.md` → "Plan closure".

## 5. Memory
| Information | Where |
|---|---|
| What is being done now | `DURUM.md` + active plan |
| Durable decision and its reason | `hafiza/kararlar.md` |
| Pitfall, hard-won knowledge, user correction or preference | `hafiza/dersler.md` |
| Tech debt, review follow-ups | `hafiza/teknik-borc.md` (create if missing, index it) |
| Knowledge of a growing area | `hafiza/<topic>.md` + one line in `HAFIZA.md` |
| Project rule for every task | CLAUDE.md |
| Derivable from code/git, temporary or secret (password, key) | Nowhere |

- All memory lives in `docs/ai/` (git carries it between machines); never Claude's local auto memory (off in settings).
- Search for an existing entry before writing; update it, don't duplicate. Short, dated, with the "why"; only verified facts. Tell the user in one line what you wrote where.
- No temporary state as durable ("editor closed now", "test broken for now"); prefer the method. Note what would invalidate an entry ("recheck if Unity is upgraded").
- Memory contradicts code → code wins; fix memory. Before relying on a file/function named in memory, check it exists.
- Only the main session writes memory and plan files; helper agents never do.
- Limits (`LC_ALL=C.UTF-8 wc -m`): CLAUDE.md ≤160 lines/10,000 characters · DURUM ≤30/3,000 · HAFIZA ≤40/4,000 · split a topic file over ~150 lines/~15,000; DURUM holds one-liners, details in plans and `hafiza/`. Over a limit → `BAKIM.md` → "Memory tidy-up".

## 6. Protect context and usage
- Read nothing "just in case": index → relevant file → relevant section.
- Broad exploration belongs to planning; during execution read what the step needs.
- **Active plan:** don't read it whole: the header, **Context**, the next step and the last log lines (search, then read that part); other sections when needed.
- Filter long output (build/test logs); errors and a summary are enough.
- **Helper agents:** your call; each costs tokens, so use one where it beats searching yourself: broad exploration, independent work in parallel, a closure review (`BAKIM.md`). An expert agent for the area → exploration and opinion in one call. Agents don't spawn agents (settings).
- **Name-only skills** (descriptions hidden by settings): `agent-protocols:*` methods (debugging, TDD, security, performance, review, docs, CI), `engineering:*` team/ops checklists (architecture, tech debt, testing strategy, incidents, deploys); use one when a step needs it. Plan mode or a plan/spec skill may be used, but the valid plan is the §3 file (its template); no skill's workflow replaces this protocol.
- State is written to disk every step. After compaction, an interruption (e.g. usage limit) or when unsure → §1 **Continue** tidy-up.
- When a plan ends or the topic changes, suggest `/clear` to the user.
