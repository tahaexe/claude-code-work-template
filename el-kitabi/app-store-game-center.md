---
title: App Store structure for iOS games (Game Center, In-App Events, first submission, direct release)
condition: "Unity project with iOS (App Store) among the target platforms. Signs: iOS in the game summary or memory; an Xcode project under `Builds/`. Unsure → ask the user one question."
read_when: Preparing an App Store release or a first submission; planning Game Center sign-in, achievements or leaderboards, In-App Events, in-app purchases on iOS, iOS quality (FPS, screens, controllers, cloud save); App Review risks (spam, metadata, privacy, ATT), privacy manifests, age rating, iPad window resizing, Accessibility Nutrition Labels.
requires: — (the user's Mac with Xcode for building, device runs and upload; Apple's GameKit plug-in is built there once if chosen)
plan_candidates:
  - "App Store 1: Game Center sign-in and achievements (Play's list), Restore Purchases · el-kitabi/app-store-game-center.md"
source: App Store Connect Help (Configure achievements · Offer in-app events · Select an App Store version release option · Release a version update in phases · EU DSA trader requirements · Accessibility Nutrition Labels: overview, Differentiate Without Color Alone, Reduced Motion and Larger Text criteria; Larger Text and Reduced Motion re-read 2026-10-17) · Unity Manual "Social API", `iOS.Xcode.ProjectCapabilityManager.AddGameCenter`, iOS Player settings (6000.5) · github.com/apple/unityplugins · App Review Guidelines 2.1, 2.3, 3.1.1, 4.3, 5.1.1, 5.1.2 · developer.apple.com/news/upcoming-requirements · Apple news 2026-07-09 (age rating: social media) · developer.apple.com/support/third-party-SDK-requirements · TN3192 (`UIRequiresFullScreen`)
tech: Unity 6.3 · Game Center via Apple.GameKit (apple/unityplugins) or Unity's Social API (deprecated) · Unity IAP v5 (StoreKit) · Xcode 26, iOS 26 SDK
added: 2026-10-09 · compiled from official docs by Claude; iOS counterpart of google-play-level-up.md · 2026-10-15 §7 before Submit for Review, Accessibility Nutrition Labels: a project session's research, each fact re-read on Apple's or Unity's page (1.46) · 2026-10-17 (1.51): own in-game settings for Larger Text and Reduced Motion (a project session's note of 2026-10-16) · 2026-10-18 (template 1.52): Accessibility Nutrition Labels criteria refined (the studio's UI research) · template 1.53: Apple.GameKit 4.1.0 and the macOS-only link step, the Social API in practice and with UMP, submitting through the API (the studio's research and shared lessons)
---
# App Store structure for iOS games

## Summary
The iOS counterpart of `google-play-level-up.md`: Game Center sign-in and achievements, In-App Events for updates, purchases with a restore button, quality items, direct release and the checks before **Submit for Review** (§7). Screenshot sets: `store-listing-optimization.md` › Limits. Play Games Rewards, Game Stats, R8 and edge-to-edge have no iOS counterpart. A game on both stores shares one achievement list and one purchase grant structure.

## Know first
- **App Store Connect work is Claude's,** in its own Chrome profile (Claude in Chrome, `tarayici-baglantisi.md`); built-in safety confirmations remain. The user keeps agreements, tax and banking, the Mac build and upload (Xcode or Transporter) and **Submit for Review** (release split). Record IDs and texts in `docs/ai/tasarim/app-store.md` (create it if missing, index it in `HAFIZA.md`).
- **Builds:** Claude builds the Xcode project into `Builds/` on Windows; compiling, device runs and upload need the user's Mac, so device checks are manual tests.
- **One achievement list for both stores:** a shared key per achievement in code, mapped to the Play ID and the Game Center ID (reverse DNS, e.g. `com.studio.game.first_win`).

## 1. Game Center sign-in
- **Capability:** a `[PostProcessBuild]` editor script adds Game Center to every generated Xcode project: `PBXProject` → main target → `new ProjectCapabilityManager(...)` → `AddGameCenter()` → `WriteToFile()`. A version with Game Center features can't be submitted without this entitlement and Game Center set up in App Store Connect.
- **Library** (decide in the plan, record in `hafiza/kararlar.md`):
  - Apple's official **Apple.GameKit** plug-in (`apple/unityplugins`, with Apple.Core): no prebuilt release; built once on the user's Mac (`python3 build.py`), then the `.tgz` packages from `Build/` are added to the project. Long-term path; default when the user can run that build.
  - Unity's **Social API** (`Social.localUser.Authenticate`, `Social.ReportProgress`, `Social.ReportScore`; `UnityEngine.SocialPlatforms.GameCenter`): works in Unity 6.3 without packages, but Unity marks it deprecated ("will be removed in a future release") → if chosen, add a tech-debt line.
