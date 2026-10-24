---
title: "Systematic debugging: root cause first, one hypothesis at a time, stop after three failed fixes"
condition: "Every project (code, tools, builds)."
read_when: "A bug, an error, a compile or build break, a crash, a failing check or unexpected behaviour, before proposing a fix; a fix that didn't hold; a second or third attempt at the same problem."
requires: "—"
source: "Adapted from the systematic-debugging skill of obra/superpowers (MIT; v7.0.1 of 2026-10-21; its SKILL.md read 2026-10-24), rewritten in our own words · the owner asked on 2026-10-23 about turning superpowers back on; the session manager's decision: the plugin stays off, the method goes into the handbook"
tech: "Engine-independent"
added: "2026-10-24 · template 1.61 · the session manager's candidate list; left out on purpose: the source's test-first step (the owner's rule of 2026-10-22: no tests while developing), its 'a skill before every task' rule, its TDD and brainstorming flows"
---
# Systematic debugging

## Rule
- No fix before the root cause is known: a symptom patch hides the bug and costs a second hunt.
- Every kind: a compile or build break, a crash, a wrong value, a slowdown, a failing check, a tool that misbehaves. "It looks simple" and haste are no exception.

## 1. Find the root cause
- Read the whole error output and stack trace, top to bottom; note file, line and error code.
- Reproduce it reliably first; when it doesn't reproduce, gather more evidence (logs, timings, the exact input), never guess.
- Look at what changed: recent diffs and commits, new packages, settings, the environment (an editor, SDK or tool update).
- Several parts (editor → build → device, a tool calling a tool): log what goes in and out at each boundary, run once, then open the part where it first goes wrong.
- Trace back from the failure to where the bad value was born; fix it there, not where it surfaced.

## 2. Compare with what works
- Find similar code in the same project that works; read a reference or example in full before borrowing its pattern.
- List every difference between the working and the broken case, small ones too, and what the broken one depends on (other parts, settings, environment, assumptions).

## 3. One hypothesis, the smallest test
- Write it down: "X is the cause because Y".
- Test it with the smallest change, one variable at a time; not confirmed → a new hypothesis, never a second change stacked on the first.
- Something not understood → say so; read the docs or ask (the manager where one is named), don't paper over it.

## 4. Fix
- One change aimed at the root cause; no clean-up or refactor bundled with it (PROTOKOL §4: surgical).
- Verify with the step's check: the error is gone, nothing else broke, the original symptom is really gone (only tool output seen in the session counts). A reproduction check (a throwaway script, the run that failed) is fine; writing tests waits for the comprehensive test stage (PROTOKOL §4).
- A failed fix: back to 1 with what it taught. **After three failed fixes, stop:** each fix exposing a new symptom, shared state or coupling elsewhere means the design is wrong, not the hypothesis; question it and decide with the user (or the manager) before a fourth attempt.

## Stop signs (back to 1)
- "Quick fix now, investigate later"; "just try changing X"; several changes at once; a fix proposed before the data flow is traced; "one more try" after two failures; every fix creating a new problem.
- The user or the manager saying "stop guessing", "are we stuck?", "isn't that happening?": the approach is wrong, not the luck.

## When the cause is outside our code
- A real environmental, timing or external cause (a service, a driver, a device): write down what was checked, add a guard (a retry, a timeout, a clear error message) and a log line where it would show again. Most "no root cause" findings are an investigation stopped early.
