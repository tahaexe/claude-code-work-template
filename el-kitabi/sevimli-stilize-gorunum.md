---
title: "Cute stylized look on mobile URP: faces, character shading and effects, cheap depth for low-poly scenes"
condition: "Unity URP mobile game with characters, creatures or toy-like objects, or with low-poly (e.g. Synty) scenery."
read_when: "Designing or polishing a character, face or mascot; writing a character shader or particle effects for low- and mid-range phones; lighting or dressing a low-poly scene; props that look like they float; a disappear or pop effect."
requires: "—"
source: "Glocker et al. 2009 (baby schema, 122 raters) · Komori et al. 2022, Frontiers in Psychology (feature height, jaw) · Crochet Kim 2022 (amigurumi eye placement) · Android Developers 'Lighting for mobile games with Unity' (2026-02-26) · Unity: 'Mobile optimization tips' part 2; Manual 6.3 (SRP Batcher compatibility, Particles Unlit); VFX Graph 17.2 requirements; ParticleSystem.Emit with EmitParams; issue tracker on runtime fog (6.1, As Designed) · Arm GPU Best Practices 2025 (discard and late ZS) · github.com/Fewes/VertexColorBaker (MIT, method only) · the studio's art research 2026-10-18 (toy faces, stylized characters, cheap depth, soft disappear)"
tech: "Unity 6000.3, URP 17, Android and iOS"
added: "2026-10-18 · template 1.53 · four art research notes of the studio merged for the session manager; owner's words: 'Oyunlar tatlı ve güzel görünsün.'"
---
# Cute stylized look on mobile URP

## Cute faces
- Baby schema reads as cute: a big round head, wide eyes, a small nose and mouth (Lorenz). Faces with stronger baby-schema features were rated cuter and raised stronger care motivation in 122 raters (Glocker et al. 2009; eye size wasn't varied). Features placed relatively low on the face and a narrow jaw go with cuteness (Komori et al. 2022). Both studies are cited from the research notes, not re-read.
- Toy faces (amigurumi practice, Crochet Kim 2022; a craft blog, not re-read): eyes low and set wide; a blush at each eye's outer corner; a tiny mouth between and just below the eyes. Centred eyes look grown-up, high eyes look odd, close-set eyes look like an old teddy bear.
- At phone scale give each eye a dark colour, a small white highlight and enough size to read (our rule of thumb, not a source: an eye ≥ ~6% of the character's width); check the face at 60 px in the icon sheet (oyun-simgesi.md) and in the store screenshot matrix.
- Keep labels and markers off the face: colour-blind marks beside or below the character (renk-korlugu-palet.md).
- Characters react: they tense as danger rises and celebrate wins (arayuz-kalitesi.md §2).

## Character shading and effects (low- and mid-range Android)
- An unlit, hand-written URP shader with fake light (top light, soft top highlight, thin rim); work in the vertex stage, half precision; every property in `UnityPerMaterial`; one material per look; no MaterialPropertyBlocks (they take the renderer out of the SRP Batcher: Unity Manual, not re-read for 1.53).
- Eyes and marks as small camera-facing quads in the same material family; hand-made art in one atlas.
- Glow only past the bloom threshold (flames, sparks); bodies stay below it.
- Particles: the built-in Particle System with URP Particles Unlit (transparent, premultiply or additive); no soft particles, camera fading or distortion unless the depth texture is already on; one system per effect kind, `Emit(EmitParams, n)` at each point; `maxParticles` sized for the largest level, warmed once.
- Not on mobile: VFX Graph (needs compute shaders and SSBOs, no OpenGL ES: its requirements page, not re-read for 1.53); preview toon packages in production.
- **Disappear or pop:** scale (0.3-0.5 s, soft ease-in) with a rise, a short squash and particles, the body staying opaque; not `discard`, alpha clip or a dithered dissolve: discard forces late depth testing on tile-based GPUs (Arm GPU Best Practices 2025, not re-read for 1.53).
- Measure draws, SetPass calls and triangles in the pre-release stage's soak; overdraw with RenderDoc on a phone.

## Cheap depth for low-poly scenes (no real-time shadows)
- Order on mobile: baked light for static scenery, light probes for moving objects, fake shadows instead of real-time ones; no dynamic lights (one directional light is the cheapest if one is needed).
- Scenery that moves per level can't use lightmaps: bake what moves with it (vertex AO in the mesh) and draw contact blobs per level.
- Contact blobs under every prop (soft dark quads, one premultiplied material, one draw) are the biggest win: props stop floating.
- Distance fog is set at edit time (Lighting window or the scene builder), never at runtime: from Unity 6.1 fog can't be changed at runtime by default (UUM-90451, "As Designed"). URP's switch back is a keyword the manual names `k_UseDynamicBranchFogKeyword` (the issue writes `k_DynamicBranchFogKeyword`); it costs performance, so it stays off in shipping builds. Shaders that must keep exact colours (a measured palette) simply don't apply fog.
- Vertex AO: a few hemisphere rays per vertex at bake time into vertex colours, read by your own shader (URP Simple Lit ignores vertex colour); no third-party baker needed.
- Check every step with one capture (the UI rule's single screenshot) and the palette checks; the cost is measured in the pre-release stage's soak.
