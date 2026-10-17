---
title: Unity project settings baseline (Unity 6.3; Android, iOS, PC)
condition: Unity project.
read_when: Setting up a new project; adding a target platform; release prep; frame rate (incl. 90 Hz phones), memory, size or build problems; a project settings question; the settings audit plan; writing `.gitattributes`, or a baked asset (NavMesh, lighting, terrain) differs between machines.
requires: — (Project Auditor, package `com.unity.project-auditor` with `com.unity.project-auditor-rules` on Unity 6.0–6.3, built in from 6.4; added inside the audit plan)
plan_candidates:
  - "Unity settings audit: Project Auditor and the baseline per platform, one area per step, exceptions recorded · el-kitabi/unity-proje-ayarlari.md"
source: Unity Manual 6.3 LTS (Android and iOS Player settings, Android application entries, Project Auditor, Application.targetFrameRate, Import assets simultaneously) · Unity "Optimize your game performance for mobile, XR, and the web (Unity 6 edition)" · Unity issue tracker UUM-68029, UUM-34028 · git's gitattributes docs (`eol` sets `text`) · Gradle docs "Configuring Gradle" (`org.gradle.jvmargs`) · Project A's git notes of 2026-10-16 (binary `.asset` files) · Project C's settings audit (2026-10-16, Project Auditor 3.1.1 with rules 2.0.0; its `hafiza/proje-ayarlari.md`) · Unity support 'How do I remove the Splash Screen from my build?' (2025-10-20) · Unity Manual 6.3 `Application.targetFrameRate`, `PlayerSettings.stripUnusedMeshComponents` and Android Developers 'Optimize refresh rates' (2026-02-26), re-read 2026-10-17; a project session's 90 Hz research (2026-10-17)
tech: Unity 6.3 LTS · URP
added: 2026-10-09 · compiled by Claude from Unity docs · 2026-10-16 (1.49): Asset Pipeline line, binary `.asset` lines and audit (Project A's finding; the audit re-run in scratch repos, its match narrowed to skip `text=auto`), To measure · 2026-10-17 (1.51): splash, iOS accelerometer and Metal validation, editor quality level, URP features, Optimize Mesh Data (Project C's audit), 90 Hz rounding, frame pacing on emulators, build memory moved out
---
# Unity project settings baseline

