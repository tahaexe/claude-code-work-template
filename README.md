# Claude Working Template

**English** · [Türkçe](README.tr.md)

A working system for Claude Code that you can use in any project. In a project where it's installed, Claude:

- **Understands the job first and makes the call itself.** It explores big jobs, ties them to a plan and starts. It waits for your approval only when the decision is yours (scope, money, hard-to-reverse operations) or the job is big enough to split into phases.
- **Follows the plan.** It carries the plan out step by step, all the way to the end. It verifies every step, records it in the plan, commits and pushes.
- **Manages its own memory.** It keeps decisions, lessons and where it left off in files inside the project, so nothing is forgotten between sessions or computers.
- **Protects the context.** Only a small core is loaded in each session; the rest is read when needed.
- **Does browser work itself.** Jobs that need a browser (Play Console, Gemini, checking a page) are done without asking, with Claude in Chrome in its own Chrome profile (each Claude account gets a profile named after it, e.g. `alex`). It never touches your profiles or other browsers; only Claude's built-in safety confirmations remain.

You don't need to memorise commands; just talk to Claude normally.

> **Quick start, commands and troubleshooting: [User guide](KILAVUZ.md) (Turkish).**

> Template version: **1.50** (2026-10-16) · Includes an extra add-on for Unity projects (below).

> [!NOTE]
> Claude talks to you in Turkish, and the files you read (user guide, manual tests, design documents) are in Turkish. The files Claude reads itself are in English.

---

## How does it work?

| Layer | Files | When it's loaded |
|---|---|---|
| **Core** | `CLAUDE.md`, `PROTOKOL.md`, `DURUM.md`, `HAFIZA.md` | Every session, automatically |
| **Active work** | `planlar/<active plan>.md` | While working on that plan |
| **Knowledge** | `hafiza/*.md` | When the topic needs it (the memory index points to it) |
| **Rare** | `sablonlar/`, `BAKIM.md`, `KURULUM.md` | When writing a plan, when a plan ends, at install |
| **Project-specific rules** | `.claude/rules/*.md` | Only when matching files are read |

**Language:** The files Claude reads itself (protocol, status, memory, plans, rules, handbook) are written as terse English bullets, so they use fewer tokens. Claude talks to you in Turkish. The files you read stay Turkish: manual tests, design documents, the Turkish README and the user guide.

```text
Request
 ├─ Small job → do → verify → commit + push
 └─ Big job   → explore → (question) → write plan → start
                 (YOUR APPROVAL first if the decision is yours or the job has phases)
                                               ↓
    Every step:  apply → verify → record in plan → commit + push → next step
                 (blocker · decision · risky operation not in the plan → stops and asks)
                                               ↓
    Closing:     summary + manual tests (manuel-testler.md) + memory update + archive
```

## Folder structure (in the project, after install)

```text
project/
├─ CLAUDE.md                 project info: filled in by Claude at install
├─ .claude/rules/            project-specific rules: written by Claude at install
├─ .claude/settings.json     permission rules: added at install, cost no context
└─ docs/ai/
   ├─ PROTOKOL.md            working rules               (fixed)
   ├─ KURULUM.md             install and update          (fixed)
   ├─ BAKIM.md               closing and cleanup         (fixed)
   ├─ sablonlar/             CLAUDE.sablon.md, plan.md   (fixed)
   ├─ araclar/               kayip-kontrol.py            (fixed)
   ├─ DURUM.md               where we are
   ├─ HAFIZA.md              memory index
   ├─ manuel-testler.md      tests for you to run (Turkish)
   ├─ hafiza/                kararlar.md, dersler.md, teknik-borc.md, …
   └─ planlar/               YYYY-MM-DD-name.md, arsiv/
```

**Fixed** files are the same in every project and are updated from the template. The rest is the project's own data.

