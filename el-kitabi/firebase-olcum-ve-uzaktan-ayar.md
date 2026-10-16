---
title: Player funnels, D1/D7 retention and remote tuning with Firebase (mobile Unity games)
condition: "Unity project that ships on Android or iOS and has the Firebase Unity SDK. Signs: an Assets/Firebase folder; google-services.json or GoogleService-Info.plist in the project."
read_when: Planning or adding Analytics events; reading where players quit; setting up Remote Config parameters or an A/B test; deciding a difficulty or reward change from player data; updating store privacy declarations after new events.
requires: — (uses the Firebase packages already in the project; adding a Firebase package the game lacks, e.g. Remote Config, is its own planned step)
source: Firebase Unity setup https://firebase.google.com/docs/unity/setup (updated 2026-10-13) · codelab "Implement A/B tests with Firebase Remote Config" https://firebase.google.com/codelabs/implement-a-b-tests-with-firebase-remote-config · pricing https://firebase.google.com/pricing (Remote Config quota and the 2026-09-01 Blaze change, verified 2026-10-14)
tech: Firebase Unity SDK (Analytics, Remote Config, A/B Testing); Unity 6000.x; Android API 24+, iOS 15+
added: 2026-10-14 · research by two project sessions (the second: currency events, sample sizes, fixed gates), reviewed by the session manager (binomial figures recomputed)
---
# Player funnels, retention and remote tuning (Firebase, mobile)

## Summary
- Where players quit and whether a version kept them longer is read from data, not guessed.
- A difficulty or reward value can be tried without a store update.
- With Firebase already in the game this needs no new SDK: one shared event plan, a funnel over the first levels, retention by version, Remote Config with A/B tests.

## Event plan (same names in every studio game)
- Keep it small: at most ~10 custom events per game. The same names in every game make games comparable.
- Use Firebase's recommended events and parameters (constants on `FirebaseAnalytics`):
  - `tutorial_begin`, `tutorial_complete` (`EventTutorialBegin`, `EventTutorialComplete`).
  - `level_start` with `level_name` (`EventLevelStart`, `ParameterLevelName`).
  - `level_end` with `level_name` and `success` (`EventLevelEnd`, `ParameterSuccess`).
  - A game with a currency: `earn_virtual_currency` and `spend_virtual_currency` with `virtual_currency_name` and `value`. They show how often a "not enough gold" moment comes.
  - Ad shown or rewarded, and purchases: check DebugView first for what the ad SDK and the stores already log (`in_app_purchase` is automatic); add only what is missing.
- Automatic events (`first_open`, `session_start`) and the **App Version** user property are collected already: never log or set them yourself.
- A level name is a stable id ("w1-l05"), not a translated title.
- Verify every new event in DebugView before shipping:
  - Android: `adb shell setprop debug.firebase.analytics.app <package>`.
  - iOS: the `-FIRDebugEnabled` launch argument.

## Reading the data
- Funnel: GA4 Explorations › Funnel exploration over `first_open` → `tutorial_complete` → `level_end` for levels 1-10. The steepest drop is the next design question.
- Retention: the D1 and D7 cohort tables with a comparison on App Version; compare the versions before and after a store release.
- Small numbers are noise. A rate from n installs is only good to ±1.96·√(p(1−p)/n) at 95% confidence:
  - 200 installs at 38% D1 means anywhere from 31% to 45%.
  - About 1,000 installs give ±3 points. Decide a retention gate on ≥1,000 installs; below that, write the rate as a range ("D1 38%, 31-45%, 200 installs").
  - Telling two versions 5 points apart (40% vs 45%, 80% power) needs about 1,500 installs per version.
- Write the gate before the data arrives: continue / extend / stop thresholds, channel, countries, target sample. Never move a threshold after seeing the data.

## Remote tuning and A/B tests
- In-app defaults first (`SetDefaultsAsync`); the game must play fully on defaults, offline included.
- `FetchAndActivateAsync` once at startup. Keep the default minimum fetch interval (12 h) in release builds; a shorter interval is for development only.
- Apply fetched values at a safe point: before a level loads or on the next launch, never in the middle of a level.
- Good parameters: wave strength, move count, first-day rewards, interstitial spacing. Never a value that can break a save or a purchase.
- A/B test rules:
  - One change per test; baseline and variant weighted alike.
  - Goal: "Retention (2-3 days)" or a 7-day retention goal; revenue only as a guardrail.
  - Set an activation event (e.g. `level_start`) so only players who reached the changed part are counted.
  - Variant assignment sticks to the installation. Decide only when the planned duration is over: no peeking.
- Quota: Remote Config is free up to 100,000 fetch requests a day per project on both plans. On Blaze, since 2026-09-01, every request above that is billed ($0.06 per 10K). One fetch per launch with the 12 h interval stays far below it; never fetch in a loop or per level.

## Consent and declarations
- Consent goes through `FirebaseAnalytics.SetConsent` together with the ads consent (UMP), never separately:
  - `analytics_storage` and `ad_storage` follow UMP.
  - On iOS, `ad_user_data` and `ad_personalization` are granted only when ATT is authorized. If ATT was denied or never asked, both are denied. Reason: data used for ads after a denied ATT counts as tracking (App Review 5.1.2); studio rule since 2026-10-14.
- New event types: re-check before the version ships:
  - Play Data safety: gameplay events are App activity › App interactions.
  - App Store App Privacy: Product Interaction.
  - The game's privacy page.
- PC builds: Firebase's desktop libraries are a beta for development only and Analytics has no desktop support. No Firebase Analytics in a shipped PC/Steam build; plan PC measurement separately.

## Verification
- DebugView shows each planned event once per action, with the right parameters, and no duplicates of automatic events.
- A Remote Config change in the console reaches a test device on its next launch after the fetch interval; the defaults still apply with the network off.
- The store declarations and the privacy page name what the build sends.
