<div align="center">

# Claude Code Work Template

**A plan-first working system for Claude Code.**<br>
Claude plans the work, error-checks and commits every step, tests thoroughly once before each release<br>
and keeps its memory in your repository, so nothing is lost between sessions or machines.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-work%20template-D97757?logo=claude&logoColor=white)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-1.55-2EA44F)](https://github.com/tahaexe/claude-code-work-template/tags)
[![Unity add-on](https://img.shields.io/badge/Unity%206-add--on-000000?logo=unity&logoColor=white)](#unity-add-on)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**English** · [Türkçe](README.tr.md)

[Features](#features) · [How it works](#how-it-works) · [Getting started](#getting-started) · [Daily use](#daily-use) · [Unity add-on](#unity-add-on) · [Handbook](#handbook) · [Configuration](#configuration)

</div>

---

## Features

- **Plan-first execution.** Small jobs are done right away. Big ones are explored, turned into a plan and carried out step by step; every step gets an error check (it compiles, its log is clean), is recorded in the plan, committed and pushed.
- **Memory in the repository.** Decisions, lessons and the current state live in `docs/ai/` and travel with git across sessions, computers and cloud sessions. `/clear` and `/compact` never lose work.
- **Lean context.** Only a small core (about 5k tokens in a fresh project) loads each session. Everything else is read on demand, and every file has a size limit that Claude keeps itself.
- **Autonomy with guardrails.** Claude makes the technical calls and gives the reason in one line. It stops to ask only about scope, money, hard-to-reverse operations and credentials. If a machine-level `CLAUDE.md` names a session manager, those questions go to the manager instead.
- **A quality bar.** For anything players or viewers see, Claude first studies the best examples of the same work and has the area's expert agent review the plan; at closure the work is tried and judged honestly beside those examples, and weak work is fixed before it ships.
- **Tests where they pay.** No tests while developing: an error check per step and a 2-3 minute eye check (Claude plays it and takes screenshots) at the end of each plan. Before each release one thorough stage runs every existing suite, the release checklist and a pre-release test list: levels, saves, purchases, ads and consent, the clock, interruptions, screens, sound, performance and store compliance.
- **Unity add-on.** Unity CLI first, a headless test runner, C# code intelligence, code rules built on SOLID and services, game design templates and a visual style check after every UI step.
- **Conditional handbook.** Field-tested notes on Google Play, the App Store, Firebase, ASO, shaders, Synty assets and more, installed only into projects where they apply, so they cost nothing elsewhere.
- **Browser work in its own profile.** With Claude in Chrome, Claude works in its own Chrome profile (Play Console, App Store Connect, checking a page) and never touches yours.

## How it works

```text
Request
 ├─ Small job → do → error check → commit + push
 └─ Big job   → explore → (question) → write plan → start
                 (waits for your approval only if the decision is yours or the job has phases)
                                               ↓
    Every step:  apply → error check → record in plan → commit + push → next step
                 (blocker · decision · risky operation not in the plan → stops and asks)
                                               ↓
    Closing:     eye check + summary + manual tests + memory + archive
    Release:     the pre-release test stage (every suite, checklist, test list, report)
```

| Layer | Files | Loaded |
|---|---|---|
| Core | `CLAUDE.md`, `PROTOKOL.md`, `DURUM.md`, `HAFIZA.md` | Every session |
| Active work | `planlar/<active plan>.md` | While working on that plan |
| Knowledge | `hafiza/*.md` | When the topic needs it |
| Rare | `sablonlar/`, `BAKIM.md`, `KURULUM.md` | Writing or closing a plan, installing |
| Project rules | `.claude/rules/*.md` | Only when matching files are read |

Claude's own files are terse English bullets to save tokens. File and folder names are Turkish: `PROTOKOL` is the protocol, `DURUM` the status, `HAFIZA` the memory index, `planlar` the plans.

## Getting started

### Requirements

- [Claude Code](https://claude.com/claude-code) (desktop app or CLI) and Git.
- For the Unity add-on: Unity 6 through Unity Hub. Claude installs the Unity CLI, Unity's Claude plugin and C# code intelligence when they're missing (C# code intelligence needs the .NET 10 SDK).

### Install

1. **Clone** this repository, for example into `C:\Users\<you>\claude-code-work-template`.
2. **Add the global pointer** below to `~/.claude/CLAUDE.md`, with your own folders. Without it, Claude won't recognise the install request.

   ```markdown
   ## Claude work template
   Template folder: <TEMPLATE>
   Unity projeleri klasörü: <UNITY_PROJECTS> (Unity projects folder; new Unity projects are created here)
   - When the user wants to install this working system in a project ("install the template", "şablonu kur"): read <TEMPLATE>/docs/ai/KURULUM.md and apply its "Kurulum" section.
   - When the user wants to update it ("update the template", "şablonu güncelle"): apply the "Güncelleme" section of the same file.
   - When multi-step work starts in a project without docs/ai/PROTOKOL.md, suggest installing in one sentence; don't insist.
   ```
3. **Install into a project.** Open Claude Code in the project folder and say *"install the template"* (*"şablonu kur"*). Claude detects the project type (Unity or other), copies the files, sets up git, permission rules and `CLAUDE.md`, and writes project-specific rules.
4. **Update later.** Pull this repository. A project updates itself at its next plan closure; to update at once, say *"update the template"* (*"şablonu güncelle"*). Only the fixed files are refreshed; plans, memory and `CLAUDE.md` are kept.

> [!IMPORTANT]
> **Language.** Claude talks to you in Turkish by default, and the files written for you (manual tests, game design documents, the [user guide](KILAVUZ.md)) are in Turkish. To work in English, change `Turkish with the user` to `English with the user` on line 7 of `docs/ai/PROTOKOL.md`, and the two "Turkish" mentions in steps 10 and 12 of `docs/ai/KURULUM.md`, before installing. In a project that's already installed, edit its copy.

### Project layout after install

```text
project/
├─ CLAUDE.md                 project facts, filled in by Claude
├─ .claude/rules/            project-specific rules
├─ .claude/settings.json     permission rules (no context cost)
└─ docs/ai/
   ├─ PROTOKOL.md            working rules                (fixed)
   ├─ KURULUM.md             install and update           (fixed)
   ├─ BAKIM.md               closing and cleanup          (fixed)
   ├─ sablonlar/             CLAUDE.sablon.md, plan.md    (fixed)
   ├─ araclar/               kayip-kontrol.py             (fixed)
   ├─ DURUM.md               where we are
   ├─ HAFIZA.md              memory index
   ├─ manuel-testler.md      tests for you to run
   ├─ hafiza/                decisions, lessons, technical debt, …
   └─ planlar/               dated plans and their archive
```

*Fixed* files come from the template and are refreshed on update; everything else is the project's own data.

## Daily use

There are no commands to memorise; just talk. A few phrases Claude reacts to:

| You say | What happens |
|---|---|
| *"Add an inventory system"* | A small job is done directly. A big one gets a plan that is shown and started. |
| *"Show me the plan first"* (*"önce planı göster"*) | The plan waits for your approval. |
| *"Continue"* (*"devam"*) | Finishes any half-done work, runs a quick build check and moves to the next step. |
| *"Where were we?"* (*"nerede kalmıştık?"*) | A one- or two-line status from `DURUM.md` and the active plan. |
| *"Don't do that, always do this"* | Fixes it and saves the lesson; lasting rules go into `CLAUDE.md`. |
| *"Remember this: …"* (*"bunu hatırla: …"*) | Written to the right memory file. |
| *"Memory cleanup"* (*"hafıza bakımı"*) | Merges duplicates and fixes stale facts. |

When a plan ends, Claude summarises it, adds new manual tests to `docs/ai/manuel-testler.md` and lists what couldn't be verified. Type `/clear` before the next job; the state is already on disk.

## Unity add-on

Choosing Unity at install adds:

| Added | Where | Loaded |
|---|---|---|
| Unity section: skills, Unity CLI, the error check and eye check, C# code intelligence | `CLAUDE.md` | Every session |
| Read-only Unity expert agent: architecture and plan review, closure review against the quality bar | `.claude/agents/unity-uzmani.md` | When called |
| Code rules: assets, game code, UI, tests, shaders | `.claude/rules/unity-*.md` | When matching files are read |
| Headless test runner with its own log file, a time limit and one import worker | `docs/ai/araclar/testler.sh` | The pre-release test stage, editor closed |
| C# code intelligence (`csharp-lsp` plugin, `csharp-ls` server) | `.claude/settings.local.json` | Every session |
| Game design templates: game summary with design pillars, GDD, visual style guide, prototype and playtest reports, post-mortem, release checklist | `docs/ai/sablonlar/oyun/` | When used |

- **Unity CLI first.** Editor, compile and build work goes through the Unity CLI; Unity MCP only where the CLI falls short. Missing packages (`com.unity.pipeline`, `com.unity.test-framework`) are added at install.
- **Architecture.** SOLID and services behind interfaces with a single entry point. Singleton-heavy code gets a migration plan candidate, never a silent rewrite.
- **Visual identity.** A style guide is drafted before the first UI job, and after every visible change Claude compares a screenshot with it.
- **Works in the background.** The editor runs windowless, so builds and tests don't steal your focus.
- **Store release prep.** Claude prepares store versions and builds into `Builds/`; uploading and submitting for review stay with you (or follow a session manager's rules), and signing passwords are never written anywhere.

## Handbook

The handbook (`el-kitabi/`) holds notes on specific technologies, platforms and asset packs, compiled from official docs, articles and field work. Each entry has a condition: it's installed only where the condition holds and read only during related work. Entries can add plan candidates (for example the Google Play Level Up structure), and notes a project adds to an entry are proposed back to the template on update.

<details>
<summary><b>All 37 entries</b></summary>

| Entry | Installed when |
|---|---|
| Synty Sidekick: facial expressions and blinking | The project has Sidekick characters |
| Synty: turning day into night | Synty environment assets with URP |
| Posing Synty characters in the editor | The project has Synty characters |
| Sound: ambient (2D) and 3D positional sound, the mobile mix and audio session, buying music | Unity project |
| Google Play's recommended game structure (Level Up), with the R8 check `r8-kontrol.py` | Unity project targeting Google Play |
| App Store: Game Center, In-App Events, first submission | Unity project targeting the App Store |
| Unity project settings (6.3) and binary `.asset` files in git | Unity project |
| Unity CLI field notes and the windowless editor | Unity project |
| Unity player builds: headless commands, build memory, store builds, emulator checks | Unity project |
| Shader compile hitches: measure, trace, warm up | Unity 6 project |
| Browser connection: a Chrome profile per Claude account | Every project |
| Layer Lab GUI Pro UI packs | The project uses GUI Pro |
| Player funnels, D1/D7 retention and Remote Config with Firebase | Mobile Unity project with the Firebase SDK |
| Store listing and ASO | Released on Google Play or the App Store |
| Store events: Play promotional content, App Store In-App Events and featuring nominations, seasons | Released game or app |
| C# code intelligence, an editor-free compile check and tests outside Unity | Unity or any C# project |
| Fair difficulty and failure | Unity game |
| Goal layers, safe stopping points and healthy leaderboards | Mobile game with progression, events or leaderboards |
| Competitor or reference game study, with players' own words from reviews | Game project, on request only |
| Colour-blind-safe palettes (with `cvd_palette.py`) | Colour-matching game |
| Short videos in launch week (Shorts, TikTok, Reels) | Released or launching game |
| Reading short-video metrics, a weekly review and an outlier clip's beat sheet | Project that posts short videos |
| Steam store page, Next Fest, Playtest and demo, accessibility tags | Game planned for Steam |
| Rewarded ads in puzzle and casual games: AdMob's rules, placements, sizing | Unity game with rewarded ads |
| UI quality bar: what the leaders do, screen recipes, an honest side-by-side | Unity game with player-facing UI |
| UI visual rules and traps: palette, type, buttons, touch, safe area, two languages | Unity game with player-facing UI |
| Game feel: response timing, UI motion, reduce motion, haptics, screen shake | Unity game with player-facing UI or touch input |
| UI test list: a screen matrix on 5 phone and tablet profiles in the pre-release stage, 23 automated checks | Unity game with player-facing UI |
| UI test harness: shared package layout, capture on device profiles, headless capture and fake input | Unity game with player-facing UI |
| Game icon: what reads and converts, store files, the build's icon, icon tests, alternate and seasonal icons | Released on Google Play or the App Store |
| Cute stylized look on mobile URP: faces, character shading and effects, cheap depth for low-poly scenes | Mobile URP game with characters or low-poly scenery |
| The first minute: tutorial, first win, unlock pacing, first ad and offer | Mobile game with levels |
| Local notifications for a daily reason to return (Android 13+, iOS) | Mobile game with a daily puzzle, reward or event |
| Claude Code on Windows: Git Bash path conversion, Windows paths in files, Python flags, non-ASCII text through curl | Project worked on with Claude Code on Windows |
| Public text check: claims ledger, machine-sounding patterns, fresh review, store listing audit | Project that publishes store, site, press or video text |
| YouTube thumbnails for a channel that renders its own scenes: real frames, Test & compare, policy limits | YouTube channel that renders its own scenes |
| Pre-release test list: every check before a store release (levels, saves, purchases, ads and consent, the clock, services, interruptions, screens, sound, performance, crashes and analytics, store compliance) with how, the pass bar and a report | Game shipping to a store |

</details>

To add a source, open Claude Code in the template folder and say *"add this video to the handbook: &lt;link&gt;"*. The steps and the analysis prompt are in [`el-kitabi/NASIL.md`](el-kitabi/NASIL.md).

## Configuration

What the install writes into Claude Code's own settings costs no context.

<details>
<summary><b>Settings applied at install</b></summary>

- **Permission rules** (`.claude/settings.json`): step commits and pushes run without prompts (force push only with `--force-with-lease`), as do the Unity verification commands and the Claude in Chrome tools. Deleting, other package adds, builds and free-form C# still ask outside bypass mode.
- **Plugins:** superpowers is disabled in projects because its strict flow fights the protocol; plugin-dev is on only in the template folder. This saves an estimated 1.9–3.2k tokens per session. agent-protocols and engineering are not installed and are turned off at user scope where present: the former's SessionStart hook breaks on Windows, and neither's skills were used.
- **Skill list:** `/batch` is off (a worktree and PR per part doesn't fit single-branch step commits); `/simplify` stays on.
- **No nested agents:** Claude decides how many helpers to open, but a helper can't open its own.
- **Local auto-memory off** (`autoMemoryEnabled: false`): memory lives only in `docs/ai/` and git; notes left on the computer are moved into the project once.
- **`.gitignore` and `.gitattributes`:** editor and machine files are ignored (and untracked if needed), `.sh` files keep LF, and Unity's binary `.asset` files get `binary` lines so bakes don't break between machines.

</details>

<details>
<summary><b>Context budget</b></summary>

Measured with `/context` in a Unity project: the core came to 20,939 characters, **8.2k tokens** (about 2.5 characters per token). Estimates at that ratio:

| Case | Loaded every session | ≈ Tokens |
|---|---|---|
| Freshly installed project | ~12,200 characters | ~4,900 |
| Unity project (Unity section and agent definition) | ~15,000 characters | ~6,000 |
| A project filled to its limits | ~27,600 characters | ~11,000 |

| File | Limit |
|---|---|
| `CLAUDE.md` | 160 lines, 10,000 characters |
| `DURUM.md` | 30 lines, 3,000 characters (technical debt goes to its own file) |
| `HAFIZA.md` | 40 lines, 4,000 characters |
| Memory topic file | Split past ~150 lines or 15,000 characters |
| Plan | Phased past ~15,000 characters; steps of at most 6 lines; read piece by piece |

</details>

<details>
<summary><b>Design decisions</b></summary>

- **`@` only for the core.** `@file` loads every session; plain paths are read on demand.
- **State on disk at every step,** so `/compact` and `/clear` never lose work, and `CLAUDE.md` is re-read after compaction.
- **`CLAUDE.sablon.md`, not `CLAUDE.md`,** for the template file, so it isn't auto-loaded from subfolders.
- **Rules under `.claude/rules/`** with `paths:` load only for matching files.
- **One commit per step** makes any step easy to roll back.
- **One step format:** every plan step is a single checkbox line (`- [ ] **N. Title**: details`), and `DURUM.md` starts its active-plan line with the plan's path and N/M progress, so a restart or a status tool finds the next step without reading the whole plan.
- **Lossless shortening:** `kayip-kontrol.py` checks that commands, paths, numbers, dates and dropped clauses survive when memory is condensed or translated.
- **Defaults, not fixed thresholds:** Claude adapts the rules to the situation and says why; only "ask before hard-to-reverse operations" is fixed.
- **Helpers only when they pay off:** broad exploration, independent parallel jobs, a closing review.

</details>

## Documentation

| Document | Contents |
|---|---|
| [`KILAVUZ.md`](KILAVUZ.md) | User guide: setup, daily use, updating, troubleshooting (Turkish) |
| [`docs/ai/PROTOKOL.md`](docs/ai/PROTOKOL.md) | The working protocol Claude follows |
| [`docs/ai/KURULUM.md`](docs/ai/KURULUM.md) | Install and update steps |
| [`eklentiler/unity/KURULUM-UNITY.md`](eklentiler/unity/KURULUM-UNITY.md) | Unity add-on setup |
| [`el-kitabi/`](el-kitabi) | Handbook entries |

## Acknowledgements

Parts of the Unity add-on are adapted from *Claude-Code-Game-Studios* (version `7ed2c3e`, 2026-09-24).

## License

[MIT](LICENSE) · Version **1.55** · 2026-10-21
