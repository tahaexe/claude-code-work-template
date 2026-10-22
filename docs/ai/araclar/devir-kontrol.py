#!/usr/bin/env python3
"""Check the project record a newcomer depends on (template 1.59).

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
   than 10, or over 40 lines or 4,000 characters (counted with LF line ends);
5. hafiza/magaza.md or hafiza/yazisma.md over ~15,000 characters (their older
   log lines go to hafiza/arsiv/).

Usage:  python docs/ai/araclar/devir-kontrol.py [--root PROJECT]
        --root: the project folder (default: git's top level, else the current folder)
        python docs/ai/araclar/devir-kontrol.py --dene    # self-test in memory
Exit:   0 nothing to fix · 1 something to fix (listed) · 2 usage error
Read-only: it reads the project's files and writes nothing.
"""
import argparse
import pathlib
import re
import subprocess
import sys

DEVIR = "docs/ai/DEVIR.md"
MAGAZA = "docs/ai/hafiza/magaza.md"
YAZISMA = "docs/ai/hafiza/yazisma.md"
CLAUDE = "CLAUDE.md"
HAFIZA = "docs/ai/HAFIZA.md"
FILES = [DEVIR, MAGAZA, YAZISMA, CLAUDE, HAFIZA]
SECTIONS = ["Read first", "Open threads", "Handover log"]
MAX_LINES, MAX_CHARS, MAX_READ, MAX_LOG, MAX_TOPIC = 40, 4000, 6, 10, 15000
COMMENT = re.compile(r"<!--.*?-->", re.S)
PLACEHOLDER = re.compile(r"‹[^‹›\n]*›")  # a ‹…› pair; a lone › is a breadcrumb (BAKIM.md › After release)
DATED = re.compile(r"[-*]\s+\d{4}-\d{2}-\d{2}\b")
LINK = re.compile(r"`[^`]+`|\]\(")
IMPORT = re.compile(r"^@docs/ai/DEVIR\.md[ \t]*$", re.M)


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


def check(texts):
    """texts: {path: text or None}; returns the list of things to fix."""
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
        if path != DEVIR and len(text) > MAX_TOPIC:
            problems.append(f"{path}: {len(text):,} characters, over ~{MAX_TOPIC:,}: its older log lines "
                            "to docs/ai/hafiza/arsiv/, or split it by topic (BAKIM.md › Memory tidy-up)")

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
        lines = devir.count("\n") + (0 if devir.endswith("\n") or not devir else 1)
        if lines > MAX_LINES or len(devir) > MAX_CHARS:
            problems.append(f"DEVIR.md: {lines} lines, {len(devir):,} characters; limit {MAX_LINES}/{MAX_CHARS:,} "
                            "(ended threads out, older handover lines to hafiza/arsiv/devir.md)")
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
                                "older → docs/ai/hafiza/arsiv/devir.md")
    return problems


def read_project(root):
    texts = {}
    for path in FILES:
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
        DEVIR: "# Handover\n<!-- format notes ‹like this› -->\n\n## Read first\n"
               "- `planlar/2026-10-22-levels.md`: the active plan\n- `hafiza/magaza.md`: store IDs\n\n"
               "## Open threads\n- —\n\n## Handover log\n- 2026-10-22 — → agent-a: project record (1.59)\n",
        MAGAZA: "# Store and portal record\n\n## IDs\n- 2026-10-22: no store or portal yet\n\n## Listing names\n- —\n",
        YAZISMA: "# Correspondence\n<!-- `YYYY-MM-DD HH:MM · source · question or task → answer` -->\n\n"
                 "- 2026-10-22 14:40 · chat · task: install the working system → done\n",
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
    case("DEVIR over 40 lines is listed", has(check(crowded), "limit 40/4,000"))
    case("a lone dash is no content, a dated 'none yet' line is",
         content("## IDs\n- —\n") == [] and content("## IDs\n- 2026-10-22: no store yet\n") != [])
    case("a › breadcrumb is no placeholder, a ‹…› pair is",
         not PLACEHOLDER.search("Console › Production › Edit release") and PLACEHOLDER.search("- ‹store: ID›"))
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
    parser = argparse.ArgumentParser(description="Check the project record: DEVIR, magaza, yazisma.")
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
        print(f"Project record in {root}: {len(problems)} to fix")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"OK: {root} has its project record (DEVIR, magaza, yazisma, the import and HAFIZA lines).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
