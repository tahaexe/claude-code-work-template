---
title: "Studying a competitor or reference game: a layered reading"
condition: "Game project; used on demand only, when the user or a plan asks to study a competitor or reference game. Never start such a study yourself."
read_when: "Only when the user or a plan asks to study, compare with or learn from a competitor or reference game."
requires: — (the game on a device, its store page or gameplay videos; pages and videos through the account's own Chrome profile)
source: "Raph Koster, A Theory of Fun for Game Design (2004) and 'A Grammar of Gameplay' (GDC 2005) · Robin Hunicke, Marc LeBlanc and Robert Zubek, 'MDA: A formal approach to game design and game research' (AAAI workshop, 2004) · Steve Swink, Game Feel (2008) · App Review Guideline 4.1 (copycats) and Google Play's impersonation and intellectual property policies. Written in our own words from these works."
tech: engine-independent
added: 2026-10-15 · written by Claude from the published works at the session manager's request (template 1.45); on demand only, the rejected automatic reference research stays rejected
---
# Studying a competitor or reference game

## Rules
- On request only (the user or a plan). Never start a reference study yourself; at most suggest one in a line.
- Only checked facts. Tag every claim: [played], [video <link> mm:ss], [store page], [not checked]. Never invent numbers (downloads, revenue, retention, prices) or features; unknown → "not checked".
- One game per file: `docs/ai/tasarim/rakip-<game>.md`, written in Turkish (the user reads it), one or two screens. Decisions go to the GDD or DURUM's **Up next**.
- Mechanics and ideas may inspire; never copy art, audio, text, level layouts, names or UI one to one (App Review 4.1 "Copycats"; Google Play's impersonation and intellectual property policies).

## Read in layers, then check that they agree
After Raph Koster: a game's formal core (the patterns a player learns to master) and its dressing (theme, art, sound, story) are different things, and the dressing can carry the core or contradict it. So read each layer on its own first, then compare them.
1. **Rules and verbs:** what the player can do (tap, swap, drag, aim, build, wait), how a round is won or lost, the resources. Bare, no adjectives.
2. **Systems and loops:** how the verbs combine: core loop (seconds), session loop (minutes), meta loop (days: unlocks, events, economy); where each resource comes from and where it goes.
3. **Likely design purpose:** what each system seems to be for (teach, pace, retain, monetize, let skill show). Always "likely": the designers' intent is not visible.
4. **Feel, moment to moment:** input response and timing, weight, feedback on every action (hit stop, shake, particles, sound), how success and failure land (game feel in Steve Swink's sense).
5. **Presentation:** art style, audio, UI layout and readability, text tone, onboarding, what the store page promises.
6. **Agreement:** do the layers support each other or fight (calm art over a punishing timer; a "relaxing" game behind an energy wall; a store promise the first minutes don't keep)? A fight is deliberate tension or a flaw: say which, and why. MDA: designers work from the rules toward the experience, players from the experience toward the rules; read from both ends.
7. **Take / avoid:** what we take, with the pillar it serves (game summary › Tasarım sütunları), and what we avoid, with the reason.

## File outline (in Turkish)
- Header: game, version, platform, date, how it was studied (played / video / store page).
- The seven layers, 2-5 bullets each, every claim with its evidence tag.
- What we take · what we avoid · what was not checked.
