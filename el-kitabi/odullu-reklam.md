---
title: "Rewarded ads in puzzle and casual games: AdMob's rules, placements, sizing and measurement"
condition: "Unity game project with rewarded ads (Google Mobile Ads, LevelPlay or AppLovin MAX in `Packages/manifest.json` or `Assets/`, or a rewarded offer in the game summary or plans)."
read_when: "Adding, moving or resizing a rewarded ad offer; writing its button text; a rewarded interstitial; deciding daily caps; reading rewarded-ad analytics; a policy warning from AdMob."
requires: —
source: "Google AdMob Help 'Policies for ad units that offer rewards' (answer 7313578), re-read 2026-10-17 · a project session's research (2026-10-16; its vendor benchmarks left out) · the studio's interstitial rule in `google-play-level-up.md` §9"
tech: "Engine-independent design; Unity for the notes on Remote Config and analytics events."
added: "2026-10-17 · template 1.51 · a project session's research for the session manager; the policy rules re-read on AdMob's page"
---
# Rewarded ads

## AdMob's rules (binding, also when LevelPlay or MAX mediates AdMob)
- Show a rewarded ad only after the player clearly opts in (a button that means yes). A rewarded interstitial (shown without that tap) needs an intro screen with a visible, working "no" and time enough to decline.
- Before each ad, say clearly what the player does and gets. Several ads for one reward: say so ("watch 3 ads now to receive 100 gold coins").
- Random rewards: state the chance before the ad, list every possible reward (and whether "nothing" is one); the chance of a reward is above 0.
- Declining never blocks normal play.
- No text or icon beyond describing the reward: no steering ("watch this ad to support us").
- Rewards are non-transferable (only the player who earned it uses it) and never money: no cash, crypto or gift cards.

## Placements that fit puzzles (studio practice)
- The player chooses the moment: after a win, a multiplier on the win's coins (×2 is the safe start); when stuck, one helper (hint, shuffle, undo, extra moves) once its stock is out; an extra slot or a continue after a fail, so a long level isn't lost.
- Interstitials follow their own rule (never between a tap and where it leads, never at level start: `google-play-level-up.md` §9).

## Sizing (studio practice)
- A video's reward stays smaller than the same thing in the cheapest coin or cash bundle, so ads don't replace purchases.
- Remove Ads removes interstitials and banners; rewarded offers stay, optional.

## Caps and measurement
- No 2025-2026 source measured daily caps against retention; published gaps compare watchers with non-watchers (self-selection), so no cap by default.
- Log per placement: offer shown, accepted, reward granted (a `placement` parameter; event plan in `firebase-olcum-ve-uzaktan-ayar.md`).
- Caps live in Remote Config, off by default; turn one on only when data shows farming. One change at a time with an A/B test, judged on D7 retention and ARPDAU together.

## Before a release
- Every rewarded button names its reward with a number; declining keeps the game going; a rewarded interstitial has its intro screen with a visible "no"; the per-placement events arrive in DebugView.
