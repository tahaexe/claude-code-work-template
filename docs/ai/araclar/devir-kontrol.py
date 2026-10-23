#!/usr/bin/env python3
"""Check the memory a newcomer depends on: the project record, every size limit, reachability (template 1.60).

The handover test: an agent that reads only CLAUDE.md (with its imports), DEVIR,
DURUM and the HAFIZA index can continue, needing nothing from an earlier agent's
Claude memory, chat, mailbox or working folder. This lists what would break it:
1. a missing or empty record file: docs/ai/DEVIR.md, docs/ai/hafiza/magaza.md,
   docs/ai/hafiza/yazisma.md. Empty: no line left once HTML comments, headings,
   blank lines, lines that hold only a dash and lines with a ‹…› placeholder go;
2. a ‹…› placeholder left in one of them (fill it, or write — for "none");
3. CLAUDE.md without its `@docs/ai/DEVIR.md` line; HAFIZA.md without a line
   for hafiza/magaza.md or hafiza/yazisma.md;
4. DEVIR without its sections (Read first, Open threads, Handover log), with no
   file in Read first or more than 6, with no dated Handover log line or more
   than 10;
5. a file over its PROTOKOL §5 limit: CLAUDE.md 160 lines/10,000 characters,
   DURUM 30/3,000, DEVIR and HAFIZA 40/4,000, every topic file under
   docs/ai/hafiza/ (not hafiza/arsiv/) ~150 lines/~15,000 (hafiza/magaza.md and
   hafiza/yazisma.md: their oldest log lines go to hafiza/arsiv/ with
   hafiza-arsiv.py), the active plan's index (DURUM's Active plan line) ~15,000;
6. a docs/ai/hafiza/**/*.md file no index reaches: links are followed from
   HAFIZA.md and DEVIR.md (read whole) through the tops of the hafiza/ files they
   name (the part before the first `## ` heading: a file family's members listed
   by file name at the top of its main file count, a mention deep in an entry
   doesn't); a mention of the folder hafiza/arsiv/ covers the archive files. A link is a path or file
   name ending in .md (in backticks, a Markdown link or plain text), read from
   docs/ai/, from the linking file's folder, from docs/ai/hafiza/ or from the
   project root; a glob (`kararlar-*.md`) or a shorthand (`-<x>.md`) reaches nothing.
Characters are counted with LF line ends, like `LC_ALL=C.UTF-8 wc -m` on an LF file.

Usage:  python docs/ai/araclar/devir-kontrol.py [--root PROJECT]
        --root: the project folder (default: git's top level, else the current folder)
        python docs/ai/araclar/devir-kontrol.py --dene    # self-test in memory
Exit:   0 nothing to fix · 1 something to fix (listed) · 2 usage error
Read-only: it reads the project's files and writes nothing.
"""
import argparse
import pathlib
import posixpath
import re
import subprocess
import sys

AI = "docs/ai"
DEVIR = "docs/ai/DEVIR.md"
MAGAZA = "docs/ai/hafiza/magaza.md"
YAZISMA = "docs/ai/hafiza/yazisma.md"
CLAUDE = "CLAUDE.md"
HAFIZA = "docs/ai/HAFIZA.md"
DURUM = "docs/ai/DURUM.md"
HAFIZA_DIR = "docs/ai/hafiza/"
ARSIV_DIR = "docs/ai/hafiza/arsiv/"
FILES = [DEVIR, MAGAZA, YAZISMA, CLAUDE, HAFIZA, DURUM]
SECTIONS = ["Read first", "Open threads", "Handover log"]
MAX_READ, MAX_LOG, MAX_TOPIC, MAX_TOPIC_LINES, MAX_PLAN = 6, 10, 15000, 150, 15000
# (lines, characters) per always-loaded file: PROTOKOL §5
LIMITS = {CLAUDE: (160, 10000), DURUM: (30, 3000), DEVIR: (40, 4000), HAFIZA: (40, 4000)}
COMMENT = re.compile(r"<!--.*?-->", re.S)
PLACEHOLDER = re.compile(r"‹[^‹›\n]*›")  # a ‹…› pair; a lone › is a breadcrumb (BAKIM.md › After release)
DATED = re.compile(r"[-*]\s+\d{4}-\d{2}-\d{2}\b")
LINK = re.compile(r"`[^`]+`|\]\(")
IMPORT = re.compile(r"^@docs/ai/DEVIR\.md[ \t]*$", re.M)
SPANS = re.compile(r"`([^`\n]+)`|\]\(([^)\s]+)\)")
BARE = re.compile(r"(?<![\w./-])((?:docs/ai/)?hafiza/[\w./-]*)")
NAME = re.compile(r"(?<![\w./<-])([\w-]+(?:\.[\w-]+)*\.md)\b")
PLAN = re.compile(r"`((?:docs/ai/)?planlar/[^`\s]+\.md)`")


