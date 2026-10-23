#!/usr/bin/env python3
"""Move the oldest dated entries of a memory log into its archive, word for word (template 1.60).

Logs and archives (paths under docs/ai/):
  devir    DEVIR.md › Handover log      → hafiza/arsiv/devir.md    over 10 dated lines: the newest 10 stay
  yazisma  hafiza/yazisma.md (the file) → hafiza/arsiv/yazisma.md  over ~15,000 characters: the oldest move
  magaza   hafiza/magaza.md › Store-state log → hafiza/arsiv/magaza.md  until the file is under 12,000,
                                                                     the newest 10 entries always stay
An entry is a dated bullet (`- YYYY-MM-DD …`) with the indented lines under it; the
oldest go by date (a tie: the lower line, as logs are newest first). The archive is
written before the source is trimmed: under the same `## ` heading, newest first, the
moved entries above the ones archived before. The source keeps a line naming its
archive (at its top, where devir-kontrol.py looks). Nothing is summarized or dropped;
lines inside HTML comments are never entries. A log the tool can't find, or a source
still over its limit after the move → "manual" (fix by hand: BAKIM.md › Memory tidy-up).

Usage:  python docs/ai/araclar/hafiza-arsiv.py [--root PROJECT] [--dry-run] [devir|yazisma|magaza …]
        (no name: all three) · --dry-run: show what would move, write nothing
        python docs/ai/araclar/hafiza-arsiv.py --dene    # self-test in memory
Exit:   0 nothing to do or moved · 1 a log needs manual work · 2 usage error
Then:   python docs/ai/araclar/kayip-kontrol.py --rev HEAD <source> <archive> (nothing may be
        missing) and commit both files together.
"""
import argparse
import pathlib
import re
import subprocess
import sys

KEEP = 10
TRIGGER, TARGET = 15000, 12000
LOGS = {
    "devir": {"source": "docs/ai/DEVIR.md", "archive": "docs/ai/hafiza/arsiv/devir.md",
              "section": "Handover log", "title": "Handover log archive", "by_count": True},
    "yazisma": {"source": "docs/ai/hafiza/yazisma.md", "archive": "docs/ai/hafiza/arsiv/yazisma.md",
                "section": None, "title": "Correspondence archive", "by_count": False},
    "magaza": {"source": "docs/ai/hafiza/magaza.md", "archive": "docs/ai/hafiza/arsiv/magaza.md",
               "section": "Store-state log", "title": "Store and portal record archive", "by_count": False},
}
DATED = re.compile(r"^[-*][ \t]+(\d{4}-\d{2}-\d{2})\b")
HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$")


def comment_mask(lines):
    """True for each line inside (or opening or closing) an HTML comment."""
    mask, inside = [], False
    for line in lines:
        start = inside
        text = line
        while True:
            if inside:
                end = text.find("-->")
                if end < 0:
                    break
                inside, text = False, text[end + 3:]
            else:
                begin = text.find("<!--")
                if begin < 0:
                    break
                inside, text = True, text[begin + 4:]
        mask.append(start or inside or "<!--" in line)
    return mask


def section_range(lines, name):
    """(first, end) line indexes of the section under `## name` (whole file when name is None)."""
    if name is None:
        return 0, len(lines)
    mask = comment_mask(lines)
    first = None
    for i, line in enumerate(lines):
        match = HEADING.match(line) if not mask[i] else None
        if match and first is None and match.group(1).strip().lower() == name.lower():
            first = i + 1
        elif match and first is not None:
            return first, i
    return (first, len(lines)) if first is not None else None


def entries(lines, first, end):
    """[(date, start, stop)] of the dated entries between first and end (stop exclusive)."""
    mask = comment_mask(lines)
    found, i = [], first
    while i < end:
        match = DATED.match(lines[i]) if not mask[i] else None
        if not match:
            i += 1
            continue
        stop = i + 1
        while stop < end and lines[stop][:1] in (" ", "\t") and lines[stop].strip():
            stop += 1
        found.append((match.group(1), i, stop))
        i = stop
    return found


