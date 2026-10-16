---
title: "Fair difficulty and failure: attribution, the failure loop, perceived randomness, flow, level difficulty scores"
condition: "Unity game project (ProjectSettings/ProjectVersion.txt exists and the project is a game, not a tool or app)."
read_when: "Tuning difficulty or a difficulty curve; scoring generated or solver-checked levels; reading fail rates and attempts per level; designing death, retry, continue or checkpoints; bosses or special enemies; loot, drop, reward or offer odds; players calling something unfair, cheap or rigged; reading a playtest report's losses."
requires: —
source: "Bernard Weiner, 'An attributional theory of achievement motivation and emotion' (Psychological Review, 1985) · Amos Tversky and Daniel Kahneman, 'Belief in the law of small numbers' (Psychological Bulletin, 1971) and 'Judgment under uncertainty: heuristics and biases' (Science, 1974) · Mihaly Csikszentmihalyi, Beyond Boredom and Anxiety (1975) and Flow: The Psychology of Optimal Experience (1990) · App Review Guideline 3.1.1 and Google Play's Payments policy (odds of paid random items). Written in our own words from these works. §5: Radek Pelánek, 'Difficulty Rating of Sudoku Puzzles: An Overview and Evaluation' (arXiv 1403.7373, 2014, Table 3) · Petr Jarušek and Radek Pelánek, 'Difficulty rating of Sokoban puzzle' (Frontiers in AI and Applications 222, 2010), as cited in Sina Baghal, 'Solvable Sokoban Without a Solver via Diffusion' (arXiv 2608.15958, 2026, §1.1.2) · Ahmed Khalifa, Dan Gopstein, Julian Togelius, 'ELIMINATION from Design to Analysis' (arXiv 1905.06379, 2019) · Pavel Korbut (SayGames), 'How to Work with Difficulty in Hybrid Puzzles So Players Don't Leave — but Stay and Pay' (blog.say.games, 2026-07-30). §5 sources read 2026-10-16."
tech: "Engine-independent design; Unity for the notes on tuning values (ScriptableObject or config, Remote Config where the game has Firebase) and seeded randomness."
added: 2026-10-15 · written by Claude from the published works at the session manager's request (template 1.45) · 2026-10-16 §5 (template 1.49): a project session's research, every number re-read on its source by Claude for the session manager
---
# Fair difficulty and failure

## Summary
- Players play on after a loss they can pin on their own choice, and quit after one they pin on the game.
- Four levers: a readable cause (attribution), a cheap and instructive failure loop, randomness that doesn't feel rigged, challenge that rises with skill (flow). Levels are scored on what players feel and tuned on live data (§5).
- Design side: the GDD's optional "Tempo ve zorluk eğrisi" table (`tasarim/`). Test side: the playtest report's "Kayıplar ve oyuncunun açıklaması" (`sablonlar/oyun/oyun-testi.md`).

## 1. Attribution: let the player blame their own choice
- Weiner: how people explain a failure decides what they do next. Explanations differ on three axes: inside or outside the person, stable or changeable, controllable or not.
  - "I moved too early" (inside, changeable, controllable) → retry, often with more effort.
  - "The game cheated", "I had no chance" (outside, stable, uncontrollable) → quit, bad review.
- Make the honest explanation of every loss the first kind:
  - **Telegraph** each threat that can end a run: a wind-up (animation, sound, ground marker, color change) long enough to react to on the slowest target device. Bosses and special enemies: one distinct tell per attack; introduce a new enemy alone before mixing it with others.
  - **Counterplay:** each threat has an answer the player already has (dodge, block, interrupt, positioning, a tool); show the answer before the test.
  - **Clear feedback:** what hit, from where, why it counted (hit flash, direction marker, a one-line cause or a short replay on the fail screen).
  - **Consistent rules:** hitboxes match the visuals; the same input gives the same result; no damage from off-screen or unseen sources; no hidden rules.
  - **Inputs that never betray:** a swallowed input reads as the game's fault. Buffer an input pressed slightly early, accept a jump just after leaving a ledge ("coyote time"), keep touch targets large (Android 48 dp, iOS 44 pt).
- A playtest loss blamed on the game or on luck is a design bug to fix, not a player to train.

## 2. Failure loop: cost, lesson, what is kept
- For each failure write three things in the GDD: what it **costs** (time, progress, currency, a life), what it **teaches** (its cause, readable as above), what it **keeps** (progress, unlocks, knowledge, partial rewards).
- Punishment never exceeds clarity: the higher the cost, the more obvious the cause must be. A big loss for an unclear cause is what players call unfair.
- Measure the time from failure to the next meaningful attempt (playing again, not a menu). Every screen, animation, load or ad in between adds to it; retry is one tap on the fail screen. With Firebase: the gap between a `level_end` with `success` false and the next `level_start` (`firebase-olcum-ve-uzaktan-ayar.md`).
- Checkpoints just before the hard part, not before the walk to it. Long runs keep something (meta progress, shortcuts, unlocks).
- An ad on the fail screen is part of the cost; weigh it in the game's ad plan.