def normalize(text):
    return text.replace("\r\n", "\n")


def body(text):
    """Non-blank lines outside HTML comments, stripped."""
    return [line.strip() for line in COMMENT.sub("", text).splitlines() if line.strip()]


def content(text):
    """Lines that say something: no heading, no lone dash, no placeholder."""
    return [line for line in body(text)
            if not line.startswith("#") and line.strip("-*—– ") and not PLACEHOLDER.search(line)]


def sections(text):
    """{'## heading': [its lines]} outside comments."""
    found, current = {}, None
    for line in body(text):
        heading = re.match(r"##\s+(.+)", line)
        if heading:
            current = heading.group(1).strip()
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return found


def line_count(text):
    return text.count("\n") + (0 if text.endswith("\n") or not text else 1)


def short(path):
    """docs/ai/hafiza/x.md → hafiza/x.md (PROTOKOL's paths)."""
    return path[len(AI) + 1:] if path.startswith(AI + "/") else path


def link_targets(path, text, known):
    """Repo paths (files in `known`, or folders ending in /) that `text` (the file at `path`) names."""
    raw = []
    for match in SPANS.finditer(text):
        raw.append(match.group(1) or match.group(2))
    raw += [m.group(1) for m in BARE.finditer(text)]
    raw += [m.group(1) for m in NAME.finditer(text)]
    found = set()
    folder = posixpath.dirname(path)
    for item in raw:
        item = item.strip().replace("\\", "/")
        item = re.split(r"[#\s]", item, maxsplit=1)[0]
        item = re.sub(r":\d+(?:-\d+)?$", "", item).rstrip(".,;:")
        if not item or "*" in item or "?" in item or "://" in item or "<" in item:
            continue
        for base in (AI, folder, HAFIZA_DIR.rstrip("/"), ""):
            candidate = posixpath.normpath(posixpath.join(base, item)) if base else posixpath.normpath(item)
            if item.endswith("/"):
                candidate += "/"
            key = candidate.lower()
            if key in known:
                found.add(known[key])
                break
            if item.endswith("/") and candidate.lower().startswith(HAFIZA_DIR):
                found.add(candidate)
                break
    return found


def head(text):
    """A file's top: everything before its first '## ' heading (title, comments, an index list)."""
    match = re.search(r"^## ", text, re.M)
    return text[:match.start()] if match else text


def unreached(texts):
    """hafiza/**/*.md files no link reaches from HAFIZA.md or DEVIR.md (read whole) through the tops of hafiza/ files."""
    memory = sorted(p for p, t in texts.items() if t is not None and p.startswith(HAFIZA_DIR) and p.endswith(".md"))
    known = {p.lower(): p for p in memory}
    roots = [p for p in (HAFIZA, DEVIR) if texts.get(p) is not None]
    reached, folders, queue = set(), set(), list(roots)
    seen = set(queue)
    while queue:
        path = queue.pop()
        text = texts[path] if path in roots else head(texts[path])
        for target in link_targets(path, text, known):
            if target.endswith("/"):
                folders.add(target.lower())
                continue
            reached.add(target)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    missing = []
    for path in memory:
        if path in reached:
            continue
        lowered = path.lower()
        if any(lowered.startswith(folder) and folder.startswith(ARSIV_DIR) for folder in folders):
            continue
        missing.append(path)
    return missing


