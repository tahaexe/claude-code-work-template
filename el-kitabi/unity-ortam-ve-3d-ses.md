---
title: "Sound in Unity: ambient (2D) and 3D spatial audio, the mobile mix and audio session, buying music"
condition: Unity project (ProjectSettings/ProjectVersion.txt exists). Not specific to Synty.
read_when: "Adding ambient sound to a scene or 3D sound to an object; sound is silent or its position feels wrong; measuring a mobile game's loudness; the iOS silent switch, calls and alarms; buying a music or sound pack."
requires: —
source: '"Unity 6 Audio Tutorial: Ambient Sound & 3D Spatial Audio" · Synty Studios · https://www.youtube.com/watch?v=FOewaiJeM2k · about 3.5 min · publish date unknown'
tech: Unity 6; pipeline-independent
added: 2026-09-28 · Gemini video analysis (technical steps and visual layout merged), reviewed by Claude · timestamps approximate · 2026-10-01 translated to English · 2026-10-18 (template 1.53): mobile mix and audio session (Sony ASWG-R001 v1.10, Apple AVAudioSession categories, Unity 6.3 Player Settings, AudioSettings.Mobile and Audio Manager, the 6000.3.17f1 iOS trampoline source), buying music (vendor and forum sources on Content ID; the studio's audio research)
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

## Mobile mix and audio session (Android, iOS)
- **Loudness:** measure the whole mix of a representative gameplay take with ITU-R BS.1770 (K-weighted, gated). The only published game target is Sony's ASWG-R001 (v1.10, 2013): portable −18 ±2 LUFS, true peak ≤ −1 dBTP, all sound together, ≥ 30 minutes of play (sources disagree on its home-console value; mobile needs only the portable one). Apple and Google publish none that we found. Project C's first 32 s take: −18.6 LUFS integrated, sample peak −4.7 dBFS.
- **iOS session:** with Unity's audio on, FMOD sets up the audio session. Keep "Mute Other Audio Sources" off (Player Settings › Other Settings, iOS and Android) so the player's own music plays on; the Ambient and SoloAmbient categories both obey the Ring/Silent switch and the screen lock. Recording or voice chat ("Prepare iOS for Recording", microphone) changes that: test the switch again.
- **Calls and alarms:** the engine restarts audio after an interruption (the iOS trampoline re-reads the state 0.1 s after the app becomes active); an app's own CallKit calls are the known exception (`AudioSettings.Reset()` brings audio back but stops every source). Manual test: a call or alarm in the middle of a level.
- **Volume at zero:** `AudioSettings.Mobile.muteState`, `OnMuteStateChanged`, `stopAudioOutputOnMute` (stops the audio thread while muted; a small battery and heat gain, measure it in a soak).
- **Phone speakers:** no reliable measured low cutoff found (forums: weak below ~200-400 Hz); high-pass what a phone can't play (we used 80-180 Hz) and judge on a phone. Library foley can hit late (a soft scrape before the impact): check where the hit lands, not just a −30 dB start trim.

## Buying music or sound packs
- "Royalty-free" doesn't mean outside Content ID: a track its maker registered with a distributor can still claim streamers' and our own videos (vendor and forum sources; YouTube's own page not found), and the Asset Store EULA's wording on trailers is unclear (forum).
- Before buying, ask the seller in writing and keep the answer with the pack in `docs/ai/tasarim/`: (1) is any track registered with Content ID or a distributor (DistroKid, CD Baby, TuneCore)? (2) may streamers monetise videos of the game, and how fast is a claim whitelisted? (3) may we use it in the store video, trailers and our own channel? (4) does one licence cover the team's computers? (5) was it made without generative AI? No answer → don't buy.

## Notes
- The video's scene was built with the POLYGON Gang Warfare pack and freesound.org sounds; the technique itself doesn't depend on the pack.
