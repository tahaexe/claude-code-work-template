---
title: "Reading short-video metrics (YouTube Shorts, TikTok, Instagram Reels) and a weekly review"
condition: "Project or folder that posts short videos for its games (YouTube Shorts, TikTok, Instagram Reels). Signs: a promo calendar, a short-video upload queue or posting plan in DURUM, plans or memory. Unsure → ask the user one question."
read_when: "Judging posted clips; planning the next cut or test; the weekly promo review; a clip or an account with near-zero views; setting up metric pulls (YouTube Analytics API)."
requires: "YouTube Analytics API with the channel owner's OAuth consent for `yt-analytics.readonly` (free; the consent click belongs to the owner or the session manager, never a project session); TikTok Studio and Instagram insights read by hand in the account's own Chrome profile"
source: "Research by the promo session, 2026-10-16, pages read that day: YouTube blog 'engaged views explained' (2026-08-19) and Help 12220281 (both re-read), Help 9314415, 11914225, 16391400, 12942217; YouTube Analytics API revision history, metrics, dimensions and channel reports; TikTok Creator Academy (analytics), Display API video object (2026-08-24), Newsroom (For You 2020, Account Check 2024, Content Check Lite 2025, guidelines 2025); Instagram Help 202865988324236, 'Instagram ranking explained' (2023), Trial Reels (2024), Graph API media insights; third-party sources are marked [3P] in the text (Search Engine Journal 2023, 1of10 2026, Social Media Today 2025-2026, Social Samosa 2025)"
tech: "YouTube Shorts, TikTok, Instagram Reels; YouTube Analytics API v2. Definitions move (YouTube changed view counting in 2025 and 2026): recheck monthly (checked 2026-10-16)."
added: "2026-10-16 · template 1.50 · research by the promo session, approved by the session manager as a handbook entry with its weekly routine"
---
# Reading short-video metrics

## Summary
- Each platform counts a view differently: compare a clip only with the same platform's 4-week median for the same game, never across platforms or games.
- Diagnose in a fixed order: eligibility and reach → hook (first seconds) → middle (pacing) → ending (loop) → shares. Change one thing per test, as a new cut.
- No platform publishes benchmarks. Creator-reported targets (e.g. 70-80% "viewed" on Shorts [3P]) are lore, not goals.

## Know first: what each number means
### YouTube Shorts
- **Views:** since 2025-03-31 every start and replay of a Short counts, with no minimum; since 2026-08-24 every format counts from the first frame, autoplay included. The old count lives on as `engagedViews` (watched past the first seconds, loops excluded).
- Retention, average view duration and CTR stay on engaged views; recommendations and YPP didn't change (YouTube blog, 2026-08-19).
- **Hook:** Studio's "Stayed to watch" (a Short › "How viewers engaged"): share of times viewers stayed past the first seconds. Studio only, not in the API; the cutoff in seconds isn't published [3P].
- **Average view duration and percentage:** among those who stayed. Above 100% means loops [3P]; the API's `audienceWatchRatio` above 1 near the end says the same.
- **Retention curve** (Help 9314415): flat = watched through; gradual decline = losing interest; spike = rewatched or shared; dip = dropped or skipped there. "Typical retention" compares with the channel's last 10 videos of similar length. Key moments need ≥60 s and ≥100 views: none on 10-30 s clips.
- **Ranking inputs** (Help 11914225): the share who chose to view, average view duration and percentage, likes, surveys; competition, topic interest and season can lower impressions; "no minimum posting cadence". Shorts have no thumbnail A/B test (Help 16391400).

