---
title: "Store events: Google Play promotional content, App Store In-App Events and featuring nominations, seasons (free visibility for real in-game content)"
condition: "Game or app that ships on Google Play or the App Store. Signs: Android or iOS among the targets in the game summary or memory; a store listing or App Store Connect record mentioned in the plans."
read_when: "Planning a release that brings content players will see (levels, modes, areas, seasons) or a timed in-game event (challenge, competition, live event); writing, submitting or measuring a Play promotional content item or an App Store In-App Event; nominating a new game or big update for App Store featuring; a seasonal event; a store rejected or limited one."
requires: "— (Play Console and App Store Connect through the account's own Chrome profile)"
source: "Play Console Help 12929944 ('Reach more customers by adhering to our content quality guidelines') and 12932541 ('Create promotional content') · google.play/business/programs/promotionalcontent · google.play/business/guides/premium-growth-tools · Apple, developer.apple.com/app-store/in-app-events. All read 2026-10-16. · 2026-10-18: App Store Connect Help 'Nominate your app for featuring', developer.apple.com/app-store/getting-featured, App Store Connect API 3.8 (nominations), ASO.dev (form limits); Android Publisher v3 discovery document (revision 20261015); Play Console Help 12932541 (CSV); GameRefinery via AppSamurai (seasons)"
tech: "Google Play Console, App Store Connect"
added: "2026-10-16 · template 1.49 · research by a project session; every claim re-read on the official pages above by Claude for the session manager; featuring found limited to titles above the Premium growth tools thresholds · 2026-10-18 (template 1.53): featuring nominations, the API state of both event types, seasons (the studio's featuring, seasonal and event-API research)"
---
# Store events

## Rule (studio)
- Every release that brings content players will see gets a **store event** step in its plan: a Play promotional content item and an App Store In-App Event (Major Update or the fitting badge), dated to the release.
- Only for content that is really in the game on those dates. Never for bug fixes, UI tweaks, routine dailies, always-on content, a "we launched" announcement or a plain discount.
- Free on both stores. Discounts, offers and coupons cost money → only with the user's OK. Submit after the approval the project requires (studio: the session manager).

## Google Play: promotional content
- **Who:** all games; apps only above the Premium growth tools thresholds. Not for discounts on paid titles.
- **Where:** the store listing; it may also show on Home, Search and other Play surfaces (the algorithm picks; players see different events). Level Up games also get it on the `You` tab (`google-play-level-up.md` §8).
- **Types:** offers (discount, bonus value, reward); time-limited events (competition or challenge, real-time, special); major updates (features and announcements, content, a pre-registration update).
- **Durations:** an event ≤4 weeks (a time-limited event ends within 30 days of its start); a major update fixed at 28 days; a pre-registration announcement fixed at 1 week.
- **Timing:** submit ≤60 days and ≥4 days before the start (review takes up to 4 days; the start must be >24 h away). A submitted event can't be edited; "Copy to new event" makes a new one.
- **Rules:** for all players (only new-player offers may be targeted); runs in the game during its dates; easy to find on opening the game; no general service descriptions, evergreen content or routine events; offers worth ≥10%, never an "everyday low price" or limited quantity; tagline ≤80 characters, description ≤500; one item at a time, no repeated identical resubmissions.
- **Media:** the primary image and the required square image carry no text (no logo, slogan, game or event name) and nothing critical in the cutoff zones; an animation is optional and also text-free; a video is highly recommended: a public, embeddable, landscape YouTube video with monetization off.
- **No API:** the Android Publisher API has no promotional content endpoint (checked 2026-10-17); Play Console only, by form or by its CSV bulk upload (types `OFFER`, `TIME-LIMITED_EVENT`, `MAJOR_UPDATE`).
- **Featuring** (games: 4 broad-audience and 2 specific-audience requests a quarter, submitted ≥14 days ahead), deep links and custom audiences: only for titles above the Premium growth tools thresholds (e.g. ≥1.6M daily MAU over 3 months with ≥1.6M active installs, or ≥$40,000 consumer spend a month for 3 months). Below them, plan without featuring.
- Breaking the guidelines limits the event's exposure; empty or non-informative descriptions are rejected, busy images may be.