def check(texts):
    """texts: {repo path: text or None}; returns the list of things to fix."""
    problems = []
    for path in (DEVIR, MAGAZA, YAZISMA):
        text = texts.get(path)
        if text is None:
            problems.append(f"missing: {path}")
            continue
        if not content(text):
            problems.append(f"empty: {path} (only comments, headings, dashes or ‹…› placeholders)")
        left = [line for line in body(text) if PLACEHOLDER.search(line)]
        if left:
            problems.append(f"placeholder left in {path}: {left[0][:90]} (fill it, or write — for none)")

    claude = texts.get(CLAUDE)
    if claude is None:
        problems.append(f"missing: {CLAUDE}")
    elif not IMPORT.search(claude):
        problems.append("CLAUDE.md has no `@docs/ai/DEVIR.md` line (Working system, after DURUM)")
    hafiza = texts.get(HAFIZA)
    if hafiza is None:
        problems.append(f"missing: {HAFIZA}")
    else:
        for name in ("hafiza/magaza.md", "hafiza/yazisma.md"):
            if name not in hafiza:
                problems.append(f"HAFIZA.md has no line for {name}")

    devir = texts.get(DEVIR)
    if devir is not None:
        found = sections(devir)
        for name in SECTIONS:
            if name not in found:
                problems.append(f"DEVIR.md has no '## {name}' section")
        if "Read first" in found:
            reads = [line for line in found["Read first"] if LINK.search(line) and not PLACEHOLDER.search(line)]
            if not reads:
                problems.append("DEVIR.md › Read first names no file")
            elif len(reads) > MAX_READ:
                problems.append(f"DEVIR.md › Read first has {len(reads)} links; keep 3-{MAX_READ}")
        if "Handover log" in found:
            log = [line for line in found["Handover log"] if DATED.match(line)]
            if not log:
                problems.append("DEVIR.md › Handover log has no dated line (YYYY-MM-DD from → to: reason)")
            elif len(log) > MAX_LOG:
                problems.append(f"DEVIR.md › Handover log has {len(log)} lines; keep the newest {MAX_LOG}, "
                                "older → docs/ai/hafiza/arsiv/devir.md (`python docs/ai/araclar/hafiza-arsiv.py devir`)")

    fixes = {CLAUDE: "details to a hafiza/ file with a one-line pointer (BAKIM.md › Memory tidy-up)",
             DURUM: "one-liners; details into the plan or hafiza/, tech debt into hafiza/teknik-borc.md",
             DEVIR: "ended threads out, older handover lines to hafiza/arsiv/devir.md (hafiza-arsiv.py)",
             HAFIZA: "a file family takes one line, its members listed at the top of its main file "
                     "(PROTOKOL §5); never trim a hint to a topic name"}
    for path, (max_lines, max_chars) in LIMITS.items():
        text = texts.get(path)
        if text is None:
            continue
        lines = line_count(text)
        if lines > max_lines or len(text) > max_chars:
            problems.append(f"{short(path)}: {lines} lines, {len(text):,} characters; limit {max_lines}/{max_chars:,}: "
                            f"{fixes[path]}")

    for path, text in sorted(texts.items()):
        if text is None or not path.startswith(HAFIZA_DIR) or path.startswith(ARSIV_DIR) or not path.endswith(".md"):
            continue
        lines = line_count(text)
        if len(text) <= MAX_TOPIC and lines <= MAX_TOPIC_LINES:
            continue
        if path in (MAGAZA, YAZISMA):
            name = posixpath.basename(path)[:-3]
            fix = (f"its oldest log lines to hafiza/arsiv/{name}.md (`python docs/ai/araclar/hafiza-arsiv.py {name}`), "
                   "or split it by topic (BAKIM.md › Memory tidy-up)")
        else:
            fix = "split it by topic, each part indexed (BAKIM.md › Memory tidy-up)"
        problems.append(f"{short(path)}: {lines} lines, {len(text):,} characters, over ~{MAX_TOPIC_LINES} "
                        f"lines/~{MAX_TOPIC:,}: {fix}")

    durum = texts.get(DURUM)
    if durum is not None:
        active = next((line for line in durum.splitlines() if "Active plan" in line), "")
        plan = PLAN.search(active)
        if plan:
            path = plan.group(1)
            path = path if path.startswith(AI + "/") else f"{AI}/{path}"
            text = texts.get(path)
            if text is None:
                problems.append(f"DURUM.md › Active plan names a missing file: {short(path)}")
            elif len(text) > MAX_PLAN:
                problems.append(f"{short(path)}: the active plan's index has {len(text):,} characters, over "
                                f"~{MAX_PLAN:,}: phases (PROTOKOL §3 Split); a one-file plan from before 1.57: its older "
                                "log entries to planlar/arsiv/<plan-name>-log.md")

    for path in unreached(texts):
        problems.append(f"{short(path)}: no index reaches it: a HAFIZA.md line, or a line at the top of its "
                        "family's main file (PROTOKOL §5)")
    return problems


