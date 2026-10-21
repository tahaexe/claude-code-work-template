# Step ‹N›: ‹Short title›
<!-- Step file of `planlar/‹plan›.md` (the index holds the state: [ ] ○ to do · [~] ▶ in progress · [x] ✓ done · ⛔ blocked). Written with the plan; while the step runs, this is the only plan file read besides the index (PROTOKOL §6). Short: ~40 lines; what other steps need too goes into the index's Context. Tool, Verify and Final test are required. -->

- **What:** ‹1-3 lines: what this step builds or changes, and why›
- **Files:** `‹path›` ‹…›
- **Tool:** ‹skill or CLI (e.g. `unity:ui`, Unity CLI); else —›
- **Verify:** ‹the error check (PROTOKOL §4): e.g. editor-free compile clean, no errors in the log; the last building step of the plan or phase: + eye check (2-3 min, screenshots)›
- **Checklist:** ‹item ids from `el-kitabi/proje-kontrol-listesi.md` (e.g. 5.8) whose "Done when" this step meets; else —›

## Kaldığım yer
<!-- Resume note (Taha's three states: Tamamlandı · Devam ediyor · Yapılacak). Rewritten, not appended: at the ~90 % context checkpoint, before stopping mid-step, and the moment a background job starts (write-ahead: what runs, how its end shows: a file, a log line, a ticket). Holds: what is done · the next small action · what is open (editor, emulator, build, helper agent). Times from `date`. Emptied (—) when the step is done. -->
- —

## Log
<!-- This step's own log, one entry per work session or milestone, ≤2 lines (~300 characters): what, and the check's short result, never full output; "not verified" if the check didn't run; ⛔ = stop reason. -->
- ‹YYYY-MM-DD HH:MM› · ‹what› · tool: ‹…› · verify: ‹command run → short result›

## Decisions
<!-- This step's decisions, one line each; plan-wide ones go into the index's Decisions; durable ones move to hafiza/kararlar.md at closure. -->
- ‹YYYY-MM-DD: decision; why›

## Final test
<!-- Written with the step, run only in the comprehensive test stage (BAKIM.md): how this step's result is tried when everything is ready. A pass is a number or a clear state, never "works". The checklist item's "Final test" and the test list's row (`el-kitabi/yayin-oncesi-test-listesi.md` § n) go here when they apply. -->
- **How:** ‹what is tried, where: editor, emulator, store build, device›
- **Pass:** ‹e.g. "granted once after a kill between payment and grant", "average ≥55 FPS on the lowest phone"›
- **Evidence:** ‹command output, log excerpt or screenshot, under `Logs/claude/release/‹version›/` in a release›
