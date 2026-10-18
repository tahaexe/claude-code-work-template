---
title: "Goal layers, safe stopping points, reasons to return and healthy leaderboards (mobile games)"
condition: "Mobile game (Android or iOS target) with progression (levels, unlocks, upgrades), timed events or leaderboards. Signs: the game summary or memory names levels, events or leaderboards; Play Games Services or Game Center leaderboards in the plans or code. Unsure → ask the user one question."
read_when: "Designing level, reward or goal flow; adding daily rewards, streaks, events, notifications or leaderboards; deciding where a session can end; reading why players don't come back (D1/D7)."
requires: — (leaderboards through Play Games Services or Game Center, the services set up by `google-play-level-up.md` and `app-store-game-center.md`; server-side leagues need a backend, see the `unity:build-live-game` skill)
source: "Ran Kivetz, Oleg Urminsky and Yuhuang Zheng, 'The goal-gradient hypothesis resurrected' (Journal of Marketing Research, 2006) · Richard M. Ryan, C. Scott Rigby and Andrew Przybylski, 'The motivational pull of video games: a self-determination theory approach' (Motivation and Emotion, 2006) · Leon Festinger, 'A theory of social comparison processes' (Human Relations, 1954) · José P. Zagal, Staffan Björk and Chris Lewis, 'Dark patterns in the design of games' (Foundations of Digital Games, 2013) · App Review Guidelines 3.1.1, 4.5.4 and 5.6 · Google Play Payments policy · Android 13 notification permission. Written in our own words from these works. · 2026-10-18: Silverman and Barasch, 'On or Off Track: How (Broken) Streaks Affect Consumer Decisions' (Journal of Consumer Research, 2023); Duolingo's Q2 2026 shareholder letter of 2026-08-05 (via Pulse2's report of 2026-08-10); European Commission Digital Fairness fitness check (2024, via Freshfields) and DFA consultation summary (2025-12-19, via Slaughter and May)"
tech: "Engine-independent; Play Games Services and Game Center leaderboards; Firebase Analytics for D1/D7."
added: 2026-10-15 · written by Claude from the published works at the session manager's request (template 1.45) · 2026-10-18 (template 1.53): streak and daily-reward rules with evidence, revival win-back, month-calendar daily puzzle, EU direction (the studio's daily reward, streak and daily-loop research)
---
# Goal layers and reasons to return

## Summary
- Players come back for a goal they can see, to a game that let them stop on a good note. They leave for good when stopping is punished or returning feels like a chore.
- Build three goal layers and safe stopping points; give healthy reasons to return, never guilt; keep leaderboards climbable.
- Measure with D1/D7 by version (`firebase-olcum-ve-uzaktan-ayar.md` › Reading the data).

## Goal layers
- Always show three goals at once:
  - **This minute:** the current level, order or combo (the core loop).
  - **This session:** finish a world or a set, an upgrade, the daily puzzle, a chest (5-15 minutes).
  - **This week:** an event, a collection, a league rank, the next world.
- Goal gradient (Kivetz, Urminsky and Zheng): people speed up as a goal gets near, and a goal that already looks started pulls harder. Show progress as a bar or "3/5"; start a new track with a step done only when it is honest.
- Each new goal or reward names the design pillar it serves (game summary › Tasarım sütunları, where the project has one).

## Safe stopping points
- A session ends well after a finished unit (level, round, day, order): reward already given, progress saved, one next goal visible ("2 levels to the next world", "event 3/5, ends Sunday").
- Leaving never costs: no lost progress beyond the unfinished level, no resources that decay while away, no "you'll lose your streak" pop-up on exit.
- Save at every stopping point and when the app goes to the background (the OS may kill it).

