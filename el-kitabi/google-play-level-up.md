---
title: Google Play's recommended game structure (Level Up) and Play Games Rewards
condition: "Unity project with Android (Google Play) among the target platforms. Signs: Android in the game summary or memory; `AndroidKeystoreName` set in `ProjectSettings/ProjectSettings.asset`; `Assets/Plugins/Android/` exists. Unsure → ask the user one question."
read_when: Preparing a Google Play release (a first release too); planning Play Games Services, achievements, Play Games Rewards, in-app purchases, Game Stats, cloud save, an FPS target, large screens or controller support; judging what Level Up pays (fees, Quests); Play Console warnings (R8, edge-to-edge), Android vitals memory, promotional content, release settings; placing interstitial ads.
requires: — (Google Play Games plugin for Unity and Unity IAP are added inside the relevant plan)
plan_candidates:
  - "Level Up 1: PGS sign-in, 10+ achievements, reward delivery, 2 one-time Play Games Rewards · el-kitabi/google-play-level-up.md"
  - "Level Up 2: Game Stats, 1 repeatable Play Games Reward · el-kitabi/google-play-level-up.md"
  - "Level Up 3: 60 FPS, Vulkan, large screens, controller and keyboard/mouse, cloud save · el-kitabi/google-play-level-up.md"
  - "Play Console warnings: R8 keep rules, edge-to-edge · el-kitabi/google-play-level-up.md §9"
source: Google Play games guidelines (Level Up program) · Android Developers · https://developer.android.com/games/guidelines · also /games/rewards, /games/pgs/gamestats, /games/pgs/unity/unity-start, /games/pgs/unity/gamestats, /games/pgs/console/setup, /games/pgs/unity/migrate-to-v2, /games/playgames/start, /topic/performance/vitals/code-optimization · google.play/business/levelup · Play Console Help 112622 (fees), 17492799 (memory), 9859654 (review), 9857753 (Ads policy), "Promotional content" · the plugin's GitHub releases and `scripts/proguard.txt` · Android Developers Blog 2025-06-30 (Quests), 2025-10 "New tools and programs to accelerate…"
tech: Unity 6 · Google Play Games plugin for Unity on PGS v2 (v11 or later, then numbered 2.x; latest 2.3.0, 2026-09-29) · Unity IAP v5 (`com.unity.purchasing`)
added: 2026-09-30 · compiled from official docs (pages as of September 2026), Claude · 2026-10-01 dates removed, build order and 3rd plan candidate added · 2026-10-01 translated to English · 2026-10-07 Play Console work via Claude in Chrome · 2026-10-09 PGS console setup, direct release, promotional content, store warnings (R8, edge-to-edge) · 2026-10-15 fees, Quests, exemptions, title availability, memory, PGS keeps (Project B), first release, interstitial placement (studio rule): the Project F session's research, each fact re-read on its official page (1.46) · 2026-10-16 §8: featuring needs the Premium growth tools thresholds (the Level Up+ page now redirects to Level Up); details moved to `store-events.md` (1.49)
---
# Google Play's recommended game structure (Level Up)

## Summary
With the Level Up guidelines Google Play recommends a structure for Android games: Play Games Services sign-in, achievements, Game Stats, Play Games Rewards, cloud save and quality targets (FPS, large screens, controller). This entry shows how to add that structure to the game **in the right order**. The structure is voluntary; missing parts don't remove the game from the store (the memory thresholds in section 7 are Play-wide rules, not part of the choice). Play Games Rewards are free in-game items Google Play grants when the player finishes a quest or a social challenge on Play. Official skill for purchase code: `unity:implement-in-app-purchases`. Also here: what the program pays, Play Games Services setup in Play Console, promotional content, store warnings, interstitial placement and direct release (first release too). iOS counterpart: `app-store-game-center.md`.

## Build order
Each part builds on the previous one; keep the order. Size each plan by `PROTOKOL.md` §2; split it if large.

