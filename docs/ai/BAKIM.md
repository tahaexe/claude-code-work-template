# Maintenance: Plan Closure and Memory Tidy-up
<!-- Read only when needed: a plan ends, a file exceeds a limit, or the user asks for a tidy-up. -->

## Plan closure
1. **Verify:** check each acceptance criterion against tool output seen in this session. A check that couldn't run or was never tried is "not assessed" in the report, never "passed". Non-automatable checks (e.g. game feel, on-device performance) go to manual tests.
2. **Review (your call):** worth it when the plan was risky (save data, purchases, data migration), weakly verified automatically (scenes, prefabs, UI) or long, and the project has a review agent for the area (e.g. `unity-uzmani` for Unity code): have it review the files the plan changed; ask only for bugs and requirement gaps. The plan changed what the player sees and `tasarim/gorsel-stil.md` exists → also pass the step screenshots for a visual consistency review. Small, test-verified plan → no review; report "review: not needed". Serious findings → a fix plan (PROTOKOL §3), not fixes inside the closure. Follow-ups not fixed now → `hafiza/teknik-borc.md`.
3. **Result:** plan status `done`; in **Result** write what changed, known limits, recommendations.
4. **Move durable knowledge** (only what will matter later):
   - decisions not specific to the plan → `hafiza/kararlar.md`
   - pitfalls learned → `hafiza/dersler.md`
   - knowledge of a growing area → `hafiza/<topic>.md` (create if missing, add a line to `HAFIZA.md`)
5. **Manual tests:** copy the plan's manual tests into `manuel-testler.md` (Turkish) under the fitting area, tagged with the plan's short name; skip items already there.
6. **Archive:** move the plan to `planlar/arsiv/` (`git mv` if git).
7. **DURUM:** clear the active plan or move to the next approved plan/phase; add the finished plan to **Recently completed** as one line ≤150 characters (max 5; drop the oldest).
8. **Tidy:** apply "Memory tidy-up" below only to memory files changed in this plan.
9. **Commit** (if git): `docs: close plan <short-name>`.
10. **Report** (Turkish): short summary, how many manual tests were added (the list is in `manuel-testler.md`), checks not assessed, review findings (if any), CLAUDE.md rules added, the next task and `/clear` before a new task. If the project has `docs/ai/sablonlar/oyun/`, suggest the fitting doc: prototype report after a prototype plan, playtest report when a build goes to players, post-mortem after a major milestone.

Cancelled plan: status `cancelled`, reason in **Result**, archive, update DURUM.

## Memory tidy-up
- **Duplicates:** merge entries that say the same thing, entry by entry. Never rewrite a whole file as a summary.
- **Staleness:** check entries against the code; search the file/function names they mention. Fix or delete what is no longer true.
- **Unneeded:** delete what is easily derivable from code or git history, one-off, or no longer important.
- **Decisions:** don't delete a superseded decision at once; strike its title (`~~…~~`) and add "→ changed by YYYY-MM-DD decision". Delete very old, irrelevant ones.
- **Size:** check the limits with `LC_ALL=C.UTF-8 wc -m` (PROTOKOL §5; plain `wc -m` in Git Bash counts bytes). Move DURUM detail into plans or `hafiza/`, tech debt into `hafiza/teknik-borc.md`; split topic files by topic and index them. CLAUDE.md over its limit → trim it yourself: details to a `hafiza/` file with a one-line pointer; tell the user.
- **No fact loss:** after rewriting or moving entries, run `python docs/ai/araclar/kayip-kontrol.py --rev HEAD <changed files>`: restore every reported missing fact; for each listed clause make sure its reason, condition or exception survived (reworded is fine).
- **Index:** one line per memory file in `HAFIZA.md` (handbook entries share one line, each hint keeping the tasks of its `read_when`; never trim a hint to a topic name), paths relative to `docs/ai/`, with a correct "when to read" hint; delete lines and entries pointing to missing files.
- **Commit** (if git): `docs: tidy Claude memory`.
