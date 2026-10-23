---
title: "Pre-release test list: every check before a store release, how to run it, its pass bar, the report"
condition: "Game project that ships to a store (Google Play, App Store or Steam), first release included. Android and iOS rows need that target."
read_when: "The comprehensive test stage of every release (a release plan's penultimate step, BAKIM.md); writing a release plan or a step file's Final test; deciding whether a new test is worth writing."
requires: "The release checklist (`docs/ai/sablonlar/oyun/yayin-kontrol-listesi.md`); an Android emulator or phone with adb and bundletool; iOS rows need the user's Mac and an iPhone (they go to the manual list)."
source: "Read 2026-10-18/19: Play Console Help 9842757 (pre-launch report), 11926878 (target API), 9859372 (size limits) · Android Developers: Core app quality guidelines, Adaptive app quality tier 3, vitals (crash, ANR, launch time), Page sizes (16 KB), Play Billing › Test · Apple: App Review Guidelines, the privacy manifest news of 2024-02-29 and the third-party SDK list, App privacy details, Sandbox Apple Account settings, WWDC23 10142, Audio Session Programming Guide (archived) · Google Mobile Ads for Unity: test ads, privacy (UMP), Ad Inspector; the iOS IDFA message · Firebase: Crashlytics for Unity, DebugView · Unity: Android requirements (16 KB, API levels), iOS Player settings · secondary: a game-testing vendor's interrupt list · the studio's lessons: the test review of 2026-10-18 (§4, bugs that reached players or nearly did) and the shared lessons (emulator, stores, Unity, analytics) · the template entries named in the rows"
tech: "Unity 6000.3, Android 15-16 (target API 36), iOS 26, Unity IAP 5, Google Mobile Ads with UMP, Firebase Analytics and Crashlytics"
added: "2026-10-19 · template 1.54 · asked by the session manager for the owner ('Her taşın altına finalde bakalım'), after the owner's test decision of 2026-10-18 (only an error check while developing, one thorough stage before each release) · template 1.57: the step files' Final tests first, the order, the device matrix, real taps, the report file and the hold rules, from the studio's project research of 2026-10-21 (proje-kontrol-listesi.md) and the owner's words ('en sondan bir önce artık her şey hazır denilen noktada her aşama tek tek test edilsin') · template 1.60: the monkey run in §13, Firebase Test Lab out of the device matrix (the owner's test rule of 2026-10-22: no phone, device-lab or owner rounds)"
---
# Pre-release test list

## 0. How to use
- Once per version, in the comprehensive test stage (BAKIM.md: a release plan's penultimate step, when everything is declared ready). The release checklist says what must be true; this list says how to check it, the pass bar and which games need the row. The test step's matrix starts with every step file's **Final test** in plan order (the version's earlier plans' and phases' too), then the rows here that apply; a skipped row says why. A pass bar is a number or a clear state ("average ≥ 55 FPS", "granted once", "the form shows"), never "works"; a row without one gets one first.
- Order, cheap to expensive: build scans (§1); every suite once and the level solver over every level (§1-2); the store build on an emulator (§13); the step rows in plan order, with §2-8 and §10 grouped in; screens (§9); performance and memory (§11); analytics and crashes (§12); the device matrix and manual rows; store reports after the upload (§14); then the expert's review and the honest check. After a fix: rerun what it touched plus §13's smoke run; on the final build, §1's scans and §13's monkey run again.
- The tested build is the build that ships: same commit and settings; the report names the commit and the SHA-256 of the AAB and IPA (a fix → a new build, new hashes).
- Evidence per row: the command and its result, a log excerpt or a screenshot under `Logs/claude/release/<version>/`. Report: §15. "UI check #n" = arayuz-kalitesi-testleri.md §2.
- Rows whose Pass names a studio bug (the save overwritten at launch, the Monday-only weekly reset, missing currency glyphs, navigation hidden around an ad, the solver passing where the real game fails, a lower jump apex, classes R8 removed) are the permanent regression list: every release runs them.
- Games column: **all** · **levels** · **iap** (purchases) · **ads** · **rew** (rewarded ads, daily or streak rewards) · **time** (anything on the clock) · **pgs** · **gc** · **notif** · **cloud** · **fb** (Firebase) · **and** · **ios**; plain words ("with tests", "links") mean games that have that thing.
- Settings a row changes on a device (clock, network, battery saver, developer options) are changed only on the emulator and put back at the row's end: `adb shell settings put global auto_time 1`, `svc wifi enable`, `svc data enable`, `settings put global low_power 0`, "Don't keep activities" off; then a cold boot.
- New tests only where a row keeps failing or a bug would cost players or money (the Unity test rule › New tests); a test for a fixed bug is seen failing without the fix first.