| # | Part | Why in this order | Plan |
|---|---|---|---|
| 1 | Play Games Services sign-in | Achievements, Game Stats and rewards are tied to the player's Play Games identity | Level Up 1 |
| 2 | Achievements | One-time rewards come from quests on Play; quests are built on achievements | Level Up 1 |
| 3 | Reward delivery structure (Unity IAP) | Rewards reach the game through Play Billing; without the delivery structure a reward is lost | Level Up 1 |
| 4 | 2 one-time rewards | once 1-3 are ready | Level Up 1 |
| 5 | Game Stats | Repeatable rewards come from social challenges; challenges are built on Game Stats | Level Up 2 |
| 6 | 1 repeatable reward | once 3 and 5 are ready | Level Up 2 |
| 7 | 60 FPS and Vulkan, large screens, controller and keyboard/mouse, cloud save | Touches the game itself, independent of the reward chain | Level Up 3 |

Sidekick, PC, devices, stability and memory need no plan of their own; check them during release prep with the release checklist (table in section 7).

## Know first
- **What Level Up pays** (google.play/business/levelup; Help 112622): a developer's first $1M a year pays 10% (+5% billing fee on Play Billing purchases); above it subscriptions 10%, other purchases 20%/25% (new/existing installs), or 15%/20% once the game meets every guideline announced 2026-06-24 (enrolled games don't switch by themselves). By player location: AU, EEA, JP, UK, US since 2026-09-30, KR 2026-12-31, the rest 2027-09-30 (15% on the first $1M until then). Extras: the `You` tab, Sidekick, Leagues (Game Stats leaderboards), Quests (Play rewards earned achievements, e.g. with Play Points; needs Play Points participation, PGS v2, achievements in Play Console, ≥4 earnable in the first hour).
- **Order this implies:** below $1M a year only the extras pay off → Level Up 1 in every game, Level Up 2 next; Level Up 3's controller, PC and cloud save once earnings near $1M or a feature needs them; 60 FPS, large screens, stability and memory always (Play-wide vitals).
- **Exemptions (check before planning):** a game aimed mainly at under-13s needs neither Play Games Services nor the parts tied to it (Sidekick, achievements, Game Stats, rewards, cloud save). A paid game (full game at install or with a single in-game purchase) needs no rewards.
- **Source may change:** when planning, glance at the source page's "Change notes", don't read the whole page. If the structure changed after the entry was compiled (`added` in the front matter), tell the user.
- **A reward is an out-of-app purchase:** Play grants the reward outside the game and the game receives it through Play Billing. Even a game that sells nothing needs Play Billing (Unity IAP in Unity) and a product in Play Console. The player must open the game within **3 days** to receive the reward.
- **Identity:** a reward is shown only if the player's Play Games identity and Play Billing account match. If the game has several in-game accounts, ask the player which one gets the reward.
- **Play Console work is Claude's,** in its own Chrome profile (Claude in Chrome, `tarayici-baglantisi.md`) without asking permission (built-in safety confirmations still apply). Record the values (product ID, name, description, CSV) in `docs/ai/tasarim/google-play-games.md` (create it if missing and index it in `HAFIZA.md`). The user keeps the payments profile (bank and tax data) and accepting program terms. Chrome not connected → the user enters the values; write the steps to the manual tests.