def top_end(lines):
    """Index of the first '## ' heading outside comments (the end of the file's top), else the file's end."""
    mask = comment_mask(lines)
    for i, line in enumerate(lines):
        if not mask[i] and HEADING.match(line):
            return i
    return len(lines)


def plan(kind, source, archive):
    """Pure core: (new source, new archive, report, manual?) for texts with LF line ends; archive may be None."""
    spec = LOGS[kind]
    name = spec["archive"].split("docs/ai/", 1)[1]
    lines = source.split("\n")
    if not spec["by_count"] and len(source) <= TRIGGER:
        return source, archive, f"nothing to move ({len(source):,} characters)", False
    span = section_range(lines, spec["section"])
    if span is None:
        return source, archive, f"manual: no '## {spec['section']}' section in {spec['source']}", True
    found = entries(lines, *span)
    if spec["by_count"]:
        due = len(found) > KEEP
    else:
        due = len(source) > TRIGGER
    if not due:
        size = f"{len(found)} dated lines" if spec["by_count"] else f"{len(source):,} characters"
        return source, archive, f"nothing to move ({size})", False
    order = sorted(range(len(found)), key=lambda k: (found[k][0], -found[k][1]))  # oldest first
    movable = order[:max(0, len(found) - KEEP)]
    chosen = []
    if spec["by_count"]:
        chosen = movable
    else:
        size = len(source)
        for k in movable:
            if size <= TARGET:
                break
            _, start, stop = found[k]
            chosen.append(k)
            size -= sum(len(lines[j]) + 1 for j in range(start, stop))
    if not chosen:
        return source, archive, f"manual: {len(source):,} characters but no entry beyond the newest {KEEP} to move", True
    chosen.sort(key=lambda k: found[k][1])  # file order, newest first
    moved = []
    drop = set()
    for k in chosen:
        _, start, stop = found[k]
        moved.extend(lines[start:stop])
        drop.update(range(start, stop))
    kept = [line for j, line in enumerate(lines) if j not in drop]

    pointer = f"`{name}`"
    top = kept if spec["by_count"] else kept[:top_end(kept)]
    if pointer not in "\n".join(top) and name not in "\n".join(top):
        note = f"- Older entries, moved word for word: {pointer}"
        if spec["by_count"]:
            span2 = section_range(kept, spec["section"])
            at = span2[1]
            while at > span2[0] and not kept[at - 1].strip():
                at -= 1
        else:
            at = top_end(kept)
            while at > 0 and not kept[at - 1].strip():
                at -= 1
            if at == len(kept) or at == 0:
                at = len(kept)
                while at > 0 and not kept[at - 1].strip():
                    at -= 1
        kept.insert(at, note)
    new_source = "\n".join(kept)

    heading = f"## {spec['section'] or 'Correspondence'}"
    if archive is None:
        source_name = spec["source"].split("docs/ai/", 1)[1]
        new_archive = (f"# {spec['title']}\n<!-- Older entries moved word for word from `{source_name}` by "
                       f"`araclar/hafiza-arsiv.py`, newest first. Never edited; read it for an old fact the "
                       f"source no longer holds. -->\n\n{heading}\n" + "\n".join(moved) + "\n")
    else:
        alines = archive.split("\n")
        mask = comment_mask(alines)
        at = None
        for i, line in enumerate(alines):
            match = HEADING.match(line) if not mask[i] else None
            if match and ("## " + match.group(1).strip()).lower() == heading.lower():
                at = i + 1
                while at < len(alines) and mask[at]:
                    at += 1
                break
        if at is None:
            while alines and not alines[-1].strip():
                alines.pop()
            alines += ["", heading] + moved + [""]
        else:
            alines[at:at] = moved
        new_archive = "\n".join(alines)
    dates = sorted(found[k][0] for k in chosen)
    report = (f"{len(chosen)} entries ({dates[0]} … {dates[-1]}) → {name}; "
              f"{spec['source'].split('docs/ai/', 1)[1]} {len(source):,} → {len(new_source):,} characters")
    manual = False
    if not spec["by_count"] and len(new_source) > TRIGGER:
        report += f"; still over ~{TRIGGER:,}: manual (split by topic, BAKIM.md › Memory tidy-up)"
        manual = True
    return new_source, new_archive, report, manual