## App Store: In-App Events
- **Who:** Apple's page sets no threshold; events are reviewed independently of app versions. Up to 15 approved events in App Store Connect, 10 published at a time.
- **API:** the App Store Connect API has the `appEvents` resource with its localizations (a review submission item sends it), so events can be built without the browser where the project has an API key. Its `appEventScreenshots` and `appEventVideoClips` resources are deprecated (the App Asset Library and placements replace them): read the current API docs before uploading event media.
- **Where:** the product page (all published events), search results (events are searchable themselves), editorial and personalized picks on the Today, Games and Apps tabs.
- **Badges:** Challenge, Competition, Live Event, Major Update (significant new features, content or experiences, beyond UI adjustments or bug fixes), New Season, Premiere, Special Event.
- **Limits:** lasts ≤31 days, promoted up to 14 days before its start; name ≤30 characters (title case), short description ≤50, long description ≤120 (sentence case).
- **Media:** event card 16:9 (1920×1080 to 3840×2160), details page 9:16 (1080×1920 to 2160×3840), image or 30/60 fps video; avoid text and logos; no borders or gradients (the App Store adds its own).
- **Not good candidates:** daily tasks or rewards, price promotions without new content, general promotion of the app. A specific price in the metadata gets rejected. No unverifiable claims ("the best", "#1"), filler words ("game event"), a call to action as the name, all caps or excess punctuation; only content you made or license.

## App Store: featuring nominations
- **Who and where:** Account Holder, Admin, App Manager or Marketing; *Apps › the game › Featuring › Nominations › +*, or the App Store Connect API (`GET`/`POST /v1/nominations`, API 3.8+). Open to every app (no threshold), new or old.
- **Types:** App Launch (a new game or a pre-order), App Enhancements (new features, a big update), New Content (content, an offer, an event). Type and related apps can't change after sending; a sent nomination can be updated until it is archived (archived ones can be copied, not restored).
- **Form:** name ≤ 60 characters, description ≤ 1,000 (goal, priority, what's new; both limits from ASO.dev, Apple's page states none), a date or a range, up to 10 related apps from the account, an approved or live In-App Event, up to 5 links (documents, art, a public TestFlight link), supporting details ("Helpful Details": accessibility, inclusivity, the nomination's priority, anything unique about the app or team; localizations are a separate, pre-selected field); drafts allowed; a CSV bulk upload sends at once.
- **When:** as soon as the date is known: at least 3 weeks ahead (Help's recommended minimum, not a deadline); Getting Featured says at least two weeks, up to three months for wider consideration. A pre-order gives a new game that time by itself.
- **Results:** Apple says only Today-tab picks are notified (App of the Day, Game of the Day: through the App Store Connect app); editors may e-mail the Admin, App Manager and Marketing roles for art. They weigh usability, UI design, innovation, uniqueness, accessibility, localization and the product page; for games also gameplay, art and animation, controls, replay value, sound and music, technical performance and overall value. Picks are made per country.
- **Studio rule:** every new game and big update gets a nomination as a plan step, sent with the release's submission list for approval; name what editors look for (shape marks for colour-blind players, languages, calm play, art).

## Seasons (Halloween, winter holidays)
- ~90% of the top-100-grossing iOS games run seasonal events (GameRefinery, via a secondary source). The cheapest touch needs no release: Play's store icon, feature graphic and screenshots change with a listing edit (still reviewed); an App Store icon change needs a release or a PPO treatment (oyun-simgesi.md).
- Timing: an App Store event is promoted up to 14 days before it starts, so submit about three weeks ahead to use the window; Play: ≥ 4 days before the start, ≥ 14 with a featuring request. For 31 October that means Play by ~27 October and App Store visibility from 17 October; plan a winter event in October-November.

## Steps
1. Release plan: a store-event step for each release with new content: type or badge, dates (Play: submitted ≥4 days ahead; App Store: shown up to 14 days early), texts in every store language.
2. Media from the game's own captures of that content (`unity-cli-saha-notlari.md` › Screenshots), without text; for Play a public, embeddable, landscape YouTube video with monetization off.
3. Count every text against the limits in every language.
4. Create both: Play Console *Grow users › Store presence › Promotional content* with the Claude in Chrome tools (no API), App Store Connect *In-App Events* through the API or the browser; submit after approval; record them in the project (e.g. `docs/ai/tasarim/google-play-games.md`).
5. A week later: App Analytics per event (downloads, acquisition sources, impressions, details page views, app opens, players who asked to be notified) and the event's figures in Play Console; 2-3 lines in the project memory decide the next event.
