---
title: "Public text check: claims ledger, machine-sounding patterns, proof, fresh review, store listing audit"
condition: "Project that publishes player- or viewer-facing text: store listings, release notes, a site or catalog page, a press kit, video titles and descriptions. Signs: a store record, a `store/` folder, a press kit or a channel in the plans or memory."
read_when: "Writing or reviewing store text, release notes, site, press or video copy; before every release (the claims check); auditing a store listing; a listing rejected for its wording."
requires: "—"
source: "Ideas from coreyhaines31/marketingskills (MIT; read 2026-10-18: copywriting's AI-tells reference and its six-step self-check, copy-editing's proof and specificity sweeps, the aso skill's scoring criteria and report template, the claim-drift loop) · conorbronsdon/avoid-ai-writing (MIT; found through hesreallyhim/awesome-claude-code, 2026-10-18) · affaan-m/everything-claude-code (santa-method: a fresh reviewer with written criteria; 2026-10-18) · their cited sources: Wikipedia 'Signs of AI writing', Kobak et al. 2024 (PubMed vocabulary), Juzek & Ward (COLING 2025) · the studio's store facts files (since 2026-10-10). Written in our own words; nothing installed."
tech: "Google Play, App Store, YouTube and the studio's site; English and Turkish"
added: "2026-10-18 · template 1.53 · the session manager's selection from the day's repository research"
---
# Public text check

## 1. Claims ledger: `store/facts.md`
- Every sentence we publish about the game (store text in every language, release notes, the site or catalog page, press kit, video titles, descriptions and pinned comments) traces to a line in `store/facts.md`; every line traces to the game itself (code, assets, a page we own) with its path.
- End the file with a ledger, one row per claim that appears outside the game: claim · source of truth · where it appears · last checked version. A "Don't claim" list beside it: planned, partial or removed features creep into copy.
- **Every release:** read the release's changes against the ledger, fix every place a changed claim appears, set "last checked" to the new version (release checklist). Prices, legal and privacy claims go to the user as they are (the studio: to the session manager). Drift seen: a press kit said 30 levels while the site said 27.

## 2. Write, then check
- **Patterns that make text read machine-written** (cut them):
  - Structures: "It's not X, it's Y" and other contrast reveals; "No X, no Y, no Z" runs in body text (a short caption naming a real feature, like "No timers, no lives", is fine); a question the next sentence answers; a colon before the payoff; a trailing pile of benefits; "Whether you're A or B"; "Get ready to…"; a tidy closing line that restates the section.
  - Words used as praise (seamless, immersive, robust, elevate, unleash, unlock, next level, game-changer, journey, adventure awaits, boasts, serves as; a literal "unlock a new area" is fine); in Turkish "eşsiz deneyim", "sürükleyici macera", "sizi bekliyor" (our own guess; the sources have no Turkish list).
  - Form: em dashes (none in short copy, 1-2 in a long text), bold on every line, emoji as bullets, Title Case Everywhere.
  - Caps per section: one three-item list, one sentence fragment; two capped words in one paragraph → rewrite. A real list of three features is fine.
- **Self-check, in order** (after marketingskills' six steps):
  1. Scan headlines and short lines for negations, question marks, colons and dashes; fix the patterns above.
  2. Flag sentences over 20 words with three or more commas.
  3. Count three-item lists, fragments and capped words per section.
  4. Read it aloud: a press-release or social-post tone gets rewritten.
  5. Swap test: a line that would fit any game of the genre gets this game's mechanic, mode or level count.
  6. Endings and rhythm: no tidy closer per section, no "wisdom" sentence, sections of different lengths.
  A fix that needs a fact we don't have → ask for the fact; never write around the gap.
- **Two sweeps:** prove it (every claim is in the ledger, or it goes) and specific (numbers and names, not adjectives: "30 levels, 6 elements", not "lots of content").
- These are style rules with counter-views, not laws: a formal voice with specific claims is fine.

## 3. Fresh review before it goes out
- Text that is hard to take back (store listing in both languages, release notes, data declarations, a video's title and description) gets one reviewer with a clean context: a subagent given only the text, the ledger and these criteria, never the writer. Pass or fail:
  1. every claim is in the ledger;
  2. no wording the stores reject (store-listing-optimization.md › Wording and imagery);
  3. both languages say the same thing (numbers, features, tone);
  4. declarations (data safety, privacy labels, ads, purchases) match the code;
  5. none of §2's patterns.
- At most 3 rounds, a new reviewer each round; still failing → to the user with the open points. One reviewer instead of the method's two, to keep the token cost down.

## 4. Store listing audit
- Before a big release or a listing rework, per store. Score each area 0-10 and weight it: title and subtitle 20%, description 15%, visuals (icon, screenshots, video) 25%, ratings and reviews 20%, freshness (last update, languages, events, category) 10%, conversion signals (value before download, clear prices, a credible developer) 10%; sum × 10 = score out of 100. The weights follow marketingskills' aso scoring; judge each area against store-listing-optimization.md and the genre leaders, not against that skill's own anchors.
- Report: header (game, store, link, date, score) → score table → three quick wins under an hour, current text beside the proposal → findings per area → keywords with placement and reason (search volume needs a paid tool: write "not measured") → 2-3 genre leaders side by side when useful → actions by effort → what couldn't be measured.
- Never take a third party's store specs or benchmarks as rules: that skill's Play file says 3 experiment variants, Play's Help says 2 (store-listing-optimization.md › Experiments).
