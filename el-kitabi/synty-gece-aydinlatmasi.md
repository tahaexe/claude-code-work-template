---
title: Turning day into night in Synty scenes (night lighting)
condition: Project has Synty environment assets (a folder under Assets with "Synty" or "Polygon" in its name) and uses URP (com.unity.render-pipelines.universal in Packages/manifest.json).
read_when: "Giving a scene a night atmosphere or turning a day scene into night: ambient light, fog, sky, post-processing (Global Volume) and interior lights."
requires: — (uses ready objects from Synty packages such as Skydome, Sunbeam and Fog Plane; no extra program)
source: '"NIGHT TIME lighting in UNITY: Convert DAY to NIGHT!" · Synty Studios · https://www.youtube.com/watch?v=bd6ppAVwxZA · about 5-6 min · publish date unknown'
tech: URP (Unity version not stated in the video)
added: 2026-09-27 · Gemini video analysis, reviewed by Claude · timestamps approximate · 2026-10-01 translated to English
---
# Synty: turning day into night

## Summary
A Synty scene built for daytime becomes a cold, blue-toned night through the main light, ambient light, fog, sky, Global Volume and interior lights. Warm interior light leaking from windows contrasts with the cold outside.

## Know first: pitfalls
- **Leftover daytime objects:** daytime clouds (`Clouds`) and `Sunbeam` particles clash with the night sky and fog; delete them or adapt them to night.
- **Too cold:** don't push White Balance `Temperature` all the way to cold; the scene goes lifeless. Lower it from the day value and leave it around 10.
- **Dim interior lights:** once outside is dark, interior lights fall short; raise `Range` and `Intensity`.
- **Mobile cost:** 4K shadows and many shadow-casting point lights are expensive on mobile. With separate URP Assets for PC and mobile, apply high settings only to the PC one.

## Steps (timestamps approximate)
1. **Shadow resolution (~00:35):** select the URP Asset in the `Settings` folder (in the URP template usually `PC_RPAsset` and `Mobile_RPAsset`). Raise the main light's shadow resolution from 2048 to 4096 (Unity 6 URP: `Lighting > Main Light > Shadow Resolution`).
2. **Moonlight (~00:50):** `Directional Light` → `Color` from a warm tone to cold blue.
3. **Ambient light (~01:05):** `Window > Rendering > Lighting` → `Environment` → Environment Lighting `Source` = `Gradient`. `Sky Color` blue, `Equator Color` dark blue or whitish, `Ground Color` dark with less warmth.
4. **Fog and clouds (~01:30):** same tab: `Fog` color blue, bring the fog closer to the camera (`Start`/`End` or density). Delete the daytime clouds.
5. **Sky (~01:50):** search `Skydome` in Project, put the prefab from the `Generics` folder in the scene and scale it up; material color dark blue. Pull the scene's `Fog Plane` to dark blue too.
6. **Global Volume (~02:20):** `Bloom`: lower `Threshold`, raise `Intensity` · `Vignette`: on · `Lift Gamma Gain`: shift the wheels to cold/blue · `White Balance > Temperature`: about 10.
7. **Moon beam (~03:10):** put the `Sunbeam` prefab in the scene, angle it as if from the moon, pull its color to blue.
8. **Particles (~03:40):** lower the foreground `Fog Particle` and adjust its color for contrast (green in the video). Delete leftover daytime `Sunbeam` and extra particles.
9. **Interior lights (~04:10):** interior `Point Light` → raise `Range` and `Intensity` noticeably, `Shadow Type` = `Soft Shadows`. In URP, point-light shadows need `Additional Lights > Cast Shadows` on in the URP Asset.

## Verification
- The scene has a cold, blue night atmosphere; no daytime clouds or sun beams visible.
- Warm interior light with soft shadows leaks from windows and doors.
- FPS is acceptable on the target device, especially mobile. Visual and performance checks go to manual tests.

## Automation notes for Claude
- **Keep presets:** separate `Volume Profile` assets for day and night (e.g. `Day_VolumeProfile`, `Night_VolumeProfile`); keep ambient light and fog values in a ScriptableObject preset too. Switching is a small script that swaps the profile and values.
- **Environment settings in code:** `RenderSettings.ambientMode = AmbientMode.Trilight` (Gradient in the UI), `ambientSkyColor`, `ambientEquatorColor`, `ambientGroundColor`; fog: `RenderSettings.fogColor`, `fogStartDistance`, `fogEndDistance`.
- **Editor work:** add/delete objects and set components via Unity CLI or editor code; never hand-edit the scene file (unity-varliklar rule).
- **Day-night cycle:** the video turns the scene into night permanently; an in-game cycle over time isn't covered. If needed, plan a separate timed transition between the two presets.

## Notes
- With baked or mixed lights, moving characters need a `Light Probe Group` to be lit correctly by interior and exterior light; fully realtime lights don't.
- Names and locations of Skydome, Sunbeam and Fog Plane vary by Synty pack; search the project first.