def read_project(root):
    texts = {}
    for path in FILES:
        file = root / path
        texts[path] = normalize(file.read_bytes().decode("utf-8", "replace")) if file.is_file() else None
    memory = root / HAFIZA_DIR
    if memory.is_dir():
        for file in sorted(memory.rglob("*.md")):
            path = file.relative_to(root).as_posix()
            texts[path] = normalize(file.read_bytes().decode("utf-8", "replace"))
    active = next((line for line in (texts.get(DURUM) or "").splitlines() if "Active plan" in line), "")
    plan = PLAN.search(active)
    if plan:
        path = plan.group(1)
        path = path if path.startswith(AI + "/") else f"{AI}/{path}"
        file = root / path
        texts[path] = normalize(file.read_bytes().decode("utf-8", "replace")) if file.is_file() else None
    return texts


def dene():
    """Self-test on texts in memory; writes nothing."""
    good = {
        CLAUDE: "# Game\n\n## Working system\n@docs/ai/PROTOKOL.md\n@docs/ai/DURUM.md\n@docs/ai/DEVIR.md\n"
                "@docs/ai/HAFIZA.md\n",
        HAFIZA: "# Memory Index\n- `hafiza/magaza.md`: store record. → Before store work.\n"
                "- `hafiza/yazisma.md`: every Q&A and task. → Before asking again.\n",
        DEVIR: "# Handover\n<!-- format notes ‹like this›; older → `hafiza/arsiv/devir.md` -->\n\n## Read first\n"
               "- `planlar/2026-10-22-levels.md`: the active plan\n- `hafiza/magaza.md`: store IDs\n\n"
               "## Open threads\n- —\n\n## Handover log\n- 2026-10-22 — → agent-a: project record (1.59)\n",
        MAGAZA: "# Store and portal record\n\n## IDs\n- 2026-10-22: no store or portal yet\n\n## Listing names\n- —\n",
        YAZISMA: "# Correspondence\n<!-- `YYYY-MM-DD HH:MM · source · question or task → answer` -->\n\n"
                 "- 2026-10-22 14:40 · chat · task: install the working system → done\n",
        DURUM: "# Status\n- **Active plan:** `planlar/2026-10-22-levels.md` 1/4 steps done\n",
        "docs/ai/planlar/2026-10-22-levels.md": "# Plan: Levels\n- [x] **1. A**: a\n",
    }
    starter = dict(good)
    starter[DEVIR] = ("# Handover\n\n## Read first\n- ‹`path`›: ‹why›\n\n## Open threads\n- —\n\n"
                      "## Handover log\n- YYYY-MM-DD ‹from› → ‹to›: ‹reason›\n")
    starter[MAGAZA] = "# Store and portal record\n\n## IDs\n- ‹store: ID›\n"
    starter[YAZISMA] = "# Correspondence\n<!-- format -->\n\n"
    missing = dict(good)
    missing[DEVIR] = None
    missing[CLAUDE] = "# Game\n@docs/ai/PROTOKOL.md\n@docs/ai/DURUM.md\n@docs/ai/HAFIZA.md\n"
    missing[HAFIZA] = "# Memory Index\n- `hafiza/kararlar.md`: decisions.\n"
    long_log = dict(good)
    long_log[DEVIR] = good[DEVIR] + "".join(f"- 2026-10-{day:02d} agent-b → agent-c: moved\n" for day in range(1, 11))
    crowded = dict(good)
    crowded[DEVIR] = good[DEVIR].replace("## Open threads\n- —\n",
                                         "## Open threads\n" + "- 2026-10-22 · job · build\n" * 40)
    over = dict(good)
    over[HAFIZA] = good[HAFIZA] + "- `hafiza/x.md`: " + "a long hint " * 340 + "\n"
    over["docs/ai/hafiza/x.md"] = "# X\n" + "- a fact\n" * 160
    over[DURUM] = good[DURUM] + "- one more line\n" * 30
    over[CLAUDE] = good[CLAUDE] + "x" * 10000 + "\n"
    over[YAZISMA] = good[YAZISMA] + "- 2026-10-21 · chat · q → a\n" * 600
    over["docs/ai/planlar/2026-10-22-levels.md"] = "# Plan\n" + "- step text\n" * 1400
    family = dict(good)
    family[HAFIZA] = good[HAFIZA] + "- `hafiza/kararlar.md` (+ its family, listed at its top): decisions.\n"
    family["docs/ai/hafiza/kararlar.md"] = "# Decisions\n- Family: `kararlar-teknik.md` (code), `hafiza/kararlar-ui.md`.\n"
    family["docs/ai/hafiza/kararlar-teknik.md"] = "# Technical decisions\n"
    family["docs/ai/hafiza/kararlar-ui.md"] = "# UI decisions\n"
    family["docs/ai/hafiza/arsiv/devir.md"] = "# Handover log archive\n"
    family["docs/ai/hafiza/arsiv/yazisma.md"] = "# Correspondence archive\n"
    family[YAZISMA] = good[YAZISMA].replace("answer` -->", "answer`; older → `hafiza/arsiv/yazisma.md` -->")
    orphans = dict(family)
    orphans["docs/ai/hafiza/kararlar.md"] = "# Decisions\n- see `hafiza/kararlar-*.md`\n"
    orphans[DEVIR] = good[DEVIR].replace("older → `hafiza/arsiv/devir.md`", "older lines elsewhere")
    orphans[YAZISMA] = good[YAZISMA]
    checks = []

    def case(name, ok):
        ok = bool(ok)
        checks.append(ok)
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")

    def has(problems, *parts):
        return all(any(part in p for p in problems) for part in parts)

    case("a filled record passes", check(good) == [])
    case("CRLF line ends count like LF", check({k: normalize(v.replace("\n", "\r\n")) for k, v in good.items()}) == [])
    found = check(starter)
    case("starter copies fail: placeholders, empty file, no Read first file, no dated handover line",
         has(found, f"placeholder left in {DEVIR}", f"empty: {YAZISMA}", f"placeholder left in {MAGAZA}",
             "Read first names no file", "Handover log has no dated line"))
    found = check(missing)
    case("missing DEVIR, import and HAFIZA lines are listed",
         has(found, f"missing: {DEVIR}", "no `@docs/ai/DEVIR.md` line", "no line for hafiza/magaza.md",
             "no line for hafiza/yazisma.md"))
    case("an 11-line handover log is listed", has(check(long_log), "Handover log has 11 lines"))
    case("DEVIR over 40 lines is listed", has(check(crowded), "DEVIR.md: 51 lines", "limit 40/4,000"))
    case("a lone dash is no content, a dated 'none yet' line is",
         content("## IDs\n- —\n") == [] and content("## IDs\n- 2026-10-22: no store yet\n") != [])
    case("a › breadcrumb is no placeholder, a ‹…› pair is",
         not PLACEHOLDER.search("Console › Production › Edit release") and PLACEHOLDER.search("- ‹store: ID›"))
    found = check(over)
    case("every limit is listed: HAFIZA, DURUM, CLAUDE.md, a topic file, yazisma, the active plan",
         has(found, "HAFIZA.md: 4 lines", "limit 40/4,000", "DURUM.md: 32 lines", "CLAUDE.md: 8 lines",
             "hafiza/x.md: 161 lines", "hafiza/yazisma.md:", "hafiza-arsiv.py yazisma",
             "the active plan's index has"))
    case("a family listed in its main file and archives named by DEVIR and a folder link are reached",
         check(family) == [])
    found = check(orphans)
    case("a glob reaches nothing; an archive no file names is listed",
         has(found, "hafiza/kararlar-teknik.md: no index reaches it", "hafiza/kararlar-ui.md: no index",
             "hafiza/arsiv/devir.md: no index", "hafiza/arsiv/yazisma.md: no index"))
    linked = dict(orphans)
    linked[HAFIZA] = orphans[HAFIZA] + "- `hafiza/arsiv/`: older log lines, word for word.\n"
    case("a hafiza/arsiv/ folder link covers the archives",
         not has(check(linked), "hafiza/arsiv/devir.md: no index") and not has(check(linked), "arsiv/yazisma.md: no"))
    short_names = dict(good)
    short_names[HAFIZA] = good[HAFIZA] + "- Lessons: `hafiza/dersler.md` → planning; `dersler-unity.md` → Unity code.\n"
    short_names["docs/ai/hafiza/dersler.md"] = "# Lessons\n<!-- Zombies: kararlar-zombi.md (split 2026-10-11). -->\n"
    short_names["docs/ai/hafiza/dersler-unity.md"] = "# Unity lessons\n"
    short_names["docs/ai/hafiza/kararlar-zombi.md"] = "# Zombie decisions\n"
    short_names["docs/ai/hafiza/kararlar-efekt.md"] = "# Effect decisions\n"
    short_names["docs/ai/hafiza/kararlar-ses.md"] = "# Sound decisions\n"
    short_names["docs/ai/hafiza/dersler.md"] += "\n## Tests\n- 2026-10-12: see kararlar-ses.md for the mix.\n"
    found = check(short_names)
    case("a bare name and a plain-text name at a file's top reach their files; a shorthand or a mention "
         "below the first ## heading doesn't",
         len(found) == 2 and has(found, "hafiza/kararlar-efekt.md: no index", "hafiza/kararlar-ses.md: no index"))
    gone = dict(good)
    gone[DURUM] = "# Status\n- **Active plan:** `planlar/2026-10-30-gone.md` 0/3\n"
    case("an active plan line naming a missing file is listed",
         has(check(gone), "Active plan names a missing file: planlar/2026-10-30-gone.md"))
    print(f"dene: {sum(checks)}/{len(checks)} ok")
    return 0 if all(checks) else 1


def git_top():
    try:
        done = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    except OSError:
        return None
    top = done.stdout.strip()
    return pathlib.Path(top) if done.returncode == 0 and top else None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Check the project record, the memory limits and reachability.")
    parser.add_argument("--root", type=pathlib.Path, help="project folder (default: git's top level, else here)")
    parser.add_argument("--dene", action="store_true", help="self-test in memory, then exit")
    args = parser.parse_args()
    if args.dene:
        return dene()
    root = (args.root or git_top() or pathlib.Path.cwd()).resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}")
        return 2
    problems = check(read_project(root))
    if problems:
        print(f"Memory in {root}: {len(problems)} to fix")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"OK: {root} has its project record, every memory file within its limit and reached from an index.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
