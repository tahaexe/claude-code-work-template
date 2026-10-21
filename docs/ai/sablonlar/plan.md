# Plan: ‹Title›
<!-- The plan index: short, read on every restart. Each step's details live in its own file `planlar/‹this plan's name›/NN-‹slug›.md` (template `sablonlar/adim.md`), read only while that step runs. -->

- **Status:** draft <!-- draft · approved · in-progress · on-hold · done · cancelled -->
- **Mode:** auto <!-- auto: runs to the end · step-by-step: stops after each step -->
- **Dates:** created YYYY-MM-DD · updated YYYY-MM-DD
- **Progress:** 0/‹N› steps

## Goal
‹What and why, 1-3 sentences.›

## Acceptance criteria
<!-- What "done" means; every item verifiable. -->
- [ ] ‹…›

## Scope
- **In:** ‹…›
- **Out:** ‹…›

## Context
<!-- Gist of exploration so later steps and sessions don't rescan the code. ≤15 lines; what only one step needs goes into its step file. -->
- **Relevant files:** `‹path›`: ‹role›
- **Current state:** ‹how the system works now›
- **Constraints / watch out:** ‹…›
- **Related memory:** ‹hafiza/… › heading›

## Review
<!-- Work players or viewers see (PROTOKOL §3): written before the steps; the closure judges the work by it. Otherwise delete this section. -->
- **Pre-research:** ‹the report this plan builds on: `tasarim/on-arastirma/YYYY-MM-DD-on-arastirma….md` (new project or big job, PROTOKOL §3); else —›
- **Best examples:** ‹2-3 references: what they do (measured where possible), what we take, what we avoid›
- **Expert:** ‹agent and its plan review: findings, what changed in the plan›
- **Bar at closure:** ‹how "beside the best" is checked: side-by-side, scores, eye check, feel on a device›

## Phase map
<!-- Only if the work was split; each phase is its own plan file (index + step folder). Otherwise delete this section. -->
1. ‹Phase 1: goal› ← this plan
2. ‹Phase 2: goal›

## Steps index
<!-- One format only, so a restart, the plan view and status tools read just these lines: one checkbox line per step `- [ ] **N. Short title**: one-line what → `planlar/‹plan›/NN-‹slug›.md`` (a sub-step `- [ ] **N.M Short title**: …` with its own file `NN-M-‹slug›.md`, e.g. 4.1, 6a.1); no other checkboxes in this section. States on the line: `[ ]` ○ to do (Yapılacak) · `[~]` ▶ in progress (Devam ediyor) · `[x]` ✓ done (Tamamlandı) · blocked: `⛔ ‹why›` at the line's end (Engellendi), the box unchanged. Files, Tool, Verify, Kaldığım yer, the step's log, decisions and Final test live only in the step file, one per step, written with the plan (a later phase's when that phase's plan is written). DURUM: **Active plan:** `planlar/‹this file›.md` N/M steps done; **Next action:** `Adım N başla: …` or `Adım N devam: …` (PROTOKOL §4). One commit per step. Penultimate step: the comprehensive test stage (BAKIM.md); last: the release or delivery. No stage in a prototype that won't ship or in a plan whose work ships with a later release plan: its Final tests run in that plan's stage. Index over ~15,000 characters or independent parts → phases. -->
- [ ] **1. ‹Short title›**: ‹one-line what› → `planlar/‹plan›/01-‹slug›.md`
- [ ] **2. ‹Short title›**: ‹one-line what› → `planlar/‹plan›/02-‹slug›.md`
- [ ] **‹N-1›. Comprehensive test**: every step file's Final test one by one; a release: the release checklist and the test list (`el-kitabi/yayin-oncesi-test-listesi.md`), every existing test suite once; the report → `planlar/‹plan›/‹NN›-kapsamli-test.md`
- [ ] **‹N›. ‹Release or delivery›**: ‹store submission, deploy or hand-over; a release is announced the same day (BAKIM.md › After release)› → `planlar/‹plan›/‹NN›-‹slug›.md`

## Risks and open questions
- ‹…›

## Decisions
<!-- Plan-wide decisions, one line each (a step's own go into its file); durable ones move to hafiza/kararlar.md at closure. -->
- ‹YYYY-MM-DD: decision; why›

## Manual tests
<!-- Turkish (for the user); copied to docs/ai/manuel-testler.md at closure. -->
- [ ] ‹…›

## Result
<!-- Filled at closure: what changed, known limits, next suggestions. -->