## 3. Perceived randomness
- Tversky and Kahneman: people expect a short run of random results to look like the long-run odds (the "law of small numbers") and treat a success as due after a run of misses (the gambler's fallacy). Fair rolls still make streaks that players read as rigged: three misses in a row at 70% happen 2.7% of the time, so across many players they happen every day.
- **Input randomness** (rolled before the player acts: the map, the hand, the next wave, the shop) feels fair: the player plans around it. **Output randomness** (rolled after the player commits: a miss chance, a crit, a drop on a kill) decides what the player can't influence; keep it small and frequent, never the sole decider of a loss or a boss kill.
- Tame streaks:
  - Shuffle bag (draw without replacement from a bag that holds the target ratio) for drops, tiles and spawns.
  - A chance that grows after each miss and resets on a hit (pseudo-random distribution) for crits and procs.
  - Bad-luck protection ("pity timer"): a guaranteed rare reward after N misses; show the counter where money is involved.
- A shown percentage means what it says: never skew a displayed number in secret. Hidden rolls may lean in the player's favour.
- Random items bought with money (loot boxes, packs, gacha; treat premium currency as money): show the real odds before the purchase (App Review 3.1.1, Google Play Payments policy). Random rewards from rewarded ads: show the odds too (our practice).
- Unity: one seeded generator per system (`System.Random` or `Unity.Mathematics.Random`; the seed stored and logged in development builds) so a bug report or a test replays the same rolls; EditMode tests check the distribution and the streak caps with fixed seeds.

## 4. Flow: challenge rises with skill
- Csikszentmihalyi: deep absorption ("flow") comes when the challenge matches a growing skill; a challenge far below the skill bores, one far above it makes anxious. The target is a channel that rises with skill, not a straight line.
- Shape: one new demand at a time, first in a safe setting, then combined with known ones; after a peak (boss, hard level, hard night) a breather (an easier level, a reward, a calm moment). A sawtooth, not a ramp.
- Hybrid games (fast reaction and slow planning): plan the switches and announce them; a sudden switch to fast reaction after a long planning phase reads as unfair.
- Write the curve in the GDD table (new demand · expected skill · expected state: akış / sıkılma / kaygı); check it against playtest losses and, with Firebase, the fail rate per level in the funnel.
- Values live in config (ScriptableObject); with Firebase tune them with Remote Config and one-change A/B tests.
- Help after repeated failures (an offered hint, a softer retry) is fine when small and visible; never take a deserved win away from a good player (rubber-banding is noticed).

## 5. Level difficulty: score what players feel, tune on live data
- **Search effort is not human difficulty.** Models of how people solve predict it; raw search measures don't:
  - Sudoku (Pelánek 2014: >1,700 puzzles, hundreds of solvers; Pearson r with mean solving time): backtracking steps 0.16-0.25, below the plain number of givens (0.25-0.27); models of human solving techniques 0.67-0.87; a combination 0.84-0.95.
  - Sokoban (Jarušek and Pelánek 2010): state-space size had no significant correlation (r = −0.11), shortest solution length a weak one (r = 0.30); how far a puzzle splits into independent parts ρ = 0.82; a random-walk player model r = 0.76.
- **Generated or solver-checked levels** (e.g. a level factory with a difficulty score): build the score from human-like terms; state counts serve only as the search budget. Candidate terms (our hypothesis, refit on player data): the share of tempting wrong moves (traps), the number of real decisions, the solver line's estimated human time, the game's pressure, how often random play wins.
- **Shape:** the §4 sawtooth inside each block: a new element on an easy level, a rising middle, the block's peak just before a breather. A generator can hold it: ELIMINATION's evolved levels showed the intended sawtooth in play traces of almost a thousand users (Khalifa, Gopstein, Togelius 2019).
- **Read live data as attempts** (SayGames 2026): a 50% fail rate means 2 attempts on average, 80% means 5 (1 / (1 − fail rate)). Averages hide tails: an average-2 level has players at 10-20 attempts, an average-5 level some at 50 who still fail; watch a high percentile, not the mean. "Churn" at a hard level is often a pause over sessions or days: judge it over time. A level where motivated players stall (a "black hole") is fixed first.
- **Near wins** (about to lose, still a chance) make boosters and rewarded ads feel worth it (SayGames); design them into peaks, never by rigging outcomes (§3).
- **Tune:** new level chains go to a limited audience first, judged on fail rate, churn, attempts, level duration and rewarded ad views, then roll out or get refined (SayGames); soften, harden or move spikes without redrawing levels; with Firebase, Remote Config and one-change A/B tests (§4). Refit the score's weights on real fail rates.

## Checklist
- [ ] Every threat that can end a run has a tell readable on the slowest target device and an answer the player already has.
- [ ] The fail screen shows the cause at a glance; retry is one tap; the time to the next attempt is measured.
- [ ] No failure costs more than its cause is clear; long runs keep something.
- [ ] No single hidden roll decides a loss; streaks are capped (shuffle bag, growing chance or pity); shown percentages are true.
- [ ] Paid random items show their real odds before purchase.
- [ ] The GDD's tempo table has breathers; in the last playtest most losses were blamed on the players' own choices.
- [ ] Generated levels are scored on human-like terms; fail rates are read as attempts with their tails; new level chains reach a small audience first.