## 1. Play Games Services sign-in (`LU-PA-GAA`)
- **PGS v2 only:** Google Play Games plugin for Unity v11 or later (newer releases are numbered 2.x: 2.3.0 of 2026-09-29; Game Stats calls need 2.2.0+, which requires minSdk 24) from the official GitHub repo (`playgameservices/play-games-plugin-for-unity`: import `current-build/GooglePlayGamesPluginForUnity-<version>.unitypackage` with *Assets > Import Package > Custom Package*). v10 and earlier use the retired v1, which can't ship new versions → upgrade first (Google's "Migrate to Play Games Services v2 (Unity)": remove the old plugin folders; `Authenticate()` replaces `PlayGamesClientConfiguration`).
- Play Console's "Integrate PGS v2 for core features" → the live version has no v2 sign-in yet; it clears once a version with this section is live.
- **Play Console setup** (Claude in Chrome; *Grow users > Play Games Services > Setup and management > Configuration*):
  1. New game: "No, my game doesn't use Google APIs" → name → **Create**. *Properties*: display name and description as in the store listing, category, graphics (needed to publish).
  2. OAuth consent screen (**Configure** opens Google Cloud): available to all players; scopes `games`, `games_lite`, `drive.appdata` (no verification needed); publish it at once; **Done** back in Play Console.
  3. *Credentials > Add credential > Android*, twice with the same package name: SHA-1 of the **app signing key** (store builds) and of the **upload key** (builds made on this computer); both are on Play Console's *App integrity > App signing* page. Every OAuth client needs its own credential, or achievements don't attach.
  4. No testers (Direct release, below): publish the PGS configuration before the game version goes live; ask the user once in chat before pressing publish.
- *Configuration > Get resources* → copy the Android (XML) content and paste it into Unity's *Window > Google Play Games > Setup > Android Setup*; it carries the application ID and generates a C# class with the ID constants.
- Call `PlayGamesPlatform.Instance.Authenticate(callback)` at startup. If sign-in fails, don't block the game: turn PGS features off and let an optional sign-in button call `ManuallyAuthenticate`. No in-game account system is needed.
- Optional (plugin 2.1.0+): the manifest `<application>` meta-data `com.google.android.gms.games.SUPPRESS_GAME_PROFILE_CREATION` = `true` stops Play's automatic profile-creation screen for players without a Play Games profile; they stay signed out (no achievements, Quests or rewards) until the button's `ManuallyAuthenticate` offers it. Default off; decide in the Level Up 1 plan.

## 2. Achievements (`LU-AC`)
- At least 10 achievements spread across the game (40+ recommended).
- Each with a unique name, description and icon; the description says what to do.
- **For quests, at least 4 must be reliably earnable by everyone in the first hour** (e.g. finish the tutorial, clear the first level, get the first item).
- Derive them from progress: level, high score, unlocked area, defeated enemies, collected items.
- Code: `PlayGamesPlatform.Instance.UnlockAchievement(id, callback)`; `IncrementAchievement` for incremental ones.