Unity projects also get `.claude/agents/unity-uzmani.md`, `.claude/rules/unity-*.md`, `docs/ai/sablonlar/oyun/` and `docs/ai/tasarim/` for the filled-in design documents. Handbook entries whose condition holds are installed under `docs/ai/el-kitabi/`.

---

## Install and use

Step-by-step install (including the global pointer), daily use, updating, tips and troubleshooting are in the [user guide](KILAVUZ.md) (Turkish). In short:

1. Clone this repo, for example into `C:\Users\<you>\claude-code-work-template`.
2. Add the global pointer block from the user guide (section 1) to `~/.claude/CLAUDE.md`, with your template and Unity folders. Without this block Claude doesn't recognise "şablonu kur".
3. In a project, say **"şablonu kur"** ("install the template"). Claude works out the project type from the folder (if it can't, it asks Unity or Other) and does the rest.
4. As the template evolves, say **"şablonu güncelle"** ("update the template") in the project. Only the fixed files are refreshed; plans, memory and CLAUDE.md are kept. When a new version is out, Claude mentions it in one line in the session's first reply.
5. In daily work, just talk. Big jobs get a plan and move step by step; every step is committed and pushed.

---

## Unity add-on

When you say "şablonu kur" and pick Unity as the project type, the Unity add-on is installed along with the general install. The add-on lives in `eklentiler/unity/` in the template.

| Added | Where in the project | When it's loaded |
|---|---|---|
| Unity section: skills, Unity CLI, verification, C# code intelligence | In `CLAUDE.md` | Every session |
| Unity expert agent (read-only reviews; doesn't load the CLAUDE.md chain when called) | `.claude/agents/unity-uzmani.md` | Its definition every session (~70–90 tokens), the agent itself when called |
| Code rules: assets, game code, UI, tests, shaders | `.claude/rules/unity-*.md` | Only when matching files are read |
| Test runner: with the editor closed, runs the tests with the project's Unity version, its own log file, a time limit and one import worker (less memory) | `docs/ai/araclar/testler.sh` | When tests run with the editor closed |
| C# code intelligence: new compiler errors after every `.cs` edit, definitions and references found by symbol (`csharp-lsp` plugin, `csharp-ls` language server; pitfalls in the handbook entry) | `.claude/settings.local.json` (not in git; installed separately on every computer and Claude account) | Active every session; the error report arrives when a `.cs` file is edited |
| Unity project settings: the right values per platform (handbook entry) | `docs/ai/el-kitabi/unity-proje-ayarlari.md` | In a new project, when adding a platform, preparing a release, in performance and size work |
| Game design templates: game summary (with design pillars), GDD, visual style guide, prototype report, playtest report, post-mortem, release checklist | `docs/ai/sablonlar/oyun/` (filled-in ones in `docs/ai/tasarim/`) | When used |

**Three layers keep the Unity CLI and the skills from being forgotten:**
1. The Unity section in CLAUDE.md reminds every session: use the matching `unity:*` skill first; editor, compile (`unity recompile`) and build work goes through the Unity CLI. Tests run with Pipeline's test command in an open editor and with `docs/ai/araclar/testler.sh` when the editor is closed; `unity test` isn't used (it has no log option and writes into the shared `Editor.log` that your open editor also uses). For connecting to Unity the Unity CLI comes first (your preference); the skills' MCP steps are done with the CLI too. Unity MCP isn't banned: where the CLI isn't enough, Claude may use it and says so. A missing CLI or Pipeline package is installed (without asking on the template owner's computer, asking once elsewhere).
2. The **Tool** field of every plan step. The skill or tool is picked when the plan is written and is ready in the step while running automatically.
3. The Unity rules kick in when the related files are read.

**Also during install:**
- Checks the Unity CLI, Unity's Claude plugin (`unity:*` skills) and C# code intelligence (`csharp-ls` and `csharp-lsp`; skipped if the computer has no .NET 10 SDK) and installs what's missing: without asking on the template owner's computer, asking once elsewhere. Checks whether an editor is open.
- Adds missing packages: `com.unity.pipeline` so the CLI can control the editor, `com.unity.test-framework` for tests.
- Writes the verification commands into CLAUDE.md (commands seen working in a real project are the defaults).
- Fits the rule files to the project's folder layout.
- Looks at the architecture in a project that already has code: if there are global singletons and huge manager classes, it queues a "move to a service architecture" plan candidate. The code doesn't change until you start that plan.

**Code architecture:** SOLID, clean code and a service structure are written as short bullets in the game code rule: services sit behind interfaces and are set up at a single entry point, every class has one responsibility, old code is moved over step by step. In a new game the first plan starts with the entry point where the services are set up.

**Visual identity:** For every game Claude drafts a visual style guide (colours, fonts, UI language, scene look) before the first UI job, and you correct it. After every step that changes something the player sees, Claude takes a screenshot and compares it with the guide, fixes clear deviations and puts matters of taste into the manual tests. Taste is your call; Claude checks the match with the guide. At closing, the Unity expert also reviews the screens for consistency.

**Works in the background:** While you work, the editor opens without a window, and builds and test games run in the background. A window comes forward only if a test needs it, and only after you've been told. The Unity CLI pitfalls learned in the field are in the "Unity CLI field notes" handbook entry (below).

**Release:** Claude creates the new version in the stores (Play Console, App Store Connect) and enters the release data: version name, release notes in two languages, the store listing if needed. Releases are always direct: production track at 100% on Play, automatic release after approval on the App Store; no test tracks, TestFlight or phased rollout. It sets the version numbers, builds Android (signed AAB) and iOS (Xcode project) into `Builds/` in the project folder and waits. You upload the builds to the stores and send them for review; Claude doesn't upload builds or submit them for review. For Android signing you type the keystore password into the open editor; the password is never written to any file, document or command.

**Android games:** A handbook entry is installed for the game structure Google Play recommends with Level Up (Play Games Services sign-in, achievements, Play Games Rewards, Game Stats, cloud save, FPS, large screens, controllers). The entry also covers Play Games Services' Play Console setup (consent screen, signing fingerprints, publishing the configuration), promotional content for updates, Play Console warnings (R8, edge-to-edge), what Level Up pays (fees, Quests), the memory thresholds starting in February 2027, the first release and where interstitial ads go. Three plan candidates that add this structure in the right order, and one for the warnings, are written to the **Up next** list in DURUM (see "Handbook" below).

**iOS games:** A separate handbook entry is installed for the App Store counterpart of the same structure: Game Center sign-in and achievements, a restore purchases button, In-App Events for updates, quality items, direct release settings and what to check before submitting for review (rejection risks, privacy, the age rating questionnaire, iPad, accessibility labels). Play Games Rewards and Game Stats have no iOS counterpart. One plan candidate is written.

> Adapted from: Claude-Code-Game-Studios, version `7ed2c3e` (2026-09-24). If that repo is updated, it is compared with this version.

---

## Handbook

Notes on a specific technology, platform or asset pack, compiled from outside sources (videos, articles, official docs). They live in `el-kitabi/` in the template.

- **Installed only where needed.** Every entry starts with a condition, for example "the project has Synty Sidekick characters". At install and on "şablonu güncelle", the entries whose condition holds are copied into the project and added to the shared handbook line in the memory index with a few-word hint. If the condition doesn't hold, nothing is added and the context cost in that project is zero.
- **Read only in related work.** The entry itself is opened only while working on that topic.
- **Needed tools are suggested.** If an entry needs a tool (for example Sidekick Character Creator) that the project doesn't have, Claude offers to install it. If you don't want it, it moves on and doesn't ask again.
- **Adds a plan candidate if needed.** If an entry describes work to do in the project (for example Google Play Level Up), that work is written to the **Up next** list in DURUM as a plan candidate on install. If it's already done, nothing is added.
- **Notes added in a project aren't lost.** If Claude adds a field note to an entry in a project, "şablonu güncelle" keeps it and proposes it to the template. What one project learns travels to the others.
- **Entries are in English:** Claude reads them, so they're terse English bullets.

| Entry | Condition | When it's read |
|---|---|---|
| Synty Sidekick: facial expressions and blinking | The project has Sidekick characters | Facial expression, blendshape, blinking and Face layer work |
| Synty: turning day into night | The project has Synty environment assets and uses URP | Night atmosphere, ambient light, fog, sky, post-processing and interior lighting work |
| Posing Synty characters in the editor | The project has Synty characters | Posing, and preparing promo, store or concept images |
| Ambient sound (2D) and 3D positional sound in Unity | Unity project (not Synty-specific) | Adding ambient or 3D sound, sound problems |
| The game structure Google Play recommends (Level Up) | Unity project targeting Android (Google Play) | Google Play releases (the first one too), Play Games Services, achievements, rewards, purchases, Game Stats, cloud save, FPS, large screens and controllers; looking at what Level Up pays (fees, Quests); Play Console warnings (R8, edge-to-edge), Android vitals memory metrics, promotional content and release settings; placing interstitial ads. Adds 4 plan candidates on install |
| App Store structure: Game Center, In-App Events, first submission, direct release | Unity project targeting iOS (App Store) | App Store releases and the first submission (rejection risks, privacy and ATT, privacy manifests, age questionnaire, iPad window size, accessibility labels), Game Center sign-in, achievements, leaderboards, purchases on iOS, In-App Events and iOS quality work. Adds 1 plan candidate on install |
| Unity project settings (Unity 6.3; Android, iOS, PC) and Unity's binary `.asset` files in git | Unity project | Setting up a new project (applied at once), adding a platform, preparing a release, FPS, memory, size or build problems; writing `.gitattributes`, or when a baked asset (NavMesh, lighting, terrain) differs between computers. Adds 1 plan candidate for a settings audit with Project Auditor |
| Unity CLI field notes and the windowless editor | Unity project | Unity CLI work beyond routine compiles and tests (driving the editor, eval, screenshots, PlayMode tests, packages, builds) and when a command behaves unexpectedly. Small windowless jobs open the editor with one import worker (in one project the memory peak dropped from 8.1 GB to 4.4 GB with the same duration). Compiled from the field notes of two Unity projects |
| Shader compile hitches: measure, trace, warm up (Unity 6 `GraphicsStateCollection`) | Unity 6 project | When a build hitches the first time an effect, material, area or quality level appears; preparing a release, demo or store video; moving to DX12, Vulkan or Metal; adding new quality levels or many new materials. From a project session's research |
| Browser connection: each Claude account gets its own Chrome profile | Every project | Setting up Claude's browser profile; when Claude in Chrome won't connect, errors or can't open a tab; when Claude says "opened" but you see nothing (ordered troubleshooting steps). Compiled from a project's field notes |
| Layer Lab GUI Pro UI packs (Casual Game, Survival Clean, Fantasy RPG) | The project has a GUI Pro pack or its UI will be redone with GUI Pro | UI audits, taking parts from a pack, measuring buttons and touch areas, safe area work in Unity 6000.6 |
| Player funnels, D1/D7 retention and remote config with Firebase | Unity project targeting Android or iOS with the Firebase Unity SDK | Planning or adding analytics events, looking at where players drop off, setting up Remote Config or A/B tests, difficulty or reward decisions, store privacy declarations after new events |
| Store listing and ASO (Google Play, App Store) | Project released on Google Play or the App Store | Preparing store text, icons, screenshots (including the App Store's required sizes) or preview videos; planning store A/B tests or App Store custom product pages; picking when to ask for ratings; before sending the listing for review |
| Store events: Google Play promotional content and App Store In-App Events (free visibility) | Game or app released on Google Play or the App Store | Planning a release with new player-visible content (level, mode, area, season) or a timed in-game event; writing, submitting and measuring promotional content or In-App Events; when a store rejects one. Template rule: a store-event step in the plan of every release with new content. From a project session's research |
| C# code intelligence: the `csharp-lsp` plugin and the `csharp-ls` language server; an editor-free compile check for Unity | Unity project, or any C# project with `.csproj` files | Setting up or checking C# code intelligence; when no error report arrives after a `.cs` edit or LSP calls fail; when errors that aren't real show up in a new file or after new asmdefs; touching another project's C# code; checking Unity C# code in seconds while the editor can't open (busy, closed or a heavy job queued). Tried in a Unity project; the compile check comes from two projects |
| Fair difficulty and failure: letting players blame their own choices, the failure loop, perceived luck, flow, level difficulty scores | Unity game project | Tuning difficulty and the difficulty curve; scoring solver-generated or solver-checked levels; reading fail rates and attempt counts per level; designing death, retry, continue and checkpoints; bosses and special enemies; loot, reward or offer odds; when players call something "unfair"; reading the losses in a playtest report |
| Goal layers, safe stopping points, reasons to return and healthy leaderboards | Mobile game with progression, events or leaderboards | Designing level, reward and goal flow; adding daily rewards, streaks, events, notifications or leaderboards; deciding where a session can end; looking at why players don't come back (D1/D7) |
| Competitor or reference game study (layered reading) | Game project; used only on request | Only when you or a plan asks to study a competitor or reference game. Claude doesn't start research on its own and doesn't write facts it hasn't checked |
| Colour-blind-safe palettes (colour-matching games) | The game's core rule tells pieces apart by colour (colour sort, jam, match, colour defence) | Picking the colours that carry meaning, the background or the light that paints them; writing the style guide; planning a colour-blind mode; before store images that show the palette; when a player says two colours look alike. Comes with the measuring tool `cvd_palette.py` |
| Short videos in launch week (YouTube Shorts, TikTok, Instagram Reels), without an ad budget | Game released on a store (Google Play, App Store) or preparing its launch (promoting a big update too) | Planning launch week (L-5 → L+7) or promoting a big update; making and posting short videos; putting store links on video platforms; pre-registration, pre-order and custom store page links; reaching out to creators; reading the first days' numbers. From the promo session's research |
| Reading short-video view data and a weekly review (YouTube Shorts, TikTok, Instagram Reels) | Project or folder that posts short videos of its games | Evaluating posted clips, planning the next cut or test, the weekly promo review, a clip or account with near-zero views, setting up the measurement pull (YouTube Analytics API) |

**Adding a new entry:** Open Claude Code in the template folder and type "bu videoyu el kitabına ekle: <link>" ("add this video to the handbook"). If Claude in Chrome is connected, Claude has Gemini analyse the video itself; otherwise paste the note Gemini produced. The steps and the Gemini prompt are in `el-kitabi/NASIL.md`.

---

## Settings (cost no context)

These are Claude Code's own settings. They aren't shown to Claude, so they cost no context and no usage.

- **Permission rules** (`.claude/settings.json`, added at install):
  - Step commits and push (`git add`, `git commit`, `git mv`, `git push`) run without approval. Force push isn't banned: when history has to be rewritten, Claude uses `--force-with-lease`, so commits from another computer aren't lost.
  - In Unity projects the verification commands (`unity status`, `recompile`, `test`, `list`) and installing the Pipeline package (`unity pipeline install`) also run without approval.
  - Claude in Chrome tools run without approval too. Running JavaScript on a page, like free-form C#, follows the permission mode.
  - Deleting, other package adds, builds and free-form C# open a permission prompt except in bypass mode.
  - This way fewer permission questions interrupt automatic progress.
- **Plugins** (`enabledPlugins`): superpowers is off in projects, because it brings a strict flow that tells every session "you must use this skill"; on the template owner's computers install and update also turn it off at user level (1.33). plugin-dev is only needed for developing the template: off in projects, on in the template folder. Saves an estimated 1.9–3.2k tokens per session in a project.
- **Skill list** (`skillOverrides`): The agent-protocols and engineering skills that the desktop app adds to every session are listed by name only. Their long descriptions stay out of the context, leaving room for the Unity skills; Claude can still call one when a step needs it. PROTOKOL has one line saying what these two groups are for. The unity-perf skills are hidden; for Unity only Unity's official skills are used.
- **Plugins to install:** Install and update add agent-protocols and engineering at user level if they're missing (without asking on the template owner's computer, asking once elsewhere) and remove `tianzhiying/unity-perf` wherever it's found. The desktop app brings plugins per claude.ai account, so this closes the gap between accounts.
- **Agents can't open agents** (`env`): Claude decides how many helper agents to open. The only limit is that an agent can't open its own agents: the main Claude can't see that cost. It isn't verified yet that the desktop app honours this variable.
- **`/batch` off** (`skillOverrides`): Its flow of a separate worktree and PR per part doesn't fit the projects' single-branch, step-commit routine. `/simplify` is on; Claude uses it when needed.
- After install, typing `/context` once in a new session is recommended: the core files should show and the disabled plugins' skills shouldn't.
- **Notifications:** In the desktop app the "task done", "question" and "permission needed" notifications are already on by default and can be changed in the app's settings.
- **Status line (statusLine):** Only shows in the terminal interface. It isn't shown in the desktop app, so it wasn't added.
- **Local memory off** (`autoMemoryEnabled`): The automatic memory Claude keeps on the computer is off in projects; Claude neither reads nor writes it. All memory lives in the project's `docs/ai/` folder and in git, so nothing is lost when you work on another computer. Install and update first move old notes left on the computer into the project, then delete that local folder.
- **`.gitignore`:** Install and update add editor- and computer-specific files to the ignore list: `.vscode`, `.idea`, `.vs`, Claude's local settings and worktrees, the files Windows and macOS generate; in Unity also the solution files Unity generates. Existing lines are left alone. If these files are tracked in git, they're untracked: the files stay on the computer, are deleted on the other computer at the next pull, and the editor recreates them. This keeps `git status` clean and avoids conflicts between computers.
- **`.gitattributes`:** Install and update add the `*.sh text eol=lf` line and leave existing lines alone. Because git converts line endings on Windows (`core.autocrlf=true`), `.sh` scripts (such as the test runner) arrived with CRLF in a fresh clone and didn't run in bash. In Unity projects with a rule that treats `.asset` files as text (like `*.asset text eol=lf`), `binary` lines are added after it for the `.asset` files Unity writes in binary (baked NavMesh, lighting data, terrain): otherwise every commit strips their CR LF bytes and the file comes out broken on the other computer (seen in one project's NavMesh).