- Sign in at startup; a failure never blocks the game: Game Center features stay off until signed in (as on Play).
- **Apple.GameKit 4.1.0** (2026-09-16): still no prebuilt packages; `build.py` needs a Mac with Xcode, python3, npm and Unity; requires Apple.Core 3.3.0, iOS 15.0+, Unity 2022.3+. Apple's plug-ins add their native libraries to the Xcode project in a step compiled only on macOS (`#if UNITY_EDITOR_OSX` in Apple.Core's `AppleBuild.cs` `[PostProcessBuild]`, likewise Accessibility's build step): an Xcode project exported on Windows may lack them (open issue #125 in `apple/unityplugins`; read from the source, untested) → export on the Mac or check the link. `Assets/Plugins/iOS/*.mm` files are copied on Windows too (enough for reduce motion and haptics: oyun-hissi.md).
- **Social API in practice** (read 2026-10-17, Unity 6000.3.17f1): its iOS code calls current GameKit (`setAuthenticateHandler:`, `+[GKAchievement reportAchievements:withCompletionHandler:]`, `setShowsCompletionBanner:`) and looks classes up by name, so GameKit deprecations don't break the link; callbacks run on the main thread. `Social.ShowAchievementsUI()` opens `GKGameCenterViewController`, deprecated since iOS 26 (still works; Apple names no replacement, but `GKAccessPoint`'s trigger methods open the same screens: GameKit only).
  - Report only while `Social.localUser.authenticated`: a report without a session logs "Must authenticate first" and may never call back. Send only the ids `Social.LoadAchievementDescriptions` lists; if that list fails to load once at launch, nothing goes through that session, so reload it on the next report.
  - Unity keeps one static sign-in callback, so GameKit's later state changes (a sign-in or sign-out in iOS Settings while the game is in the background) don't reach the game: while signed out, sign in again when the app returns.
  - The sign-in sheet can appear over the UMP consent form or an open ad: start sign-in only when no form or ad is showing (a UMP timeout covers only the consent update). Example: Project D `GameRoot.Achievements.SignInWhenNothingShows`, `GameCenterAccount.LoadListAgain`.

## 2. Achievements
- App Store Connect: *Apps > app > Game Center > Achievements > Add Achievement*. The same list as Google Play (at least 10; the 4 earnable in the first hour fit both).
- Fields: reference name, achievement ID (permanent), points (100 per achievement, 1,000 per game), hidden until earned, earnable more than once. Per language: title, pre-earned and earned description, image (512×512 or 1024×1024).
- Up to 100 per app. Once live, an achievement can't be deleted and its points can't change.
- Players see an achievement only after approval: add new ones to the app version's Game Center section, so they are reviewed with it.
- Leaderboards: same place, optional; only for a score worth ranking.

## 3. Purchases (Unity IAP on StoreKit)
- The grant structure of `google-play-level-up.md` section 3 applies unchanged: grant once, save before confirm; pending purchases (Ask to Buy) arrive later.
- **Restore Purchases button** for non-consumables (App Review Guidelines 3.1.1); API in `unity:implement-in-app-purchases` (Apple extensions).
- New products go to review with an app version.

## 4. In-App Events (counterpart of Play's promotional content)
- For each content update or in-game event: App Store Connect *In-App Events*: event name ≤30 characters, short description ≤50, long description ≤120, a badge (e.g. Major Update, Live Event, Challenge), card and details media, start and end (15 minutes to 31 days).
- Reviewed on its own once the app is approved (the first one goes with the first version); submit a few days ahead.
- Claude creates it; discounts and offer codes cost money → only with the user's OK.
- Badges, limits, media, what gets rejected and the per-release plan step: `store-events.md`.

## 5. Quality
| Item | What the game does |
|---|---|
| 60 FPS | `Application.targetFrameRate = 60` (Unity runs at 30 FPS on mobile by default) |
| Screens | UI inside `Screen.safeArea` (notch, Dynamic Island, home indicator); iPad aspect ratios |
| Controllers | Input System: MFi, Xbox and PlayStation controllers work on iOS |
| Cloud save | Unity Cloud Save (`unity:build-live-game`), shared with Android, if the game keeps progress across sessions |

## 6. Direct release (no testing; user decision 2026-10-09)
- No TestFlight.
- Version page: *App Store Version Release* → "Automatically release this version"; *Phased Release for Automatic Updates* → "Release update to all users immediately".
- New Game Center items, purchases and events ride with the version.
- Claude fills the version (release notes in both languages, metadata); the user uploads the build and presses **Submit for Review**.
- Trade-off: no phased pause; a fix ships as a new version.

