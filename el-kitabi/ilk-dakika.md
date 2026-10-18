---
title: "The first minute: opening, tutorial, first win, unlock pacing, first ad and offer (hybrid-casual puzzles)"
condition: "Mobile game project (Android or iOS) with levels."
read_when: "Designing the first level, the tutorial or the first win; deciding when features and boosters unlock or when the first ad or offer appears; reading the first-levels funnel or D1."
requires: "—"
source: "Gamigion on Royal Match's onboarding (why it waits 22 levels for its first live op) and on the hole genre (All in Hole's first interstitial at ~52 min; single source) · Teeny Tiny Teardown of All in Hole (2024-10-09) · GameAnalytics benchmarks 2025 and 2026 · Google AdMob Help 6066980 (interstitial guidance) and 6201362 (disallowed interstitial implementations) · Airflux case study (2025, vendor) · Deloitte and Google AdMob player survey (2025, via Playio) · the studio's first-60-seconds research 2026-10-18"
tech: "engine-independent"
added: "2026-10-18 · template 1.53 · the studio's first-60-seconds research for the session manager"
---
# The first minute

## Why it matters
- A game that hasn't shown its value in the first 5-15 minutes loses the player (GameAnalytics' 2026 summary). D1 median ~22%, top 10% ~40%; D7 median ~4%, top 10% ~12% (GameAnalytics 2026, 2025 data). The first minute is about a fifth of a top-quartile first session (~5.2 min).

## Rules
- **Show the fun, teach while playing:** no text screens; a hand shows the one gesture and disappears at the first touch (GUI Pro's `Tutorial_Hand`).
- **Early wins:** first reward within 10 s, first growth or combo within ~15 s, first level won in 30-45 s. Levels 1-3 can't be lost: no lose offer, a timer that runs out restarts the level.
- **Unlock one thing at a time** and give the first of each booster free with a one-tap demo; keep the unlock calendar in one file (`docs/ai/tasarim/`).
  - Royal Match: first blocker at level 4, pre-level booster at 7, hammer at 8, new blockers at 11-21, tutorial over at 22 (levels 11-22 short and forgiving, ~1.1 attempts per win), live events from 23 (after a typical first session), first sale offer at 32, season pass at 37, first truly hard level at 39.
  - All in Hole (the hole genre's leader): learned "in a minute", new objects arrive as levels end, no squeeze in the first hour, coins weak for ~50 levels.
  - Royal Kingdom (same studio) puts a blocker in level 1 on purpose: there's no single right pace, but the leaders of our genres unlock slowly.
- **First ad:** no interstitial at app launch or exit (AdMob disallows it; app open ads are the launch format) and none in the first session; later only at natural breaks, preloaded, at most one per two player actions (Back counts as one) and never two in a row (AdMob Help 6201362) (google-play-level-up.md › Interstitial placement). Studio default (shared monetization package): after level 8, ≥ 180 s apart, on a won level's result screen with its buttons visible.
  - Evidence: All in Hole's first interstitial at ~52 min (~37 levels and ~2 ads in the first hour; single source). Moving a puzzle's first interstitial from 1 to 3.5 min raised D1 28% and LTV 22% (Airflux 2025, vendor, method not given). In a 2025 survey of 7,000 players in 5 countries, ~1 in 5 had quit a game they liked over bad ads (stated, not measured).
- **First offer:** no purchase offer before the first session ends (Royal Match: level 32); rewarded ads only when the player asks.

## Measure
- `tutorial_complete` and `level_end` with time and result; read the first-10-levels funnel and D1 per release (firebase-olcum-ve-uzaktan-ayar.md).