### Device matrix (at least)
| Profile | Looks at | Where |
|---|---|---|
| Android low end: 3-4 GB RAM, near minSdk, a weak GPU | FPS, memory, heat, launch | A real device (emulators don't measure FPS): the pre-launch report's performance data, or a low-end phone where the user has one (manual; buying one is the user's call). The studio runs no phone or device-lab rounds (the owner's rule, 2026-10-22): there the pre-launch report and the emulator rows stand in, and an unmeasured FPS is "not assessed: no device" |
| Android current: 15-16, edge-to-edge, 16 KB | System bars, cutouts, new API behaviour, 16 KB pages | Emulator (Android 15-16 and a 16 KB system image) |
| Emulator with the Play Store | Rating card, purchases with test cards, Play Games sign-in | A Play Store image signed in to the studio's test account |
| Tablet 10" and a foldable or resizable | Rotate, fold, split, resize; state kept | Medium Tablet, Pixel Fold, Resizable emulators (§8) |
| 5 screen profiles × 2 languages | Layout and scores | arayuz-kalitesi-testleri.md (§9) |
| iPhone with a notch or Dynamic Island | ATT order, silent switch, Game Center, sandbox purchases | The user's iPhone (manual) |
| iPad, when the game runs on iPad | iPad layout, window sizes | Manual, or the simulator on a Mac |

## 1. Suites and build scans
| Check | How | Pass | Games |
|---|---|---|---|
| Every suite once | EditMode and PlayMode from the Commands table (`testler.sh` with the editor closed) | Exit 0 with a total above 0 (the Unity test rule › Result); red handled as BAKIM.md says | with tests |
| 16 KB pages | AAB: `bundletool dump config --bundle=<aab> \| grep alignment` → `PAGE_ALIGNMENT_16K`. APK: `zipalign -c -P 16 -v 4 <apk>` (build-tools 35+) → "Verification successful", or `check_elf_alignment.sh <apk>` → every arm64-v8a library ALIGNED | Aligned. From 2027-02-01 Play refuses updates that target API 35+ without it. Unity 6000.0.38f1+ builds it (Unity's Android requirements page), so the risk is old third-party `.so` files (ads, Firebase); a 4 KB build doesn't run on 16 KB phones (Unity staff on its forum) | and |
| Target API, permissions | `bundletool dump manifest --bundle=<aab>` | targetSdk 36 (Play, new apps and updates from 2026-08-31; Unity 6000.0.46f1+, its Android requirements page); only needed permissions, no VIBRATE (`Handheld.Vibrate`) | and |
| Test settings gone | Search the project and the build for test device IDs, Google's demo ad units (`ca-app-pub-3940256099942544/…`), a Crashlytics tester, UMP debug geography, cheat menus | None in the store build (Google: remove test-device code before release) | ads, fb |
| Minified build | `r8-kontrol.py` (google-play-level-up.md); then §7 and §13 on the release build | Achievements list, rating prompt, ads, purchases and notifications work | and |

## 2. Levels and progression
| Check | How | Pass | Games |
|---|---|---|---|
| Every level finishable in the real game | Puzzles: replay the solver's moves through the game's own input and rules, not the solver's model (Project E's cars stacked while the solver passed). Movement or physics games: a bot or reachability scan over every level with the real controller (jump apex, speeds), whenever movement, physics or level data changed | 100% of levels; the report names the tightest margins | levels |
| Feel unchanged | Movement or physics changed: measure jump height, speeds and timings against the last release's numbers, never against the new setting (Project B 5.0: coyote time and a jump buffer lowered the real apex 1.34 → 1.15 m, level 13 needs 1.5 m, and the step's test measured the new setting) | Same, or the change is intended and written in the plan | levels with physics |
| Progression | First to last level: unlocks, stars, rewards; finishing the last level; level select afterwards | No dead end, crash or empty screen | levels |

