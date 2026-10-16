---
title: Store listing optimization (Google Play, App Store): limits, wording rules, experiments, custom pages, rating prompts
condition: "Project that ships on Google Play or the App Store. Signs: Android or iOS among the targets in the game summary or memory; a store listing or App Store Connect record mentioned in the plans."
read_when: Writing or changing store texts, icon, screenshots or preview videos; planning a store A/B test or an App Store custom product page; choosing when and how to ask for a rating; checking a listing before it is sent for review.
requires: — (Play Console and App Store Connect, through the account's own Chrome profile; no third-party ASO tool or store API key)
source: Play Console Help 6227309 (store listing experiments), 9866151 (preview assets), 9898842 (metadata policy) · Android Developers "In-app reviews" · Apple developer pages: product page, product page optimization, custom product pages, ratings and reviews · App Store Connect Help "Screenshot specifications" · App Review Guidelines 2.3.7. Read 2026-10-14; experiment, custom-page and asset rules re-checked by the session manager the same night; App Store screenshot sets checked by the session manager and Claude on 2026-10-15.
tech: Google Play Console, App Store Connect
added: 2026-10-14 · research by a project session, reviewed by the session manager · 2026-10-15 App Store screenshot sets (a project session's research, 1.46)
---
# Store listing optimization

## Summary
- Listing changes are free and reach all organic traffic, so they are among the cheapest ways to raise installs.
- This entry has the hard limits, the wording that gets a listing rejected or removed, and how to test one asset at a time.
- Promotional content (Play) and In-App Events (App Store): `store-events.md`.

## Limits
- **Google Play:**
  - Title ≤30 characters, short description ≤80, full description ≤4,000.
  - Icon 512×512; feature graphic 1024×500.
  - Screenshots: 2 to 8 per device type, JPEG or 24-bit PNG (no alpha), 320-3,840 px, long side at most 2× the short side.
  - Games, to be eligible for recommendation formats that use screenshots: ≥3 in-game screenshots, all 16:9 landscape (≥1920×1080) or all 9:16 portrait (≥1080×1920).
  - Alt text ≤140 characters on the feature graphic and on every screenshot.
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

## Preview video
- **Play** (a YouTube link):
  - Monetization off; public or unlisted, never private; not age-restricted; embeddable.
  - Real gameplay as early as possible within the first 10 seconds. Only the first 30 seconds autoplay, muted.
  - A game needs a preview video to appear in some parts of Google Play.
- **App Store:** up to 3 previews of ≤30 s each, made from real app footage.
- Music in a video needs a license that covers the store; prefer the game's own sound.

## Experiments: test one asset at a time
- **Play store listing experiments:**
  - One default-graphics experiment, or up to five localized experiments (up to five languages), at a time.
  - Up to 2 variants against the current listing. The audience share is split evenly between them.
  - Metric: unique user install clicks (or open / pre-registration clicks).
  - Advanced settings: minimum detectable effect (smaller differences end as a draw) and confidence level. A smaller effect or a higher confidence makes the test run longer.
  - Experiments stop on their own after 6 months, and nothing is applied.
  - Low-traffic games mostly end in a draw: test the biggest lever first (icon, then the first screenshot), one asset per test.
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
- **Apple:** the system prompt shows at most 3 times in 365 days, whatever the code asks. Ask after a completed level or task, never mid-play. Reply to reviews in App Store Connect. Reset the summary rating only rarely, with a new version.
- **Google Play In-App Review API:**
  - A time-bound quota applies: a second call within about a month may show nothing.
  - Never wire the API to a "Rate us" button; a button opens the store listing instead.
  - Ask nothing before or while the card shows ("Do you like the game?", "5 stars?"), and never change the card.
- A rule like "after the 5th round, 60 days apart, at most 3 a year, at the end of a won round" fits both stores. The studio's revenue package uses it.

## Before sending a listing for review
- Count characters per field and language; check every image and video frame against the wording rules above.
- Record what changed and why in the project's store notes. Sending for review needs the session manager's approval.
- Anything paid (ads, boosts, featuring purchases) is out of scope; never open it.
