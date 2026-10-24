---
title: "UI layout map: where things go and how big, measured from the leaders (8 portrait screens, icon sizes, type scale, fonts)"
condition: "Unity game project with player-facing portrait UI (not a non-game app). Landscape-only games are not covered yet (§7)."
read_when: "Laying out or resizing a portrait screen, popup, HUD, icon or text style; writing the style guide's type scale or picking its UI font (docs/ai/tasarim/gorsel-stil.md); the Quality Gate's layout check against the leaders."
requires: "arayuz-kalitesi.md (bar, screen recipes, timings), arayuz-kurallari.md (floors, touch, safe area, two languages), arayuz-kalitesi-testleri.md (device matrix, checks #3, #4, #6, #19)"
source: "The studio's measurements, 2026-10-23: 185 boxes from gameplay frames and store images, each with its source, frame and pixels (kept with the studio, outside the template). Royal Match: YouTube ZRkyBxLXCY4 (iPhone 375 pt; home, HUD, level start, win, unlock and task popups), zfX-isS_QRs (2022; continue offer, level failed), ibmMWhv5iIg (shop), GpayHAfNEp4 (settings; tablet-shaped capture: structure only). Color Block Jam: J8qcoSAqrU0 (HUD, win, unlock). Block Blast: Z19Sy2srRQ8 (HUD, adventure loss), h1fYAFA8550 (game over). Vita Mahjong: Tpw6OiHsHPQ (HUD, win). Bus Traffic Fever: App Store image (home; marketing). Hole.io: App Store preview P1349413633 (action HUD). Tomb of the Mask: App Store image (platformer HUD). Thumb zone: Steven Hoober, 'How Do Users Really Hold Mobile Devices?' (UXmatters 2013), 'Design for Fingers, Touch, and People' (2017). Expert review by a senior mobile game UI designer agent, 2026-10-23. Pilot on a studio game's reward popup, 2026-10-23 evening (§6). Fonts: OFL files from github.com/google/fonts checked with fontTools 4.64; platform type scales: Material 3 type-scale tokens, Apple HIG Typography."
tech: "Unity 6000.3 uGUI + TextMeshPro; CanvasScaler Scale With Screen Size, reference width 1080, match = width (0)"
added: "2026-10-24 · template 1.61 · the owner asked on 2026-10-23 for a template from the best mobile games for icon sizes and placement, font sizes and font choice ('boyut ve konum, font seçimi gibi faktörlerde'); approved 17:3x the same day, piloted on a studio game's reward popup before entering the template"
---
# UI layout map

