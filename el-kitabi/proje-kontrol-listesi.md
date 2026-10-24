---
title: "Project checklist: what a game does from the first idea to after release (done when, final test, sources) and the new mobile game plan skeleton"
condition: "Game project (any engine; written for a hybrid-casual mobile game on Google Play and the App Store, PC/Steam differences in §4) or a video channel project (§4). Signs: a game summary, a store target, a channel or upload plan in DURUM, plans or memory."
read_when: "Writing a game's or channel's plan (a new mobile game's first plan copies §5's skeleton; later plans and versions take their phase's items); writing a step file's Checklist, Done when and Final test; the comprehensive test stage (the Final test column); a new version after the post-release analysis (phases 11-12)."
requires: "—"
source: "The studio's project research for the session manager, 2026-10-21 (Turkish, 12 phases and 100 items; official pages read that day unless §6 says otherwise; publisher and benchmark posts are company writing, not policy) · the owner's test decisions (2026-10-18: an error check while developing, one thorough stage before release; 2026-10-21: every step tested one by one at the penultimate step) · the studio's lessons (bugs that reached players or nearly did) · the template entries named in the rows"
tech: "Unity 6.3 (URP, IL2CPP), Google Play (target API 36, Billing Library 8), App Store (Xcode 26, iOS 26 SDK), AdMob with UMP, Unity IAP 5.4, Firebase Analytics, Crashlytics and Remote Config, Steamworks, YouTube"
added: "2026-10-21 · template 1.57 · the owner's request ('bir projede yapılması gerekenler gibi detaylı bir araştırma yap buraya ekle'), researched for and relayed by the session manager · template 1.58: the Polish & Quality Gate as skeleton step 39, the concept pre-check in 1.4, 9.5 pointed at the gate (`kalite-kapisi.md`) · template 1.60: a fresh player instead of the owner's 10 minutes, a trademark search (1.5), the level filter and solver hints (2.3, 4.2), the licence list from the first asset (4.8), back-translation (6.4), a monthly look at shelved games (12.6) (the session manager's list from an outside model's review, approved by the owner on 2026-10-22) · template 1.61: 2.6's three 7-8 s clips against the studio's 1-2 s retention baseline (a study of how big studios work, 2026-10-23; the owner approved this item and the event slot, not the others)"
---
# Project checklist