def decode(data):
    """(text with LF, the newline the file uses)."""
    raw = data.decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), newline


def read(path):
    """(text with LF, newline used) or (None, '\\n')."""
    if not path.is_file():
        return None, "\n"
    return decode(path.read_bytes())


def write(path, text, newline):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.write(text.replace("\n", newline))


def run(root, kinds, dry):
    manual = False
    touched = []
    for kind in kinds:
        spec = LOGS[kind]
        source_path, archive_path = root / spec["source"], root / spec["archive"]
        source, newline = read(source_path)
        if source is None:
            print(f"{kind}: no {spec['source']}; nothing to do")
            continue
        archive, archive_newline = read(archive_path)
        new_source, new_archive, report, needs_hand = plan(kind, source, archive)
        manual = manual or needs_hand
        print(f"{kind}: {report}")
        if new_source == source or dry:
            continue
        write(archive_path, new_archive, archive_newline if archive is not None else newline)  # archive first
        write(source_path, new_source, newline)
        touched += [spec["source"], spec["archive"]]
    if touched:
        print("Next: python docs/ai/araclar/kayip-kontrol.py --rev HEAD " + " ".join(touched)
              + "  (nothing may be missing), then commit them together.")
    elif dry:
        print("Dry run: nothing written.")
    return 1 if manual else 0


