---
title: Unity project settings baseline (Unity 6.3; Android, iOS, PC)
condition: Unity project.
read_when: Setting up a new project; adding a target platform; release prep; frame rate, memory, size or build problems; a project settings question; the settings audit plan; writing `.gitattributes`, or a baked asset (NavMesh, lighting, terrain) differs between machines.
requires: — (Project Auditor, package `com.unity.project-auditor` with `com.unity.project-auditor-rules` on Unity 6.0–6.3, built in from 6.4; added inside the audit plan)
plan_candidates:
  - "Unity settings audit: Project Auditor and the baseline per platform, one area per step, exceptions recorded · el-kitabi/unity-proje-ayarlari.md"
source: Unity Manual 6.3 LTS (Android and iOS Player settings, Android application entries, Project Auditor, Application.targetFrameRate, Import assets simultaneously) · Unity "Optimize your game performance for mobile, XR, and the web (Unity 6 edition)" · Unity issue tracker UUM-68029, UUM-34028 · git's gitattributes docs (`eol` sets `text`) · Gradle docs "Configuring Gradle" (`org.gradle.jvmargs`) · Project A's git notes of 2026-10-16 (binary `.asset` files)
tech: Unity 6.3 LTS · URP
added: 2026-10-09 · compiled by Claude from Unity docs · 2026-10-16 (1.49): Asset Pipeline line, binary `.asset` lines and audit (Project A's finding; the audit re-run in scratch repos, its match narrowed to skip `text=auto`), To measure
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
| Color Space | Linear | Correct lighting with URP; Gamma only for a deliberate look |
| Active Input Handling | Input System Package (New) | "Both" isn't supported on Android |
| Version | `bundleVersion` plus version code / build number raised for every store build | Stores reject a repeated number (release split) |

## Android
- Target Architectures **ARM64** (Play needs 64-bit; ARMv7 only for a deliberate old-device audience).
- Target API: the highest installed; Minimum API: Unity's lowest unless a plugin needs more.
- Application Entry Point **GameActivity** (Unity 6's default for new projects); keep Activity in old projects whose plug-ins need Java-thread execution.
- Auto Graphics API on: Vulkan first, GLES3 fallback (Google Play entry: Vulkan primary).
- Texture compression **ASTC**.
- Minify **Release** on (R8), Debug off; narrow keep rules (Google Play entry, section 9).
- Optimized Frame Pacing: decide on a device at the shipping frame cap, on vs off. It snaps a target to a divisor of the refresh rate (UUM-68029) and adds a library (UUM-34028).
- Resizeable Activity on (large screens, Google Play entry section 7). UI inside `Screen.safeArea`; *Render outside safe area* has no effect on Android 15+, which is always edge-to-edge.
- Split Application Binary (Play Asset Delivery) once the build passes Play's size limit.

## iOS
- ARM64 only, IL2CPP, Metal.
- Target minimum iOS version: Unity's lowest unless a needed API asks for more.
- Usage descriptions (camera, microphone, location) only for sensors the game uses, each saying why; Requires Persistent WiFi off unless the game is online-only.

## PC (Windows, Steam)
- x86_64; IL2CPP (Mono only if a plug-in needs it); Graphics API automatic (DX12/DX11).
- Fullscreen Window by default; resolution, quality and vSync in the game's settings menu.
- Run In Background on (overlays, alt-tab).

## Frame rate and quality
- Mobile: `Application.targetFrameRate = 60` at startup; vSync count has no effect on Android and iOS. PC: vSync per quality level, or a frame cap.
- Few quality levels: mobile 2 (Low, High), PC 3 (Low, Medium, High); set the default level per platform.
- Each level has its own URP asset: render scale, HDR (off on low mobile), MSAA (off or 2x on mobile), shadow distance and resolution, per-object light limit.
- URP Global Settings: strip unused shader variants (post-processing, debug); keep *Always Included Shaders* short. Dynamic Batching has no effect under URP.
- Adaptive Performance (thermal state on mobile) only by plan, when long sessions heat the device.

## Physics and time
- Auto Sync Transforms off; Reuse Collision Callbacks on; layer collision matrix trimmed to the pairs that really collide.
- Fixed Timestep 0.02 unless the game's physics needs a finer step.

## Assets and size
- Textures: max size per platform, ASTC on Android, no mipmaps for UI; sprite atlases (`unity:manage-sprite-atlas`).
- Audio import: `unity:optimize-audio`; text: `unity:optimize-text-mesh-pro`.
- Strip Engine Code on; Addressables for large content.

## To measure (not yet rules)
- IL2CPP: a build's peak memory and time with C++ Compiler Configuration Release vs Master on a development or check build (the table keeps Master for store builds only).
- Android Gradle: the build JVM's heap (`org.gradle.jvmargs` in the generated `gradle.properties`; Gradle's own default is `-Xmx512m -XX:MaxMetaspaceSize=384m`, Unity's template value unchecked): measure a build's peak before setting it.

## Verification
- Project Auditor's issue counts before and after the plan.
- On a device: startup time, FPS at the cap, memory; screenshots where the look changed. Device and feel checks → manual tests.