## 3. Save and data
| Check | How | Pass | Games |
|---|---|---|---|
| Relaunch | Kill mid-level, after a win, after a purchase (`adb shell am force-stop <package>`; iOS: swipe it away), relaunch | Progress, currency, purchases and settings intact | all |
| Upgrade over the last release | APK sets from the previous release's AAB (kept from that release) and from the new one with `bundletool build-apks --connected-device`: without `--ks` both get the same debug key, so no keystore password. `install-apks` the old one, play and buy (license testers may sideload debug-signed builds), then the new one over it. A local build can't replace the Play-signed store install (another signature) | Save intact; migrations run once | all after a first release |
| Old save files | Load a save kept from each released version (one fixture per release) | Loads; nothing reset | all |
| Launch order | Cold start with a full save; log when the save loads and when store restore, ads or cloud callbacks first write | Nothing writes before the save has loaded (Project L 1.3-1.5: the remove-ads restore ran first and overwrote the save with defaults; a closure code review found it) | iap, cloud |
| Broken or missing save | Truncate the save file, start | Starts; the file or its backup is kept, never overwritten with defaults | all |
| Clean install | Uninstall, install, start | First run again (tutorial, consent), no leftovers | all |
| Cloud save | Second device, or reinstall and sign in | Newest progress wins, nothing lost | cloud |

## 4. Purchases
| Check | How | Pass | Games |
|---|---|---|---|
| Every product, Android | A license tester with Play's test payment methods: always approves, always declines, a slow card that approves or declines after a few minutes | Approved → granted once; declined → nothing granted, a message; slow → granted only once it approves, and still nothing after a slow decline and a restart | iap |
| Acknowledged | Wait ~5 minutes after a test purchase; look at the order in Play Console | Not refunded (Play refunds an unacknowledged test purchase within minutes, a real one after 3 days) | iap |
| Every product, iOS | A Sandbox Apple Account on the user's iPhone; "Interrupt Purchases for This Tester" for the interrupted path (manual) | As on Android; an interrupted purchase is granted once after the tester accepts the terms | iap + ios |
| Double tap, kill in between | Two taps in one frame (UI check #22); kill the app between payment and grant | One charge, one grant; after relaunch the pending order is granted once (grant, then one save: the shared package's `SaveScope`) | iap |
| Restore | Reinstall, then Restore Purchases (iOS needs a restore mechanism, App Review 3.1.1); Android restores on start | Non-consumables and remove-ads come back | iap |
| Refund | Refund a tester order in Play Console's order management | As designed (revoked or kept), no crash | iap |
| Price text | The store's localized price strings in tr, en and foreign currencies (₺ ₹ ₽ € R$ £ ₩) on every price label | Every symbol renders, never "□" (Project G: 11 of 12 labels lacked ₺ ₹ ₽) | iap |

## 5. Ads and consent
| Check | How | Pass | Games |
|---|---|---|---|
| Test ads only | Every test build: the device's ID in `RequestConfiguration.TestDeviceIds` via `MobileAds.SetRequestConfiguration`, or Google's demo units; Ad Inspector (Unity plugin 7.0.0+, test devices only) shows each network | AdMob ads carry a "Test Ad" label; mediated ads carry none, so we never tap a live one (Google: clicking ads outside test mode risks the account) | ads |
| Rewarded | Watch to the end; close early; no fill; offline | Reward once, after completion; none when closed early; the button only when an ad is loaded; offline says so | rew |
| Interstitial placement | Play through results and navigation | The release checklist's interstitial line holds: navigation never hidden around an ad; no ad right after a tap that leads somewhere, at level start or on exit | ads |
| Remove ads | Buy, relaunch, restore | No interstitials afterwards; rewarded still offered | iap + ads |
| Consent in the EEA | `ConsentDebugSettings` with `DebugGeography.EEA` and the device's `TestDeviceHashedIds` (works only on test devices); `ConsentInformation.Reset()` between runs | `Update()` on every launch, then the form if required; ads requested only when `CanRequestAds()`; the choice persists; a settings entry reopens it (UMP's privacy options) | ads |
| Consent elsewhere | Debug geography off | No form; ads serve | ads |
| iOS order | Fresh install on an iPhone; to ask again, uninstall and reinstall (manual) | UMP's IDFA explainer comes before Apple's tracking alert (Google's page; consent form first is a secondary reading); declining sends no IDFA and ads still serve | ads + ios |
| Nothing before consent | Emulator: logcat by the game's pid, or a DNS log (unity-derleme-ve-bellek.md › Emulator checks) | Before the answer only UMP's and the store's hosts (Project B's check) | ads, fb |

