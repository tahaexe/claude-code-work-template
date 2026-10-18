---
title: Colour-blind-safe palettes for colour-matching games
condition: "Game project whose core rule tells pieces apart by colour (colour sort, jam, match, colour defence). Signs: the game summary (`docs/ai/tasarim/oyun-ozeti.md`) or GDD names colour matching as the rule; a gameplay colour enum or palette (e.g. `Element`, `PieceColor`, a colour table for pieces). Unsure → ask the user one question."
read_when: "Choosing or changing gameplay piece colours, the board background or lighting that tints them (night scenes, fog, bloom, colour grading); writing the style guide; planning a colour-blind mode; before store screenshots that show the palette; a player says two colours look alike."
requires: "Python 3.6+ (standard library only) for `cvd_palette.py`, which the template ships beside this entry (`el-kitabi/araclar/cvd_palette.py`); copy it to the project's `Tools/Palette/` and replace its example palettes with the project's own."
source: "Game Accessibility Guidelines, 'Ensure no essential information is conveyed by a fixed colour alone' (Basic) · https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-colour-alone/ · Machado, Oliveira, Fernandes, 'A physiologically-based model for simulation of color vision deficiency', IEEE TVCG 15(6):1291-1298, 2009 · https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html · Can I Play That, Color-Blindness Accessibility Guide · https://caniplaythat.com/?p=8897 · colour-science docs (Machado matrices by severity) · https://colour.readthedocs.io/en/latest/colour.blindness.html · field measurements: Project C palettes, 2026-10-16 · 2026-10-18: Apple's 'Differentiate Without Color Alone' evaluation criteria, Xbox Accessibility Guideline 103 (additional cues), WCAG 2.2 SC 1.4.11 (non-text contrast)"
tech: "Engine-independent (sRGB colours); measured for Unity 6.3 URP mobile games; Python 3 standard library"
added: "2026-10-16 · template 1.48 · drafted by Claude from the sources above and a project's palette measurements; checked by the session manager (Machado 2009 severity-1.0 matrices compared with the published values; the script imports only `math`) · 2026-10-18 (template 1.53): shape-mark roles and contrast, luminance against the floor, linear blending, phone and Grayscale checks (the studio's colour-blind and value-hierarchy research)"
---
# Colour-blind-safe palettes for colour-matching games

## Summary
- Roughly 8-10% of male players have trouble telling some colours apart (GAG); in a game whose rule is "match the colour" that breaks levels, not just looks.
- Two layers: every gameplay colour also carries a shape mark (default look, not a hidden mode), and the palette is measured so that pairs stay apart under the three dichromacies and against the board background.
- `cvd_palette.py` does the measuring in a second: CIEDE2000 distance of every colour pair under normal vision, protanopia, deuteranopia and tritanopia (Machado 2009, severity 1.0), plus the colour nearest to the background.

## Know first: pitfalls
- **Picking hues is not enough.** Colours with similar lightness collapse for protan/deutan players (red/orange vs brown/green, purple vs blue) and cyan vs turquoise for tritan players. Spreading lightness fixes most cases at once.
- **The background is part of the palette.** A mid-grey stone floor erased a teal piece under protanopia (difference 1.8) while the same palette on dark stone kept every piece ≥ 22 away (a colour-matching project, 2026-10-16). A light sand floor swallowed yellow under tritanopia (10.3).
- **Lighting shifts colours.** Night scenes, emissive materials, fog, bloom and colour grading move the rendered colour away from the material colour; measure the rendered result before calling a palette safe.
- **Shared "element" palettes from other games may not fit.** One tower-defense game's element colours (four near-identical yellows) score 9.1 even for normal vision: fine for effects, unusable for matching.
- **Colour distance can pass while lightness fails.** CIEDE2000 under CVD doesn't see luminance: check the WCAG relative-luminance contrast of each piece's body against its floor too (aim ≥ 3:1, at the least contrasting ring). Project C's navy Blue Fire (#1B2A80) on dark stone (#3E3833) passed every colour check yet is 1.08:1 and vanishes in greyscale: a dark hue on a dark floor gets a light outline or halo (2026-10-18).
- **Semi-transparent colours blend in linear light:** predict them sRGB → linear → mix → back and confirm with a screenshot pixel (arayuz-kurallari.md › Traps).
- **Whole-screen recolour filters are a last resort** (GAG; Apple calls a colour-scheme setting a last resort or stop-gap too: app-store-game-center.md): they change everything, including what was already readable. Prefer shapes plus a measured palette by default; a preset per CVD type only if a colour must stay.

