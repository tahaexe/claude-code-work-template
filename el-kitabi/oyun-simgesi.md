---
title: "Game icon: what reads and converts, store files, the build's icon, tests, seasonal and alternate icons"
condition: "Game or app that ships on Google Play or the App Store. Signs: Android or iOS among the targets in the game summary or memory."
read_when: "Making or changing the app icon; choosing between icon candidates; checking a store build's icon before release; planning an icon test (Play experiment, App Store PPO), alternate icons or a seasonal icon."
requires: "—"
source: "Google Play icon design specifications (developer.android.com, updated 2026-06-15) · Apple HIG 'App icons' (change log 2025-06-09, 2026-06-08) · Apple: product page optimization page, App Store Connect Help › Configure test treatments, Xcode 'Configuring your app to use alternate app icons' (Xcode 26, iOS 18+), forum threads 734491 and 787804 (icon tab) · SplitMetrics ASO Benchmarks 2024 via PocketGamer.biz 2024-08-22 (vendor figures, method not public) · AppFollow 2026 (A/B testing for mobile games) · ASOMobile 2025 (visual ASO) · seasonal cases: SplitMetrics MyTona (vendor), Gummicube, AppFollow · studio: a yarn game's icon review against 6 rivals at 60 px (2026-10-18), Project M 1.0's default-icon slip (2026-10-17)"
tech: "Google Play, App Store; Unity Player Settings icons and an iOS post-process build step"
added: "2026-10-18 · template 1.53 · the studio's icon, seasonal-touch and iOS alternate-icon research for the session manager"
---
# Game icon

## What reads and converts
- One subject from the game's own render (studio: no AI images in store art), its face or silhouette readable; a plain ground in a colour the subject stands out on (an orange toy on orange vanishes); no text; the subject fills ~80-95% of the square but stays inside the masks (Play rounds 30%, iOS a rounded square). The 6 leading yarn-sort games all show one bright object and no text (studio review, 2026-10-18).
- Outlines read, shapes don't: a cat's eared silhouette survives small sizes, an egg shape doesn't, and a flat cylinder cut by the edge stops reading as a spool. Eyes need size and a highlight to read (sevimli-stilize-gorunum.md).
- Judge every candidate at 60 and 48 px, on a light and a dark ground, beside the genre leaders' icons. If two candidates need a second look to tell apart, a store test will end in a draw (AppFollow 2026).
- Evidence (vendor figures, direction only, not re-verified): an optimised icon brought up to +25% users and a plain ground +26% over a cluttered one (SplitMetrics 2024: ~200 apps, 3,500+ tests); for games the icon is the highest-leverage asset to test, a concept change (another character or action) typically moving 5-10% and a palette change 4-8% (AppFollow 2026). Only ~25% of developers put text in icons (ASOMobile 2025).

## Store files
- **Google Play store icon:** 512×512, 32-bit PNG, sRGB, ≤ 1024 KB, full square: Play applies the mask (corner radius 30% of the size) and its own shadow, so no shadow or rounded corners in the file; no ranking, deal or Play-program text or graphics, nothing misleading; an opaque brand ground (transparent areas show Play's UI colour).
- **Android launcher icon:** separate from the store icon; adaptive layers (foreground and background) from a wider render of the same view, the subject centred.
- **App Store:** 1024×1024 px. Apple's HIG (change log 2025-06-09 and 2026-06-08) recommends a layered icon and still accepts a flat opaque image; layers are delivered square and the system rounds the corners; appearances default, dark, clear and tinted (check that the subject reads in each); text only when essential, never words like "Play" or "New".

## The build's icon (before every store build)
- No build check (AAB checks, R8, 16 KB) looks at the icon: with no icon set in Player Settings, Unity's default icon silently ships (Project M 1.0, 2026-10-17). Look at the AAB's `base/res/mipmap-xxxhdpi-v4/app_icon.png` and the Xcode project's AppIcon set by eye (release checklist).

## Tests, alternate and seasonal icons
- Store tests: Play store listing experiments and App Store product page optimization (store-listing-optimization.md › Experiments: size the test first; little traffic ends in a draw, so test the biggest difference first).
- **App Store icon test:** every tested icon must be in the binary of the live version, so the test starts only after the version carrying the candidates is out; treatments go through App Review. Unity has no setting for alternate icons; in the iOS post-process build step:
  - one `.appiconset` per candidate in `Images.xcassets` (a single 1024 universal image);
  - `PBXProject.SetBuildProperty`: `ASSETCATALOG_COMPILER_ALTERNATE_APPICON_NAMES` (Xcode then writes `CFBundleAlternateIcons`; never edit those Info.plist keys by hand) and `ASSETCATALOG_COMPILER_INCLUDE_ALL_APPICON_ASSETS = YES` (in Xcode's Build Settings Reference, not in the alternate-icon article; forum reports: without it the icon tab may not appear in App Store Connect; some needed Apple support even with it);
  - verify the two settings in the exported `project.pbxproj` and the sets in `Images.xcassets`, then `CFBundleAlternateIcons` in the archived `Info.plist`; each 1024 icon adds a few hundred KB. Third-party helpers exist (`AppIconChangerUnity`); our own step is enough.
- **Seasonal icon:** on Play the store icon changes without a release (the listing change is still reviewed); the App Store icon comes from the binary (one release to add it, one to remove it, or a PPO treatment shown to a share of traffic for up to 90 days). Changing the icon from inside the app (`setAlternateIconName`) shows a system alert every time: not for a silent seasonal swap. Evidence is thin: a pumpkin-headed icon converted ~9% better in one hidden-object game (SplitMetrics case, vendor, not re-verified), other tests favoured unthemed art (AppFollow): test it, don't keep it blind, and only on a strong base icon. Store-side timing for seasons: store-events.md.
