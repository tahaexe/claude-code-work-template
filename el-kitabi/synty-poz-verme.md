---
title: Posing Synty characters in the editor (Animation Rigging · Bone Renderer)
condition: Project has Synty characters (a folder under Assets with "Synty", "Polygon" or "Sidekick" in its name). Works on any character with a skeleton.
read_when: Posing a character or any rigged object in the editor; preparing a scene and camera for promo, store or concept images.
requires: — (posing needs the Animation Rigging package, com.unity.animation.rigging; add it when the work comes, not at install.)
source: '"How to EASILY pose characters in Unity 6" · Synty Studios · https://www.youtube.com/watch?v=9m0MsrdbqVU · length and publish date unknown'
tech: Unity 6; pipeline-independent (Animation Rigging works in every pipeline)
added: 2026-09-27 · Gemini video analysis, reviewed by Claude · timestamps approximate · 2026-10-01 translated to English
---
# Posing Synty characters in the editor

## Summary
Animation Rigging's `Bone Renderer` component makes bones selectable in the Scene view; rotating them poses the character by hand. The camera is aligned to the Scene view and an image is taken. This is static pose and image prep in the editor, not in-game animation.

## Know first: pitfalls
- **Play mode resets the pose:** a running Animator on the character drives the bones in Play mode. Take the posed image in edit mode or save the pose into an animation clip. (not in the video)
- **Don't Apply to the prefab:** if the character in the scene is a prefab instance, rotated bones become scene overrides; `Apply` changes the prefab's default pose. To reset the pose use `Revert` on the instance. (not in the video)
- **Global axis:** rotating bones on the `Global` axis bends joints unnaturally; switch to `Local` in the toolbar (~01:30).
- **Aligning the camera by hand:** wastes time; set the angle in Scene and use `Align With View` (~00:15).

## Steps (timestamps approximate)
1. **Camera (~00:15):** set the angle in Scene; with `Main Camera` selected `GameObject > Align With View` (Ctrl+Shift+F). Dock the Game tab beside it; fine-tune FOV and position if needed.
2. **Scene (~00:30):** place characters and objects; set scale and direction.
3. **Package (~00:45):** if missing, `Window > Package Manager` → `Unity Registry` → `Animation Rigging` → `Install`.
4. **Show bones (~01:10):** select the character → top menu `Animation Rigging > Bone Renderer Setup`. Bones show as lines in Scene.
5. **Pose (~01:30):** select a bone in Scene → `E` (Rotate) → rotate on the `Local` axis (head, arms, legs…).
6. **Clean up (~02:00):** when done, disable or remove the `Bone Renderer` component.

## Verification
- After `Bone Renderer Setup` bones are visible in Scene; the mesh deforms correctly with rotated bones.
- With the component off the pose stays; the Game view frame gives the wanted image.

## Automation notes for Claude
- **Claude prepares, the user poses:** posing is creative, visual work. Claude adds the package and prepares the `Bone Renderer` (`AddComponent<BoneRenderer>()`, bones in its `transforms` array) and the camera; the user poses.
- **Taking the image:** once pose and camera are ready, editor code run via Unity CLI can take it: render the camera into a RenderTexture and save a PNG; in Play mode `ScreenCapture.CaptureScreenshot`. For store images pick the target resolution (related to the release checklist's store items).
- **Keeping the pose:** a reusable pose can be stored by writing bone rotations into a single-frame animation clip or a ScriptableObject.
- **Assets:** editor work via Unity CLI or editor code; never hand-edit the scene file (unity-varliklar rule).

## Notes
- `Bone Renderer` draws only in the Scene view; invisible in game, negligible runtime cost. Still, remove it when done, for tidiness.