---

## Context budget

**Measurement** (in a Unity project, `/context` after moving to 1.14): the core came to 20,939 characters, **8.2k tokens** (CLAUDE.md 2k, PROTOKOL 3.6k, DURUM 1.2k, HAFIZA 1.4k). That's about 1 token per 2.5 characters. The rows below are estimated with that ratio:

| Case | Loaded every session | Approx. tokens |
|---|---|---|
| Freshly installed project | ~12,200 characters | ~4,900 |
| Unity project (+ Unity section and agent definition) | ~15,000 characters | ~6,000 |
| A project filled to its limits | ~27,100 characters | ~10,800 |

The difference between Turkish and English wasn't measured: measuring a project's old Turkish core (28,600 characters) was dropped on 2 October, as the new core worked better in use. Files read when needed (estimates): plan template ~0.8k, `BAKIM.md` ~1.4k, `KURULUM.md` ~2.8k tokens.

For the exact number, open Claude Code in the project and type `/context`. The per-file breakdown is on the "Memory files" line.

The limits are defined in the protocol and Claude keeps them itself. They limit the files reloaded with every message, not Claude: without limits the files bloat (in one project DURUM had grown to 7,500 characters) and rules in a long CLAUDE.md get followed less. If a file passes its limit, Claude tidies it up itself (CLAUDE.md included):

