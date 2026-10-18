---
title: Player funnels, D1/D7 retention and remote tuning with Firebase (mobile Unity games)
condition: "Unity project that ships on Android or iOS and has the Firebase Unity SDK. Signs: an Assets/Firebase folder; google-services.json or GoogleService-Info.plist in the project."
read_when: Planning or adding Analytics events; reading where players quit; setting up Remote Config parameters or an A/B test; deciding a difficulty or reward change from player data; updating store privacy declarations after new events.
requires: — (uses the Firebase packages already in the project; adding a Firebase package the game lacks, e.g. Remote Config, is its own planned step)
source: Firebase Unity setup https://firebase.google.com/docs/unity/setup (updated 2026-10-13) · codelab "Implement A/B tests with Firebase Remote Config" https://firebase.google.com/codelabs/implement-a-b-tests-with-firebase-remote-config · pricing https://firebase.google.com/pricing (Remote Config quota and the 2026-09-01 Blaze change, verified 2026-10-14)
tech: Firebase Unity SDK (Analytics, Remote Config, A/B Testing); Unity 6000.x; Android API 24+, iOS 15+
added: 2026-10-14 · research by two project sessions (the second: currency events, sample sizes, fixed gates), reviewed by the session manager (binomial figures recomputed) · 2026-10-18 (template 1.53): the GA4 audit before a first release (Project F 1.0, the session manager's standard of 2026-10-17)
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

## Before the first release: GA4 audit (studio standard)
Every Firebase game, before its first release (Project F's GA4 property was empty, and two other games' too; 2026-10-17). Applied in Project F 1.0; Google's own pages not re-read for this list:
1. **Custom dimensions:** every event parameter the game sends (e.g. `level_name`, `success`, `source`, `item_name`) is an event-scoped custom dimension in *GA4 › Admin › Custom definitions*. Not retroactive: register a new parameter before the build that sends it (one not seen in the data yet can be typed in).
2. **Event data retention 14 months** (*Data collection and modification › Data retention*; the default is 2 months, and explorations look back only that far).
3. **Play's pre-launch robots:** the report runs on Firebase Test Lab devices. When `Settings.System` "firebase.test.lab" is "true", collect no analytics (send no events); Crashlytics and ads stay on (Google's ad networks filter Test Lab traffic themselves: Test Lab docs). Unity: `new AndroidJavaClass("android.provider.Settings$System").CallStatic<string>("getString", resolver, "firebase.test.lab")` (Project F `Assets/_Game/Ads/TestLabDevice.cs`). Emulator test: `adb shell settings put system firebase.test.lab true`, afterwards `settings delete system firebase.test.lab`.
4. **AdMob link** (*GA4 › Product links › Google AdMob links*): without it no `ad_impression`, so no ads per player. GA4 lists only AdMob apps with store details: after store approval add the store listing to the AdMob app, then link.
5. **Developer traffic filter** (*Data filters › Create filter › Developer traffic*: events carrying `debug_mode` or `debug_event`, exclude): "Testing" first, "Active" after a DebugView check; "Active" is permanent, matching events never come back.
6. **End-to-end check:** on an emulator `adb shell setprop debug.firebase.analytics.app <package>` (verbose log: `setprop log.tag.FA VERBOSE`, `setprop log.tag.FA-SVC VERBOSE`); open the game, give consent, play a level; logcat shows "Logging event" and "Successful upload ... 204", and *GA4 › Realtime* shows the event and its parameter values. DebugView may show the device late or never (Project F: empty for 6 minutes while Realtime had the events). Afterwards `setprop debug.firebase.analytics.app .none.` and uninstall.

## Verification
- DebugView shows each planned event once per action, with the right parameters, and no duplicates of automatic events.
- A Remote Config change in the console reaches a test device on its next launch after the fetch interval; the defaults still apply with the network off.
- The store declarations and the privacy page name what the build sends.
