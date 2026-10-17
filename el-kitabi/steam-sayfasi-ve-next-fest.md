---
title: "Steam store page, Next Fest, Playtest and demo, accessibility tags and Unity 6.3's screen reader (PC game)"
condition: "A game planned for Steam (Steam named in the project's CLAUDE.md, game summary or memory)."
read_when: "Preparing the Steam store page, its assets, tags or content survey; planning a Coming Soon page, a Playtest, a demo or a Next Fest entry; declaring accessibility features; adding screen reader support or a camera-shake setting to a Unity 6.3 game."
requires: — (Steamworks partner site in the account's own Chrome profile; submitting a page or build for review and publishing follow the release split)
source: "Steamworks docs, re-read 2026-10-17: store/coming_soon, store/assets/standard, store/tags, store/application/demos, gettingstarted/contentsurvey, marketing/upcoming_events/nextfest, features/playtest, accessibility_features · research by two project sessions (2026-10-16/17) · Unity Manual 6.3 'Get started with screen reader support' (re-read 2026-10-17) · a project's quit-crash plan (2026-10-17; UUM-146676 quoted from Unity's release notes) and its settings code"
tech: "Steamworks (2026) · Unity 6.3 Accessibility module. Steam's rules and Next Fest editions change: re-read the page before acting."
added: "2026-10-17 · template 1.51 · two project sessions' research, verified on the cited pages for the session manager"
---
# Steam store page, Next Fest, Playtest and demo

## Timeline
- Coming Soon page live at least 2 weeks before release (new products); wishlists open as soon as the page is public, so earlier is better.
- Submit the store page for review at least 7 business days before it should go live; builds are reviewed too: leave room before any date.
- Order: Coming Soon page → Playtest waves (does it run, is it fun) → freeze the best build → cut the demo from it (does it win strangers) → Next Fest with the demo live → release.

## Next Fest
- Eligible: one Next Fest per title; not released before the edition ends; the base game's store page published and public; a publicly playable demo by the start; not a prologue or short version of a game already on Steam.
- Demo in review at least 5 weeks before the fest to be live for Press Preview (opens 11 days before the fest), else at least 3 weeks; no exclusivity, newness or length rule.
- Edition dates live on Steamworks' Next Fest page: read them there for each edition, never copy them into memory as fixed.
- A live Playtest doesn't affect eligibility, but Valve advises none during the fest (it splits players from the demo): close its signups and set it Not Playable before.

## Playtest
- A free child app of the base game (its own app ID), with no store page: signups sit on the base game's page. Access: limited (default; you admit requesters in groups, Steam picks them at random), open (everyone who asks), Standard Release keys, or friend invites (experimental; friends of 30+ days, 1-3 invites each).
- Never charged for, keys never sold (a paid work-in-progress build is Early Access). Joining or leaving doesn't touch the wishlist; playtest-only players can't review the game; its playtime counts toward neither refunds, achievements nor cards.
- To end it: signups off first, then Not Playable (granted keys stay). Reset is irreversible: it disables every key and removes every tester.

## Demo
- A separate demo app (base game › associated packages, DLC, demos and tools › Add Demo) with its own depots and builds; its own store page is optional (players can review the demo there).
- Link it under the base game's Special Settings › Associated Demos, then re-publish the base page so the Download Demo button appears.
- The wishlist notification (email and mobile app, to everyone wishlisting the game) is sent once, by hand, within 14 days of the demo's first launch; wishlist notifications have a 2-week cooldown per app, so keep 2+ weeks from the launch or a discount. A demo released months before the fest gets no second one.

## Store page
- Capsules: header 920×430, small 462×174, main 1232×706, vertical 748×896; no text on them but the game's title. Library assets and trailer specs: Steamworks' asset pages when making them.
- Screenshots: at least 5, 1920×1080 or larger (16:9), gameplay only; mark at least 4 "suitable for all ages" (no gore, violence or suggestive themes), or the game may miss places such as the front page's hover.
- Tags: at least 5 before launch, up to 20 (only the top 20 count); the top 5 should picture the game, the first 15 in order of relevance (some filters use them); specific sub-genres over generic tags ("indie", "singleplayer").
- Content survey: AI-made content players consume is disclosed, pre-generated (made with AI tools during development and shipped) and live-generated (also its guardrails against illegal content); the section is about shipped content, not efficiency tools used while developing.

## Accessibility tags
- Store pages show an "Accessibility Features" panel and search filters by 19 tags, declared in Steamworks › store page › Basic Info › Accessibility Feature Wizard:
  - Gameplay: Adjustable Difficulty, Save Anytime.
  - Audio: Custom Volume Controls, Narrated Game Menus, Stereo Sound, Surround Sound.
  - Visual: Adjustable Text Size, Subtitle Options, Color Alternatives, Contrast Controls, Camera Comfort, Playable without Vision.
  - Input: Keyboard Only Option, Mouse Only Option, Touch Only Option, Playable without Quick Time Events, Playable at Your Own Pace, Chat Text-to-speech, Chat Speech-to-text.
- Before a release or a Next Fest, map the game's settings to the tags and declare only what exists (Project A 2026-10-17): volume sliders → Custom Volume Controls; positional audio → Stereo Sound; colour-blind palettes → Color Alternatives; no timed button sequences → Playable without Quick Time Events; FOV slider, no motion blur and a camera-shake setting → Camera Comfort. Surround Sound only after listening on a real 5.1/7.1 setup.
- A camera-shake slider scales only visual shake (damage, reload clips), never recoil that moves the aim, or it turns into an aiming advantage.

## Screen reader (Unity 6.3)
- The Accessibility module reaches TalkBack, iOS VoiceOver, Windows Narrator and macOS VoiceOver, but no UI is read by itself (uGUI or UI Toolkit): build an `AccessibilityHierarchy` with one `AccessibilityNode` per control (`label`, `role`, `state`, its screen rectangle in `frame`), handle the node's `invoked` (named `selected` before 6.3), assign the hierarchy to `AssistiveSupport.activeHierarchy` and again on `AssistiveSupport.screenReaderStatusChanged` (Unity sets it to null when the reader turns off). Check in Play mode with *Window › Accessibility › Hierarchy Viewer*, then with the platform's reader on a build.
- Before 6000.3.21f1 the Windows player crashes at every quit once a UI Automation client has touched its window: screen readers, the touch keyboard, translators, window tools (UUM-146676; Project A 2026-10-17). Update the engine patch before screen reader work; expect the crash in reports from older builds.
