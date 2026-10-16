---
paths:
  - "**/*.unity"
  - "**/*.prefab"
  - "**/*.asset"
  - "**/*.meta"
  - "**/*.mat"
  - "**/*.controller"
  - "**/*.anim"
  - "Packages/manifest.json"
  - "ProjectSettings/**"
---
# Unity asset rules
<!-- unity add-on v1.33 · paths fitted to the project at install -->

- **No hand edits:** scenes, prefabs, ScriptableObject `.asset`, materials, animators and `.meta` files are YAML but never hand-edited. Change them through the editor via Unity CLI (`unity:unity-cli`). If the CLI can't reach the editor, ask the user before any hand edit.
- **`.meta` and GUID:** every asset's `.meta` is created, moved and committed with it. Move or rename assets through the editor so the GUID survives; never delete or regenerate a `.meta` (references break).
- **Scene structure:** split big scenes into small prefabs (nested prefabs, prefab variants); keep changes in the relevant prefab. Smaller diffs, fewer conflicts, less to read when verifying.
- **Packages:** adding one is your call (say why in one line); upgrading or removing one asks first unless the approved plan explicitly includes it (hard to reverse). Package work: `unity:unity-package-management`.
- **Project settings:** change `ProjectSettings/` via the editor or CLI and mention it in the commit message; don't change platform or build settings outside a plan.
- **Runtime loading:** prefer Addressables and `AssetReference`; `Resources.Load` only for small, always-needed content. Sprite atlases in 2D (`unity:manage-sprite-atlas`).
- **Visual changes** (lighting, materials, post-processing, scene look): after the step take a screenshot into `Logs/claude/screens/` (handbook `unity-cli-saha-notlari.md` → Screenshots) and compare it with `docs/ai/tasarim/gorsel-stil.md` (palette, light and mood, readability). Fix clear deviations; matters of taste → manual tests.
- **Import settings:** set texture, audio and model settings per target platform (e.g. texture compression on mobile, audio Load Type). Audio: `unity:optimize-audio`.