### TikTok
- **Studio analytics:** average watch time, "watched full video" %, retention; available on a personal account with one public post.
- **Display API:** counts only (views, likes, comments, shares, duration). Watch time, retention and traffic sources come from Studio by hand.
- **For You signals** (TikTok, 2020): interactions, video information (caption, sound, hashtags), device and account settings (weaker); finishing a longer video is a strong signal; follower count and past hits are "not direct factors".
- **Eligibility:** repeated For You rule breaks can make the whole account ineligible (notified, appealable). Account Check (last 30 posts, restrictions) is in the app: Settings and privacy › Account › Account status; the web settings' "Account control" is only deactivate/delete (checked 2026-10-16).
- **Before posting:** the web uploader (TikTok Studio › Upload) has Content check lite and a music copyright check under "Checks" once a video is selected; "No issues detected" doesn't stop a later removal. A dry run can be discarded unposted ("Delete" on the form).
- Commercial content must be disclosed (guidelines from 2025-09-13).
- **Not found officially:** definitions of the For You share, "new viewers" and view counting; a 2025-2026 statement of ranking weights; the posting hour.

### Instagram Reels
- **Views** = starts and replays; **viewers** = unique accounts that saw it (an estimate); **average watch time** = watch time ÷ first plays.
- **Skip rate** (August 2025 [3P]): share skipping in the first 3 s; every Reel has a retention chart ("the flatter the line, the more engaged your audience is"). No official threshold.
- **Signals** (Mosseri, 2025 [3P]): watch time, likes and sends rank most; watch average watch time, likes per reach and sends per reach; sends weigh more with non-followers.
- **Less reach** (Instagram, 2023): low-resolution or watermarked Reels, and Reels already posted on Instagram. Hashtags barely add reach; at most 5 per post [3P].
- **Trial Reels:** shown to non-followers first and kept off the profile; results after about 24 h, compared with earlier trials; optional sharing to followers after a strong 72 h. API: `trial_params.graduation_strategy`.
- API insights need a professional account; some metrics need 100+ followers.

## Weekly review (one day a week)
1. Clips posted 3-10 days ago (YouTube Analytics data lands 48-72 h late; trial Reels need 72 h).
2. **YouTube by API** (`yt-analytics.readonly`): Top videos report with `dimensions=video,creatorContentType`, `sort=-views`, `maxResults` ≤200 (`creatorContentType` is a dimension there, not a filter: keep the `SHORTS` rows); metrics `views,engagedViews,averageViewDuration,averageViewPercentage,likes,shares,subscribersGained`. Titles and lengths from the Data API (`videos.list`, 50 ids per call).
3. **Retention** for the best and worst 3: `dimensions=elapsedVideoTimeRatio`, `filters=video==<one id>`, metrics `audienceWatchRatio,relativeRetentionPerformance` (0.5 = median of similar-length videos). Low-traffic videos can come back empty.
4. **By hand:** Studio's stayed-to-watch; TikTok's average watch time, watched-full % and For You share; Instagram's skip rate, average watch time, sends and likes.
5. **One row per clip:** platform, game, hour, length, hook type, ending, caption; derived: watch % (average view duration ÷ length), `engagedViews ÷ views` (a lower bound of the stay rate, since views count loops), likes and sends per reach.
6. **Compare** with the same platform's 4-week median for the same game; flag the top and bottom quartile; clips under ~100 engaged views don't count (studio heuristic, YouTube's own key-moments floor).
7. Log each decision with its reason; recheck the definitions monthly.

## Diagnosis → what to change
- Low stayed-to-watch or a high skip rate → the first second: the game itself, the question or the payoff at once; on-screen text for sound-off viewers.
- The curve falls in the middle → pacing or length. No official length target ("To what length do you need to tell your story?", YouTube, 2023 [3P]).
- Average percentage ≥100% or `audienceWatchRatio` > 1 at the end → the loop works: keep the ending.
- Saves high, shares low → valuable but not shareable (Instagram's Edits blog, 2026).
- Good metrics, low reach: early Shorts views are exploratory (a few hundred or thousand, then they taper) [3P]; never repost the same Short (spam): learn and make a new cut.
- TikTok near zero → Account Check (app) and Content Check Lite first, the creative after.
- Posting hour and hashtag count are not levers on YouTube or Instagram (TikTok: not found).

## Tests
- One variable per test, as a new cut of the same footage, never a re-upload; decide after at least 3 pairs.
- Instagram: Trial Reels keep tests off the profile grid.
- A clean, watermark-free master for each platform.
