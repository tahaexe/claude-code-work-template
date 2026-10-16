---
paths:
  - "Assets/**/UI/**"
  - "**/*.uxml"
  - "**/*.uss"
---
# Unity UI rules
<!-- unity add-on v1.35 · paths fitted to the project at install -->

- **Skills:** UI work → `unity:ui` (by the project's system `unity:ui-ugui` or `unity:ui-uitk`); text and fonts → `unity:optimize-text-mesh-pro`.
- **Style guide:** follow `docs/ai/tasarim/gorsel-stil.md` (fonts and sizes, palette, spacing, UI language). Missing → before the next UI or visual work, draft it yourself from `docs/ai/sablonlar/oyun/gorsel-stil.md`, the game summary, existing design docs and decisions (`tasarim/`, `hafiza/`) and current visuals (Turkish); show it, apply the user's corrections (taste is theirs) and index it in `HAFIZA.md`.
- **Visual check:** after a step that changes what the player sees, take a screenshot into `Logs/claude/screens/` (handbook `unity-cli-saha-notlari.md` → Screenshots) and compare it with the style guide: fonts and sizes, palette, alignment and spacing, contrast and readability, safe area, Turkish characters (ğ ş ı İ). Fix clear deviations; matters of taste → manual tests. Keep the screenshots for the closure review.
- **UI system:** follow what the project uses. For new runtime UI consider UI Toolkit; uGUI for world space and where UI Toolkit falls short.
- **State ownership:** UI doesn't own game state or change it directly; it only displays and requests changes via events or commands (data binding / MVVM).
- **Text:** no user-visible text in code; it comes from the localization system (`unity:localization`).
- **Input:** every interactive element works with keyboard/mouse, gamepad and (on mobile) touch.
- **Animation:** skippable; respects the reduced-motion preference.
- **Audio:** UI sounds go through the audio event system, not played directly.
- **Flow:** UI never blocks the game loop; heavy work is async.
- **Accessibility:** plan scalable text and a color-blind mode from the start.
- **Performance:** pool items in long lists; in uGUI toggle visibility with a Canvas Group instead of enable/disable.
- **Check:** try screens at the smallest and largest supported resolutions, and on mobile with safe area/notch and orientation → manual tests.