def dene():
    """Self-test on texts in memory; writes nothing."""
    checks = []

    def case(name, ok):
        ok = bool(ok)
        checks.append(ok)
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")

    head = ("# Correspondence\n<!-- One line each, newest first. A 2026-01-01 date in a comment is no entry:\n"
            "- 2026-01-01 · not an entry -->\n\n")
    lines = [f"- 2026-10-{30 - i // 3:02d} 1{i % 10}:00 · mailbox · question {i} " + "x" * 260 for i in range(60)]
    lines[5] += "\n  - an indented note that belongs to entry 5"
    yazisma = head + "\n".join(lines) + "\n"
    new, arch, report, manual = plan("yazisma", yazisma, None)
    old_lines, new_lines, arch_lines = set(yazisma.split("\n")), set(new.split("\n")), set(arch.split("\n"))
    case("yazisma over 15,000 drops under 12,000, newest kept, oldest moved",
         len(yazisma) > TRIGGER and len(new) <= TARGET and lines[0] in new and lines[-1] in arch and not manual)
    case("every old line survives word for word in the source or the archive",
         old_lines <= (new_lines | arch_lines))
    case("the comment's dated line is not moved", "- 2026-01-01 · not an entry -->" in new
         and "2026-01-01" not in arch)
    case("an indented note moves with its entry, or stays with it",
         ("an indented note" in new) == (lines[5].split("\n")[0] in new))
    case("the source names its archive (a file without ## headings: after its last entry)",
         new.rstrip("\n").endswith("`hafiza/arsiv/yazisma.md`"))
    case("the archive starts with its title, comment and heading",
         arch.startswith("# Correspondence archive\n<!--") and "\n## Correspondence\n- 2026" in arch)
    new2, arch2, report2, _ = plan("yazisma", new, arch)
    case("a second run under the limit moves nothing", new2 == new and arch2 == arch and "nothing" in report2)
    fresh = "".join(f"- 2026-11-{9 - i // 4:02d} 08:00 · chat · new question {i} " + "y" * 300 + "\n" for i in range(30))
    at = new.index(lines[0])
    newer = new[:at] + fresh + new[at:]
    new3, arch3, _, _ = plan("yazisma", newer, arch)
    dates = re.findall(r"^- (\d{4}-\d{2}-\d{2})", arch3, re.M)
    case("a later run puts its (newer) entries above the archived ones: the archive stays newest first",
         len(dates) > len(re.findall(r"^- \d{4}", arch, re.M)) and dates == sorted(dates, reverse=True))
    case("…and the source still names its archive once", new3.count("hafiza/arsiv/yazisma.md") == 1)
    devir = ("# Handover\n<!-- older → `hafiza/arsiv/devir.md` -->\n\n## Read first\n- `DURUM.md`: state\n\n"
             "## Open threads\n- —\n\n## Handover log\n"
             + "".join(f"- 2026-10-{23 - i:02d} a{i} → a{i + 1}: work\n" for i in range(13)))
    new4, arch4, report4, manual4 = plan("devir", devir, None)
    case("DEVIR keeps its newest 10 handover lines, the 3 oldest go to arsiv/devir.md",
         new4.count("\n- 2026-10-") == 10 and arch4.count("\n- 2026-10-") == 3 and "- 2026-10-23 a0" in new4
         and "- 2026-10-11 a12" in arch4 and not manual4)
    case("DEVIR's comment already names the archive: no extra line", new4.count("hafiza/arsiv/devir.md") == 1)
    magaza = "# Store and portal record\n\n## IDs\n- com.example.game\n\n## Products and prices\n- —\n"
    _, _, report5, manual5 = plan("magaza", magaza + "x" * 16000, None)
    _, _, report5b, manual5b = plan("magaza", magaza, None)
    case("magaza without a Store-state log section: over the limit manual and unchanged, under it nothing to do",
         manual5 and "manual" in report5 and not manual5b and "nothing" in report5b)
    store = ("# Store and portal record\n<!-- record -->\n\n## IDs\n- " + "id " * 1500 + "\n\n## Store-state log\n"
             + "".join(f"- 2026-10-{28 - i // 2:02d} · play · 1.{i} · released → ok " + "z" * 500 + "\n" for i in range(24))
             + "\n## Products and prices\n- —\n")
    new6, arch6, report6, manual6 = plan("magaza", store, None)
    kept6 = re.findall(r"^- 2026-10-\d\d · play", new6, re.M)
    case("magaza moves only Store-state log entries, names its archive at its top, keeps the other sections",
         new6.index("`hafiza/arsiv/magaza.md`") < new6.index("## IDs") < new6.index("## Store-state log")
         and "## Products and prices" in new6 and len(new6) <= TARGET + 100 and len(kept6) >= KEEP
         and "\n## Store-state log\n- 2026-10-" in arch6 and not manual6)
    case("CRLF is read as LF and its newline kept for the write",
         decode(b"# T\r\n- 2026-10-01 x\r\n") == ("# T\n- 2026-10-01 x\n", "\r\n")
         and decode(b"# T\n")[1] == "\n")
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
    parser = argparse.ArgumentParser(description="Move the oldest dated memory log entries to hafiza/arsiv/, word for word.")
    parser.add_argument("logs", nargs="*", help="devir, yazisma, magaza (default: all three)")
    parser.add_argument("--root", type=pathlib.Path, help="project folder (default: git's top level, else here)")
    parser.add_argument("--dry-run", action="store_true", help="show what would move, write nothing")
    parser.add_argument("--dene", action="store_true", help="self-test in memory, then exit")
    args = parser.parse_args()
    if args.dene:
        return dene()
    unknown = [name for name in args.logs if name not in LOGS]
    if unknown:
        print(f"Unknown log: {', '.join(unknown)} (use devir, yazisma, magaza)")
        return 2
    root = (args.root or git_top() or pathlib.Path.cwd()).resolve()
    if not (root / "docs/ai").is_dir():
        print(f"No docs/ai/ in {root}")
        return 2
    return run(root, args.logs or list(LOGS), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
