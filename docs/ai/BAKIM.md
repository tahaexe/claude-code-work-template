# Maintenance: Plan Closure, Pre-release Test Stage, After Release, Memory Tidy-up
<!-- Read only when needed: a plan ends, a release is next or went out, a file exceeds a limit, or the user asks for a tidy-up. -->

## Plan closure
1. **Verify:** check each acceptance criterion against tool output seen in this session: the error check and the eye check (PROTOKOL §4); no test suite runs here (the pre-release test stage runs them). A check that couldn't run or was never tried is "not assessed" in the report, never "passed". Non-automatable checks (e.g. game feel, on-device performance) go to manual tests.
2. **Review:** work players or viewers see (screens, feel, art, store pages, videos) → always: the area's expert agent reviews the result (with the step and eye-check screenshots; `tasarim/gorsel-stil.md` exists → visual consistency too), then an honest check against the plan's **Review** section: was it tried (UI, feel, smoothness), and how does it stand beside the best examples? Weak → fixed before it ships; the answer goes in **Result**. Other plans (your call): worth it when the plan was risky (save data, purchases, ads, rewards and time, data migration) or long, and the project has a review agent for the area (e.g. `unity-uzmani` for Unity code): have it review the files the plan changed; ask only for bugs and requirement gaps. Small plan with a clean error check → no review; report "review: not needed". Serious findings → a fix plan (PROTOKOL §3), not fixes inside the closure. Follow-ups not fixed now → `hafiza/teknik-borc.md`.
3. **Result:** plan status `done`; in **Result** write what changed, known limits, recommendations.
4. **Move durable knowledge** (only what will matter later):
   - decisions not specific to the plan → `hafiza/kararlar.md`
   - pitfalls learned → `hafiza/dersler.md`
   - knowledge of a growing area → `hafiza/<topic>.md` (create if missing, add a line to `HAFIZA.md`)
5. **Manual tests:** copy the plan's manual tests into `manuel-testler.md` (Turkish) under the fitting area, tagged with the plan's short name; skip items already there.
6. **Archive:** move the plan to `planlar/arsiv/` (`git mv` if git).
7. **DURUM:** clear the active plan or move to the next approved plan/phase; add the finished plan to **Recently completed** as one line ≤150 characters (max 5; drop the oldest). A release plan also adds the post-release line to **Up next** ("After release" below).
8. **Tidy:** apply "Memory tidy-up" below only to memory files changed in this plan.
9. **Commit** (if git): `docs: close plan <short-name>`.
10. **Template update:** the template's PROTOKOL (folder: global CLAUDE.md) newer than line 2 here → run `KURULUM.md` → "Güncelleme (Update)" yourself now (it keeps the project's own CLAUDE.md lines, memory and plans); one line on what changed for this project goes into the report.
11. **Report** (Turkish): short summary, how many manual tests were added (the list is in `manuel-testler.md`), checks not assessed, review findings (if any) and the honest check's answer, CLAUDE.md rules added, the next task and `/clear` before a new task. If the project has `docs/ai/sablonlar/oyun/`, suggest the fitting doc: prototype report after a prototype plan, playtest report when a build goes to players, post-mortem after a major milestone.

Cancelled plan: status `cancelled`, reason in **Result**, archive, update DURUM.

## Pre-release test stage
Before every release (store build, deploy), once per version and thorough: a release plan's last step, then its closure (expert review, honest check). Not for a prototype that won't ship: the error and eye checks are enough there.
1. **Run:** every existing test suite once; the release checklist; the test list (`el-kitabi/yayin-oncesi-test-listesi.md` where installed: in games every level through the real controller, saves with a relaunch and an old save, purchases, ads, rewards and the clock, ad and navigation flows, screens in both languages, the store build on an emulator) with its report (item, result, evidence) in the plan; then the manual list.
2. **Red:** a bug is fixed before the release; a stale or flaky test is updated, or disabled with its reason in `hafiza/teknik-borc.md`. Never delete or loosen a test or hard-code its result to hide a bug; unclear cause → stop and ask (PROTOKOL §4).
3. **New tests** only here, as many as needed, where a bug would cost players or money; a test for a fixed bug is seen failing without the fix first.

## After release: measure, analyse, decide
A game or app released to a store is measured before new content is built on it.
1. **Measure from the first release:** version 1 already ships the measurement events: level start and end, session length, ad and purchase events, D1 and D7 by version (mobile with Firebase: `el-kitabi/firebase-olcum-ve-uzaktan-ayar.md`); crashes (Crashlytics, Android vitals) and store conversion come from the consoles. The gate (D1, D7, day-1 minutes; continue and grow thresholds) is set before the data arrives (game summary › Ölçüm hedefleri) and never moved after it.
2. **Window:** at least 14 days from the release going live without new content (levels, modes, maps, events); fixes, compliance and store-policy changes and review replies go on. The release plan's closure adds to **Up next**: "<version>: no new content until 14 days after it goes live, then the post-release analysis (`BAKIM.md` › After release)"; the date is filled in once the release is live.
3. **Analysis report** (Turkish; a session manager's analyst writes it where the machine has one, else this session): D1, D7 and day-1 minutes against the gate (a range on few installs; too few → "not enough data", the window grows), the level funnel (where players quit), session length, crashes, ad and IAP revenue, store conversion, ratings and review themes; at most 3 recommendations, each tied to a finding.
4. **Decision** (the user's): develop (a new version), maintenance (fixes only) or shelve; recorded in DURUM's **Up next** with its date, the reason and the report's path.
5. **Next version:** its plan starts from the analysis findings (the biggest drop fixed, what players like grown, revenue improved) plus a short pre-research of the relevant areas (`el-kitabi/on-arastirma.md`); both go into its **Review** section. After it goes live → step 2 again.

## Memory tidy-up
- **Duplicates:** merge entries that say the same thing, entry by entry. Never rewrite a whole file as a summary.
- **Staleness:** check entries against the code; search the file/function names they mention. Fix or delete what is no longer true.
- **Unneeded:** delete what is easily derivable from code or git history, one-off, or no longer important.
- **Decisions:** don't delete a superseded decision at once; strike its title (`~~…~~`) and add "→ changed by YYYY-MM-DD decision". Delete very old, irrelevant ones.
- **Size:** check the limits with `LC_ALL=C.UTF-8 wc -m` (PROTOKOL §5; plain `wc -m` in Git Bash counts bytes). Move DURUM detail into plans or `hafiza/`, tech debt into `hafiza/teknik-borc.md`; split topic files by topic and index them. CLAUDE.md over its limit → trim it yourself: details to a `hafiza/` file with a one-line pointer; tell the user.
- **No fact loss:** after rewriting or moving entries, run `python docs/ai/araclar/kayip-kontrol.py --rev HEAD <changed files>`: restore every reported missing fact; for each listed clause make sure its reason, condition or exception survived (reworded is fine).
- **Index:** one line per memory file in `HAFIZA.md` (handbook entries share one line, each hint keeping the tasks of its `read_when`; never trim a hint to a topic name; an entry that CLAUDE.md or PROTOKOL already routes to gets no hint), paths relative to `docs/ai/`, with a correct "when to read" hint; delete lines and entries pointing to missing files.
- **Commit** (if git): `docs: tidy Claude memory`.