| File | Limit |
|---|---|
| `CLAUDE.md` | at most 160 lines and 10,000 characters |
| `DURUM.md` | at most 30 lines and 3,000 characters; technical debt goes to `hafiza/teknik-borc.md` |
| `HAFIZA.md` | at most 40 lines and 3,500 characters |
| Memory topic file | split if it passes about 150 lines or 15,000 characters |
| Plan | split into phases if it has independent parts or passes about 15,000 characters; a step's description is at most 6 lines; the active plan is read piece by piece |

---

## Why this design?

- **The core is added with `@`:** Files added with `@file` load at the start of every session. A plain path without `@` doesn't load. So `@` is used only for the four small files that are always needed; the rest are given as plain paths and read when needed.
- **CLAUDE.md is re-read after compaction:** After `/compact`, the CLAUDE.md at the project root is read from disk again. Because the status is written to disk at every step, compaction or `/clear` doesn't lose work.
- **The template is named `CLAUDE.sablon.md`:** If a subfolder had a file named `CLAUDE.md`, Claude would load it automatically whenever it read a file in that folder. The different name prevents that.
- **Project-specific rules under `.claude/rules/`:** Thanks to the `paths:` field they load only when the related files are read, so they don't fill the context every session.
- **Memory is kept in the repo:** Claude's built-in automatic memory stays only on that computer and isn't in git. Memory in the repo can be used on another computer and in cloud sessions too. That's why automatic memory has been off in projects since 1.25; personal preferences and corrections are also written to `docs/ai/hafiza/`.
- **Every step is a separate commit:** Makes it easy to go back to any step during automatic progress.
- **Claude's files are in English:** Terse bullets are scanned fast, and English is expected to take fewer tokens for the same information; the gain wasn't measured (in one project the core went from 28,600 to 20,939 characters by moving content out). Turkish memory in old projects is translated once, losslessly, by "şablonu güncelle": `docs/ai/araclar/kayip-kontrol.py` checks that every command, path, number and date in the old text is still in the new text, and the originals stay in git history.
- **Nothing is lost when shortening:** When memory is tidied up or shortened, `kayip-kontrol.py` checks two things: whether the concrete facts in the old text (commands, paths, numbers, dates, names) are still in the new one, and whether any sentence fragments no longer appear together in any new line. The second catches a reason, condition or exception dropped while the rest of the line stayed ("…otherwise the references break"). Claude checks that the meaning of every listed fragment is kept. Handbook hints also keep their "when it's read" tasks when shortened; the shared line says to look at the entry's header when unsure.
- **Limits in characters too:** A line limit could be beaten with long lines (in one project a 28-line DURUM was 7,500 characters). The character limit and a separate technical debt file prevent that.
- **Claude makes the decisions:** It picks technical and design options, when to start a plan and how many helper agents to open, and writes the reason in one line. It only asks about scope, money, hard-to-reverse operations (including deletions git can't bring back) and credentials it can't make up; this cuts question-and-answer rounds and usage.
- **Rules are defaults, no fixed numbers:** The protocol's rules are defaults; where one doesn't fit, Claude does what serves the goal best and says why. Only the rule to ask before hard-to-reverse operations is fixed. Thresholds like "plan at 3 steps", "ask at 8 steps", "stop after 3 tries" and "2 agents per plan" were removed in 1.33; the rule's purpose is written in their place, so Claude can decide case by case.
- **Helper agents are Claude's call:** Parallel multi-agent systems use the most usage, so Claude opens an agent only when it will do better than its own search: broad exploration, independent parallel jobs, a closing review. Working at the same time doesn't raise total usage, it only speeds things up. Exploration uses the Explore agent, which doesn't load CLAUDE.md.

---

## Version

This repo is the public copy of version **1.50** of the template (16 October 2026). The version number is also on line 2 of `docs/ai/PROTOKOL.md`.

## License

[MIT](LICENSE)