## 3. Reward delivery structure (Unity IAP v5)
Current API and details: `unity:implement-in-app-purchases`.
1. Set up the store connection at startup. Subscribe to `OnPurchasePending` and `OnPurchaseConfirmed` **before** `Connect`; pending rewards can arrive as soon as the connection is up.
2. Call `FetchPurchases()` at startup and every time the game returns to the foreground (`OnApplicationPause(false)`). This is the check Google asks for: a reward granted outside the game is caught this way.
3. On `OnPurchasePending`, in order: is the product in the reward table → validate the receipt (the skill's method; local validation if there is no server) → grant the item → **save** → show it to the player ("Google Play reward: …", localized) → `ConfirmPurchase`. Save comes before confirm: an unconfirmed order arrives again on the next launch, so the reward isn't lost.
4. **Grant once:** the same order can arrive more than once. Keep granted order IDs in the save and skip repeats. If a one-time item is already owned, don't grant it again but still confirm the order.
5. A consumable reward is consumed once confirmed and `FetchPurchases` never returns it again; record the grant in your own save.
6. Put the grant logic in a small class separate from the store (e.g. `PlayRewardGranter`: order → grant → save), so EditMode tests can use a fake store and a fake save.

## 4 and 6. Play Games Rewards
| | One-time (4) | Repeatable (6) |
|---|---|---|
| How many | at least 2 offers | at least 1 offer |
| Granted when | the player finishes a **Quest** on Play | a **social challenge** ends; at most 1 per player per week |
| Examples | character, costume (skin), weapon, avatar, profile badge | in-game currency, lives/energy, temporary booster, daily reward |
| Unity IAP product type | `NonConsumable` | `Consumable` |
| Builds on | achievements | Game Stats |

Every reward must reach every player in every published region at least once via Play and be meaningful or attractive to the player (`LU-RE-GAA`, `LU-RE-GAB`). It can be an item already in the game or a new one. When designing:
1. Read the game summary (and the GDD, if any); choose rewards that fit the game's progression and economy.
2. **One-time:** a visible, lasting item that is hard to get in the game (e.g. a special costume or character). Don't give power that unbalances the game.
3. **Repeatable:** a small value fit for weekly grants (e.g. currency worth one day of play, or 1-3 boosters). Don't give amounts that break the economy.
4. **Product ID:** reuse the existing ID if the item is already sold, else `reward_<name>` (lowercase, underscores). IDs in Play Console must match the code exactly.
5. Show the reward and achievement design to the user at plan approval.

## 5. Game Stats (`LU-GS`)
- At least 5 **recurring** stats (at least 1 suited to competition) and, if there is a primary progression, 1 **progress** stat; at most 50 in total.
- When the core loop ends, send an event with its properties (e.g. `level_completed`, `run_completed`). For progress send the `progressUpdate` event with the `currentProgress` property at every session start and whenever progress changes.
- Stats must not grow from purchases, watching ads or generic use like "open the game", must hold no personal data and must be open to all players.
- Code (plugin 2.2.0+; 2.3.0 adds `RecordEventImmediate`): `new PlayerGameEvent.Builder("level_completed").AddProperty("level", 12).Build()` → `PlayGamesPlatform.Instance.RecordEvent(e)` → `RequestEventsUpload()`.
- The event schema (CSV) and stat definitions (3 CSVs plus icons, ZIP) are uploaded to Play Console. Events that don't match the schema are rejected.

## 7. Quality and other guidelines
| Guideline | What the game does |
|---|---|
| Performance (`LU-PR`) · Level Up 3 | 60 FPS target in active play on reference devices: average ≥ 55, P90 ≥ 50, P99 ≥ 30. **Unity runs at 30 FPS on mobile by default:** set `Application.targetFrameRate = 60`. Exempt on tablets and foldables, and for games that draw frames only on player interaction |
| Vulkan (`LU-VK`) · Level Up 3 | Unity 2023+: Vulkan as the primary graphics API (top of *Player Settings > Other Settings > Graphics APIs*); OpenGL ES in under 10% of frames (ads, web views) is fine. Built-in Render Pipeline games may use ANGLE on Android 17+ until 2027-09-30, then Vulkan (URP recommended) |
| Large screens (`LU-LS`) · Level Up 3 | UI follows `Screen.safeArea`. No crash on rotation, folding, split screen or window resize; game state is kept (*Resizable Window*). Landscape games full screen without black bars at 4:3, 16:10 and 21:9; portrait games at 3:4, 10:16 and 9:21. A single-orientation game letterboxes itself cleanly on the other orientation; no second layout needed |
| Input (`LU-IC`) · Level Up 3 | The whole game, menus included, is playable with a controller and with keyboard/mouse (Input System); keyboard or mouse alone counts as K&M. No controller needed for drawing or fast drag-and-drop (K&M still is); neither for AR/location, ambient sensors (microphone, sleep tracking), turning the body 360°, gyro/accelerometer aiming or multi-touch rhythm. Tap-to-select puzzles have no exemption |
| Cloud save (`LU-CS`) · Level Up 3 | With an in-game account, progress is kept in the cloud and restored at startup; on conflict with the local save the player chooses. PGS Saved Games (up to 3 MB) or Unity Cloud Save (`unity:build-live-game`). Exempt with guest play only or no cross-session save |
| Sidekick (`LU-SK`) | No code: publish as an AAB, turn Sidekick on in Play Console |
| PC (`LU-PC`) | Playable on Google Play Games on PC; hardware and permissions missing on PC aren't marked required in the manifest. ARM-only builds run on Intel/AMD PCs (Intel Bridge); x86-64 recommended, not required; compatibility-mode keyboard/mouse is enough; certification: 30 FPS on a lower-tier PC, 60 on a higher-end one. Exempt: AR/location, ambient sensors, 360° turning, an IP licence excluding PC, paid games with an existing PC price gap |
| Devices (`LU-FF`) | Distribution on phones, foldables and tablets turned on; Android XR, TV, Googlebook and Auto from 2027-09-30 (not necessarily through Play) |
| Simultaneous launch (`LU-TA`) | Release on Android at the same time as on a comparable non-Android platform (e.g. iOS): 15 days to be live on Play (up to 30 if Google's review or a Google-side issue caused the delay), else the rate card waits 6 months; not in the EEA. → Android first or together |
| Stability (`LU-ST`) | Over the last 28 days on reference devices with ≥1,500 sessions in that time: crashes < 1%, ANR < 2%; on 4 GB+ RAM devices < 2% and < 3% |
| Memory (`LU-MM`) | From Feb 2027 for all of Play (Level Up needs every threshold): Android 13+ phones and tablets, P90 over 28 days; games on 4 GB devices ≤2.25 GB in the foreground (anonymous RSS + swap); bitmaps >200 MB (user-perceived or background) or >400 MB (cached) fail; >50 MB DEX → ≥25% each of shrinking, optimization and obfuscation (R8, §9; App bundle explorer). Misses can cut visibility and publishing (Help 17492799). Check Android vitals' memory metrics before each release |

## 8. Promotional content (store listing, `You` tab)
- For each content update or in-game event (not a bug fix): Play Console *Grow users > Store presence > Promotional content > Create event*: name, description, image or YouTube video, start and end. It shows on the store listing for every game and on the Play Store's `You` tab for Level Up games (featuring and deep links: only above the Premium growth tools thresholds).
- Submission opens 60 days before the start; review takes up to 4 days → submit at least 4 days ahead.
- Claude creates it and records it in `docs/ai/tasarim/google-play-games.md`. Discounts and Play Points coupons cost money → only with the user's OK.
- Rules, limits, the per-release plan step and the iOS counterpart (In-App Events): `store-events.md`.

## 9. Store warnings (recommended actions) and ad placement
Before each release prep Claude reads Play Console's recommended actions and Android vitals for the latest version (Chrome) and queues the fixes worth doing as plan candidates, one line each with the reason. Plan candidate exemption: neither warning below (R8, edge-to-edge) shows. Known ones:
- **R8 / DEX code optimization** ("Improve your app's memory and performance with R8 optimization"; from Feb 2027 a Play-wide threshold for games with >50 MB DEX, §7 Memory):
  - Unity: *Publishing Settings > Minify > Release* on; a custom launcher template uses `proguard-android-optimize.txt` (`proguard-android.txt` carries `-dontoptimize`).
  - Usual remaining cause: package-wide keep rules in `Assets/Plugins/Android/proguard-user.txt` (`-keep class com.google.firebase.** { *; }` style) that exempt whole libraries from R8. Libraries ship their own consumer rules; keep only the JNI and reflection entry points the C# side calls (e.g. the Unity plugins' bridge classes).
  - PGS: the plugin's own `scripts/proguard.txt` has 23 keeps, many package-wide (`gms.common.api.**`, `signin.**`, `dynamite.**`, `nearby.**`…). One project's block (2026-10-10, matched to the calls its C# makes) needs 4: `com.google.games.bridge.**`, `com.google.android.gms.games.**`, `com.google.android.gms.tasks.**`, `com.google.android.gms.common.api.Status`. Game Stats or Saved Games may need more: check every release build (Project B's and Lantern's `docs/ai/araclar/r8-kontrol.py`).
  - Measure first: DEX total `unzip -l <aab> | grep '\.dex$'`; scores (AGP 8.10+) in `BUNDLE-METADATA/com.android.tools/r8.json`. Small DEX → low priority.
  - One library per step; after each, the release build on a device: startup, sign-in, ads, purchases, Firebase/Crashlytics. A missing keep shows as `ClassNotFoundException` or a JNI error in logcat.
- **Edge-to-edge** ("Edge-to-edge may not display for all users", "Your app uses deprecated APIs or parameters for edge-to-edge"):
  - Target SDK 35+ → Android 15+ draws behind the system bars: UI inside `Screen.safeArea` (UI rule); check on an Android 15+ device with a cutout.
  - Deprecated calls (`Window.setStatusBarColor`, `setNavigationBarColor`…): open the warning in Play Console and read where they start. Unity's classes (`com.unity3d.player…`) → not project code; a newer patch of the same Unity line may drop them (an upgrade asks first; the warning doesn't block publishing). A plugin (ads, Firebase…) → update it. Own code → AndroidX insets.
- **Interstitial placement** (studio rule since 2026-10-14, after Play's Ads policy, Help 9857753: it bans unexpected full-screen ads, e.g. after a tap before the tap's action happens or at a level's start, and names the spot after a game's score screen as one that interrupts nothing):
  - Never between a tap and where it leads (Next/Continue/Retry → ad → level), never at level start.
  - On the result screen without waiting for a tap, ~0.5 s after the score count-up; the panel's buttons stay hidden until the ad closes, so no tap comes just before the ad or lands on it. No ad or no fill → buttons at once.

## Play Console work (Claude in Chrome)
Claude enters the values; the user keeps the payments profile and program terms:
1. **User:** create a payments profile if missing (bank and tax data; needed to define in-app products).
2. *Monetize with Play > Products > One-time products*: create a one-time product for each ID in the reward table, then add a **Play Games Reward** offer to each. To withdraw a reward, deactivate its offer.
3. *Play Games Services*: setup (section 1), achievements (name, description, icon), Game Stats event schema and stats ZIP.
4. Turn on Sidekick; the **user** enrolls in the Level Up program (program terms).
5. Releases as in *Direct release* (below); promotional content (section 8); recommended actions (section 9).

## Direct release (no testing; user decision 2026-10-09)
- Production track directly; no internal, closed or open testing tracks.
- Rollout 100% (no staged rollout); *Publishing overview > Managed publishing* off, so approved changes go live by themselves.
- **First release:** no managed publishing, so the app goes live once approved (launch day = approval day). Review takes hours to 7 days (longer for new accounts), counted from the last change sent; a change sent during review can push the app to the back of the queue (Help 9859654) → listing, all translations, graphics, in-app products and declarations before the first *Send for review*, then nothing until approval.
- PGS configuration and OAuth consent screen published, products and reward offers active, no tester lists.
- Claude prepares the release (version name, release notes in both languages, listing changes); the user uploads the AAB and sends it for review (release split).
- Trade-off: a 100% release can't be halted; a fix ships as a new version.
- Play Console demands a closed test before production (new personal developer accounts) → Google's rule: tell the user.

## Verification
- **EditMode tests** (on the grant class, with a fake store and a fake save):
  - The same order arriving twice grants the item once.
  - If saving fails, confirm isn't called.
  - An owned one-time item isn't granted again, but its order is confirmed.
  - The consumable reward's amount is added correctly.
- **Before release** (no testing track): the release build made on this computer runs on a device: it starts, PGS sign-in works (upload-key credential), nothing crashes.
- **On the live version** (manual tests, a license test account): to try the out-of-app flow, create a promo code for the product in Play Console and redeem it in the Play Store. The reward must arrive at startup and when returning from the background, and must not arrive a second time after restarting the game. Unlocked achievements and Game Stats must show in the Play Games profile. The reward offer itself can be tried only after it is created in Play Console.