## How to use
- **New project:** apply this right after creation (`KURULUM-UNITY.md` → New project).
- **Existing project:** the audit plan (plan candidate). First Project Auditor (*Window > Analysis > Project Auditor*; its Project Settings view lists setting issues with the reason and sometimes an automatic fix), then the tables below for the project's target platforms.
- The project's recorded decisions (`hafiza/kararlar.md`) outrank this baseline; a deliberate difference gets one line there with its reason. Plan candidate exemption: an audit is already recorded there.
- Change settings through the editor via Unity CLI: `PlayerSettings`, `QualitySettings`, `EditorSettings`, `Physics` in an eval; a setting without an API → `SerializedObject` on its `ProjectSettings/*.asset` (handbook `unity-cli-saha-notlari.md`). Never hand-edit `ProjectSettings/`.
- One area per plan step; verify with compile and tests, plus a device, FPS or screenshot check where speed or the look changes.
- **A plan of their own** (old projects): Gamma → Linear (the look changes: before/after screenshots, taste is the user's), Input Manager → Input System (code migration, game code rule), Mono → IL2CPP (build time, plugin check).

## Version control and editor
- *Editor*: Asset Serialization **Force Text**, Version Control **Visible Meta Files** (Unity's defaults; git can diff and merge only text).
- *Editor › Asset Pipeline*: Parallel Import and the import worker count stay at their defaults (parallel import is faster for big imports and first opens); small headless jobs lower the count per launch (`unity-cli-saha-notlari.md` › Headless editor).
- **`.gitattributes` and binary `.asset` files:** Unity writes some `.asset` files in binary even under Force Text (Project A: baked NavMesh, LightingData, terrain data). A text rule that matches them (`*.asset text eol=lf`; `eol=` alone implies `text`) strips their CR LF byte pairs on every commit, so every other checkout gets a broken bake (Project A 2026-10-16: NavMesh 476,964 bytes on disk, 476,962 in git). Keep the text rule for YAML assets and add after it (the later line wins):
  - `Assets/**/NavMesh*.asset binary` (only under `Assets/`: `ProjectSettings/NavMeshAreas.asset` is YAML) · `**/LightingData.asset binary` · `**/Terrains/Terrain.asset binary` (Project A's terrain path; fit it to the project's TerrainData files).
  - Audit, prints nothing when safe: `git ls-files --eol | awk '$1=="i/-text" && $3=="attr/text"'` (binary content under a text rule; the looser `$3 ~ /attr\/text/` also lists files under `text=auto`, which git leaves unconverted). One file: `git hash-object <file>` equals the hash in `git ls-files -s <file>`.
  - Already committed under the text rule: fix the rule, then `git add --renormalize <file>` on the machine that baked it (its disk copy is intact) or rebake, and commit.

## Player: all platforms
| Setting | Value | Why |
|---|---|---|
| Scripting Backend | IL2CPP | Speed; Android ARM64 and iOS need it |
| C++ Compiler Configuration | Master for store builds, Release while iterating | Unity's recommendation for shipping builds |
| Managed Stripping Level | Low; Medium only with a `link.xml` and a device check | Higher levels strip code reached by reflection |
| Use incremental GC | On | Spreads garbage collection over frames: fewer spikes |
| Show Splash Screen (*Splash Image*) | Off | Unity 6 lets every plan turn it off, Personal too; it only lengthens a cold start. Studio rule (2026-10-16): a studio logo, if any, only on the game's own loading screen, never an extra wait |
| Color Space | Linear | Correct lighting with URP; Gamma only for a deliberate look |
| Active Input Handling | Input System Package (New) | "Both" isn't supported on Android |
| Version | `bundleVersion` plus version code / build number raised for every store build | Stores reject a repeated number (release split) |

## Android
- Target Architectures **ARM64** (Play needs 64-bit; ARMv7 only for a deliberate old-device audience).
- Target API: the highest installed; Minimum API: Unity's lowest unless a plugin needs more.
- Application Entry Point **GameActivity** (Unity 6's default for new projects); keep Activity in old projects whose plug-ins need Java-thread execution.
- Auto Graphics API on, or a manual list in the same order (Unity 6.3's template): Vulkan first, GLES3 fallback (Google Play entry: Vulkan primary).
- Texture compression **ASTC**.
- Minify **Release** on (R8), Debug off; narrow keep rules (Google Play entry, section 9).
- Optimized Frame Pacing: decide on a device at the shipping frame cap, on vs off. It snaps a target to a divisor of the refresh rate (UUM-68029) and adds a library (UUM-34028). On an x86_64 emulator the ARM64 release build crashed in Swappy at launch with it on (two projects): emulator smoke tests use a variant with it off (`unity-derleme-ve-bellek.md`), the store build keeps the device's decision.
- Resizeable Activity on (large screens, Google Play entry section 7). UI inside `Screen.safeArea`; *Render outside safe area* has no effect on Android 15+, which is always edge-to-edge.
- Split Application Binary (Play Asset Delivery) once the build passes Play's size limit.

## iOS
- ARM64 only, IL2CPP, Metal.
- Target minimum iOS version: Unity's lowest unless a needed API asks for more.
- Usage descriptions (camera, microphone, location) only for sensors the game uses, each saying why; Requires Persistent WiFi off unless the game is online-only.
- Accelerometer Frequency **Disabled** unless the game reads the accelerometer (template projects sample it at 60 Hz for nothing); Metal API Validation off (it only serves debugging from Xcode). Project Auditor flags both (Project C's audit, 2026-10-16).

## PC (Windows, Steam)
- x86_64; IL2CPP (Mono only if a plug-in needs it); Graphics API automatic (DX12/DX11).
- Fullscreen Window by default; resolution, quality and vSync in the game's settings menu.
- Run In Background on (overlays, alt-tab).

## Frame rate and quality
- Mobile: `Application.targetFrameRate = 60` at startup; vSync count has no effect on Android and iOS, and the default -1 runs a fixed 30 FPS there (a game without the line ships at 30). PC: vSync per quality level, or a frame cap.
- **90 Hz Android phones (risk, measure first):** Unity rounds a target down to a divisor of the *current* refresh rate (6.3 manual), so 60 runs at 45 on a 90 Hz panel (48 on 144 Hz); 60 and 120 Hz panels and iOS (ProMotion off = 60 Hz) are unaffected, and Android 15+ already runs games at 60 Hz unless they ask for more. Unity has no Android call to pick the display mode. Check on a 90 Hz phone on Android 14 or older (Developer options › Show refresh rate; high refresh rate on, no battery saver, not charging), with Optimized Frame Pacing on and off; a fix (asking Android for a 60 Hz mode through the window's `preferredDisplayModeId`, API 23+) enters a game only after that test.
- The editor draws with the quality level the project last selected: template projects open on the PC level (`m_CurrentQuality: 1`, `PC_RPAsset`), so a mobile game makes its mobile level the editor's, or editor captures don't show the phone's look (Project C, Project D 2026-10-16).
- Few quality levels: mobile 2 (Low, High), PC 3 (Low, Medium, High); set the default level per platform.
- Each level has its own URP asset: render scale, HDR (off on low mobile), MSAA (off or 2x on mobile), shadow distance and resolution, per-object light limit.
- URP Global Settings: strip unused shader variants (post-processing, debug); keep *Always Included Shaders* short. Dynamic Batching has no effect under URP.
- The mobile URP asset's unused *Supports* features off (terrain holes, light layers, LOD cross-fade, lens flares, probe blending, box projection): fewer shader variants; a look that needs one turns it back on. The default render pipeline asset needs no change when every quality level of the platform overrides it.
- Adaptive Performance (thermal state on mobile) only by plan, when long sessions heat the device.

## Physics and time
- Auto Sync Transforms off; Reuse Collision Callbacks on; layer collision matrix trimmed to the pairs that really collide.
- Fixed Timestep 0.02 unless the game's physics needs a finer step.

## Assets and size
- Textures: max size per platform, ASTC on Android, no mipmaps for UI; sprite atlases (`unity:manage-sprite-atlas`).
- Audio import: `unity:optimize-audio`; text: `unity:optimize-text-mesh-pro`.
- Strip Engine Code on; Addressables for large content.
- Optimize Mesh Data strips vertex data that no shader in the build uses: keep it off when meshes or materials are built or swapped at run time (Project C's board from ScriptableObject meshes with material copies; Unity's own caution: a shader switched at run time misses stripped tangents).

## To measure (not yet rules)
- IL2CPP: a build's peak memory and time with C++ Compiler Configuration Release vs Master on a development or check build (the table keeps Master for store builds only).
- Android build memory: measured (a project, 2026-10-16) → `unity-derleme-ve-bellek.md`: the peak is the IL2CPP phase, not Gradle; Gradle keeps Unity's heap (Maximum JVM heap size, 4096 MB).

## Verification
- Project Auditor's issue counts before and after the plan; it can run by an eval in the open editor (Project C `docs/ai/araclar/denetim.py run|compare`, ~90-110 s a full run; Project A `tools/auditor`).
- On a device: startup time, FPS at the cap, memory; screenshots where the look changed. Device and feel checks → manual tests.