## How to use
- Every item can become a plan step. Its id (e.g. `5.8`) goes into the step file's **Checklist** line; the step file copies the item's **Done when** (its acceptance) and **Final test** (how the comprehensive test stage tries it, `sablonlar/adim.md`).
- An item that doesn't fit the game isn't deleted: the plan says "None: ‹why›".
- While developing: the error check only (PROTOKOL §4; a phase's last building step adds the eye check). The Final test column runs only in the comprehensive test stage (BAKIM.md), never per step.
- TL = `yayin-oncesi-test-listesi.md` (§n its section) · RC = the release checklist `sablonlar/oyun/yayin-kontrol-listesi.md` · [G01]… = §6 sources · `*.md` names = this handbook.
- Pages change: re-read a dated requirement's source when turning it into a step. Benchmarks are reference points, not targets.

## 1. Key findings
- 12 phases. A new game's first plan covers 1-10 (§5's skeleton, 41 steps); 11-12 are separate plans after release.
- The costliest mistakes come early, so they are early items: a concept without pre-research, measurement added late, purchases without a delivery ledger, the wrong consent order (UMP → KVKK → ATT), store declarations that don't match the code.
- Quality: style guide and one finished screen before content multiplies; 60 FPS, no per-frame garbage in play; phone and tablet; a colour-blind-safe palette. A hook sentence and a top-3 table at concept time (1.4); before the test stage the Polish & Quality Gate: the finished game scored blind beside its top 3, a fresh player agent's 10 minutes, no store or portal submission without `KAPI: GEÇTİ` (`kalite-kapisi.md`).
- Test: only the error check while developing; right before release the comprehensive stage (every finished step one by one, the release checklist, the device matrix, hold rules, a report).
- Dated (October 2026): Play target API 36 and Billing Library 8 (since 2026-08-31), 16 KB pages (updates from 2027-02-01), memory thresholds (Feb 2027); Apple Xcode 26 / iOS 26 SDK (since 2026-04-28), minimum iOS 13 (since 2026-09-09), the iOS 27 SDK from April 2027 (7.3, 12.1).
- For every game (2026-10-21): Crashlytics velocity and new-issue alerts are off by default and C# exceptions don't count as crashes without a setting (5.11); Remote Config's free quota changes for existing Spark projects on 2026-12-01 (5.9); Play's Financial features and Health declarations are required for every app (7.6); check the UMP and ad plugin versions for TCF v2.3 consent strings (5.2); Unity IAP 5.4.4+ (5.8); accept Apple's developer agreement of 2026-10-13 (phase 7); Firebase Test Lab closes 2027-09-30 (12.1); Unity 6.0 LTS standard support ends October 2026 (not verified, 12.2).
- After release: ≥14 days of data, the scorecard (the studio's gate: D1 ≥35%, D7 ≥12%, day-1 ≥15 min), then develop / maintain / shelve; the next version comes from the data.

## 2. Phases

### Phase 1 · Pre-research and concept
Before a new game's first plan; the short form before a big new job (`on-arastirma.md`). With a session manager, it approves no first plan without the pre-research.

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 1.1 | **Market and competitors:** the genre's top 5-7: installs and revenue estimate, rating, release date, update rhythm, review themes in players' own words | Which market, with what difference, from data | A table, every row linked and dated; one "our difference" paragraph | Document; 9.5's honest check puts the game beside them | `on-arastirma.md`, `rakip-oyun-incelemesi.md` |
| 1.2 | **Area by area:** gameplay and levels, art style, shaders and VFX, feel (motion, sound, haptics), UI screens, icon, audio and music, store page, first minute, monetization; competitors played on a Play Store emulator | Quality decided up front, not patched later | ≥3 observations, captures or clips per area in `tasarim/on-arastirma/`, take and avoid; the owner's one-page summary and reference sheet | Document; screen scores and 9.5 use its findings | `on-arastirma.md`, `ilk-dakika.md` |
| 1.3 | **Quality bar:** two comparison screens each for home, HUD, win, lose and shop, and how they're scored | "Beside the best" made measurable | Comparisons in the plan's Review; floor 3, target 4 on win, lose and shop | Screens scored beside them (`arayuz-kalitesi.md` §5) | `arayuz-kalitesi.md` |
| 1.4 | **Concept and difference:** one-page game summary: core loop, 3-5 pillars, not for whom, 1-3 distinctive mechanics; the hook sentence ("<genre> where <the one thing> so that <feeling>") and the top-3 table (the three most-played games of the exact subgenre: parity, our edge ≥1 and ideally 2, our gaps) in `tasarim/farklilik.md` from `sablonlar/farklilik-dosyasi.md` | Apple 4.3(b) rejects apps not distinguishable from common ones, and repeated low-effort submissions can end membership (examples added 2026-06-08); 4.3(a): no second bundle ID for the same game [A01]; clone lawsuits. A clone is stopped here, not at the gate | `tasarim/oyun-ozeti.md` filled; the hook sentence and the top-3 table with ≥1 edge none of the three has; no copied name, art or characters | The Review's "our difference" points show in the game; the gate scores Differentiation ≥4 | [A01] 4.3; `kalite-kapisi.md` |
| 1.5 | **Name, IDs, slug:** an English name; `com.<studio>.<name>` package and bundle ID; the name free on the App Store; Play search; a trademark search before choosing it (WIPO Global Brand Database, Nice classes 9 and 41: software and games, entertainment); the site slug | IDs and slug never change after release; a name taken as a trademark in those classes can force a rename | Decision in project memory with the trademark search's date and result, before the first store, Firebase and AdMob record | The build's IDs equal the records (`bundletool dump manifest`, `Info.plist`) | studio naming rule |
| 1.6 | **Revenue model:** ad placements, rewarded offers, IAP products (Remove Ads, packs); the competitors' models | Hybrid-casual earns from ads and purchases mixed; SayGames: effective rewarded ads can carry a game with medium retention [E03]; hybrid-casual day-7 ROAS median 8-12% [E08] | A revenue table: placement, frequency, product, price tier, Remote Config key (the game summary's model line, details in a GDD) | Tried through 5.5-5.8 | [E03] [E08] |
| 1.7 | **Gates written first:** the prototype gate; after release D1 ≥35% (grow ≥40%), D7 ≥12%, day-1 ≥15 min (the studio's gate, game summary › Ölçüm hedefleri); the sample rule (~1,000 installs, else read as a range) | A threshold is never moved after the data. Outside: Voodoo's hybrid targets D1 ≥45%, D7 ≥15% (puzzle 20%), D30 ≥10% [E02]; GameAnalytics 2026, all genres: D1 median ~22%, top 10% ~40%; D7 median <4%, top 10% 11-12% [E06]: the studio's gate sits near the top 10% | Gates in the plan's acceptance criteria, dated | Document; read in 11.3 | [E02] [E06]; `firebase-olcum-ve-uzaktan-ayar.md` |
| 1.8 | **Technical targets and budgets:** Android minimum API, iOS minimum, phone and tablet from day one, 60 FPS, no per-frame garbage in play, memory, size, languages | Expensive to change later | A budget table in the plan's Context | §3's measurements read against it (TL §11) | [G20] |
| 1.9 | **Expert review and approval:** the area's expert (`unity-uzmani`) reviews the pre-research and the plan; a session manager approves where there is one | No blind plan | Findings in the plan's Review; an approval line | The closure and 9.5 judge the work by them | PROTOKOL §3 |

### Phase 2 · Prototype and fun gate
A prototype doesn't ship: no test stage, the error and eye checks are enough. Target 2-3 weeks (studio rule).

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 2.1 | **Technical skeleton:** the settings baseline (URP, IL2CPP + ARM64, AAB, target API, `Application.targetFrameRate = 60`, Input System, Unity splash off), `.gitattributes`, the studio's shared monetization package if any, Firebase, Unity Localization | A late foundation touches everything; Unity stays at 30 FPS on mobile by default; on Android and iOS only `targetFrameRate` counts (vSyncCount is ignored) and a target that doesn't divide the refresh rate rounds down: 60 → 45 on a 90 Hz screen is possible, check on 90/120 Hz [U02] | `unity-proje-ayarlari.md` rows applied; the editor-free compile clean | TL §1 scans (target API, permissions, 16 KB, no test settings) | `unity-proje-ayarlari.md`; [U02] [U04] |
| 2.2 | **Core loop prototype:** one mechanic, 10-20 levels; grey boxes allowed only here | Find the fun the cheapest way; publishers suggest ~30 min of original play for a retention test (CrazyLabs) [E05] | A playable build; a 2-3 min eye check logged | None in the prototype; the mechanic later through 4.2 and TL §2 | [E05] |
| 2.3 | **Level generator and solver:** levels built by code; a solver plays them by the game's own rules and scores difficulty; trivial levels (shortest solution ≤2 moves) and duplicates (the same start state) filtered out; hints replay the solver's line (`adil-zorluk-ve-basarisizlik.md` §5) | No unsolvable level reaches players (the studio's lessons) | The solver finishes every level; scores in a table; the filter's count; ≥50 valid levels before the fun gate (2.5) | TL §2: the solver's moves through the game's own input and rules, 100% | `adil-zorluk-ve-basarisizlik.md` §5 |
| 2.4 | **Save foundation:** a versioned save; atomic write (temp file + rename) with a backup; migration code; nothing writes before the save has loaded | Save loss is the worst player loss (a quiz game's restore overwrote saves in 1.3-1.5). `persistentDataPath` survives updates; on iOS the path depends on the bundle ID, so a changed ID loses the save [U11]; atomic write (temp file, `File.Replace`, `.bak`) is general .NET practice, not in Unity's docs | A corrupt file opens from the backup; the launch order shows in the log | TL §3: relaunch, install over the last version, old save files, broken save, clean install, launch order | TL §3; [U11] |
| 2.5 | **Fun gate:** first play, the expert's view, "would I keep playing?"; an optional publisher test (Rollic, SayGames, Homa, Kwalee; whether it's free and the IP stays ours isn't on their pages: ask in writing before signing) | No months on an idea that doesn't hold. Publishers measure first with ad videos (CPI, clicks), then retention and playtime [E04] [E05]; SayGames ignores CPI early in hybrid and plays the game itself before testing it [E03] | A decision line: continue / change / drop, with why | A decision; no test | [E03] [E04] [E05] |
| 2.6 | **Marketability:** a 15-30 s gameplay clip and an icon draft; an organic short-video trial; a paid CPI test only by the user's decision | Whether it gets clicks shows early; hyper-casual CPI targets were $0.20-0.30 [E01] [E04]; in hybrid CPI alone is no gate [E03] | Three 7-8 s vertical clips of the prototype's best moment, real gameplay only, one variable between them (the hook line), posted in the studio's normal slots (the session manager's call where one is named); after 48 h each clip's 2 s retention (TikTok) and stayed-to-watch (Shorts) beside the studio's baseline (its best clip, 2026-10-23: 75 % at 1 s, 46 % at 2 s); all three below it → change the hook or the theme once; below again → the result goes to 2.5's decision. CPI and D1 if a publisher test ran | A decision; no test | [E01] [E04]; `kisa-video-olcumu.md` |

### Phase 3 · Vertical slice and look
The style guide and one finished-looking screen come before content multiplies.

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 3.1 | **Style guide:** palette (colour plus shape, colour-blind safe), fonts (tr, en and the target languages' letters, currency signs), GUI Pro parts, light, camera, VFX language | The look fixed before content multiplies | The guide in `tasarim/`; the palette at CIEDE2000 ≥20 under protan, deutan, tritan | TL §9 accessibility; screen scores | `renk-korlugu-palet.md`, `layerlab-gui-pro.md`, `sevimli-stilize-gorunum.md` |
| 3.2 | **One finished screen:** the game screen and HUD at final quality, beside the comparisons | The bar proven early | Score ≥3 (target 4); the screenshot in the plan | TL §9 screen matrix (5 profiles × 2 languages) and scores | `arayuz-kalitesi.md` |
| 3.3 | **Game feel:** response on the tap's frame, smooth transitions, reward landing, the haptics bridge, reduce motion | Feel drives retention | `oyun-hissi.md`'s list applied | A feel and smoothness pass on a device (RC › Kalite) | `oyun-hissi.md` |
| 3.4 | **Sound and music:** from the licensed library, mixer groups, the iOS silent switch and other apps' music | Sound is half the feel; the wrong audio category annoys players | A sound list with licences; the mixer | TL §10 | TL §10; `unity-ortam-ve-3d-ses.md` |
| 3.5 | **First minute:** seconds from launch to the first tap; a tutorial by playing; a quick first win; consent and permission prompts don't cut the first play | A player lost in the first session doesn't return; the day-1 15-minute gate. The first experience is the 30-60 s after install; test the tutorial with many people, find the drop point [E09] | `ilk-dakika.md`'s rules; `tutorial_*` events | A clean-install first-minute run, times measured | `ilk-dakika.md`; [E09] |
| 3.6 | **UI screen set:** home, HUD, pause, settings, win, lose, shop, reward offers; safe area; phone and tablet layouts; touch targets 48 dp / 44 pt | No grey box or bare Unity UI in a store; tablets in every game. Android's adaptive app quality (the large-screen guidelines were archived 2026-01-21): even the lowest tier wants the screen filled (no letterbox), state kept across configuration changes, multi-window and basic keyboard and mouse [G19]; Android 15+ draws edge-to-edge and `renderOutsideSafeArea` has no effect: the UI follows `Screen.safeArea` [U08] | Every screen follows the guide and fits the tablet profile | TL §9: the matrix, the navigation walk, real taps | `arayuz-kurallari.md`, `arayuz-kalitesi-testleri.md`; [G19] [G20] |
| 3.7 | **Performance base:** 60 FPS on the lowest target phone; GC Alloc 0 B per frame in play; memory and draw-call budgets; ASTC; pooling | Late optimization is expensive; Play's FPS and memory bars. At 60 FPS a frame is 16.66 ms; leave ~35% for heat: ~11 ms; incremental GC (on by default) doesn't reduce garbage, it only slices it and can add ~1 ms a frame; none on the Web [U01] [U03] | A device Profiler capture in the plan | TL §11: FPS, GC, memory, launch, heat | [U01] [U03] [G20] |
| 3.8 | **Icon draft:** 3 candidates, small, in the competitors' grid | The first thing seen in a store; the marketability trial needs it | The choice with why | The AAB's `app_icon.png` and the Xcode icon by eye (RC › Build) | `oyun-simgesi.md` |

### Phase 4 · Content

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 4.1 | **Level plan and difficulty curve:** the launch level count; the first levels teach and are easy; breathers; order by difficulty score | Content and flow for the day-1 15 minutes and D1 | A level table and the curve | TL §2 progression: first to last unlock, after the last level | `adil-zorluk-ve-basarisizlik.md` |
| 4.2 | **Build and prove the levels:** the filter (no trivial or duplicate level) and the solver's hints on every level | No unsolvable, trivial or repeated level reaches players | The solver at 100%; the tightest margins in the report; no level with a shortest solution ≤2 moves past the tutorial, no two with one start state | TL §2 | — |
| 4.3 | **Goal layers and reasons to return:** stars, collections, daily reward, streak; never guilt | The structure that carries D1 and D7 | `hedef-katmanlari-ve-geri-donus.md`'s checklist | TL §6: day change, week and month ends, clock tricks, offline | `hedef-katmanlari-ve-geri-donus.md` |
| 4.4 | **Economy:** soft-currency sources and sinks, reward sizes, prices; tuning values in Remote Config | Balance without an update | An economy table and the key list | TL §4-6; a Remote Config change reaches the test device | `firebase-olcum-ve-uzaktan-ayar.md` |
| 4.5 | **Platform services:** Play Games Services v2 sign-in and ≥10 achievements (≥4 reachable in the first hour); Game Center sign-in and achievements | Play's Level Up rules and visibility tools | The PGS configuration published; an achievement table | TL §7: sign-in; the achievements list opens in the R8 build; Game Center manual | [G20]; `google-play-level-up.md`, `app-store-game-center.md` |
| 4.6 | **Settings and help:** sound, music, haptics, language, reduce motion, privacy options (UMP), restore purchases, the privacy policy link, a way to report an inappropriate ad, the support e-mail, credits | Apple: restore (3.1.1), the privacy policy inside the app (5.1.1), a way to report inappropriate ads in an ad-supported app (2.5.18) [A01]; UMP's privacy options [F11] | Every row works | TL §9 navigation; §5 privacy options; §4 restore; the report way opens mail or a form | [A01]; [F11] |
| 4.7 | **Local notifications (optional):** the permission moment, content, frequency | A reason to return; misuse costs ratings. Android 13+ asks for the permission in context, after an action (e.g. the 3rd-4th launch) [G28] | `yerel-bildirimler.md` › Verification | TL §7 notifications | `yerel-bildirimler.md`; [G28] |
| 4.8 | **Licences and credits:** a licence list `tasarim/lisanslar.md` from the first imported asset (one row per pack or file: name, source, licence, where used, credit line): asset and sound packs, UI kits, fonts (OFL), CC BY credits | Legal risk; the App Store review note says what is ours and what is licensed from it (`kalite-kapisi.md` › Review Notes) | The list current at every import; a credits screen | RC › İçerik: licence notices | RC |

### Phase 5 · Monetization and measurement
The studio's shared monetization package from day one, where there is one. Measurement ships with the first version: an event added later loses the first 14 days.

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 5.1 | **Monetization kit:** UMP and ATT, the ad rules, IAP and Remote Config from the shared package | The same correct behaviour in every game; lessons live in the package | The package version in the project; the compile clean | Through 5.2-5.9 | — |
| 5.2 | **Consent (UMP):** consent info updated at every launch; the form when required (EEA, UK, Switzerland); a separate message for 20 US states [F11]; privacy options in settings; ad requests only after `CanRequestAds()`; Firebase consent mode follows UMP | Personalized ads in the EEA and UK (since 2024-01-16) and Switzerland (since 2024-07-31) need a Google-certified CMP integrated with the TCF; AdMob's own EU messages are certified; otherwise at most non-personalized or limited ads [F12]. Consent strings created from 2026-03-01 must be TCF v2.3; most errors fall back to limited ads [F14] | Before consent only UMP's and the store's hosts are contacted | TL §5: EEA debug geography, outside the EEA, nothing before consent | [F11] [F12] [F14] |
| 5.3 | **KVKK (Turkey):** the information notice for players in Turkey; the legal route for transfer abroad; the text complete in a static font | KVKK art. 10: inform when collecting (controller, purpose, recipients, method and legal basis, rights); art. 9: transfer abroad since 2024-06-01 by an adequacy decision (no country yet) or the Board's standard contract, a signed contract notified within 5 working days [F13]. Firebase and AdMob data leave Turkey: a lawyer should confirm the route | The text equals the privacy page; no missing letter in tr | TL §5 and §9 glyph pass (tr) | [F13] |
| 5.4 | **ATT, deferred:** UMP's IDFA explainer (one "Continue" button, no close, doesn't imitate or show Apple's alert [A19]) → Apple's alert at a natural moment (not at first launch; no tracking data before it); no reward, pressure or lock; declined → no IDFA, ads still serve; Firebase `ad_user_data` and `ad_personalization` only with permission | Tracking and the IDFA need ATT permission; an explainer screen is allowed, a feature lock or reward isn't (5.1.2(i)). In the EU from iOS 27.2 an alternative prompt (the only one in Germany, France, Italy, Poland, Romania; may be asked again after a year in the EU) [A05] | `NSUserTrackingUsageDescription` clear and true; the order in code | TL §5 iOS order (iPhone, manual) | [A05]; [A01] 5.1.2; `firebase-olcum-ve-uzaktan-ayar.md` |
| 5.5 | **Interstitial rule:** only after a win, from ~level 10-11; 180-300 s apart (Remote Config); on the result screen ~0.5 s after the score count, only if loaded; a tap cancels it; buttons always visible. Never at level start, between a tap and its target, at launch or at exit | Play: no unexpected full-screen ad at level start, between a tap and its action or before the splash; no back-to-back interstitials, none that can't close after 15 s; after the score screen is an allowed example [G21]. Apple 2.5.18: a clearly visible close or skip [A01]; a hidden navigation button was rejected (a quiz game's 1.4). AdMob: none at launch or exit, at most one per two user actions, not right after another closes [F08]; without consent (limited ads) AdMob's frequency cap may not work, so the game keeps its own interval (inference) [F08] | The rule in code; defaults and keys written | TL §5 placement run; the interval measured with a counter | [G21] [F08]; `google-play-level-up.md` §9 |
| 5.6 | **Rewarded ads:** the player chooses; the reward stated first; granted only in the completion callback; the button only when loaded; an offline message; a daily cap | AdMob: rewarded only on explicit opt-in; every ad states the action and the reward first; declining never blocks play; a rewarded interstitial needs an intro screen with a "no"; the reward is in-game, non-transferable, given after watching [F09]. Play: player-chosen rewarded ads are exempt from the 15 s rule [G21]; Apple 3.2.2(x) allows rewards for watching ads [A01] | `odullu-reklam.md` applied | TL §5: watch to the end, close early, no fill, offline | [F09] [G21]; [A01] 3.2.2; `odullu-reklam.md` |
| 5.7 | **Catalogue and prices:** Remove Ads and packs; the same product IDs on both stores; price tiers (the Turkey price rule); the store's localized price text; currency signs in the font | Revenue; a wrong price or "□" costs trust. Apple 3.1.1: bought currency never expires; loot box odds shown before purchase [A01] | A product and price table, dated | TL §4 price text (₺ ₹ ₽ € R$ £ ₩) | `google-play-level-up.md` › Play Console work |
| 5.8 | **Delivery ledger and restore:** one delivery per order ID; the grant and the ledger in one save, then confirm (pending → confirm); acknowledged on Play within 3 days; iOS "Restore purchases" button; Android restores at launch | Play: grant only in PURCHASED; an unacknowledged purchase is refunded after 3 days; query pending orders at launch and on resume [G10]. Apple 3.1.1: a restore mechanism [A01]. Double grants are the risk. Unity IAP 5: OnPurchasePending → grant and save → `ConfirmPurchase`; an unconfirmed order comes back after a crash and on every FetchPurchases, so keep your own replay check; an empty or partial fetch never revokes; server validation recommended, no built-in validator [U05]. Use 5.4.4+ (5.4.0 Billing 9; 5.4.3 and 5.4.4 restore and StoreKit 2 fixes) [U10] | The ledger in the save (one save scope) | TL §4: every product, double tap, kill between payment and grant, restore, refund, acknowledge | [G10] [U05] [U10]; [A01] 3.1.1 |
| 5.9 | **Remote Config and kill switches:** in-app defaults; one fetch at launch (12 h interval); values applied at a safe point; keys for interstitials on/off, the start level, the interval, offers, events and new features; no value that can break saves or purchases | Turn a broken feature off without an update. Firebase: the default minimum fetch interval is 12 h; activate the cached values at launch and fetch in the background for the next one (in an A/B test on the loading screen, with your own timeout); values are readable by anyone, never secrets; a new feature flag defaults off and opens 1% → 10% → 50% → 100% [F03]. From 2026-09-01, 100,000 fetches a day free (existing Spark projects from 2026-12-01; throttled 30 days after going over): at a 12 h interval ~50,000 daily devices [F03] | A key table; with the network off the game plays fully on defaults | A console change reaches the test device at its next launch; every key switched off leaves the game working | [F03]; `firebase-olcum-ve-uzaktan-ayar.md` |
| 5.10 | **Analytics from day one:** `tutorial_begin`/`tutorial_complete`, `level_start`/`level_end` (`level_name`, `success`), `earn_virtual_currency`/`spend_virtual_currency`, ads and purchases (automatic events never re-logged); ~10 custom events at most; the GA4 audit (custom dimensions, 14-month retention, the AdMob link, a developer-traffic filter, Test Lab excluded) | Funnel and D1/D7 by version readable from the first version. At most 500 event types per app [F01]; GA4's recommended game events `level_start` (`level_name`), `level_end` (`level_name`, `success`), `post_score`, `unlock_achievement` [F02] | An event table; the GA4 settings done | TL §12: each event once in DebugView or Realtime with the right parameters, none before consent or on Test Lab | [F01] [F02]; `firebase-olcum-ve-uzaktan-ayar.md` |
| 5.11 | **Crashlytics:** SDK 11.7.0+; Android IL2CPP symbols with `firebase crashlytics:symbols:upload` ("Create symbols.zip"); a decision on `ReportUncaughtExceptionsAsFatal`; caught errors as non-fatals (`LogException`); custom keys (level, version); velocity and new-issue alerts on | Crashes read and seen fast. C# exceptions count in crash-free rates and velocity alerts only with `ReportUncaughtExceptionsAsFatal = true` (SDK 10.4.0+); velocity alerts (default: 1% of sessions in 30 min and 25 users) and new-issue alerts are off by default [F05] | A test crash in a test build shows in the console within minutes with a readable stack | TL §12 crash row | [F05] |
| 5.12 | **app-ads.txt:** one file at the site's root (no BOM); the developer website on both stores; verified in AdMob | AdMob looks for it at the root of the developer site on the store page, in IAB format, crawled within 24 h; since January 2025 a new app gets full ads only after app-ads.txt verification and the readiness review (2-3 days after linking the store, limited ads meanwhile) [F10] | AdMob says "verified" | 10.6's release-day check | [F10] |

### Phase 6 · Localization and accessibility

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 6.1 | **Unity Localization from day one:** all text in tables, none hard-coded, stable keys; en-US primary, Turkish an option; the device language at first launch, changeable in settings | Adding a language stays cheap. Locale selectors are read top-down: the player's choice (Player Pref) above the system language (inference); Smart Strings for plurals and variables [U06] | Table coverage complete; the choice persists | TL §9 two-language pass | [U06] |
| 6.2 | **Font coverage:** every language's letters (ã ç ß é ñ İ ı), currency signs, a fallback font per language (Noto, OFL); no TMP case styles on localized labels | "□" and Turkish İ/ı bugs | The glyph scan clean | TL §9 glyph and casing row | `arayuz-kurallari.md` |
| 6.3 | **Overflow:** pseudo-localization and the longest language (German) on every screen | Overflow costs scores and trust; Unity's Pseudo-Locale (Accenter, Expander, Encapsulator) shows overflow, untranslated text and right-to-left problems [U06] | No overflow | TL §9 screen matrix | [U06] |
| 6.4 | **Store pages in several languages:** es-419/es-MX, es-ES, pt-BR, fr, de, ar, ru; search terms from the store's analytics; in-game order es, pt-BR, fr, de (the studio's multi-language plan) | The visibility bottleneck: players search in their language | Name, short description or subtitle, keywords, description and image text in each language; each translation back-translated blind into English and compared before upload (`metin-denetimi.md` §3) | Every language's page opens; the field limits hold | `store-listing-optimization.md` |
| 6.5 | **Arabic and right-to-left:** in the game only if data shows demand, as its own plan | Unity 6.3 shapes right-to-left text only in UI Toolkit with the Advanced Text Generator (off by default); uGUI and TextMeshPro have no official support, the third-party RTLTMPro is needed (not verified) [U06] | A decision line | If it ships: Arabic screens in the matrix | [U06] |
| 6.6 | **Colour-blind-safe palette:** game colours also carry shapes; CIEDE2000 ≥20 under protan, deutan, tritan | In colour-matching games some players can't tell the colours apart | The measurement output in the plan | TL §9; a Grayscale pass | `renk-korlugu-palet.md`; [A17] [E10] |
| 6.7 | **Readability:** body text readable; contrast 4.5:1 for text, 3:1 for elements; an optional in-game text size | Unreadable text drives players away; Apple's Larger Text label | UI check #7 green | TL §9 | [A17] [E11] |
| 6.8 | **Reduce motion, haptics, sound:** both switches read the system setting; what sound tells also shows on screen | Motion sensitivity; players without sound | The switches work | TL §9 accessibility row | `oyun-hissi.md`; [E10] |
| 6.9 | **Accessibility declarations:** App Store Accessibility Nutrition Labels only for features that really work in all common tasks | Optional now, later required for new apps and updates (no date); on iOS 26+ a product page without one shows "not yet indicated" [A17] | A declaration list with reasons | A Grayscale and large-text run | [A17]; `app-store-game-center.md` §7 |

### Phase 7 · Compliance, privacy and store records
Once per company, outside plans: developer accounts, the payments profile, tax, DSA trader status, agreements (Apple's new developer agreement of 2026-10-13 must be accepted in the account [A23]), Turkey's VERBİS (exempt under 50 employees and a balance sheet under TRY 100 M [F13]).

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 7.1 | **Records:** the Play Console app (default language en-US); the App Store Connect app (bundle ID, SKU, en-US); Firebase apps; the AdMob app and ad units | IDs fixed; the build depends on them | IDs in project memory; new store records requested from the user | The build's IDs equal the records | — |
| 7.2 | **Signing:** Play App Signing; the upload key backed up, outside the repo, its password typed by the user; no password left in Gradle copies after a build; iOS signing on the Mac | A lost upload key is reset through Play Console; a self-managed signing key can't be. Firebase and Google sign-in (PGS) also list the SHA-1/SHA-256 of Google's signing key [G08] | A backup in two places; a scan of `Library/Bee` clean | RC › Platform line | [G08] |
| 7.3 | **Dated technical requirements:** Play: new apps and updates target API 36 since 2026-08-31 [G01]; from 2027-02-01 an update targeting API 35+ without 16 KB page support can't be published [G02]; IL2CPP ARM64 (Unity 6000.0.38f1+ supports 16 KB, Unity 6.3 can target API 36; Burst 1.8.21+, native plugins rebuilt [U04]). iOS: Xcode 26 and the iOS 26 SDK since 2026-04-28, minimum iOS 13 since 2026-09-09 [A02]. Play Billing Library 8+ (since 2026-08-31; Unity IAP 5.0.0+ ships it) [G09] [U10] | Unmet → the update can't be uploaded | `bundletool`: targetSdk and `PAGE_ALIGNMENT_16K`; the Xcode version in the package note | TL §1 | [G01] [G02] [A02] [U04] [G09] |
| 7.4 | **R8 and symbols:** minify on in Release; no package-wide keep rules; `r8-kontrol.py` clean; native debug symbols and the mapping file in the bundle | Play's memory and code thresholds (Feb 2027); readable crashes: the mapping file travels in the AAB, native symbols are uploaded per release (800 MB limit) and only decode later crashes [G25]. Unity's Minify is off by default; once on, Unity 6 runs R8 in full mode and classes reached through JNI need keep rules in `Assets/Plugins/Android/proguard-user.txt` [U07]; symbols in the AAB: Build Profiles › Android › Debug Symbols (Symbol Table, Include in Bundle) [U08] | `BUNDLE-METADATA/com.android.tools.build.debugsymbols` in the AAB | TL §1 minified build and §13 smoke run | `google-play-level-up.md` §9; [G20] [G25] [U07] [U08] |
| 7.5 | **Privacy page and catalog:** the game's own privacy page on the studio site (tr + en; later es, pt-BR, fr, de), the catalog record and a news item; the privacy URL on both stores; a link inside the game | A store requirement; privacy follows code | The page answers 200 in both languages | The live page and the in-game link open | [A01] 5.1.1; [G03] |
| 7.6 | **Play declarations:** Data safety (the SDKs' collection too: AdMob, Firebase, Unity IAP 5.4+), contains ads, Advertising ID, target audience and content, the IARC rating, app access, the Financial features and Health declarations (even without those features) | Data safety is required for every app on closed, open and production tracks, even one that collects nothing; SDK data is declared too; Google doesn't verify it, and a mismatch can block updates or remove the app [G03]. Apps targeting Android 13+ declare the AD_ID permission [G17]. Without the Financial features declaration an app can't be updated since 2025-10-30; no app without a content rating [G18] | The App content tasks empty | TL §12 declarations: SDK list = declarations = privacy page | [G03] [G04] [G17] [G18] |
| 7.7 | **Apple declarations:** App Privacy (an ad game is never "Data Not Collected"); privacy manifests (UnityFramework, Firebase; Unity adds its own API reasons, the game's native code and every SDK separately; a custom `PrivacyInfo.xcprivacy` in `Assets/Plugins` [U13]); the ATT text; AdMob's SKAdNetwork IDs; the encryption declaration; the age rating questionnaire; the review note (the 4.3 difference, the products) | App Privacy: everything you and your SDKs collect (an ad SDK typically: device ID, advertising data, product interaction, crash data, coarse location) [A03]; Apple's manifest list names UnityFramework and Firebase parts, not Google Mobile Ads [A04]; the age questionnaire has 13+/16+/18+ and social media questions from September 2026 [A06]; no trader status → removal from the EU (2025-02-17) [A07]; HTTPS only → `ITSAppUsesNonExemptEncryption` = NO [A16]; ad networks in `SKAdNetworkItems` [A24] | Nothing missing in App Store Connect | TL §14 iOS rows | [A03] [A04] [A06] [A07] [A16] [A24]; `app-store-game-center.md` §7 |
| 7.8 | **Children, audience, age assurance:** declared not to target under-13s where true; the Families policy and Kids category rules if the look appeals to children; age assurance where a law requires it (Declared Age Range API) | Play: with children in the audience every Families rule applies (only Families-certified ad SDKs, no interest-based ads, every ad closable within 5 s, no interstitial at launch); a neutral age screen for mixed audiences; a wrong audience declaration is a removal reason [G04]. Play's age signals in Brazil (2026-03-17) and Texas (accounts opened after 2026-05-28); the data only for an age-appropriate experience, never ads or analytics [G23]. Apple: no third-party analytics or ads in the Kids category (limited contextual ads excepted); "Made for Kids" can't change after approval [A01]; US age checks for new accounts: Texas (2026-06-04), Utah (2026-05-06), Louisiana (2026-07-01) [A20] | The audience decision with why; whether age assurance is needed, written down (Apple is unclear for account-less games: not verified) | The declaration matches the content and the ad settings | [G04] [G23]; [A01] 1.3, 5.1.4; [A20] |
| 7.9 | **Permissions:** only what's needed (e.g. no VIBRATE); the Android 13+ notification permission; clear iOS permission texts | A needless permission costs rejections and trust | The manifest's permission list | TL §1 permissions | TL §1 |
| 7.10 | **Rights and honest declarations:** no copied name, art or characters; no competitor names in text; Play's AI-generated content declaration right; no hidden or undocumented feature | Lawsuit and removal risk; Apple 4.1(c) forbids others' icons and names, 2.5.19 hidden or dormant features [A01] | A check line | `metin-denetimi.md` §4 store audit | [A01] |
| 7.11 | **Countries and regional rules:** pick the countries; drop one whose rule isn't met (Vietnam: online games need a government licence; Korea: GRAC rating, loot box odds disclosed; Brazil: no loot boxes in games minors can use, and on Apple ads and loot boxes raise the age class; Japan: an app selling IAP shows the operator's name, phone and address) | A store removes or rejects a game that misses a regional rule | The country list with reasons | The console's country list matches the plan | [A06] [A23] [G24] |

### Phase 8 · Store page and promotion

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 8.1 | **Icon:** Play 512×512, App Store 1024×1024; readable small; the same as the build's | The first conversion driver in a store | Chosen in the competitors' grid | The AAB's `app_icon.png` by eye | [G11]; `oyun-simgesi.md` |
| 8.2 | **Screenshots:** the real game; the first 3 carry the message (App Store search shows 3); localized captions. Play: ≤8 per device type, ≥2 to publish (JPEG or alpha-free PNG, 320-3,840 px, long side ≤2× the short); for recommendation surfaces ≥3 in-game shots, all 16:9 (≥1920×1080) or all 9:16 (≥1080×1920); tablets and Chromebooks ≥4 at 1,080-3,840 px [G11]. App Store: 1-10 per size; the required iPhone set, and iPad 13" if the game runs on iPad; in every language and size more than half show the game itself (2.3.3); builds with the iOS 27.1 SDK also need an iPhone Duo set [A08] [A01] | Conversion; metadata rules | Sets uploaded in every language | The shots show the same game as the build (2.3.7) | [G11] [A08]; `store-listing-optimization.md` |
| 8.3 | **Preview video:** Play: a YouTube link (no ads; public or unlisted); App Store: a 15-30 s preview; real gameplay | Motion lifts conversion; some Play surfaces want a video | The videos uploaded | The video shows the same game as the build | [G11] [A08]; `store-listing-optimization.md` |
| 8.4 | **Text and ASO:** Play title 30, short description 80, full 4,000 characters; App Store name 30, subtitle 30, keywords 100 (Apple says bytes; a 95-character, 121-byte Turkish list was accepted), promotional text 170 (changes without a version), description 4,000 [A22]; the searched term in the title; no "best", "#1" or "free" claims, no emoji; claims in `store/facts.md` | Search visibility; rejection risk | Text in every language; the claims ledger | `metin-denetimi.md` §4 | [G12]; [A01] 2.3.7; `store-listing-optimization.md` |
| 8.5 | **Feature graphic:** Play 1024×500; text under 20% of the frame | Play surfaces and the video's cover | Uploaded | Read against the graphics rules | [G11] |
| 8.6 | **Featuring and events:** App Store featuring request ≥3 weeks ahead (one Apple page says 2; 3 is the rule), ≤3 months ahead; new content, enhancement or launch [A12]. App Store in-app events: ≤31 days long, promoted 14 days ahead, ≤10 published at once [A11]. Play promotional content, open to every game: submitted ≤60 days ahead, review up to 4 days (send ≥4 days before), an event ≤4 weeks; featuring requests ≥14 days ahead and only above the Premium growth tools thresholds (~1.6 M daily users or $40-50k monthly player spend), featuring usually 7-14 days [G14]. Play's new-game featuring form: rating ≥3.8, launch within 120 days, ≥3 weeks ahead with the build in Play Console; not for updates [G26]. Level Up [G20] | The main no-budget growth lever | Requests sent; dates in the plan | The event's content is in the game on those dates | [A12] [A11] [G14] [G20] [G26]; `store-events.md` |
| 8.7 | **Launch week:** 1-3 short videos a day (Shorts, TikTok, Reels) with store links; the community devlog; the site news | The first organic wave | The calendar and clips ready | The links open the right store page | `kisa-video-lansman-haftasi.md` |
| 8.8 | **Store experiment plan:** the icon first, then the first screenshot; Play store listing experiments, Apple product page optimization; too little traffic → change directly and compare 28 days before and after | Conversion grows with data | The plan: one variable, the duration set first | Document; after release | [G13] [A09] [A10]; `store-listing-optimization.md` |
| 8.9 | **Support:** the studio's support e-mail; the support URL is the game's site page | A store requirement | Filled on both stores | The address opens | — |

### Phase 9 · Comprehensive test stage
The plan's penultimate step, when every building step is done (BAKIM.md › Comprehensive test stage; how: TL §0, the hold rules and report: TL §15). A game going to a store or portal reaches it only after the Polish & Quality Gate's `KAPI: GEÇTİ` (`kalite-kapisi.md`; §5 step 39).

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 9.1 | **Test matrix:** every finished step's Final test + RC + the TL rows that apply + the device matrix | "Her taşın altına finalde bakalım" (the owner, 2026-10-18) | The matrix in the test step's file; per row a pass bar and an evidence place | The stage itself | TL §0 |
| 9.2 | **Run cheap to expensive** | Red shows early, fewer reruns | Every row with its result and evidence | The stage itself | TL §0 |
| 9.3 | **Fix and re-test the neighbours** | A fix mustn't break something else | No red left, or written as an accepted risk with why | The stage itself | TL §0, §15 |
| 9.4 | **Store reports:** Play's pre-launch report; App Store Connect's upload warnings | A free real-device pool and the store's own checks | No crash or ANR; findings written down | The stage itself | [G06]; TL §14 |
| 9.5 | **Expert review and the honest check** | The quality bar; the gate already scored the game beside its top 3, so no double work | The expert's note on what changed since the gate, the gate's score sheet cited; screen scores before and after | The stage itself | BAKIM.md; `kalite-kapisi.md` |
| 9.6 | **Report and go / hold** | A packaging gate may look for the report | `SONUÇ: GEÇTİ <version>-<build>`; the session manager's approval where there is one | The stage itself | TL §15 |

### Phase 10 · Release

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 10.1 | **Version data:** version name x.y; build and version code raised; release notes in both languages and the store languages | Code that reads the version as a number breaks on a three-part name (a studio lesson) | Read back from `Info.plist` and the manifest | Checked in the stage's build scans | studio rule |
| 10.2 | **Submission list:** to the session manager where there is one, sent by API after its approval; else the user uploads and submits (the Unity section's Release line) | Studio rule | An approval line | — | — |
| 10.3 | **Play first submission:** listing, all translations, graphics, products and declarations before the first "send for review"; no change while in review; direct release (production, 100%, managed publishing off) | Play's review takes hours to 7 days (longer in exceptional cases), longer for a new developer account; Google suggests at least a week between submission and launch; a change sent during review can restart the queue; the 15-minute pre-review checks aren't approval; staged rollout only for updates [G05] | Sent | — | `google-play-level-up.md` › Direct release; [G05] |
| 10.4 | **iOS submission:** the archive on the Mac (the user); by API: build choice, encryption declaration, review note (features and every product explained; a note copied from the last version is re-read), submit; each type's first IAP goes with a version; automatic release; phased release off (studio rule; Apple's goes 1% → 100% over 7 days, pausable 30 days in total) | Apple reviews 50% of submissions within 24 h and 90% within 48 h; over 40% of issues are 2.1 (completeness) [A21] | Sent | — | [A15] [A21] |
| 10.5 | **Simultaneous launch:** Android before iOS or the same day; live on Play within 15 days at the latest | The Level Up rate card's condition | The dates in the plan | — | [G20] |
| 10.6 | **Release-day check:** both store pages and their languages; the privacy URL; real ads serve (not test ads); app-ads.txt verified; GA4 Realtime and Crashlytics receive data; Remote Config values right | No blind spot live; an approved iOS version can take up to 24 h to reach every country [A21] | Every check line ✓ | — | TL §12; `firebase-olcum-ve-uzaktan-ayar.md` |
| 10.7 | **Announcement and wrap-up:** the release announced the same day (BAKIM.md › After release: `store/duyuru/<version>.md`, the studio site and the community devlog); everything pushed; the site catalog current; with a session manager, its lifecycle (shelving, the measurement window) | Players hear of it; the lifecycle measures next | The announcement published; the closure note | — | BAKIM.md |

### Phase 11 · After release: measure, analyse, decide (its own plan)

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 11.1 | **First 72 hours:** Crashlytics velocity alerts, Android vitals, reviews. Hotfix when: a launch crash, save loss, purchases or ads broken | Play can lower visibility and warn on the store page when the 28-day user-perceived crash rate passes 1.09% or ANR 0.47% (8% on one device model) [G07] | A daily check log | — | [G07] [F05] |
| 11.2 | **Window ≥14 days:** no new content; fixes, compliance, policy, review replies and small store-page content allowed | Clean data | The window's dates in DURUM | — | BAKIM.md › After release |
| 11.3 | **Scorecard (days 14-24):** D1 and D7 (with ranges), day-1 minutes, the level funnel, sessions, crashes, ad and IAP revenue, store conversion, ratings and review themes, at most 3 recommendations; "not enough data" when few | Decide from data. Outside: GameAnalytics 2025 puzzle medians D1 ~20%, D7 4-5%, D28 ~1.1%, ~30 min of daily play [E07]; the reports change their method between editions, so compare within one edition [E06] | The scorecard file | — | [E06] [E07]; `firebase-olcum-ve-uzaktan-ayar.md` |
| 11.4 | **Version decision:** develop / maintain / shelve; into DURUM; a short summary to the user | Invest by potential | A decision line | — | BAKIM.md |
| 11.5 | **The next version's plan from data:** the biggest drop, what players like, revenue; a short pre-research; A/B tests with Remote Config (one change, an activation event, the duration set first, no peeking) | No version by guesswork. Firebase A/B: ≥2 weeks recommended, stops itself after 90 days; variant weights can't change after the start; the activation event fires when the values activate; goals e.g. day-1 retention or estimated ad revenue [F04] | The data in the plan's Review | The new version's own gate (a big update, `kalite-kapisi.md`) and test stage | [F04] |
| 11.6 | **Rating prompt:** at a good moment (after a won level, not in the first session); only the system dialog; no question, reward or condition before it | Ratings move ranking and conversion. Apple: at most 3 times in 365 days, custom rating prompts forbidden (5.6.1), forced ratings forbidden (3.2.2) [A13] [A01]. Play: the quota is time-based and undisclosed (a second call within a month may show nothing); no question before or during the card; never behind a button (a button opens the store page); nothing on or around the card [G15] | The moment and frequency in code (the studio's pattern: after the 5th round, 60 days apart, ≤3 a year, at the end of a won round) | TL §7 rating prompt | [G15] [A13]; `store-listing-optimization.md` |
| 11.7 | **Review replies:** Play and App Store reviews regularly, in the player's language, to the point; bug reports to the game's owner | A player may update the rating; trust | Replies at least daily (the studio scans twice a day) | — | [G16] [A13] |
| 11.8 | **Store events:** Play promotional content and App Store in-app events with real in-game content; seasonal | Organic visibility | An event calendar | The event's content is in the game on those dates | [G14] [A11]; `store-events.md` |

### Phase 12 · Maintenance (a checklist at every version's preparation)

| # | What | Why | Done when | Final test | Source |
|---|---|---|---|---|---|
| 12.1 | **Watch dated requirements:** Play's target API has risen a step every 31 August (2025: 35; 2026: 36 for new and updated apps, older apps at least 35) [G01]; Play Billing Library (2026: 8+; probably 9+ on 2027-08-31) [G09]; 16 KB (2027-02-01) [G02]; Play's memory thresholds (Feb 2027) and Level Up dates (2027-03-01, 2027-09-30) [G20]; Apple: building with the iOS 27 SDK from April 2027 (the submission page also says minimum iOS 15, the news doesn't: not verified), an iPhone Duo set from the iOS 27.1 SDK, new declarations [A02] [A08]; Firebase Test Lab closes 2027-09-30 [F06] | Missed → updates can't be uploaded or the game disappears | Dated calendar lines | — | [G01] [G09] [G02] [G20] [A02] [F06] |
| 12.2 | **SDK and Unity updates:** AdMob, UMP, Firebase, Unity IAP current; Unity security bulletins (e.g. CVE-2025-59489, 2025-10-02: rebuild with a patched editor and publish); Unity 6.3 LTS supported until December 2027, 6.0 LTS standard support ends October 2026 (the official page wasn't opened: not verified) [U12] | Security and compliance | A version table | After an update: the stage's build scans and the smoke run | [U09] [U12] |
| 12.3 | **Privacy follows code:** when the data leaving the device changes, the policy and both stores' declarations change in the same plan | Declarations match the code | "No change" or an update line | TL §12 declarations | — |
| 12.4 | **Play's recommended actions and vitals:** read at every release preparation; fixes become plan candidates | Warnings affect visibility | A candidate list | — | `google-play-level-up.md` §9 |
| 12.5 | **Price upkeep:** Turkey's manual prices every six months or at an Apple price or tax update | Exchange rates move | A dated price table | — | `google-play-level-up.md` › Play Console work |
| 12.6 | **Stay on the shelf:** Apple can remove an app not updated for 3 years with very few downloads after 90 days' notice (one that crashes at launch goes at once). On Play, after 2026-08-31 an app targeting below API 35 isn't shown to new users on devices with newer Android (an extension until 2026-11-01 at the latest). A shelved game monthly: Play Console's policy status and the AdMob app's status (a warning acted on before it turns into a removal or limited ads) | A shelved game mustn't vanish | A yearly maintenance release in the calendar; the monthly look's date and result | — | [A18] [G01] |
| 12.7 | **Repository and keys:** everything pushed; rebuildable from a tagged commit; the signing key backed up | Ready for a maintenance release | A tag and backup check | — | RC › Build |

## 3. Comprehensive test stage
How it runs lives in one place each: BAKIM.md › Comprehensive test stage (when, matrix, red, review, decision) and TL §0 (inputs, order, the build that ships, the device matrix, the permanent regression rows) and §15 (hold rules, the report file and its format). Phase 9 above lists its items; every item's Final test column is its input.

## 4. PC/Steam and YouTube channel differences

### PC / Steam
The same phases without ads, UMP, ATT or mobile store declarations. Differences:
- **Registration and calendar:** a $100 Steam Direct fee per app (non-refundable; paid back after $1,000 adjusted gross revenue) [P01]; 21 days from paying it to release [P02]. The "Coming Soon" page public ≥2 weeks before launch; the exact date locks in the last 2 weeks [P03]. Store page and build are reviewed separately (each usually 3-5 working days; send ≥7 working days ahead, the page first); later updates aren't reviewed; an approved game doesn't release itself: press "Release App" [P03]. Order: Coming Soon page → Playtest → a demo from the best build → Next Fest while the demo is live → launch (`steam-sayfasi-ve-next-fest.md`).
- **Next Fest:** February, June and October; once per game; an unreleased game with a public page and a demo; the demo in review ≥5 weeks ahead for press previews, else ≥3. Next: 2027-02-22 to 03-01 (sign-up by 2027-01-10; demo review 01-25 or 02-08) and 2027-06-14 to 06-21 (sign-up by 2027-04-25) [P04].
- **Store page:** capsules (header 920×430, small 462×174, main 1232×706, vertical 748×896) carry only art, the game's name and an official subtitle (no scores, awards or discount text); ≥5 gameplay screenshots (1920×1080+, 16:9); a gameplay-first trailer is required; ≥5 tags (the first 20 count); the content survey declares AI content players consume (not development tools); accessibility tags only for what really exists [P11] [P12].
- **Technical:** full keyboard + mouse and controller; resolution and window modes; graphics settings saved; minimum and recommended specs written (RC › PC). Steam Deck review is separate and doesn't block sales; "Verified" needs full controller support with default settings, the right button glyphs, the on-screen keyboard, 30 FPS at 800p and text ≥9 px at 1280×800 (12 recommended); about a week. Achievements and Steam Cloud optional (Auto-Cloud needs no code) [P05].
- **Visibility and sales:** visibility can't be bought; wishlists aren't an algorithm factor (only the Popular Upcoming tab), but wishlisters get e-mails at launch and at discounts of 20%+; a review score under 40% reduces featuring; 5 update visibility rounds after launch [P07]. Refunds within 14 days and under 2 hours of play for any reason: the first 2 hours sell the game [P06]. A launch discount of 10-40% for 7-14 days; 30 days between discounts [P08]; prices set per region, unchanged in the first 30 days [P10].
- **Measurement:** no Firebase Analytics on PC; PC measurement is planned on its own (`firebase-olcum-ve-uzaktan-ayar.md`). Instead of the scorecard: wishlists, demo playtime, refund rate, Steam reviews.
- **Test stage:** a hardware matrix (minimum and recommended specs) instead of the device matrix, controller types, window modes, Steam Deck, a long session; a Windows screen reader needs Unity 6000.3.21f1+.
- **After release:** updates as "Major update" or "Patch notes" events (no announcement when there's nothing to say); reviews need no one-by-one replies; never delete discussions or criticism [P09].

### YouTube channels
The project is a channel and a video series: no ad SDK, IAP or store declarations. The phases map as:
- **Pre-research:** successful channels, their most-watched videos, titles, thumbnails, length, pacing, comments (what viewers like and don't) (`on-arastirma.md`).
- **Vertical slice:** the style and one finished scene; the thumbnail and title pattern (`youtube-kucuk-resim.md`).
- **Instead of the comprehensive test, a detailed eye inspection before upload:** every object of the scene up close (missing or floating parts, intersecting surfaces, light leaks, flicker, the loop's seam), a frame from every minute, a helper agent as a second eye; a flaw → no upload (a channel's first video once went out with an empty chimney).
- **Policy:** the YouTube Partner Program today: 1,000 subscribers + 4,000 watch hours in 12 months, or 10 M Shorts views in 90 days; new applications from 2027-02-01 need 8,000 hours or 20 M Shorts views (the current terms accepted until 2027-01-31) [Y01]. "Repetitious content" became "inauthentic content" on 2025-07-15: templated, slideshow or mass-produced-looking content can't earn; loop and ambience videos aren't named (not verified), so each video stands apart with its own scene and work [Y02]. AI disclosure only for realistic altered or synthetic scenes; clearly animated and game footage are exempt [Y03]. "Made for kids" set right on every video (COPPA); a made-for-kids video loses comments, personalized ads and end screens [Y04]. Music: the YouTube Audio Library is safe from Content ID; YouTube takes no responsibility for other "royalty-free" packs (the studio's sound packs: not verified) [Y05].
- **Localization:** title and description in 30 languages through the API's `localizations` field.
- **Approval:** uploads to the owner's channel need the owner's OK (studio rule).
- **Measurement:** watch time, audience retention (the first 30 s as the intro; compare with videos of similar length) [Y08], click-through from Home and Suggested in the first 24 h [Y09]; Test & compare: ≤3 titles or thumbnails, watch time picks the winner, ≤2 weeks, not for Shorts [Y06]; chapters start at 00:00, ≥3, each ≥10 s [Y07].

## 5. New mobile game: plan skeleton
A new mobile game's first plan copies these step lines in the plan template's format (each line ends with ` → ` and its step file's path, e.g. `planlar/<plan>/01-on-arastirma.md`); the ids in brackets are §2's items, whose Done when and Final test go into the step file (an entry's name instead: that entry's pass rule). A step that doesn't fit becomes "None: ‹why›", never deleted. With step files the index stays short, so the 41 steps fit one plan; split into phases only for independent parts (PROTOKOL §3). A pre-research already done: step 1 cites its report and is ticked.
```
- [ ] **1. Pre-research**: market and competitors, area by area, the quality bar; the owner's summary and reference sheet (1.1-1.3)
- [ ] **2. Concept and identity**: game summary, distinctive mechanics, name, package ID, slug (1.4-1.5)
- [ ] **3. Revenue model, gates, budgets**: revenue table, D1/D7/minutes gates, technical targets (1.6-1.8)
- [ ] **4. Expert review and approval** (1.9)
- [ ] **5. Technical skeleton**: project settings, monetization kit, Firebase, Localization, store records (2.1, 7.1)
- [ ] **6. Save foundation**: versioned, atomic, backed-up save and the launch order (2.4)
- [ ] **7. Core loop prototype** (2.2)
- [ ] **8. Level generator and solver** (2.3)
- [ ] **9. Fun gate and marketability**: decision line (2.5-2.6)
- [ ] **10. Style guide** (3.1)
- [ ] **11. One finished screen**: scored beside the comparisons (3.2)
- [ ] **12. Game feel and sound** (3.3-3.4)
- [ ] **13. UI screen set**: phone and tablet, safe area (3.6)
- [ ] **14. First minute** (3.5)
- [ ] **15. Performance base**: 60 FPS on a device, no per-frame garbage (3.7)
- [ ] **16. Icon** (3.8, 8.1)
- [ ] **17. Levels and difficulty curve** (4.1-4.2)
- [ ] **18. Goal layers and daily reward** (4.3)
- [ ] **19. Economy** (4.4)
- [ ] **20. Settings and help screen** (4.6)
- [ ] **21. Platform services**: PGS and achievements, Game Center (4.5)
- [ ] **22. Consent flow**: UMP, KVKK, deferred ATT (5.2-5.4)
- [ ] **23. Ads**: interstitial rule, rewarded (5.5-5.6)
- [ ] **24. Purchases**: catalogue, prices, delivery ledger, restore (5.7-5.8)
- [ ] **25. Remote Config and kill switches** (5.9)
- [ ] **26. Measurement**: analytics events, GA4 audit, Crashlytics (5.10-5.11)
- [ ] **27. Localization**: tables, fonts, overflow (6.1-6.3, 6.5)
- [ ] **28. Accessibility**: palette, readability, motion and haptics (6.6-6.8)
- [ ] **29. Notifications (optional)** (4.7)
- [ ] **30. Licences and credits** (4.8)
- [ ] **31. Signing, dated requirements, R8 and symbols** (7.2-7.4, 7.9)
- [ ] **32. Privacy page and catalog record** (7.5)
- [ ] **33. Store declarations and countries**: Play, Apple, audience, rights, regional rules (6.9, 7.6-7.8, 7.10-7.11)
- [ ] **34. Store visuals**: screenshots, video, feature graphic (8.2-8.3, 8.5)
- [ ] **35. Store text and languages** (8.4, 6.4)
- [ ] **36. Featuring requests and store events** (8.6)
- [ ] **37. app-ads.txt and support** (5.12, 8.9)
- [ ] **38. Launch week preparation**: clips, calendar, experiment plan (8.7-8.8)
- [ ] **39. Polish & Quality Gate**: the finished game beside its top 3, blind scores, a fresh player's 10 minutes, portfolio checks, ≤2 fix loops; Final test `KAPI: GEÇTİ` (kalite-kapisi.md)
- [ ] **40. Comprehensive test**: every step file's Final test, matrix, order, regressions, store reports, expert, report (9.1-9.6)
- [ ] **41. Release and announcement**: version data, submission list, Play and iOS submissions, release-day check, the announcement the same day, wrap-up (10.1-10.7)
```
After release (a separate plan): first 72 hours and the window (11.1-11.2) → scorecard and decision (11.3-11.4) → rating prompt, replies, store events (11.6-11.8) → the next version's plan (11.5). Phase 12's items: a checklist at every version's preparation.

## 6. Sources
Status: read on 2026-10-21 in the research (by the researcher or its helpers) unless marked; "via entry" = from a handbook entry, with that entry's reading date. Pages change: re-read before turning a dated requirement into a step.

**Google Play and Android** (PCH = https://support.google.com/googleplay/android-developer/answer/, AD = https://developer.android.com/)
- [G01] PCH 11926878, target API requirements
- [G02] AD guide/practices/page-sizes, 16 KB page sizes (page updated 2026-10-16)
- [G03] PCH 10787469, Data safety; SDK disclosures: https://developers.google.com/admob/android/privacy/play-data-disclosure · https://firebase.google.com/docs/android/play-data-disclosure
- [G04] PCH 9893335 (Families policy, target audience) and 9900633 (Families self-certified ads SDK program)
- [G05] PCH 9859654 (review and publishing times, managed publishing), 9859751 (publishing overview), 14807773 (pre-review checks), 6346149 (staged rollout), 9845334 (test tracks); the studio's first-release rules via `google-play-level-up.md` › Direct release
- [G06] PCH 9842757, pre-launch report
- [G07] AD topic/performance/vitals, bad-behaviour thresholds
- [G08] PCH 9842756 (Play App Signing) and 9844279 (app bundles)
- [G09] AD google/play/billing/deprecation-faq, Billing Library timeline (updated 2026-10-20)
- [G10] AD google/play/billing/integrate (acknowledge, pending purchases, query at launch)
- [G11] PCH 9866151, preview assets (field limits 9859152)
- [G12] PCH 9898842, metadata policy
- [G13] PCH 6227309, store listing experiments
- [G14] PCH 12932541 (promotional content), 11271869 (featuring timing); https://google.play/business/guides/premium-growth-tools/
- [G15] AD guide/playcore/in-app-review
- [G16] PCH 138230, ratings and reviews, replies (the 350-character reply limit isn't on this page: it's the reply API's, via entry)
- [G17] PCH 6048248, advertising ID (AD_ID permission)
- [G18] PCH 13849271 and 16550159 (Financial features, 2025-10-30), 14738291 (Health), 17134731 (content rating and app registration); policy timeline https://support.google.com/googleplay/android-developer/table/12921780
- [G19] AD docs/quality-guidelines/adaptive-app-quality and core-app-quality (updated 2026-10-03)
- [G20] AD games/guidelines, Google Play Games Level Up (first 100,000 characters read; the end of the change notes not read)
- [G21] PCH 9857753, ads policy
- [G22] AD google/play/vitals/launch-time, launch time thresholds
- [G23] AD google/play/age-signals/overview; PCH 16569691 (US state laws)
- [G24] PCH 6223646, country-specific requirements
- [G25] PCH 9848633, deobfuscation and native debug symbols
- [G26] https://support.google.com/googleplay/contact/featuring_review, featuring request form
- [G27] AD google/play/billing/test, license testers
- [G28] AD develop/ui/views/notifications/notification-permission

**Apple** (all read; App Review Guidelines as of 2026-10-16; DEV = https://developer.apple.com/)
- [A01] DEV app-store/review/guidelines/ · change news DEV news/?id=92th7e5i
- [A02] DEV news/upcoming-requirements/ · iOS 27 SDK (April 2027) DEV news/?id=k1mtkt1k · DEV app-store/submitting/
- [A03] DEV app-store/app-privacy-details/
- [A04] DEV documentation/bundleresources/privacy-manifest-files · DEV support/third-party-SDK-requirements/
- [A05] DEV app-store/user-privacy-and-data-use/ (ATT, the EU's iOS 27.2 prompt)
- [A06] DEV help/app-store-connect/reference/age-ratings-values-and-definitions · DEV news/?id=ks775ehf · DEV news/?id=tlur8uvi
- [A07] DEV help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements
- [A08] DEV help/app-store-connect/reference/app-information/screenshot-specifications · …/app-preview-specifications
- [A09] DEV app-store/product-page-optimization/
- [A10] DEV app-store/custom-product-pages/
- [A11] DEV app-store/in-app-events/
- [A12] DEV app-store/getting-featured/ · DEV help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring/
- [A13] DEV app-store/ratings-and-reviews/
- [A14] DEV help/app-store-connect/test-a-beta-version/testflight-overview · DEV help/app-review/before-submitting-for-review/configure-in-app-purchases
- [A15] DEV help/app-store-connect/update-your-app/release-a-version-update-in-phases
- [A16] DEV documentation/security/complying-with-encryption-export-regulations
- [A17] DEV help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels
- [A18] DEV support/app-store-improvements/
- [A19] DEV design/human-interface-guidelines/privacy (pre-permission screens)
- [A20] DEV support/age-assurance/ · DEV news/?id=sg176nne · DEV news/?id=8jzbigf4
- [A21] DEV distribute/app-review/ (times, common rejections)
- [A22] DEV help/app-store-connect/reference/app-information/platform-version-information
- [A23] Developer news: the new developer agreement (2026-10-13) DEV news/?id=17mwd36z · Vietnam game licence DEV news/?id=06h4gf33
- [A24] DEV documentation/storekit/skadnetwork

**Firebase, AdMob, privacy law** (FB = https://firebase.google.com/docs/, AM = https://support.google.com/admob/answer/)
- [F01] FB analytics/unity/events (500 event types, verbose logging)
- [F02] GA4 recommended events: https://developers.google.com/analytics/devguides/collection/ga4/reference/events (GA4 data retention, https://support.google.com/analytics/answer/7667196: not read)
- [F03] FB remote-config/loading · FB remote-config/unity/get-started · FB remote-config/pricing (updated 2026-10-20) · https://firebase.blog/posts/2023/06/feature-flags-with-real-time-remote-config
- [F04] FB ab-testing/abtest-config · FB ab-testing/ab-concepts
- [F05] FB crashlytics/unity/get-started · FB crashlytics/unity/customize-crash-reports · FB crashlytics/crash-free-metrics · FB crashlytics/alerts-default
- [F06] FB test-lab/usage-quotas-pricing · FB test-lab · FB test-lab/android/game-loop · FB test-lab/android/robo-ux-test
- [F07] https://developers.google.com/admob/unity/test-ads · https://developers.google.com/admob/unity/ad-inspector · AM 2753860
- [F08] AM 6066980 · AM 6201362 · AM 2936217 · AM 6244508 · AM 10105530 (interstitial guidance, disallowed implementations, placement, frequency capping, limited ads)
- [F09] AM 7313578, rewarded ads policy
- [F10] AM 9363762 · AM 14538460 · AM 10564477 (app-ads.txt, app readiness and verification, app review)
- [F11] https://developers.google.com/admob/unity/privacy · https://developers.google.com/admob/unity/privacy/us-states · AM 10862202 · AM 10115027 (UMP, US states, the IDFA explainer)
- [F12] AM 13554116, certified CMP requirement
- [F13] KVKK: Law 6698 (English text, with Law 7499's changes) https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law · transfer abroad https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim · VERBİS exemption (2023/1154) https://www.kvkk.gov.tr/Icerik/7647/2023-1154
- [F14] AM 9999955 (TCF v2.3 errors) · https://www.google.com/about/company/user-consent-policy/

**Unity** (U63 = https://docs.unity3d.com/6000.3/Documentation/)
- [U01] U63 Manual/performance-incremental-garbage-collection.html
- [U02] U63 ScriptReference/Application-targetFrameRate.html
- [U03] Unity 6 e-books: optimizing for mobile, XR and the web; profiling games (Unity's asset CDN, read)
- [U04] Unity's 16 KB announcement https://discussions.unity.com/t/info-unity-engine-support-for-16-kb-memory-page-sizes-android-15/1589588 · Unity 6.3 Android requirements https://docs.unity.com/en-us/engine/6000.3/manual/platform-specific/android/introducing/requirements-and-compatibility · U63 Manual/class-PlayerSettingsAndroid.html
- [U05] Unity IAP 5: https://docs.unity.com/en-us/iap/purchases · https://docs.unity.com/iap/restore-purchases · https://docs.unity.com/en-us/iap/receipt-validation
- [U06] https://docs.unity3d.com/Packages/com.unity.localization@1.5/manual/Pseudo-Localization.html · U63 Manual/UI-system-compare.html · U63 Manual/UIE-advanced-text-generator.html
- [U07] AD games/engines/unity/unity-r8
- [U08] U63 Manual/android-symbols.html · U63 ScriptReference/Screen-safeArea.html
- [U09] https://unity.com/security/sept-2025-01 (CVE-2025-59489)
- [U10] https://docs.unity3d.com/Packages/com.unity.purchasing@5.4/changelog/CHANGELOG.html (5.0.0 Billing 8.0.0; 5.4.0 Billing 9.0.0; 5.4.4 on 2026-10-02)
- [U11] U63 ScriptReference/Application-persistentDataPath.html
- [U12] https://unity.com/en/releases/unity-6/support: not read (a search summary only)
- [U13] U63 Manual/apple-privacy-manifest-policy.html
- [U14] U63 Manual/frame-timing-manager-enable.html · U63 Manual/device-simulator-introduction.html

**Publishers and benchmarks** (read; company posts and reports, not policy)
- [E01] Voodoo's prototype KPIs (old D1 55%, D7 22%, CPI $0.25; new 45%, 13%, $0.20), GameAnalytics blog: https://www.gameanalytics.com/blog/how-voodoo-diversified-and-lowered-game-product-kpis
- [E02] Voodoo's hybrid targets (2023 podcast summary): https://gameworldobserver.com/2023/07/25/voodoo-hybrid-games-d7-retention-games-and-names-podcast
- [E03] SayGames, a publishing model for hybrid games (2026-06-22): https://blog.say.games/posts/why-saygames-believes-hybrid-games-need-a-different-publishing-model
- [E04] Supersonic: prototype KPIs (2021) and 2025 hybrid lessons: https://supersonic.com/learn/blog/the-3-most-important-kpis-for-testing-your-hyper-casual-prototype/ · https://supersonic.com/?p=106607
- [E05] CrazyLabs' test stages (2023, sponsored): https://www.pocketgamer.biz/a-deep-dive-into-crazylabs-transparency/
- [E06] GameAnalytics 2026 benchmarks (2025 data, 16,000+ games, no genre split): https://www.gameanalytics.com/reports/2026-mobile-pc-gaming-benchmarks
- [E07] GameAnalytics 2025 benchmarks (puzzle and casual separate): https://www.gameanalytics.com/reports/2025-mobile-gaming-benchmarks
- [E08] Unity, what is ROAS (genre medians are third-party data Unity didn't verify): https://unity.com/resources/what-is-roas
- [E09] GameAnalytics, soft launch guide (the first 30-60 s, tutorial testing): https://gameanalytics.com/blog/mastering-mobile-game-soft-launch/

**Accessibility**
- [E10] Game Accessibility Guidelines (colour alone carries no information, sound alone carries none, readable default text, separate volume settings; all "basic"): https://gameaccessibilityguidelines.com/full-list/
- [E11] WCAG 2.2, 1.4.3 (text 4.5:1; large text 3:1) and 1.4.11 (UI components 3:1): https://www.w3.org/TR/WCAG22/

**Steam** (all read; SW = https://partner.steamgames.com/doc/)
- [P01] SW gettingstarted/appfee · [P02] SW gettingstarted/onboarding (21 days) · [P03] SW store/coming_soon · store/release_dates · store/review_process · store/releasing · [P04] SW marketing/upcoming_events/nextfest (…/feb_2027, …/june_2027) · [P05] SW steamdeck/compat · features/achievements · features/cloud · [P06] https://store.steampowered.com/steam_refunds/ · [P07] SW marketing/visibility · marketing/wishlist · marketing/visibility/update_rounds · [P08] SW marketing/discounts · [P09] SW marketing/event_tools · store/reviews · marketing/community_moderation · [P10] SW store/pricing · [P11] SW store/assets/standard · store/assets/rules · store/trailer · [P12] SW store/tags · gettingstarted/contentsurvey

**YouTube** (all read; YT = https://support.google.com/youtube/answer/)
- [Y01] YT 72851 · YT 12843009 · https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/ · [Y02] YT 1311392 · [Y03] YT 14328491 · [Y04] YT 9528076 · 9527654 · 9684541 · [Y05] YT 2797370 · 6013276 · 3376882 · [Y06] YT 16391400 · [Y07] YT 9884579 · [Y08] YT 9314415 · [Y09] YT 12340300 · 72431

**Unverified and conflicting** (as found on 2026-10-21)
- Apple: a minimum iOS 15 (April 2027) only on the submission page, not in the news · the required iPhone screenshot size conflicts on the size page (check Media Manager at submission) · the enforcement date of SDK privacy manifests (ITMS-91061) only on forums · no date for Accessibility Nutrition Labels becoming required · what US state age laws require of account-less games (Apple points to a lawyer) · featuring lead time differs on two pages (2 and 3 weeks; 3 taken) · Vietnam's licence start date.
- Google Play: Billing Library 9+ on 2027-08-31 is inferred from the table, the page doesn't say it · 16 KB: older Console warnings and Unity's post say 2025-11-01, Google's developer page says 2027-02-01 for updates (the studio already builds with 16 KB) · Level Up change-note IDs LU-PF and LU-GPGC don't match the guidelines' LU-PR and LU-PC · who must make the Advertising ID declaration in App content (check the Console) · test-user details for new personal accounts · AdMob's Families-certified version · DSA trader status on Play · whether API 36's orientation-lock exemption for games (`android:appCategory="game"`) is in Unity builds · tablet screenshots: 7,680 px vs the general 3,840 px limit.
- Firebase and GA4: event parameter and name length limits · the DebugView command · whether consent mode v2 reads the TCF string UMP writes · GA4 data retention, traffic filters and the AdMob link · whether our UMP and ad plugin versions write TCF v2.3 strings.
- KVKK: the 2026 re-valued fine table (the official PDF didn't open) · explicit consent per type for analytics and ad cookies (Board decisions only from summaries) · explicit consent text and the notice as separate documents (2026/347, from a summary).
- Unity: 6.3 LTS and 6.0 LTS support dates (official page not opened) · no official Arabic shaping in uGUI and TextMeshPro, RTLTMPro only from a search summary · the Pseudo-Locale's expansion ratio · a 60 FPS target dropping to 45 on 90 Hz screens is an inference.
- Publishers and benchmarks: test fees, IP and revenue share on no publisher's page · Homa's and Kwalee's pages didn't open, their figures unverified · App Store Connect and Play Console peer benchmarks not read · AppMagic's and Sensor Tower's free tiers not researched · no numeric guide for sample size found · GameAnalytics 2025 gives two figures for the top 25%'s D1 (26.5-27.7% and 28-29%).
- Steam: the controller support tags' exact names · an AI disclosure change reported in January 2026 (press only) · the Steam Cloud quota.
- YouTube: no explicit rule for loop and ambience videos · the Content ID status of "royalty-free" packs such as Sonniss.
