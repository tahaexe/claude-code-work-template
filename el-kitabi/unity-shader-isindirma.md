---
title: "Shader compile stutter on first use: measure, trace, warm up (Unity 6 GraphicsStateCollection)"
condition: "Unity 6 project (`ProjectSettings/ProjectVersion.txt` starts with `6000.`)."
read_when: "Writing or changing a code shader (HLSL), before its Unity run; a build hitches the first time an effect, material, area or quality level appears; preparing a release, a demo or store video captures; moving a build to DX12, Vulkan or Metal; adding quality levels or many new materials or effects."
requires: "Windows SDK (fxc, dxc) and Python 3 for `shader-kontrol.py` and its stub `shader-kontrol-stub.hlsl`, which ship beside this entry in `el-kitabi/araclar/` (a project's copy: `docs/ai/el-kitabi/araclar/`)"
source: "Unity Manual 6.3 LTS: Shader loading; Introduction to PSO tracing and warming; Trace and manage PSO data collections; Warm up PSOs; Other methods to warm up shaders; PSO tracing and warming example · Scripting API 6.3 `Experimental.Rendering.GraphicsStateCollection` · Unity Discussions, Unity Graphics team: 'Prevent shader compilation stutters with PSO Tracing in Unity 6' (2024-06-24, sample update 2025-01-13) and 'PSO Caching Improvements in Unity 6.5' (2026-05-08, staff replies 2026-05-27). All read 2026-10-16."
tech: "Unity 6.0-6.5 (API from 6.0, automatic fallback from 6.1, out of experimental in 6.5) · any render pipeline · DX11, DX12, Vulkan, Metal, OpenGL, GLES, WebGL"
added: "2026-10-16 · template 1.49 · research by a project session; every claim re-read on the pages above by Claude for the session manager · template 1.61: the editor-free compile check before a Unity run (a game session's tool of 2026-10-24, generalized and tried on five studio games' shaders the same day)"
---
# Shader compile stutter: measure, trace, warm up

## Before a Unity run: an editor-free compile check
- `python -I -B docs/ai/el-kitabi/araclar/shader-kontrol.py <the game's shader folder or files>` compiles each code shader's HLSLPROGRAM with the Windows SDK's fxc (SM 5) and dxc (SM 6), URP's includes swapped for a stub of its common names (`shader-kontrol-stub.hlsl`), the project's own includes kept. About a second a shader, no editor or heavy-job slot; errors point at the shader's own lines. `--cost`: fxc's instruction slots a stage, to compare two versions (a desktop proxy, not a device's cycles); `--dene`: self-test.
- It catches syntax, type and undeclared-name errors in our code; it doesn't check URP's real library, the mobile back ends or variants: a step is still verified by a Unity run that logs no shader error.
- A name missing from the stub fails as "undeclared": add it to the stub (the project's copy keeps its own lines on a template update) or pass `--stub <file>`. Tried 2026-10-24 on five games' own shaders: three passed whole (6/6, 6/6, 5/5), the rest stopped on Shader Graph types (`UnityTexture2D`) and a multi-pass shader's entry points.

## Why it stutters
- The first time Unity renders with a shader variant, the driver builds its GPU version; that can stall a frame visibly. Unity keeps it while something still references the variant (Shader loading).
- DX12, Vulkan and Metal build a pipeline state object (PSO: the compiled shader with its GPU state); the driver caches created PSOs on disk.
- Worst on a player's first run, and again whenever new materials or effects appear; OS and driver updates often invalidate the driver's PSO cache (Graphics team, 2024).
- The old warm-up (Preloaded Shaders, `ShaderVariantCollection.WarmUp`, `Shader.WarmupAllShaders`, `Experimental.Rendering.ShaderWarmup`) isn't recommended on Vulkan, DX12 and Metal: missing graphics state can make it build the wrong PSOs.

## Measure first
- Count hitch frames from the first frame of a scripted route (e.g. frames over 50 ms and over 100 ms), not after a warm-up window: averages and post-warm-up benchmarks hide first-use stalls (one project's benchmark started after its warm-up window, so they never showed in its numbers).
- Cold vs warm: clear the driver's shader cache, run the route, run it again. Windows, DX12, NVIDIA examples (Unity's post): `%USERPROFILE%\AppData\LocalLow\NVIDIA\PerDriverVersion\DXCache`, `%USERPROFILE%\AppData\Local\D3DSCache`; other platforms differ. No cold/warm difference → stop here.
- Profiler: `Shader.ParseThreaded` and `Shader.ParseMainThread` mark shader loading from serialized data; the 6.3 manual names no marker for the driver's compile, so judge by the hitch frames.

## Fix: GraphicsStateCollection (Unity 6.0+)
- `UnityEngine.Experimental.Rendering.GraphicsStateCollection`: experimental in 6.3 (may change), out of experimental in 6.5. Unity's recommended way to warm up shaders on every API: on DX11, OpenGL, GLES and WebGL it falls back to variant warm-up automatically (6.1+; on 6.0 use the old methods there).
- **Trace** (development builds only; release builds can't trace) in the player, not the editor: players meet PSOs the editor never draws. `BeginTrace()` at app or scene start, play the routes, effects and quality levels, `EndTrace()` at the end; `SaveToFile(path)` writes a `.graphicsstate` file, or `SendToEditor()` over PlayerConnection (Development Build and Autoconnect Profiler on in the build profile). A trace from another device: copy the file back by hand.
- **One collection per graphics API and platform** (GPU state varies per API), not per GPU vendor or driver. Quality levels load other variants: one collection per level (warm the matching one when the player switches), or one large trace that cycles through every setting.
- **Warm up** in release builds: `WarmUp()` schedules every PSO in the collection, `WarmUpProgressively(n)` a set number; both return a job handle (synchronous or asynchronous). Unity: during loading (app start, scene load); progressive warm-up avoids blocking. Our pattern: where the player already waits in a menu, warm progressively there and finish at the first load.
- What the trace never drew stays cold: trace again after art, effect or quality changes. Compute and ray tracing shaders can't be traced.
- Check a collection with `variantCount`, `totalGraphicsStateCount`, `graphicsDeviceType`, `runtimePlatform`, `qualityLevelName`; after warm-up `isWarmedUp`.
- Reference: Unity's Universal 3D sample (`GraphicsStateCollectionManager`, Mode Warm Up; collections in `Assets/SharedAssets/GraphicsStateCollections`; an editor stripper keeps only the build target's collections; a combiner merges collections of the same platform, graphics API and quality level).

## Platforms
- PC: DX12 needs its own collection; DX11 gets variant-level warm-up through the fallback.
- Android: Vulkan builds PSOs like DX12, so warm-up matters more there; GLES falls back to variant warm-up. Auto Graphics API tries Vulkan first (`unity-proje-ayarlari.md`). iOS: Metal builds PSOs.

## Unity 6.5+
- Out of experimental; `cacheMissCollection` collects the states a warm-up missed during play, to add to the collections; Graphics › Shader Settings can begin a trace at startup (the player sends it to the editor; Autoconnect Profiler) or warm a Preloaded Graphics State Collection at startup; a collection inspector; a warm-up utility for VFX assets' compute shaders.
- Every form of tracing still needs a development build. The URP 3D sample's collections take a few hundred KB each; a cold-start warm-up can take a few seconds, so Unity recommends progressive (time-sliced) warm-up. No backport to 6.3 announced (2026-10-16).

## Verification
- Hitch counts cold vs warm on the same route, before and after the fix; record them with the project's measurements.
- After a content update, a development build traces again and the collection's counts grow as expected.