## 1. How to read it
- Reference phone: 1080×2400 portrait = 411×914 dp (android-20x9). Safe area: 52 dp status bar / cutout on top, 24 dp gesture bar at the bottom (48 dp with Android's 3-button bar). Everything tappable or readable stays inside the safe-area container.
- Sizes are the leaders' values converted to this phone: dp = measured px ÷ source width × 411. Leaders scale their UI with the width, so %W is the portable number.
- Canvas setup the numbers assume: reference width 1080, match = width (0); then units = dp × 2.625. With another setup (some studio games use 1080×1920 and match 0.5) convert through the real scale factor, or the result is ~12% off. Tablets (aspect < 1.6): match = height, keep the phone unit sizes, centre the column, cap widths (arayuz-kurallari.md); Royal Match's iPad home keeps the button size and centres the group at 66% W.
- **Narrowest phone:** sizes shrink with the width, ×0.876 on the 360 dp android-small. So every touch area is ≥ 144 units = 55 dp on these maps (48 dp there); art may stay smaller (corner icons 36 dp, price buttons 44-51 dp tall, toggles 36 dp, close × 51-57 dp) but its hit area is enlarged (Raycast Padding or a non-drawing Graphic, arayuz-kurallari.md). Primaries: ≥ 73 dp tall here (64 dp there, test #19), ≥ 50% W alone, ≥ 39% W each when two share a row.
- Font size = cap height ÷ 0.70 (rounded bold faces: Nunito 0.705, Fredoka 0.70, Baloo 2 0.68; outlines measure ~5% large). Ranges are leaders' min-max, our value first. n ≤ 2 or one game = a direction, not a rule.

## 2. Screen maps
On the 411×914 dp phone. Thumb zone: easy where both thumbs reach; for one thumb the far bottom corner is a stretch; boards are usually held in two hands or cradled.
1. **Home / map:** top bar centred ~34 dp under the safe top: counters 33 dp tall (26-35) with a 37 dp icon (29-48) over the left end and a 23 dp green "+" (touch 55); settings top right, 36 dp art (32-40), 12 dp from the edge; offer/profile 64 dp top left (one game); side offers 73 dp (64-77) + 22 dp label strip, max 2 per side. Primary "Level N" in the bottom third: alone 222×80 dp, 54% W (Bus Traffic Fever 218×89); two in a row 174×79 dp, 42% W each, 31 dp gap (Royal Match); 34 dp above a bottom nav that rises 50-60 dp above the safe inset with its ground to the screen edge (Royal Match iPhone: 50 + 34 pt; 5 tabs, the active one double width with a 64 dp icon and the only label; one game).
2. **HUD (puzzle):** goal and moves panels top left / top right (Royal Match 122×118 dp; or one 75 dp bar + 97 dp level badge, CBJ), a reacting character or level badge between; the biggest number is moves or time left, 44 dp (leaders 23-52). Board 90-94% W, frame included (leaders 91-98: Royal Match 9 columns 98%, Block Blast 91%; the 86% in arayuz-kalitesi.md is Royal Match's 8-column board), its centre at 44-54% of the height; 8 columns at 94% W give ~46 dp cells, 40 dp on the narrowest phone: test the tap there (tile rule: arayuz-kalitesi.md › Vita ≥ 56 dp). Boosters at the bottom: round 64 dp (59-70; keep ≥ 64), 76 dp centre to centre, count badge 33 dp (25-34), their bottom 8 dp above the safe-area bottom; pause or settings last in that row at the same size (58-68 dp) or top right, 36 dp art. Banner ad: move the row up by the banner height the ad SDK reports + the safe inset + 8 dp; nothing tappable under the banner. Action HUD (Hole.io, Tomb of the Mask; one sample each): timer pill 105×39 dp top centre (text 26 dp), progress bar 86% W × 33 dp, score pill top right, floating joystick ring 150 dp / knob 63 dp, power-up bottom left 40 dp art; whole HUD ≤ 6% of the height.
3. **Level start:** panel 88% W (86-92) centred in the safe area, ribbon title 94% W at 44 dp, close × 55 dp (51-57) overflowing the top-right corner (centre 90% W), goal box with a 53 dp icon and 25 dp count, heading 28 dp, 3 booster tiles 74 dp 16 dp apart with 33 dp badges, Play 222×91 dp (54% W) at the panel's bottom, label 36 dp. Royal Match only: a direction.
4. **Win:** panel-free (CBJ, Vita): praise title 56 dp (50-60) at 29-40% of the height, a personal line 20 dp, hero reward 149 dp (109-154), rewarded ×2 208×84 dp (51% W) with a 49 dp video icon and the doubled number, plain claim 156×63 dp (38% W) visible at once; the counter stays on screen for the reward to fly into. Panel variant (Royal Match): 88% W panel, 55 dp close ×, star 149 dp, one Continue 222×89 dp. Vita: 3 stat boxes 105×68 dp, next-level button 267×79 dp (65% W) in its difficulty colour.
5. **Lose and continue:** Royal Match: full-width panel, close × 55 dp from the first frame, one "what you'll lose" card 385×172 dp, primary continue 273×92 dp (66% W) with the price and a 26 dp coin inside, a purchase card below it with a 144×44 dp store-price button (touch 55), the coin counter appears top left. No-offer variant (Block Blast): remaining goals as 60 dp icons, a 51 dp encouraging title, Retry 241×57 dp (59% W; under our height floor, ours ≥ 73 dp).
6. **Shop** (Royal Match only: a direction): full screen; header ~56 dp under the status bar: counter left (104-122×33), title 44 dp centred, close × 57 dp right; offer cards nearly full width (98%; the edge-margin exception) 163-186 dp, with item icons and a 144-155×44-51 dp price button; pack rows 65 dp on a 73 dp pitch, 56 dp icon, the amount as the biggest text (24 dp; 22-27), price button 155×45 dp (38% W) right; "More offers" 272×61 dp; Restore purchases on iOS.
7. **Settings** (Royal Match tablet-shaped capture rescaled: ±10%): same header; 2×2 switches 127×36 dp (touch: the whole cell) with a ~25 dp label and ON/OFF words; row buttons 68-71% W × 56 dp on a 66 dp pitch, icon + ~24 dp label, sized for the longest Turkish row; version and player ID at the bottom, 14 dp. Rows from arayuz-kalitesi.md › Settings.
8. **Popup** (unlock, event, reward): panel 88% W (86-92), ribbon wider than the panel, title 44 dp (32-49; long titles 34), close × 55 dp, art area, then one button ≥ 50% W × ≥ 73 dp (206×80) or two in a row 160×73 dp (39% W) 12 dp apart. Royal Match's 138×69 pair (34%) and CBJ's 180×73 single (44%) sit under our floor. Panel-free variant (CBJ): two-line 48 dp title on the dimmer, a 109×140 dp picture with rays, 20 dp text, one button.

## 3. In-game icon sizes (visible art width; touch ≥ 55 dp here)
| Icon | min | median | max (dp @411) | units | measured in (n) |
|---|---|---|---|---|---|
| Top-bar currency icon | 29 | 37 | 48 | 97 | RM, CBJ, ToM (5) |
| Counter (pill) height | 26 | 33 | 35 | 87 | RM, CBJ (4) |
| "+" badge on a counter | 19 | 23 | 27 | 60 | RM, CBJ (2) |
| Settings, top corner | 32 | 36 | 40 | 94 | RM, BB (2) |
| Back / menu, top corner | 29 | 34 | 34 | 89 | Vita, ToM (3) |
| Pause / settings in the booster row | 58 | 63 | 68 | 165 | RM, CBJ (2) |
| Booster button (HUD; keep ≥ 64) | 59 | 64 | 70 | 168 | RM, CBJ, Vita (3) |
| Booster tile (popup) | 74 | 74 | 74 | 194 | RM (2) |
| Count badge | 25 | 33 | 34 | 87 | RM, CBJ, Vita (3) |
| Close × | 51 | 55 | 57 | 144 | RM only (8) |
| Goal icon | 43 | 53 | 60 | 139 | RM, BB (3) |
| Reward hero (win, unlock) | 109 | 149 | 154 | 391 | RM, CBJ (3) |
| Side offer button (home) | 64 | 73 | 77 | 192 | RM, BTF (3) |
| Shop item icon (row) | 56 | 56 | 56 | 147 | RM (1) |
| Icon inside a button: video / coin | 49 / 26 | | | 129 / 68 | CBJ / RM (1 each) |
| Bottom-nav icon: inactive / active | 39 / 64 | | | 102 / 168 | RM (1 each) |
| Power-up / timer icon (action HUD) | 40 / 34 | | | 105 / 89 | ToM / Hole.io (1 each) |
Rule of thumb: corner controls 36 dp art in a 55 dp touch area; anything tapped every level (boosters, primary) ≥ 64 dp; the reward or goal is the biggest picture on its screen.

## 4. Type scale
Studio sizes are targets; the floors stay those of the test (arayuz-kalitesi-testleri.md #3). Sizes scale with the width, so each target stays above its floor on the 360 dp phone (body 20 → 17.5 dp, small 15 → 13.1).
| Role | leaders min-median-max (n; games) | studio dp (units) | floor dp (test role) | line height |
|---|---|---|---|---|
| Display / praise (win) | 50-56-60 (4; RM, CBJ, Vita, BB) | 56 (147) | 24 (Title) | 1.0 |
| Popup and screen title | 32-50-63 (13; RM, CBJ, BB, Vita) | 44 (116); long 34 | 24 (Title) | 1.0-1.1 |
| Heading (section, card name) | 26-29-31 (5; RM only) | 28 (74) | 14 (Body) | 1.1 |
| Primary button label | 25-36-55 (11; all) | 36 (95); 2 words 30 | 18 (Button) | 1.0 |
| Small button / price | 22-24-24 (4; RM, CBJ) | 24 (63) | 18 (Button) | 1.0 |
| Big number (moves, timer, score) | 23-23-74 (5; RM, CBJ, BB, Hole.io) | puzzle moves 44 (116); action timer 26 | 14 (Body) | 1.0 |
| Counter (top bar, amounts) | 17-25-42 (9) | 24 (63) | 14 (Body) | 1.0 |
| Body (1-2 lines) | 17-20-24 (5; RM, CBJ, Vita) | 20 (53) | 14 (Body) | 1.25-1.35 (Vita 1.3) |
| Label (HUD, stats, toggles) | 18-19-25 (7) | 19 (50) | 14 (Body) | 1.1 |
| Small (badge digits, version, sub-lines) | 13-18-26 (7) | 15 (39); version 14 | 12 (legal 11) | 1.1 |
- Blocks over two lines: line height ≥ 1.5 (arayuz-kurallari.md, WCAG 1.4.12).
- Weights: display, title, button, number and counter in the heavy weight with a dark outline (8-12% of the size); body and labels in regular or semibold without outline.
- Turkish runs 20-40% longer. Budgets at the studio sizes (heavy rounded face, ~0.6 em per character, 12 dp padding each side): a 222 dp button at 36 dp holds ~8 characters, a 160 dp one ~6, a 292 dp row at 24 dp ~19. Longer: the two-word size (30 dp), then rephrase; TMP auto-size minimum = the role's floor. Check price buttons with the test samples ("1.234,99 ₺", "R$ 24,90").

## 5. UI fonts (OFL, every Turkish letter; each game keeps its own title/logo font)
Checked with fontTools on 2026-10-23 (cmap: ç Ç ğ Ğ ı İ ö Ö ş Ş ü Ü â î û, ₺ € $, digits; tabular figures; weights).
| Pick | Mood / games | Roles | Weights | ₺ | tnum | x-height (em) |
|---|---|---|---|---|---|---|
| Baloo 2 | rounded, chunky: the casual puzzle default | title, button, number | 400-800 | yes | yes | 0.46 |
| Nunito | rounded, very readable | body and labels anywhere; Black for titles | 200-1000 | yes | no | 0.48 |
| Grandstander | playful, kids (Project I) | all | 100-900 | yes | yes | 0.53 |
| Alegreya Sans + Andika | calm, classic: mahjong, older players | Alegreya Sans titles and numbers, Andika body | 400-900 / 400-700 | yes | yes / no | 0.46 / 0.51 |
| Exo 2 (Saira for a narrow HUD) | sci-fi, action | all | 100-900 | yes | yes | 0.49 |
| Lexend | clean, minimal (arrow puzzle) | all | 100-900 | yes | no | 0.53 |
- The studio's own rounded display face (OFL Lilita One with the Turkish letters added) stays a display option.
- Fail Turkish: Fredoka, the original Lilita One, Sniglet, Concert One, Bubblegum Sans, Mochiy Pop One (no Ğ ğ İ Ş ş); Titan One and Atkinson Hyperlegible (no İ). Not OFL: Chewy, Luckiest Guy (Apache 2.0). Rubik, Figtree and Outfit pass Turkish but have no ₺ (prices need a fallback).
- Without tabular figures (Nunito, Andika, Lexend) wrap changing numbers in `<mspace>` or set them in a tnum face.
- Google Fonts ships the variable picks only as variable files; TMP needs one static TTF per weight: `python -m fontTools.varLib.instancer "Baloo2[wght].ttf" wght=800 --update-name-table -o Baloo2-ExtraBold.ttf` (tested: Turkish and ₺ kept). Lexend reserves the name "RevReading Lexend" for its own files.
- Grandstander's İ and Ü dots rise above its ascender (0.79-0.81 vs 0.73 em): wrapped titles ≥ 1.1 line spacing, top padding in masked boxes.

## 6. Placement rules that repeat on every screen
- Skeleton: counters and settings on top, the game or the panel in the middle, one big action in the bottom third. Top corners only for rarely tapped controls.
- Edge margins 12-16 dp for HUD and buttons (shop cards may run to 4 dp); the top bar's centre ~34 dp under the safe top; the bottom row's lower edge 8 dp above the safe-area bottom.
- Popups: panel 86-92% W centred in the safe area; close × 51-57 dp on the panel's top-right corner, centre at 90-91% W, from the first frame; the primary at the panel's bottom with the floors of §1; dimmer ~78% (alpha ~0.945 in linear space, arayuz-kurallari.md › Traps).
- Rewards sit at the panel's centre and are its biggest picture; the counter they fly into stays visible at the top.
- Revenue: the continue price lives inside the button with its currency icon; a purchase card sits below the continue, never in its place.
- Worked example (2026-10-23, a studio yarn game's reward popup, 1080×1920 capture): body 19 dp and the top bar (counter 32 dp, coin 39 dp) match; popup title 30 dp (target 44), button label 23 dp (36), primary 213×58 dp (≥ 73 dp tall), panel 80% W (88%). Those four are the first fixes.
- The pilot, the same popup after the fix (2026-10-23 evening; the same kit parts and look, only measures changed): title 44 dp, button label 36, the primary 73 dp tall at 55% W, body 20, counter 33 dp with a 37 dp icon, the window 88% of the safe area but at most 950 units: that game's canvas matches 0.5, so a fixed 950 would fill 98% on 20:9 (§1: convert through the real scale factor). No overflow on 16:9, 20:9 and a 10" tablet, in Turkish and English. On the tablet the bigger window covered two characters' faces behind it: lower the window a little there.

## 7. Limits of the data and what this changes elsewhere
- Device widths: Royal Match iPhone frames are 375 pt (exact); other recordings assumed by aspect ratio (±5%). The settings capture is tablet-shaped (structure only). Store images (Bus Traffic Fever home, Tomb of the Mask, Hole.io preview) are marketing material showing real screens; caption bands were excluded.
- Thin samples: close ×, headings, shop and settings each come from Royal Match alone; bus/car-jam only from one home image; the banner reserve from one CBJ frame. Refresh with two more leaders per screen at the next 6-month review.
- Landscape is not covered: the top bar stays on top, the insets move to the sides and the thumbs sit in the bottom corners; a landscape HUD map is the next piece.
- arayuz-kalitesi.md follows since template 1.61: pills in dp (26-35) instead of "4-5% of the height" (measured on 16:9 images), the board with its frame (86% = an 8-column board; 91-98% with frames), and the paired-button and dimmer values above.
- Raw data (every box with its source, frame and pixels; %W, dp and font dp; the measuring and drawing scripts; the drawn maps and the font specimen) stays with the studio, outside the template.