## Steps
1. List every colour that carries gameplay meaning (pieces, slots, lanes, UI chips that show a piece's colour) and the backgrounds they sit on.
2. Put them in the script's palette dictionary (`report("name", {"Fire": "#D9381E", ...}, "#3E3833")`, background last) and run `python -I Tools/Palette/cvd_palette.py`.
3. Read, per vision type: `min dE00` (the closest pair), the three closest pairs, and the colour nearest to the background.
4. Target (working rule, see Unclear points): every pair ≥ 20 CIEDE2000 and every colour ≥ 20 from its background, under all four vision types.
5. Fix the weakest pair first, usually by moving lightness: one very light colour (e.g. ice #BDEFFF), one very dark (navy #1B2A80), mid tones apart in saturation; then re-run. Change the background before giving up a colour.
6. **Shape marks (second channel).** Give every gameplay colour a bold silhouette recognisable by outline alone (flame, hexagon, zigzag, drop; thin details vanish at phone size); a mix shows both of its parts' marks. Choose the mark's role:
   - **Required channel** (the rule can't be solved without it): the mark needs ≥ 3:1 against the colour it sits on (WCAG 2.2 SC 1.4.11, on the specified colours, the weakest area of a gradient). A white icon always gets a dark outline: white on yellow is 1.4:1, its dark rim 11:1.
   - **Support channel** (another channel already carries the rule at ≥ 3:1, e.g. dark seams between regions): a tone-on-tone stamped mark is enough and keeps the board calm.
   - Marks are on by default or offered at first launch, never locked behind progress or purchase.
7. Record the palette and its numbers in the project (style guide `docs/ai/tasarim/gorsel-stil.md`, memory note) and add a manual test (below).

## Settings and values
| Setting | Value | Why |
|---|---|---|
| Simulation | Machado 2009, severity 1.0 (dichromacy), applied to linear sRGB (common practice; the authors' page doesn't state the space) | Covers the strongest case; milder anomalous trichromacy should pass when dichromacy does |
| Difference | CIEDE2000 (Sharma 2005 formulation) | Perceptual distance; the script implements it, no packages |
| Pair target | ≥ 20 under normal, protan, deutan, tritan | Working rule from a colour-matching project (judgement, not a study): pairs at 9-10 already looked alike |
| Background target | ≥ 20 from every gameplay colour | Pieces must not melt into the board |
| Example (palette B) | Fire #D9381E, Ice #BDEFFF, Lightning #FFD21F, Blue Fire #1B2A80, Plasma #B05CE6, Aqua #0E8F7E on #3E3833 | min 30.9 normal, 23.5 protan, 22.4 deutan, 27.0 tritan; floor ≥ 22.2 |

## Verification
- The script's numbers meet the targets for every vision type, background included.
- In the game: capture the board (headless capture or emulator, one per lighting setup), sample each piece's rendered colour and run them through the script; or view the capture in a CVD simulator.
- Manual test (Turkish, `manuel-testler.md`): levels 1-10 played from screenshots filtered for protanopia, deuteranopia and tritanopia: every piece still identifiable by colour or shape.
- Draw the marks at the smallest on-screen size, 1:1 pixels, in grey: all must stay apart.
- On phones: a few levels with Android's Developer options › Simulate color space (monochromacy, deuteranomaly, protanomaly, tritanomaly) and with iOS Grayscale (Settings › Accessibility › Display & Text Size › Color Filters).
- iOS: when common tasks pass in Grayscale, declare "Differentiate Without Color Alone" in App Store Connect's accessibility section, and re-check it every release (app-store-game-center.md).

## Can it be automated?
- Palette and background check: yes, `cvd_palette.py` (seconds, no editor).
- Rendered-colour check: partly; a capture script can sample piece pixels and feed the script (per project).
- Shape marks and readability at phone size: manual test.

## Unclear points
- The ≥ 20 target is a team working rule, not a published standard; GAG asks for "not by colour alone" and simulator testing, without a number.
- Screens, brightness and night lighting vary; the simulation is an approximation of each CVD type, not of each player.
- Whether rival colour-matching hits ship a colour-blind mode could not be confirmed from their store pages (2026-10-16).

## Extra notes
- GAG lists colour-plus-symbol puzzle games among its examples (Two Dots; Puzzle Retreat pairs a symbol with colour).
- Pair colour with audio, motion or borders where a shape doesn't fit (Can I Play That).