## 6. Rewards and time
| Check | How | Pass | Games |
|---|---|---|---|
| Day change | A fake clock in code (a test written in this stage) plus the emulator's clock (`adb shell settings put global auto_time 0`, then set the date; `auto_time 1` at the end) | A daily reward once per local day; "tomorrow" labels right | time |
| Week and month | Cross a day change from every weekday, and month and year ends | Weekly resets work from any launch day (Project G 2.6-3.x reset only on a Monday launch; an emulator run on a Sunday found it) | time |
| Clock tricks | Clock forward, then back; another time zone; a DST night | No double claim, no lost streak, no crash | time |
| Offline | Airplane mode at reward time | Works offline or says why | time |

## 7. Platform services
| Check | How | Pass | Games |
|---|---|---|---|
| Play Games sign-in | A build signed with the upload key (made in the editor where the user typed the keystore password) or, after release, the store install; a fresh account | Signs in (the credentials list the app signing key, the upload key and any earlier signing key: Project F 2026-10-18); the achievements list opens (an R8 keep rule, else nothing opens) | pgs |
| Game Center | iPhone (manual) | Banner at start, never over the UMP form or an ad; achievements unlock | gc |
| Notifications | Fresh install, Android 13+ and iOS | yerel-bildirimler.md › Verification; never used to advertise another product (Android core quality) | notif |
| Rating prompt | The release build | Opens at the planned moment only (Play's In-app Review library survives R8) | prompt |
| Deep links | `adb shell am start -a android.intent.action.VIEW -d "<url>" <package>` | The right screen opens | links |

## 8. Interruptions and lifecycle
Android's core app quality tests are the anchor (Home, Recents, sleep, a notification or call arriving; state such as game progress kept).

| Check | How | Pass | Games |
|---|---|---|---|
| Home, Recents, sleep | Mid-level: Home (`adb shell input keyevent KEYCODE_HOME`), back from All Apps and from Recents after 10 s and 10 min; screen off and on | Same state; paused while away; fair timers; sound back | all |
| Process death | Background the game, then `adb shell am kill <package>` (or the developer option "Don't keep activities", off again afterwards), return | A sensible state, no crash | and |
| Call, alarm, notification shade | Emulator: `adb emu gsm call 5551234`, then `adb emu gsm cancel 5551234`; on a phone the real thing | Pauses; sound stops or ducks and returns | all |
| Network loss | `adb shell svc wifi disable` and `svc data disable` at launch, mid-purchase, mid-ad, mid cloud save (`enable` afterwards) | No hang, a message, retry works | online parts |
| Power saving | Battery saver (`adb shell settings put global low_power 1`, `0` afterwards); iOS Low Power Mode | Playable; the reduce-motion reader copes with animator scale 0 (battery saver can set it) | all |
| Back button | `adb shell input keyevent KEYCODE_BACK` on every popup and screen | Closes only the top popup; never quits mid-level (UI check #21) | and |
| Large screens | Medium Tablet, Pixel Fold or the resizable emulator: rotate, fold, resize, split screen from Recents, Home, reopen the pair (Android's tier 3 "adaptive ready" tests) | No crash; state kept; all UI reachable; no letterboxed compatibility mode. Android 16 may ignore a portrait lock on large screens (a game exemption: not re-verified): look at landscape on a tablet | and |
| Taps through panels | Close a panel with a tap over the board | The tap doesn't act in the game (Project K) | all |
| First launch full screen | Fresh install of an immersive game | Android's one-time "Viewing full screen" notice doesn't freeze input (Unity 6000.3) | and |

## 9. Screens, text, accessibility
| Check | How | Pass | Games |
|---|---|---|---|
| Screen matrix and scores | arayuz-kalitesi-testleri.md (5 profiles × 2 languages); arayuz-kalitesi.md §5 | Green; scores as §5 rules (the floor blocks, a missed target is explained) | all |
| Navigation walk | From home, open every screen and popup and leave it again, with ads loaded and with none | Every screen reachable and left again; no dead end; close and back work | all |
| Real taps | Every screen's main buttons pressed through the input system on the emulator (`adb shell input tap`); code calls (`onClick.Invoke`, `ExecuteEvents`) and editor captures don't count (a game once shipped without an EventSystem: its buttons had only been called from code) | Every main button acts on a real tap | all |
| Glyphs and casing | Every label in tr and en with the longest strings and prices; Turkish İ/ı; no TMP case styles on localized labels | No missing glyph or fallback face; correct Turkish casing | all |
| Tablet and notch | The tablet profile; a real notch phone (manual) | Physical sizes kept; nothing under system bars | mobile |
| Accessibility basics | Reduce-motion and haptics switches; colour-blind check (renk-korlugu-palet.md); contrast (UI check #7); the App Store accessibility labels re-tried (a Grayscale run) | As declared | all |

## 10. Sound
| Check | How | Pass | Games |
|---|---|---|---|
| Silent switch | iPhone with the Ring/Silent switch on (manual) | Silent: Apple's Ambient and SoloAmbient (the default) categories are both silenced by the switch and by screen lock | ios |
| Other apps' music | Start music in another app, then open the game; and start it while the game plays | iOS: it keeps playing unless "Mute Other Audio Sources" is on (Unity's iOS Player setting). Android: the game takes and returns audio focus, and stops or lowers its sound when another app starts playing (core quality) | all |
| After an interruption | A call or alarm mid-play | Sound comes back, or the game shows it is paused | all |
| Settings | Music and sound sliders and mutes | Persist across relaunch | all |

## 11. Performance and size
| Check | How | Pass | Games |
|---|---|---|---|
| Frame rate | The lowest target phone (emulators lie about FPS); `Application.targetFrameRate` set | Play's Level Up bar: average ≥ 55, P90 ≥ 50, P99 ≥ 30 FPS (google-play-level-up.md §7) | all |
| Memory | Peak on a 4 GB-class phone | ≤ 2.25 GB in the foreground (Play's bar for all games from Feb 2027) | and |
| Heat and battery | 20-30 min on a phone (manual) | No throttling drop; warm, not hot | all |
| Cold start | Emulator: time to the logcat line where the system splash goes (`Splash Screen <package>}: Setting back callback null` on an Android 15 image), not `am start -W` (it times only the first frame); median of 5 | Well under 5 s, the bar where Android vitals calls a cold start excessive (warm 2 s, hot 1.5 s) | all |
| Long session | The checklist's 4+ hour run: the project's soak rig, or a bot over as many levels as it can | Memory flat, no slowdown, no crash | all |
| Size | Measure the AAB, APK and IPA files (never `BuildReport.summary.totalSize`: 766.7 MB for a 53.2 MB APK) | The game's budget; Play: base module ≤ 500 MB compressed, and over 200 MB players on mobile data see a dialog; iOS: ≤ 4 GB uncompressed | all |
| Live stability | Android vitals of the last release (the checklist's vitals line) | Below Play's bad-behaviour bars: user-perceived crash rate 1.09% (8% on any device model), user-perceived ANR rate 0.47% (8% per model) | and |

## 12. Crashes, analytics, privacy
| Check | How | Pass | Games |
|---|---|---|---|
| Crash reporting | A test build with Firebase's `CrashlyticsTester` sample (throws "test exception please ignore" a few seconds after start); never in a store build | Shows in Crashlytics within minutes (none after 5: turn on debug logging); Android IL2CPP symbols uploaded (`firebase crashlytics:symbols:upload --app=<app id> <symbols>`; iOS is automatic) so stacks read | fb |
| Events | firebase-olcum-ve-uzaktan-ayar.md › Verification (DebugView: `adb shell setprop debug.firebase.analytics.app <package>`, off with `.none.`) and its first-release GA4 checks | Each planned event once with its parameters; none before consent where gated | fb |
| Store robots | `adb shell settings put system firebase.test.lab true` (delete it afterwards) | No analytics event sent | fb |
| Unexpected hosts | Logcat or DNS at launch | Only the declared SDKs talk (Project H 8.4: Unity's old cloud services phoned home) | all |
| Declarations | Play Data safety and App Privacy against the SDK list and their privacy manifests (partners' collection counts); the privacy page | Same as the build; an ad game never says "Data not collected"; the policy is reachable in the app (App Review 5.1.1) | all |

## 13. The store build on an emulator (every Android release)
- **Smoke run:** install the store build from its AAB (bundletool's debug signing; Play Games sign-in is §7's), or on an x86_64 emulator its variant without Optimized Frame Pacing (it crashed under ARM translation: unity-derleme-ve-bellek.md › Emulator checks; never change the store build itself). Start, play levels 1-3, kill and relaunch, check the save, one test ad; read the consent state from the log (the EEA form is §5's, with debug settings the store build doesn't carry); logcat by the game's pid free of errors and exceptions.
- **Monkey run** (the same install, after the rows above): `adb shell monkey -p <package> -s <seed> --throttle 100 --pct-syskeys 0 -v 10000`: 10,000 random taps, swipes and keys inside the game only (`--pct-syskeys 0` leaves Home, Back and volume out), ~17 minutes at 100 ms; logcat by the game's pid: no crash (`FATAL EXCEPTION`, a native signal), ANR or uncaught exception; the seed goes into the report, so a failure replays with the same seed. It reaches what scripted rows don't press (double taps, odd orders, edges of the screen). Only with test ads (the emulator registered as a test device, §5) and a license tester's test cards: random taps on a live ad risk the AdMob account. Games: all Android.
- iOS: the user's run on an iPhone is a manual test.

## 14. Store compliance
| Check | How | Pass | Games |
|---|---|---|---|
| Pre-launch report | After the upload, before sending for review (not uploaded in this plan → "not assessed", the row goes to the submission list): Play Console › Test and release › Testing › Pre-launch report (it runs on upload and when a release is saved to production, if Google's device lab has room; US devices, Android 9+, usually within an hour) | No crash or ANR; accessibility findings fixed or written down. A game needs a game loop for a good report (Google's words; adding one is a plan of its own); test devices can't buy | and |
| iOS privacy manifests | The exported Xcode project: `PrivacyInfo.xcprivacy` of UnityFramework and of every SDK on Apple's third-party SDK list (the Firebase parts, GoogleUtilities, nanopb…), at versions that ship manifests and signatures | Present, with approved reasons for the required-reason APIs; after the upload (as with the pre-launch report), no missing-reason warning | ios |
| App Review basics | 2.1 tested on a device, no crash or placeholder, every in-app purchase complete, visible and working; 2.3 metadata and privacy information match the game, screenshots show it in use; 2.4.1 runs on iPad whenever possible; 3.1.1 a restore mechanism, bought currency never expires, loot box odds shown; 5.1.1 a privacy policy in the app, account deletion if accounts exist; 5.1.2 tracking only after ATT and never required | All hold (app-store-game-center.md §7 too) | ios |
| Age rating | The questionnaire's answers against the build (ads, purchases, chat or user content, gambling-like mechanics) | Same as the build | all |
| Store checklists | google-play-level-up.md §7 quality table; app-store-game-center.md §7 | Every line met or explained | and, ios |

## 15. Report and decision
File: `Logs/claude/release/<version>/rapor.md` beside the evidence; its summary (counts, decision, the file's path) in the test step's file, which git keeps. Then the version's rows in `manuel-testler.md` (device feel, haptics, sound balance, a real notch); the expert reviews this report and the screenshots, then the honest check (BAKIM.md › Comprehensive test stage, step 5), before the release step.
- **Hold** if any: a crash, ANR or freeze in a main flow; save loss; a wrong or double grant, restore broken, a purchase not acknowledged; an ad or analytics request before consent, a test setting in the store build, navigation hidden or delayed around an ad; declarations (Data safety, App Privacy, the privacy page) contradicting the build; a dated requirement unmet (target API, 16 KB, Xcode and SDK, privacy manifests); an unsolvable level; a screen score below the floor (3); the lowest phone missing the FPS bar without a written reason; an open critical or major bug; a crash or ANR in the pre-launch report.
- **Release:** everything green, or written as an accepted risk with its reason; the expert's note; with a session manager, its approval of the submission list. A direct 100% release can't be halted (a fix ships as a new version), so the bar stays strict.
- On release the file's first line is `SONUÇ: GEÇTİ <version>-<build>` (a packaging gate may look for it at a line's start).
```
SONUÇ: GEÇTİ 5.3-41
## Comprehensive test report: <game> <version> (<date>) · commit <…> · AAB SHA-256 <…> · IPA SHA-256 <…>
| # | Plan step / row | Check | Result | Evidence |
|---|---|---|---|---|
| 1 | — / 1.1 | Every suite once | ✓ EditMode 412/412, PlayMode 88/88 | Logs/claude/release/5.3/suites.txt |
| 2 | 17 / 2.1 | Every level finishable | ✓ 120/120, tightest L47 (0.08 m) | Logs/claude/release/5.3/levels.txt |
| 3 | 24 / 4.4 | Double tap, kill in between | ✗ → fixed in abc1234, rerun ✓ | Logs/claude/release/5.3/iap.log |
| 4 | 12 / 10.1 | Silent switch | manual (manuel-testler.md) | — |
Manual: <rows> · Not assessed: <rows, why> · Accepted risks: <…> · Red left: <none, or the tech-debt lines>
Screen scores before/after: <…> · Expert: <note> · Honest check: <one paragraph> · Decision: release / hold
```
