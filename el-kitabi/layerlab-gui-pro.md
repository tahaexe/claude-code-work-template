---
title: Layer Lab GUI Pro packs in a uGUI game (Casual Game, Survival Clean, Fantasy RPG)
condition: "Unity project that uses or is about to use one of the studio's Layer Lab GUI Pro packs. Signs: a folder under Assets whose name contains \"Layer Lab\" or \"GUI Pro\"; or the plan/memory says the game's UI is being replaced or polished with GUI Pro."
read_when: Auditing or replacing a game's UI with GUI Pro; choosing the pack and the demo prefab for a screen; importing parts of a pack; fonts and Turkish glyphs; sizing buttons and touch areas; safe-area work.
requires: — (the packs are in the studio's Asset Store account; download them in the editor via Package Manager › My Assets › "GUI Pro", without importing; they land in the Asset Store cache and each project imports from there)
source: Layer Lab pack pages (itch.io https://layerlab.itch.io/gui-pro-casual-game · Fab listing) · uGUI changelog https://docs.unity3d.com/Packages/com.unity.ugui@2.6/changelog/CHANGELOG.html (SafeArea 2.6.0 2026-03-30 ships with Unity 6000.6, RaycastReceiver 2.5.0 2026-02-27 ships with Unity 6000.5; verified 2026-10-14, corrected 2026-10-18: the studio is on 6000.3 with uGUI 2.0, unity-uzmani review) · the studio's UI market review 2026-10-18 (screen → demo prefab map, icons, font check) · platform touch-target guidance (Android 48 dp, iOS 44 pt)
tech: Unity 6000.3 (uGUI 2.0, every studio project); notes for 6000.5/6000.6 (uGUI 2.5/2.6) marked; uGUI (Canvas), not UI Toolkit
added: 2026-10-14 · research by a project session, reviewed by the session manager; owner's note: "these are good UI packs, use them" · 2026-10-18 (template 1.52): 6000.3 touch and safe-area corrections, which pack and which part, font traps (the studio's UI market research)
---
# Layer Lab GUI Pro packs in a uGUI game

## What the packs are
- The studio owns three packs: **Casual Game** (bright casual mobile UI), **Survival Clean** (survival/zombie, clean), **Fantasy RPG**. Pick the one that fits the game's identity. Never use them on pixel-art games.
- PNG sprites only: no PSD/SVG, no code, no animation. Casual Game has 1,200+ PNGs (pictograms, item icons) from 32 to 512 px.
- 9-slice borders are mostly ours to set; white parts are meant to be tinted in the game, effect parts come pre-coloured.
- Names moved between pack versions (e.g. pictograms renamed in 2.0.1). Note the imported pack version in the project memory; recheck names before updating the pack.

## Import only what a screen uses
- Import with a selection (`AssetDatabase.ImportPackage` with the chosen paths, headless is fine), never the whole pack: the packs are 134-159 MB, an APK must carry only the used sprites.
- One Sprite Atlas per game for these sprites; ASTC on mobile; mipmaps off for UI sprites (UI is the exception to a "mipmaps on" 3D texture rule).
- Set 9-slice borders in the importer (`TextureImporter.spriteBorder`) or the Sprite Editor; tint white parts with the game's palette.
- License: Asset Store standard EULA, used inside our games. Our repos are private; never push raw pack files to a public repo or site.

## Which pack, which part
- Packs per game (the studio's choice, 2026-10-14): Casual Game for casual puzzle games (with Fantasy RPG parts where they fit; white parts tinted to the palette); Survival Clean for survival and sci-fi games; none for pixel art. One pack's panel style per screen; tint white parts to the game palette.
- Demo screens are landscape (2560x1440 / 1920x1080): portrait games rebuild them from the components; centred popups carry over.
- Screen → demo prefab (Casual / Survival / Fantasy): home `Lobby` / `Lobby_Main` / `Home`; level select `Stage_Select_Type1/2` / `Play_Map` / `StageSelect`; HUD `Play_Type1/2` / `Play_Type_1` / `PlayType1`; pause `Play_Pause` (all three); lose `Play_Continue` / `Play_Explore_Result_Fail` / `PlayContinue`; win `Play_Result` / `Play_Result_Victory` / `PlayResult`; shop `Shop` / `Shop_01..04` / `Shop_Gem/Gold/Chest`; no ads `Ad_Remove` / `AD_Remove` / `ADRemove`; reward `Popup_RewardGet`, daily `Popup_RewardWeek/Month` / `Reward_Week/Month` / `RewardDaily`; settings `Popup_Setting` / `Setting` / `Settings`; tutorial `Tutorial_Hand`, `Tutorial_Character` / `Lobby_Tutorial_Focus` / `CharacterTutorialChat`; toast `ToastMessage_Topbar`. Each has a same-named image under `Preview/` in the package.
- Icons: video = `Pictoicon_Movie` (clapperboard with play; `Pictoicon_Video` is a desktop monitor); +1 life = `Pictoicon_Life_Add`; sad = `Pictoicon_Emoji_Sad`.
- Don't ship from the demos: `Rate` (custom 5-star prompt: App Review 5.6.1 allows only the system prompt; store-listing-optimization.md), login, guest, clan, chat or user-ID rows without accounts (with accounts: in-app deletion, 5.1.1(v)), push toggles without notifications, typed demo prices, paid roulettes or chests (odds before purchase, 3.1.1).

## Fonts
- **GUI Pro fonts lack Turkish** (measured 2026-10-18: all 37 font assets are static without source fonts; none has ğ Ğ ı İ ş Ş, the plain "SDF" ones also lack ç ö ü). Use a rounded font that has Turkish glyphs (e.g. an OFL Lilita One build) or build a static Turkish SDF from the OFL TTF (atlas ranges 20-7E, A0-FF, 100-17F) and list it in the label font's own fallbacks.
- Bitmap "Outline N Bitmap" fonts blur when scaled; use them only at their size or prefer SDF with an outline material.

## Touch targets and safe area
- Touch targets at least **48 dp** on every profile (Android's 48 dp, stricter than Apple's 44 pt) with ≥ 8 dp gaps (arayuz-kalitesi.md). Enlarge the hit area, not the art. Every studio project is on Unity 6000.3 (uGUI 2.0), so:
  - a negative Raycast Padding on the art's Image (no code; GraphicRaycaster honours it), or
  - a non-drawing Graphic (Project F's `RaycastTarget`: `OnPopulateMesh` → `vh.Clear()`); a transparent Image also works but draws unless `cullTransparentMesh` is on.
  - uGUI's `RaycastReceiver` (an invisible interactable area) needs uGUI 2.5 / Unity 6000.5: not available to us yet.
- Safe area: 6000.3 projects keep their own safe-area code, reading one screen provider instead of `Screen.safeArea` directly (the UI tests inject device profiles through it; arayuz-test-duzenegi.md). uGUI 2.6 / Unity 6000.6 brings an official **SafeArea** component (per-edge choice, recalculates on resolution, orientation or safe-area change); if a project moves to 6000.6: it resets offsets and conflicts with a Layout Group or Content Size Fitter on the same or a parent object (put those on a child), and its anchors must not be animated.

## Process (owner's rule: the manager decides)
1. Screenshot every screen: main menu, level select, in-game HUD, pause, win/lose, shop and reward popups, settings.
2. Mark the weak ones: flat boxes, mismatched buttons, unreadable text, empty popups. Revenue and store-screenshot screens come first.
3. Prepare before/after for each, with the parts list and the APK size change (MB), in one file for the manager. Apply after approval.
4. Keep the game's fonts and identity (studio font decisions stay).