## 7. Before Submit for Review
Mostly a first version's risks. Apple's rules move with each autumn's devices and SDKs: recheck the cited pages before a first submission.
- **Toolchain** (Upcoming requirements): uploads must be built with Xcode 26+ and the iOS 26 SDK (since 2026-04-28) and target iOS 13+ (since 2026-09-09); check the Mac's Xcode before the build day.
- **Crowded genres (4.3(b)):** Apple turns away apps that can't be told apart from what is already widely available unless they are meaningfully different or better; its named examples aren't games (flashlight, wallpaper, fortune telling…), but a familiar genre (mahjong, solitaire, match puzzles) carries the risk. The review notes say what is distinct (studio practice): "No account needed. What is distinct: <1-3 mechanics>, <accessibility>, <content and how it is checked>."
- **Submitting through the App Store Connect API** (Project F 1.0, 2026-10-17): read the version back first (Apple refuses a submission without a large iPhone set, 6.9" or 6.5"); then `reviewSubmissions` (platform) → `reviewSubmissionItems` with the `appStoreVersion` and each first product's `inAppPurchaseVersion` (`GET /v2/inAppPurchases/<id>/versions`, the `PREPARE_FOR_SUBMISSION` one) → `PATCH submitted: true`: first products ride with the version without the browser. curl needs `-g` for `fields[...]` URLs. Apple also takes a second submission while one waits (an In-App Event went beside a version, 2026-10-17). Submitting still needs the approval the project requires.
- **Review notes (2.1, 2.3.1):** explain non-obvious features and every in-app purchase (and why a configured one can't be found in the build); describe a version's new features specifically, never generically.
- **Metadata (2.3, 2.3.7):** screenshots and previews show the real game; no trademarks, other apps' names, prices or unverifiable claims in the name, subtitle or keywords (wording: `store-listing-optimization.md`).
- **Privacy (5.1.1(ii), 5.1.2(i)):** purpose strings say plainly and fully what the data is for; tracking only after ATT permission; no feature, content or reward may depend on allowing tracking or data access.
- **Privacy manifests:** no upload without approved reasons for the required-reason APIs in the game's and its SDKs' code (since 2024-05-01). Apple's list of SDKs that need their own manifest in a new app (and a signature when shipped as a binary) has `UnityFramework` and Firebase libraries (`FirebaseCore`, `FirebaseCrashlytics`…), not Google Mobile Ads or UMP. Keep SDKs current; Xcode's privacy report (when preparing distribution) shows what the build declares.
- **Age rating:** answer the current questionnaire in *App Information*, social-media questions included (required for new apps and updates since September 2026; social media = redistributing, amplifying or interacting with user content through a feed).
- **EU:** DSA trader status, given at account level (*Business > Agreements > Compliance*; per-app changes in *App Information*); apps without it are removed from the EU App Store.
- **iPad** (game runs on iPad): `UIRequiresFullScreen` (Unity: *Player > iOS > Resolution and Presentation > Requires Fullscreen*) is deprecated since iPadOS 26; Stage Manager (iPadOS 18+) and iPadOS 26's windowed apps already resize every game. Built with the iOS 27 SDK the key no longer stops resizing, and from iOS 27 a launch screen is required for submission (TN3192). The setting still matters for orientation (off, iPadOS 26+ ignores `Screen.orientation` locks even in full screen: Unity Manual): keep it on and make iPad layouts work at any window size before the iOS 27 SDK is required.
- **Accessibility Nutrition Labels** (App Store Connect, per device; optional now, required later for new apps and updates, no date announced as of 2026-10-18; iOS 26+ product pages show the section anyway, as not yet indicated): declare a feature only if every common task (main play, first launch, login, purchase, settings) works with it. Larger Text: text to 200% or more, or to the system's largest size; meaningful icons grow too; the game's own font-size control counts if it reaches equivalent sizes (no Dynamic Type needed), body text grows without overlapping or severe truncation, and Zoom or Hover Text don't count. Differentiate Without Color Alone: no common task relies on colour alone (shape or symbol on pieces qualifies; test with the Grayscale filter); where colour alone must carry meaning (charts, for example), a setting or several colour schemes also qualify, though Apple calls a setting a last resort or stop-gap. Reduced Motion: when the system setting or the game's own setting asks, depth simulation (parallax, animated blur, depth of field) and multi-axis, multi-speed, spinning or vortex motion are disabled or changed; for auto-advancing or ongoing motion Apple says to consider stopping it or offering a control (a recommendation, not a condition); the game's own setting counts when it does what the system setting does, but Apple recommends following the system setting too (skipping it is fine only for an in-game setting with finer controls). Sufficient Contrast: the default UI of every common task (text, buttons, other controls) meets the usual contrast guidelines, about 4.5:1 for most text and 3:1 for non-text elements; otherwise offer colour schemes that meet them; Apple evaluates with Bold Text, Increase Contrast and Reduce Transparency on, light and dark appearances separately, semi-transparent backgrounds included (arayuz-kalitesi-testleri.md #7 measures it). Dark Interface: the game is dark by default for every common task, or has its own dark mode or setting (Smart Invert is a last resort and inverts images). Cheapest first: a "Reduce motion" switch; Sufficient Contrast and Differentiate Without Color Alone once the UI tests pass; Larger Text only after a 200% capture fits the layout (a project, 2026-10-16). Re-check at each update. Criteria re-read on Apple's evaluation-criteria pages 2026-10-18 (the studio's UI research, checked again the same day).

## Verification
- **Automatic** (pre-release test stage): EditMode tests on the shared grant class (as in the Google Play entry).
- **Before release** (the user's Mac, a development build on a device, a Sandbox Apple Account from *Users and Access > Sandbox*): Game Center sign-in banner at startup, an achievement unlock, Restore Purchases returns owned items.
- **On the live version** (manual tests): achievements show in Game Center; purchases and restore work.
