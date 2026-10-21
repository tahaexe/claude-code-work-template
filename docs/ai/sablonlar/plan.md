# Plan: ‹Title›

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
<!-- Gist of exploration so later steps and sessions don't rescan the code. ≤25 lines. -->
- **Relevant files:** `‹path›`: ‹role›
- **Current state:** ‹how the system works now›
- **Constraints / watch out:** ‹…›
- **Related memory:** ‹docs/ai/hafiza/… › heading›

## Review
<!-- Work players or viewers see (PROTOKOL §3): written before the steps; the closure judges the work by it. Otherwise delete this section. -->
- **Pre-research:** ‹the report this plan builds on: `tasarim/on-arastirma/YYYY-MM-DD-on-arastirma….md` (new project or big job, PROTOKOL §3); else —›
- **Best examples:** ‹2-3 references: what they do (measured where possible), what we take, what we avoid›
- **Expert:** ‹agent and its plan review: findings, what changed in the plan›
- **Bar at closure:** ‹how "beside the best" is checked: side-by-side, scores, eye check, feel on a device›

## Phase map
<!-- Only if the work was split; each phase is its own plan file. Otherwise delete this section. -->
1. ‹Phase 1: goal› ← this plan
2. ‹Phase 2: goal›

## Steps
<!-- One format only, so a restart, the plan view and status tools read just these lines: each step is one checkbox line `- [ ] **N. Short title**: details`; a sub-step `- [ ] **N.M Short title**: details` (e.g. 4.1, 6a.1); ticked `[x]` when done; Files, Tool and Verify on indented lines below it, never as checkboxes; no other checkboxes in this section. DURUM: **Active plan:** `planlar/<this file>.md` N/M steps done; **Next action:** the next step's number (PROTOKOL §4). One commit each. Tool and Verify are required. Verify = the error check (PROTOKOL §4), no tests; the last step adds the eye check. A release plan ends with the pre-release test stage (`BAKIM.md`). ≤6 lines per step; independent parts or >~15,000 characters (after the older log entries moved out: Progress log) → split into phases (each phase file's steps in this format). -->
- [ ] **1. ‹Short title›**: ‹what›
  - Files: `‹…›`
  - Tool: ‹skill or CLI (e.g. `unity:ui`, Unity CLI); else —›
  - Verify: ‹error check: e.g. editor-free compile clean, no errors in the log›
- [ ] **2. ‹Short title›**: ‹what›
  - Files: `‹…›`
  - Tool: ‹…›
  - Verify: ‹error check; last step of the plan or phase: + eye check (2-3 min, screenshots)›
- [ ] **N. Pre-release test stage**: ‹release plans only: the release checklist and the test list (`el-kitabi/yayin-oncesi-test-listesi.md`), every existing test suite once›
  - Tool: ‹…›
  - Verify: ‹the test report: item, result, evidence›

## Risks and open questions
- ‹…›

## Decisions
<!-- One line each; durable ones move to hafiza/kararlar.md at closure. -->
- ‹YYYY-MM-DD: decision; why›

## Manual tests
<!-- Turkish (for the user); copied to docs/ai/manuel-testler.md at closure. -->
- [ ] ‹…›

## Progress log
<!-- One entry per step in this fixed format, at most 2 lines (~300 characters): what and the check's short result, never full output. ⛔ = stop reason. Plan file over ~15,000 characters → move the older entries to planlar/arsiv/<plan-name>-log.md and keep the last 5 here, before splitting into phases. -->
- ‹YYYY-MM-DD› · Step ‹N› ✓ · ‹what› · tool: ‹…› · verify: ‹command run → short result; "not verified" if it didn't run›

## Result
<!-- Filled at closure: what changed, known limits, next suggestions. -->
