---
title: "Synty Sidekick characters: facial expressions (blendshapes) and blinking"
condition: Project has Synty Sidekick characters (a folder under Assets with "Sidekick" in its name; Synty packages usually install under Assets/Synty/).
read_when: Work on a Sidekick character's facial expressions, blendshapes, blinking or facial animation and Animator layers.
requires: "Sidekick Character Creator tool (Synty). Comes with the Sidekick packages; installed and updated from inside Unity with the downloader in the top Synty menu; the downloader opens by itself when the first Sidekick package is imported. Check: a Sidekick tool in the Synty menu or the tool's folder in Assets; unsure → ask the user."
source: '"Learn Blendshapes in Unity 6 - Make your characters EXPRESSIVE!" · Synty Studios · https://www.youtube.com/watch?v=YjMjViBqJuU · 7:23 · publish date unknown'
tech: Unity 6; render pipeline not stated in the video (blendshapes and Animator work the same in every pipeline)
added: 2026-09-27 · Gemini video analysis, reviewed by Claude · 2026-10-01 translated to English
---
# Synty Sidekick: facial expressions and blinking

## Summary
Sidekick facial expressions are the blendshape values of the mesh's `Skinned Mesh Renderer`. Facial animations like blinking are made in a separate clip and played on a `Face` layer of the Animator with **Additive** blending, so they don't clash with body animation.

## Know first: pitfalls
- **Leave some blendshapes alone (1:47):** never reset those with `default` in their name or the `masculine` / `feminine` values; that breaks the face and body shape set in Sidekick Character Creator. When resetting an expression, reset only expression blendshapes.
- **Character slides down or teleports (5:37):** happens when the `Animator` has an Avatar but the Base Layer is empty. Lasting fix: an idle animation on the Base Layer as the default state (6:10). Setting the Avatar to `None` is only a temporary test; it turns skeleton animation off.
- **Artificial blinking (2:30):** 100% closing and evenly spaced keys look artificial. Use the values below.

## Steps
1. **Find the blendshapes (0:14):** select the mesh child in the character prefab → Inspector → `Skinned Mesh Renderer` → `BlendShapes`.
2. **Create a clip (2:01):** folder `Assets/Animations`; select the character → `Window > Animation > Animation` (Ctrl+6) → `Create` → `anim_face_idle`.
3. **Blink curve (2:30):** `Add Property` → mesh → `Skinned Mesh Renderer` → `blink_upper_left` and `blink_upper_right`:

   | Frame | Value | Meaning |
   |---|---|---|
   | 0 | 0 | eye open |
   | 20 | 80 | closing: slow, not 100% |
   | 30 | 0 | opening: fast |
   | 80 | 0 | pause between blinks |

4. **Face layer (4:58):** Animator window → `Layers` → `+` → `Face`. Gear icon → `Weight` = 1, `Blending` = `Additive`. Drag the `anim_face_idle` clip onto this layer.
5. **Base Layer (6:10):** an idle animation (e.g. `default_feminine_idle`) is the Base Layer's default state.

## Verification
- In Play mode the character plays its idle animation, blinks at the same time and doesn't slide. The visual check goes to manual tests.
- `Face` layer: Weight 1, Blending Additive.

## Automation notes for Claude
- **Runtime:** `SkinnedMeshRenderer.SetBlendShapeWeight(index, value)`. Get the index once in `Awake` with `sharedMesh.GetBlendShapeIndex("name")` and keep it.
- **Clip (editor code):** `AnimationClip.SetCurve(path, typeof(SkinnedMeshRenderer), "blendShape.blink_upper_left", curve)`; `path` runs from the Animator's root to the mesh object.
- **Layer (editor code):** `AnimatorController.AddLayer("Face")`, then on the layer `defaultWeight = 1` and `blendingMode = AnimatorLayerBlendingMode.Additive`. `controller.layers` returns a copy; assign the array back after changing it.
- **Assets:** editor work via Unity CLI or editor code; never hand-edit `.anim` and `.controller` files (unity-varliklar rule).
- **Random timing:** blinking at random intervals is only an idea in the video (3:00). If needed, schedule it in code (e.g. a random 2-6 second interval).

## Notes
- An Avatar Mask is needed only if the face layer also animates head or jaw **bones**. It has no effect on a clip that only animates blendshapes.
- Render pipeline or material conversion isn't covered in the video.
