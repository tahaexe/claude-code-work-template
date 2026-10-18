---
paths:
  - "Assets/**/UI/**"
  - "**/*.uxml"
  - "**/*.uss"
---
# Unity UI rules
<!-- unity add-on v1.54 · paths fitted to the project at install -->

- **Skills:** UI work → `unity:ui` (by the project's system `unity:ui-ugui` or `unity:ui-uitk`); text and fonts → `unity:optimize-text-mesh-pro`.
- **Quality bar:** before building or changing a player-facing screen read the handbook's `arayuz-kalitesi.md` and `arayuz-kurallari.md` (motion and haptics: `oyun-hissi.md`) when installed. Grey boxes, placeholders and bare Unity widgets never reach a store build.
- **Style guide:** follow `docs/ai/tasarim/gorsel-stil.md` (fonts and sizes, palette, spacing, UI language). Missing → before the next UI or visual work, draft it yourself from `docs/ai/sablonlar/oyun/gorsel-stil.md`, the game summary, existing design docs and decisions (`tasarim/`, `hafiza/`) and current visuals (Turkish); show it, apply the user's corrections (taste is theirs) and index it in `HAFIZA.md`. Then one finished-looking screen before content multiplies.
- **Visual check:** after a step that changes what the player sees, take one screenshot (one phone profile) into `Logs/claude/screens/` (handbook `unity-cli-saha-notlari.md` → Screenshots) and compare it with the style guide: fonts and sizes, palette, alignment and spacing, contrast and readability, safe area, Turkish characters (ğ ş ı İ). Fix clear deviations; matters of taste → manual tests. Keep the screenshots for the closure review.
- **UI system:** follow what the project uses. For new runtime UI consider UI Toolkit; uGUI for world space and where UI Toolkit falls short.
- **State ownership:** UI doesn't own game state or change it directly; it only displays and requests changes via events or commands (data binding / MVVM).
- **Text:** no user-visible text in code; it comes from the localization system (`unity:localization`).
- **Input:** every interactive element works with keyboard/mouse, gamepad and (on mobile) touch.
- **Animation:** skippable; respects the reduced-motion preference.
- **Audio:** UI sounds go through the audio event system, not played directly.
- **Flow:** UI never blocks the game loop; heavy work is async.
- **Accessibility:** plan scalable text and a color-blind mode from the start.
- **Performance:** pool items in long lists; in uGUI toggle visibility with a Canvas Group instead of enable/disable.
- **Check:** only in the pre-release test stage (`docs/ai/BAKIM.md`), the screen matrix of the handbook's `arayuz-kalitesi-testleri.md` (5 phone and tablet profiles, safe area, both languages) and the scores (`arayuz-kalitesi.md` §5); without the kit, the smallest and largest supported resolutions, safe area/notch and orientation. Feel on a device → manual tests.
