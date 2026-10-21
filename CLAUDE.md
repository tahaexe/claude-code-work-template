# Claude working template (the template itself)

This folder is the Claude working template installed into projects; not a game or app project.

- **Your role:** you own the template's development. Evaluate the ideas and sources the user brings (email, video, link); pick the best path, propose it with a short reason, apply it after approval.
- **Owner only:** develop the template (edit, commit, push) only if the global CLAUDE.md marks this as the template owner's computer. Otherwise the user is someone using the template: explain and help them use it, never change or push it.
- Files in `docs/ai/` are **empty starter files** copied into projects. In this folder never write work records into `DURUM.md`, `HAFIZA.md`, `hafiza/` or `planlar/`; edit them only to change the template.
- Adding a source to the handbook ("bu videoyu el kitabına ekle", "el kitabına not ekle"): read and apply `el-kitabi/NASIL.md`.
- **Browser work:** do it yourself with the Claude in Chrome tools, only in your account's own Chrome profile (`el-kitabi/tarayici-baglantisi.md`), without asking permission, never hand it to the user (built-in safety confirmations still apply); not connected → say so, ask before another browser.
- **Language:** files Claude reads (this file, `docs/ai/`, add-on rules and agent, handbook entries) are terse English bullets; user-facing files (`README.tr.md`, KILAVUZ, `manuel-testler.md`, game templates) stay Turkish, and `README.md` is the English copy of `README.tr.md`. Talk to the user in Turkish.
- After changing the template:
  1. Bump version marks: every version `docs/ai/PROTOKOL.md` line 2 plus the version lines of both READMEs; `eklentiler/unity/KURULUM-UNITY.md` line 2 and add-on marks (`unity add-on vX`) only if that file's content changed.
  2. Check limits: PROTOKOL ≤100 lines, `CLAUDE.sablon.md` ≤160 lines and ≤10,000 characters, Unity section ≤15 lines; keep cross-references and step numbers consistent.
  3. Update both READMEs (KILAVUZ if usage changed) and **Where we left off** below; commit, add the version tag (`vX`), push.
- **Session handoff:** update **Where we left off** after every job, so `/clear` is always safe. If the user says "not al" or "clear yapacağım", update it at once, commit and push. In a new session answer "nerede kalmıştık?" only from this section (in Turkish).
- `research_notes/` and `reports/` are outside git; never commit them.

## Where we left off (Nerede kaldık)
<!-- ≤8 lines · updated after every job -->
- **Last version:** 1.57 (2026-10-21).
- **Open work:** none.
