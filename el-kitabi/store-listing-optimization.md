---
title: Store listing optimization (Google Play, App Store): limits, wording rules, experiments, custom pages, rating prompts, replies to reviews
condition: "Project that ships on Google Play or the App Store. Signs: Android or iOS among the targets in the game summary or memory; a store listing or App Store Connect record mentioned in the plans."
read_when: Writing or changing store texts, icon, screenshots or preview videos; planning a store A/B test or an App Store custom product page; choosing when and how to ask for a rating; testing the rating prompt; replying to store reviews; sizing a listing test for little traffic; checking a listing before it is sent for review; a game's first Play Console submission (declarations, forms).
requires: — (Play Console and App Store Connect, through the account's own Chrome profile; no third-party ASO tool or store API key)
source: Play Console Help 6227309 (store listing experiments), 9866151 (preview assets), 9898842 (metadata policy) · Android Developers "In-app reviews" · Apple developer pages: product page, product page optimization, custom product pages, ratings and reviews · App Store Connect Help "Screenshot specifications" · App Review Guidelines 2.3.7. Read 2026-10-14; experiment, custom-page and asset rules re-checked by the session manager the same night; App Store screenshot sets checked by the session manager and Claude on 2026-10-15. · Rating prompts and replies (1.51): a project session's research of 2026-10-16 (Android Developers 'In-app reviews' 2026-01-30 and 'Test in-app reviews', App Review Guidelines 5.6.1, Google Play Developer API 'Reply to Reviews' 2025-12-18; 5.6.1, the review rules and the reply API re-read 2026-10-17) · little-traffic test sizing: research topic 32 (2026-10-16), the arithmetic re-checked 2026-10-17 · 2026-10-18: App Store Connect Help 'App preview specifications', Apple 'Show more with app previews', Unity Recorder 5.1 Movie Recorder, Time.captureDeltaTime; ASOMobile 2026 and yellowHEAD 2024 (captions)
tech: Google Play Console, App Store Connect
added: 2026-10-14 · research by a project session, reviewed by the session manager · 2026-10-15 App Store screenshot sets (a project session's research, 1.46) · 2026-10-17 (1.51): rating prompt additions, replying to reviews, little-traffic test sizing · 2026-10-18 (template 1.53): screenshot order and captions, App Store preview files and content, recording in Unity (the studio's store video and screenshot research), a game's first Play submission (shared lessons) · 2026-10-22 (template 1.58): the listing similarity check (kalite-kapisi.md) · template 1.61: caption size at Play's list width (two studio store sets, 2026-10-24), AI-made frames and grounds around real gameplay (the owner's rule, 2026-10-24)
---
# Store listing optimization

## Summary
- Listing changes are free and reach all organic traffic, so they are among the cheapest ways to raise installs.
- This entry has the hard limits, the wording that gets a listing rejected or removed, and how to test one asset at a time.
- Promotional content (Play) and In-App Events (App Store): `store-events.md`. The words themselves (claims ledger, machine-sounding patterns, fresh review, listing audit): `metin-denetimi.md`.

## Limits
- **Google Play:**
  - Title ≤30 characters, short description ≤80, full description ≤4,000.
  - Icon 512×512; feature graphic 1024×500.
  - Screenshots: 2 to 8 per device type, JPEG or 24-bit PNG (no alpha), 320-3,840 px, long side at most 2× the short side.
  - Games, to be eligible for recommendation formats that use screenshots: ≥3 in-game screenshots, all 16:9 landscape (≥1920×1080) or all 9:16 portrait (≥1080×1920).
  - Alt text ≤140 characters on the feature graphic and on every screenshot.
  - Tablets and Chromebooks ("Large screens"; every mobile release since the studio's 2026-10-18 rule; Play Console's 7" and 10" slots take the same shots): at least 4 screenshots of the real game, 9:16 portrait or 16:9 landscape; that section allows sides of 1,080-7,680 px while the general rule caps 3,840, so stay within 1,080-3,840 (Help 9866151, re-read 2026-10-19). No added text near the edges, some surfaces crop. The UI matrix's tablet profile checks layout only; tablet store shots are taken 9:16.
- **App Store:**
  - Name 30, subtitle 30, promotional text 170 (changes any time without a new version; no search weight).
  - Keywords 100 characters: comma-separated, no spaces. No plurals of words already used, no category names, no "app", no competitor or trademarked names.
  - Screenshots: 1 to 10 per device size, JPEG or PNG without alpha; landscape = the sizes reversed.
    - Required on iPhone: *iPhone with Dynamic Island (medium display)* 1206×2622 or 1179×2556, plus one large set: *Dynamic Island (large display)* (6.9") 1320×2868, 1290×2796 or 1260×2736, or else *Face ID (large display)* (6.5") 1284×2778 or 1242×2688.
    - iPad 13" 2064×2752 or 2048×2732 when the game runs on iPad.
    - Sets change with new devices (e.g. iPhone Duo screenshots required from April 2027 for builds on the iOS 27.1 SDK): check Apple's *Screenshot specifications* before each submission.
  - Up to 3 app previews of ≤30 s each (autoplay muted).

## Wording and imagery that cause rejection or removal
- **Play metadata policy** (title, icon, developer name; violations can remove the app):
  - No emoji or repeated special characters; no ALL CAPS unless it is the brand.
  - No words or images that claim store performance, ranking, price or promotion: "#1", "Top", "Best", "New", "10% off", "Editor's choice".
  - No keyword lists; no unattributed testimonials.
- **Play graphics** (feature graphic, screenshots, video; Google's guidance, and promotion slots depend on it):
  - Avoid "Best", "#1", "Top", "New", "Discount", "Sale", "Million Downloads"; on the feature graphic also "Free".
  - No calls to action: "Download now", "Install now", "Play now", "Try now".
  - No store badges, no device imagery, no fingers tapping a device, no notifications.
  - Screenshot taglines take less than 20% of the image.
  - Awards from Google Play ("Best of") are allowed.
- **App Store** (App Review Guideline 2.3.7): no trademarked terms, popular app names, pricing or irrelevant phrases packed into the name, subtitle or keywords.

## Screenshots: order and captions
- The App Store shows the first three screenshots in search: frame 1 the promise, 2 the play, 3 what sets the game apart. Check every set at search size (~350 px wide) beside the genre's leaders.
- One message a frame, at most five words, an active verb or an outcome ("No timers, no lives"), not a label ("Plan every peg"); at least 60 pt in the design file (ASOMobile 2026).
- Mostly game, little empty ground: bring the camera close; large bold captions with strong contrast (yellowHEAD 2024). Play: captions under 20% of the image (above).
- **Caption size:** Play's phone listing shows portrait screenshots ~150 px and landscape ~300 px wide. Caption cap height ≥5 % of the image height (portrait) or ≥10 % (landscape), one or two lines; check the first three shots side by side at that width before upload; a language that doesn't fit gets a shorter synonym first, a smaller size last. A cap height of 3-4 % fell to 5-7 dp in the list, unreadable (two studio store sets, 2026-10-24).
- Real gameplay in every screenshot; frames, grounds and caption bands may be AI-made (tools and limits: `oyun-simgesi.md` › AI images), never the gameplay itself.
- A bottom band vs a corner box has no measured winner: test it with a Play store listing experiment before changing a shared layout.

## Preview video
- **Play** (a YouTube link):
  - Monetization off; public or unlisted, never private; not age-restricted; embeddable; one video's link (no playlist, channel or timestamp), a local version per market where it differs.
  - Google's recommendations, not conditions: real gameplay within the first 10 seconds and at least ~80% real use; few logos and cutscenes; captions; no black side bars; no "Best", "#1", "Download" or sale wording; either orientation, whichever suits the game. Only the first 30 seconds autoplay, muted. The feature graphic is the video's cover (keep its focal point).
  - A game needs a preview video to appear in some parts of Google Play.
- **App Store:** up to 3 previews per language and size, 15-30 s each, made from real app footage.
  - File: ≤ 500 MB; H.264 (`.mov`, `.m4v`, `.mp4`; up to High Profile Level 4.0, 10-12 Mbps) or ProRes 422 HQ; at most 30 fps; stereo AAC 256 kbps, 44.1 or 48 kHz.
  - The accepted resolution, not the device's: 886×1920 portrait for the classes *Dynamic Island (large display)*, *Dynamic Island (medium display)* and *Face ID (large display)* (Apple names classes, not inches), 5.5" 1080×1920, iPad 13" and 11" 1200×1600 (these two not re-verified). When the UI is the same across sizes and languages, one file at the largest required size is scaled down; a language without previews shows the nearest one's.
  - Poster frame: the 5 s mark by default, seen when autoplay is off; changing it on an approved preview needs a new version.
  - Content: only footage from the app; no people, hands or devices (graphic touch marks are fine); more gameplay than cutscenes; no prices or dates; say so if the game has in-app purchases (in the footage or the last frame). It autoplays muted in search and on the product page: on-screen text carries the message, long enough to read.
- **Recording in Unity:** Recorder's Movie Recorder (Custom size, e.g. 886×1920; H.264 MP4 or ProRes; audio needs *Project Settings › Audio › Default Speaker Mode* Mono or Stereo; the Simulator view can't be recorded), or frames at a fixed step (`Time.captureDeltaTime`) plus `AudioRenderer`, joined with ffmpeg. `Time.unscaledTime` ignores `captureDeltaTime`: UI motion on unscaled time doesn't follow a fixed-step capture.
- Music in a video needs a license that covers the store; prefer the game's own sound.

## Experiments: test one asset at a time
- **Play store listing experiments:**
  - One default-graphics experiment, or up to five localized experiments (up to five languages), at a time.
  - Up to 2 variants against the current listing. The audience share is split evenly between them.
  - Metric: unique user install clicks (or open / pre-registration clicks).
  - Advanced settings: minimum detectable effect (smaller differences end as a draw) and confidence level. A smaller effect or a higher confidence makes the test run longer.
  - Experiments stop on their own after 6 months, and nothing is applied.
  - Low-traffic games mostly end in a draw: test the biggest lever first (icon, then the first screenshot), one asset per test.
- **Little traffic: size the test first** (our arithmetic, 2026-10-16: two-proportion test, 90% confidence, 80% power, two arms):
  - Read the last 28 days' store listing visitors and conversion first (Play Console › store listing performance).
  - Visitors per arm n = 6.19 × [p1(1−p1) + p2(1−p2)] / (p2 − p1)²; days ≈ 2n / daily visitors. At 30% conversion a +20% lift needs ~760 per arm (8 days at 200 a day, 31 at 50), +10% ~2,960.
  - +20% would take over 28 days → don't test: change directly and compare 28 days before and after.
  - One variant, one change, whole weeks, duration fixed in advance; never stop on an early "significant" result; not during featuring, campaigns or release weeks; follow the applied variant's D1/D7.
- **App Store product page optimization:**
  - Icon, screenshots and previews; up to 3 treatments against the original; one test at a time; up to 90 days; iOS 15+.
  - Treatments go through App Review. Alternate icons must already be in the shipped binary, so an icon test needs a build first.
  - A running test cannot be edited. Apple suggests reading results at 90% confidence.
- **App Store custom product pages:**
  - Up to 70 extra pages with their own screenshots, previews and promotional text; no own icon.
  - Assign keywords and the page shows in search results for those keywords instead of the default page. Each keyword combination may belong to only one page.
  - Reviewed independently of an app update.
  - Apple's average: +2.5 percentage points conversion when people are sent to a custom page (1.6% → 4.1%).
  - Use them for the game's different faces (e.g. boss fights, upgrades) with matching keywords.

## Rating prompts
- **Apple:** the system prompt shows at most 3 times in 365 days, whatever the code asks. Ask after a completed level or task, never mid-play, never at launch (a later launch neither) and never as the result of a tap. Use only the system prompt: App Review 5.6.1 disallows custom review prompts, so no "Rate us?" pre-dialog on iOS either; a permanent Settings row that opens the App Store page is fine (append `?action=write-review`). Reset the summary rating only rarely, with a new version.
- **Google Play In-App Review API:**
  - A time-bound quota applies: a second call within about a month may show nothing.
  - Never wire the API to a "Rate us" button; a button opens the store listing instead.
  - Ask nothing before or while the card shows ("Do you like the game?", "5 stars?"), and never change the card.
- Testing: Play's card shows only on a device or emulator image with the Play Store (a "Google APIs" image has none), for an account that hasn't reviewed the app; an internal test track install has no quota. iOS shows the prompt every time in development builds and never in TestFlight.
- A rule like "after the 5th round, 60 days apart, at most 3 a year, at the end of a won round" fits both stores. The studio's revenue package uses it.

## Replying to reviews
- Both stores tell the reviewer about a reply, and the reviewer may update the rating; replies are public and editable.
- Reply in the reviewer's language, to the specific issue, in at most 350 characters (the Play API's limit); never ask for a higher rating; no personal data, spam, marketing or links (App Review 5.6.1, Play's policy).
- When a fix ships, reply to the reviews it answers and say so in the release notes.
- Measure in Play Console's reviews analysis (updated ratings with vs without a reply); vendor figures ("+0.42 stars") are correlations.
- Play's Reply to Reviews API sees only production reviews with text from the last week and needs an OAuth client or a service account with the reply permission: not worth it at small volume, reply in the console.

## Before sending a listing for review
- Count characters per field and language; check every image and video frame against the wording rules above; new or changed text passes metin-denetimi.md §1-3 (claims, patterns, fresh review). A studio with several games: the description, promotional text and what's new stay ≤25 % similar to its other games' listings, fix-only updates' notes too (`metin-benzerlik.py`; kalite-kapisi.md › Portfolio rules).
- Record what changed and why in the project's store notes. Sending for review needs the session manager's approval.
- Anything paid (ads, boosts, featuring purchases) is out of scope; never open it.
- **A game's first Play submission** (Project M 1.0 and Project N, 2026-10-17; first-release rules: google-play-level-up.md › Direct release):
  - A never-published app's listing can't be saved through the API (an edit commit answered 400 with `changesNotSentForReview`, 403 without): enter the first listing in Play Console with "Save as draft".
  - The Advertising ID declaration isn't among the dashboard's App content tasks, but the Publishing overview's quick check flags it once a release is saved: fill it with the other forms (*App content › Advertising ID*).
  - Forms move under the pointer: IARC opens its sections one by one and a click on an unopened one is lost; in Data safety choosing "required" moves the purpose list. Take a fresh screenshot before each click; answer "Stay" if a stale click hits the side menu and a leave-page prompt appears.
  - Play switches on the "Google Play Games on PC" form factor for a new game by itself: check the Publishing overview's pending changes and turn it off (*Advanced settings › Form factors*) unless the game was tested on PC.
  - The listing editor has no alt-text fields; the AI-generated-asset labels sit in the wizard's review step, and "Label and submit" in that dialog saves them at once.