## Reasons to return: healthy, not guilt
- Healthy (the player wants to): new content, a daily puzzle or challenge, a timed event with something new to do, a goal one step from done, rivals at their level.
- Guilt and chore loops (we avoid them): streaks that shame or reset to zero after one missed day, a FOMO timer on everything, energy or lives walls that stop play, appointments (come back at a set hour or lose it), nagging notifications.
- Why: self-determination theory, applied to games by Ryan, Rigby and Przybylski: players stay when play feels chosen (autonomy), masterable (competence) and shared (relatedness); pressure to return feels controlling and wears the enjoyment down. Zagal, Björk and Lewis list "playing by appointment" among the dark patterns of game design.
- Softer forms: a streak with a grace day that never drops to zero; daily rewards that pile up or can be claimed late; events of about a week so busy players fit them in.
- Streaks and daily rewards: a missed day pauses the streak or the reward cycle, never sends it back to day 1; a weekly free freeze applies itself; missed rewards stay claimable for a few days; keep and show the longest streak. Evidence: a recorded, unbroken streak drives more later engagement than the same behaviour with a broken one, the drop is bigger when people blame themselves, and a chance to repair the streak shrinks it (Silverman & Barasch, Journal of Consumer Research 2023, seven studies; the only peer-reviewed test of broken streaks found). No public 2025-2026 experiment compares soft and hard streaks in a puzzle game.
- Win-back: a one-time revival (come back, play a few levels, get your longest streak back), announced as an In-App Event or Play promotional content (store-events.md). Duolingo's June 2026 "Streak Revival": 15.4 million learners, ~8 million of them with no active streak (the letter counts learners, not streaks; Q2 2026 shareholder letter of 2026-08-05, figures via secondary reports, the letter itself unreadable; an education app: direction only).
- A daily puzzle with a month calendar: missed days of the current month stay playable and the month's badge needs about two thirds of its days, so the loop invites without punishing (Lessmore's October event asks for every day; 2026-10-18 study).
- EU direction: the Commission's Digital Fairness fitness check (October 2024) lists engagement rewards and time-limited content among addictive-design examples; a Digital Fairness Act proposal is planned for late 2026. The genre sells streak protection (Arrows – Puzzle Escape: freezers $1.49, a fixer $4.99); selling it is a pricing decision, and the coming rules argue for waiting.
- Our calm games (mahjong, cozy puzzles for older players) have no lives and no energy (a project's design rule; decide it per game in the game summary).
- Store and platform rules:
  - Promotional push only after an explicit in-app opt-in, with an in-app opt-out (App Review 4.5.4); no manipulative practices (5.6).
  - Android 13+ asks the player for the notification permission (`POST_NOTIFICATIONS`): ask when its value is clear (e.g. after the first daily reward), never at first launch; a return loop built on push reaches only those who agreed (local reminders: yerel-bildirimler.md).
  - Paid random event rewards show their odds before purchase (App Review 3.1.1, Google Play Payments policy; `adil-zorluk-ve-basarisizlik.md` where installed).

## Leaderboard health
- People compare themselves with others close to their own level (Festinger); rank 84,512 of everyone motivates nobody.
- **Weekly reset:** a fresh start every week; all-time boards come second. Play Games Services keeps daily, weekly and all-time spans; Game Center has recurring leaderboards.
- **Rank among nearby players:** open the board centered on the player (PGS `LeaderboardStart.PlayerCentered`), not at the top.
- **Small brackets or leagues:** groups of tens of players of similar level, with promotion and relegation; they need a server (Unity Gaming Services or our own; `unity:build-live-game` skill).
- **Reward tiers that real players reach:** top 10%, top 50%, everyone who took part; not only first place.
- **Stale-board check** before launch and every few weeks: top scores out of reach (cheaters, early grinders, a balance bug) mean nobody climbs and the board kills motivation → reset, cap or remove it; reject impossible scores.
- Filler entries on a quiet board (e.g. low-score placeholders while the player base is small) only with the owner's decision: they never outscore real players and never take a reward tier. Never cite player counts in promotion or store text.

## Measure
- D1 and D7 by version, the funnel over the first levels, decisions only on enough installs: `firebase-olcum-ve-uzaktan-ayar.md`.
- One return mechanic per A/B test (e.g. the daily puzzle on or off), goal: retention.
- Events: participation, completion and return on the day after the event, not only sessions.

## Checklist
- [ ] The player always sees a goal for this minute, this session and this week.
- [ ] Every safe stopping point gives the reward, saves and shows the next goal.
- [ ] No streak shame, energy wall or appointment; lives and energy only where the game summary chose them (never in calm games).
- [ ] Push only after an opt-in asked in context; opt-out inside the game.
- [ ] Leaderboards reset weekly, open around the player, have reward tiers real players reach; a stale-board check is scheduled.
