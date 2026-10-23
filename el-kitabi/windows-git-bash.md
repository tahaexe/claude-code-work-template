---
title: "Claude Code on Windows: Git Bash path conversion, Windows paths in files, Python flags, non-ASCII text through curl, a subagent defined mid-session"
condition: "Project worked on with Claude Code on Windows (Git Bash or PowerShell tools)."
read_when: "A path or argument arrives wrong in a native program (adb, git, python, curl); writing Windows paths or other backslash text into a file from a script or heredoc; sending Turkish or other non-ASCII text in an API request; a Python script can't import a user-installed package; a subagent type isn't found right after an install."
requires: "—"
source: "The studio projects' findings, 2026-10-17 and 2026-10-18: Project C (adb pull), the shared package's sparse checkout, Project A (an unzip into the wrong folder), a notes file with a broken path, Project L 1.5 (Play release notes), the UI research's Pillow scripts"
tech: "Windows 11, Git for Windows (MSYS2 runtime), Python 3, curl"
added: "2026-10-18 · template 1.53 · the shared lessons of the studio's sessions (the adb line moved here from unity-derleme-ve-bellek.md) · template 1.60: quoted heredocs too, a subagent defined mid-session (the shared lessons of 2026-10-22/23)"
---
# Claude Code on Windows

## Git Bash rewrites paths
- An argument that starts with `/` becomes a Windows path before a native program sees it: `adb pull /sdcard/x.csv` failed "failed to stat remote object" (Project C 2026-10-17), and `git sparse-checkout set /Packages/...` became `C:/Program Files/Git/Packages/...`. Prefix `MSYS_NO_PATHCONV=1` for `adb shell`, `adb pull`, any remote path and sparse-checkout patterns, or write `.git/info/sparse-checkout` by hand.
- After a `--no-checkout` clone, `git checkout main` brings no files until `git sparse-checkout reapply`. "Filename too long" in long scratch paths: `git config core.longpaths true`.
- The reverse: a path embedded inside code or split by `shlex` isn't converted. `python -c "...extractall(r'$S/unzip')"` with `S=/c/Users/...` made Windows Python read it from the current drive's root and write into `C:\c\Users\...`. Pass `$(cygpath -w "$S")`; where `shlex` splits a command write `/`, since it eats backslashes (`C:\a\b` → `C:ab`).

## Writing Windows paths into files
- A heredoc sent through the Bash tool collapsed a doubled backslash into one, so the Python string got `\a` (the BEL character, 0x07) and an invalid `\e`: the path written into a notes file came out broken. A quoted heredoc (`<<'PY'`) doesn't protect it either: a folder name followed by digits (`notes\2026…`) reached Python as an octal escape and the file name broke (four times in one project, 2026-10-22/23). Text that holds a backslash (a Windows path, a folder name with `\`) is written only with the Edit or Write tool; in Python use `chr(92)` or forward slashes.

## Claude Code itself
- A subagent type defined during a session (e.g. an install writing `.claude/agents/unity-uzmani.md`) can't be called in that session ("agent type not found"): give a general-purpose agent the definition file as its role there; a new session calls it directly (2026-10-23).

## Python
- `python -I` (isolated mode, the advice for scripts that read downloaded files) also hides the user's site-packages (Pillow, PyAV installed with `--user`). To keep only the script's folder off `sys.path`: `python -P <script>`.
- `python3` can open the Microsoft Store alias instead of Python: call `python`.

## Non-ASCII text through curl
- Git Bash's `curl` is a MinGW program and gets its arguments in the ANSI code page (cp1254 on a Turkish system): a UTF-8 JSON body passed as `--data-binary "$BODY"` reached Google Play with every Turkish letter and bullet turned into a space, and a later draft upload re-sent the live version's release notes in the same broken form (Project L 1.5, 2026-10-18).
- Send ASCII JSON (`json.dumps`' default; never `ensure_ascii=False`), the body from a file (`--data-binary @file`) or bytes from Python's `urllib`. Read the stored text back and compare the text itself, not just the languages. The same holds for App Store Connect (`whatsNew`) and every listing text.
