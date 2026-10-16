---
title: Ambient sound (2D) and 3D spatial audio in Unity
condition: Unity project (ProjectSettings/ProjectVersion.txt exists). Not specific to Synty.
read_when: Adding ambient sound to a scene or 3D sound to an object; sound is silent or its position feels wrong.
requires: —
source: '"Unity 6 Audio Tutorial: Ambient Sound & 3D Spatial Audio" · Synty Studios · https://www.youtube.com/watch?v=FOewaiJeM2k · about 3.5 min · publish date unknown'
tech: Unity 6; pipeline-independent
added: 2026-09-28 · Gemini video analysis (technical steps and visual layout merged), reviewed by Claude · timestamps approximate · 2026-10-01 translated to English
---
# Ambient sound and 3D spatial audio in Unity

## Summary
Two kinds of sound: **2D ambient sound** heard the same everywhere (`Spatial Blend` = 0) and **3D spatial sound** that changes with distance and direction from its source (`Spatial Blend` = 1). Official skills for deeper work: import and memory → `unity:optimize-audio`, mixer routing → `unity:audio-setup-mixers`.

## Know first: pitfalls
- **No sound at all:** no `Audio Listener` on the camera, or `Mute Audio` on in the Game window (~01:30). The scene needs exactly **one** `Audio Listener`.
- **Stereo 3D sound:** without `Force To Mono` on a clip used in 3D, position perception blurs and memory doubles (~00:40). 2D ambient sounds can stay stereo.
- **Rolloff choice:** `Linear` drops the sound to exactly zero at `Max Distance`, so the radius is predictable. `Logarithmic` is more realistic but stays faintly audible far away. Small, local sources: `Linear` + a small `Max Distance` (5 in the video) (~02:10).

## Steps (timestamps approximate)
1. **Listener (~00:15):** `Main Camera` → `Add Component > Audio > Audio Listener` (if missing).
2. **3D clips (~00:40):** select the sound files for 3D use → Inspector → `Force To Mono` → `Apply`.
3. **2D ambient sound (~01:10):** `Hierarchy` → `+ > Audio > Audio Source` (e.g. named `Ambience`) → assign the clip → `Play On Awake` and `Loop` on → `Spatial Blend` = 0.
4. **3D sound (~01:50):** add an `Audio Source` to the object making the sound (e.g. a fire barrel) → assign the clip → `Loop` on → `Spatial Blend` = 1 → `3D Sound Settings` → `Volume Rolloff` = `Linear`, lower `Max Distance`.
5. **Shortcut (~02:40):** dragging a clip from Project onto a scene object adds the `Audio Source` automatically; then set it as in step 4.

## Recommended layout
- **Hierarchy:** `Main Camera` (Audio Listener) · `Ambience` (2D Audio Source) · 3D sources on the object making the sound (not on a separate empty object).
- **Folders:** `Assets/Audio/Ambience/` (stereo, 2D) and `Assets/Audio/3D/` (mono). The split lets the mono setting be automated (below).
- **Gizmo:** a selected 3D source draws two spheres in Scene: inner `Min Distance` (full volume), outer `Max Distance` (zero with Linear). A 2D source draws none.

## Verification
- In Play mode the sound grows near the source and cuts off beyond `Max Distance`; it pans left and right as the camera turns.
- Ambient sound is at the same level everywhere. These listening checks go to manual tests.

## Automation notes for Claude
- **Automatic mono:** an `AssetPostprocessor` with `OnPreprocessAudio` sets `((AudioImporter)assetImporter).forceToMono = true` when the path starts with `Assets/Audio/3D/`.
- **Source settings:** set `AudioSource` fields (`spatialBlend`, `rolloffMode = AudioRolloffMode.Linear`, `minDistance`, `maxDistance`, `loop`, `playOnAwake`) with editor code via Unity CLI; never hand-edit the scene file (unity-varliklar rule).
- **Listener check:** the scene must have exactly 1 `AudioListener`; add or remove it with editor code.

## Notes
- The video's scene was built with the POLYGON Gang Warfare pack and freesound.org sounds; the technique itself doesn't depend on the pack.
