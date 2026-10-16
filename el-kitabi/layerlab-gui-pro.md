---
title: Layer Lab GUI Pro packs in a uGUI game (Casual Game, Survival Clean, Fantasy RPG)
condition: "Unity project that uses or is about to use one of the studio's Layer Lab GUI Pro packs. Signs: a folder under Assets whose name contains \"Layer Lab\" or \"GUI Pro\"; or the plan/memory says the game's UI is being replaced or polished with GUI Pro."
read_when: Auditing or replacing a game's UI with GUI Pro; importing parts of a pack; sizing buttons and touch areas; safe-area work on Unity 6000.6.
requires: — (the packs are in the studio's Asset Store account; download them in the editor via Package Manager › My Assets › "GUI Pro", without importing; they land in the Asset Store cache and each project imports from there)
source: Layer Lab pack pages (itch.io https://layerlab.itch.io/gui-pro-casual-game · Fab listing) · uGUI changelog https://docs.unity3d.com/Packages/com.unity.ugui@2.6/changelog/CHANGELOG.html (SafeArea 2.6.0 2026-03-30, RaycastReceiver 2.5.0 2026-02-27, uGUI 2.6 ships with Unity 6000.6; verified 2026-10-14) · platform touch-target guidance (Android 48 dp, iOS 44 pt)
tech: Unity 6000.3 (uGUI 2.x) and 6000.6 (uGUI 2.6); uGUI (Canvas), not UI Toolkit
added: 2026-10-14 · research by a project session, reviewed by the session manager; owner's note: "these are good UI packs, use them"
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

## Touch targets and safe area
- Touch targets at least **48 dp (Android) / 44 pt (iOS)** with ~8 dp gaps. Enlarge the hit area, not the art:
  - Unity 6000.6 (uGUI 2.5+): `RaycastReceiver`, an invisible interactable area.
  - Unity 6000.3: a transparent Image with Raycast Target on.
- Unity 6000.6 (uGUI 2.6) has an official **SafeArea** component (per-edge choice, recalculates on resolution, orientation or safe-area change). It resets offsets, and it conflicts with a Layout Group or Content Size Fitter on the same or a parent object: put those on a child. Don't animate its anchors. 6000.3 projects keep their own safe-area code.

## Process (owner's rule: the manager decides)
1. Screenshot every screen: main menu, level select, in-game HUD, pause, win/lose, shop and reward popups, settings.
2. Mark the weak ones: flat boxes, mismatched buttons, unreadable text, empty popups. Revenue and store-screenshot screens come first.
3. Prepare before/after for each, with the parts list and the APK size change (MB), in one file for the manager. Apply after approval.
4. Keep the game's fonts and identity (studio font decisions stay).
