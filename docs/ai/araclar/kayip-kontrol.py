#!/usr/bin/env python3
"""Check that rewritten Claude memory files kept every fact and every point.

Reads the old versions of the given files from a git revision and lists:
1. facts (code spans, URLs, paths, file names, dates, identifiers, numbers)
   that no longer appear in the new versions in the working tree;
2. old clauses whose words don't come back together in any one new line:
   lines are cut at punctuation and before "or", "unless", "because", "but",
   "if"… (also "yoksa", "çünkü", "ama"…), so a dropped reason, condition or
   exception shows up even when the rest of its line survived. The fact check
   can't see such losses in plain prose. It's a heuristic: rewording to new
   words or splitting a clause over lines can be listed too, so review each.
Facts and clauses may move between the given files: all new files are checked
as one text.

Usage:  python docs/ai/araclar/kayip-kontrol.py [--rev HEAD] [--facts-only]
                                                [--threshold 0.5] FILE [FILE ...]
        --facts-only skips the clause check (use it for a translation, where
        every word changes).
Exit:   0 nothing to review · 1 missing facts or clauses to review · 2 usage error
Review the lists: restore real facts (names, paths, commands, numbers, dates);
for each listed clause make sure its point survived somewhere (reworded is
fine); words that were only translated (e.g. Turkish labels) can stay.
"""
import argparse
import pathlib
import re
import subprocess
import sys

PATTERNS = [
    r"`([^`\n]+)`",                                    # code spans
    r"(https?://[^\s)>\]]+)",                          # URLs
    r"\b(\d{4}-\d{2}-\d{2})\b",                        # ISO dates
    # paths (ASCII segments): with an extension, 2+ slashes, or a trailing slash
    r"(?<![\w./])((?:[A-Za-z0-9_.*<>-]+/)+[A-Za-z0-9_.*<>-]*\.[A-Za-z]\w{0,11}"
    r"|(?:[A-Za-z0-9_.*<>-]+/){2,}[A-Za-z0-9_.*<>-]*"
    r"|[A-Za-z0-9_.*<>-]+/(?![\w/]))",
    r"\b([\w-]+\.(?:md|cs|py|json|asset|unity|prefab|asmdef|shader|hlsl"
    r"|log|txt|png|xml|ya?ml|inputactions|uxml|uss|exe))\b",  # file names
    r"\b([A-Za-z_][A-Za-z0-9]*(?:[A-Z_][A-Za-z0-9]*)+)\b",  # CamelCase, snake_case
    r"(\d+(?:[.,]\d+)*)",                              # numbers
]
# Words too common to tell clauses apart; condition words (only, never, unless…) stay.
STOP = set("""the and for with that this these those from into onto than then when
are was were been being has have had its their they them there here what which who whom
can could may might will would should shall does did done each every any all some such per via
more most less same other also just very much many own out off over under about above below
one two three new old his her our your you not""".split())
CUT = re.compile(r"[;:,.()\[\]→—]|\s(?=(?:or|unless|except|because|since|but|if|so|otherwise|"
                 r"yoksa|ama|fakat|çünkü|ancak|eğer)\s)", re.I)


def normalize(text):
    """Treat 0,35 and 0.35 alike (Turkish vs English decimals)."""
    return re.sub(r"(?<=\d),(?=\d)", ".", text)


def facts(text):
    found = set()
    for pattern in PATTERNS:
        for match in re.findall(pattern, text):
            match = normalize(match).strip().rstrip(".,;:")
            if len(match) >= 2:
                found.add(match)
    return found


def stem(word):
    for end in ("ing", "ed", "es", "s", "e"):
        if word.endswith(end) and len(word) - len(end) >= 4:
            return word[: -len(end)]
    return word


def words(text):
    text = normalize(text).lower()
    return {stem(w) for w in re.findall(r"[a-zçğıöşü]{3,}", text) if w not in STOP}


def lost_points(old_text, new_text, threshold):
    """Old clauses whose words don't come back together in any one new line."""
    new_lines = [words(l) for l in new_text.splitlines()]
    new_lines = [w for w in new_lines if w]
    new_flat = re.sub(r"\s+", " ", normalize(new_text).lower())
    flagged, seen = [], set()
    for raw in old_text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("<!--", "---")):
            continue
        for clause in CUT.split(line):
            clause = clause.strip(" -*`|>#")
            key = re.sub(r"\s+", " ", normalize(clause).lower())
            if len(key) < 12 or key in seen or key in new_flat:
                continue
            seen.add(key)
            clause_words = words(clause)
            if len(clause_words) < 2:
                continue
            kept = max((len(clause_words & nl) for nl in new_lines), default=0)
            gone = len(clause_words) - kept
            if gone >= 2 and gone / len(clause_words) >= threshold:
                flagged.append((clause, line))
    return flagged


def old_version(rev, rel_path):
    result = subprocess.run(["git", "show", f"{rev}:{rel_path.as_posix()}"],
                            capture_output=True)
    if result.returncode != 0:
        return ""  # file is new
    return result.stdout.decode("utf-8", "replace")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Fact- and point-loss check for rewritten memory files.")
    parser.add_argument("--rev", default="HEAD", help="git revision holding the old versions")
    parser.add_argument("--facts-only", action="store_true", help="skip the clause check (translations)")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="share of a clause's words missing from its best new line before it is listed (default 0.5)")
    parser.add_argument("files", nargs="+", help="old and new files (repo paths)")
    args = parser.parse_args()

    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if top.returncode != 0:
        print("Not inside a git repository.")
        return 2
    root = pathlib.Path(top.stdout.strip()).resolve()

    old_text, new_text = "", ""
    for name in args.files:
        path = pathlib.Path(name).resolve()
        try:
            rel = path.relative_to(root)
        except ValueError:
            print(f"Outside the repository: {name}")
            return 2
        old_text += "\n" + old_version(args.rev, rel)
        if path.exists():
            new_text += "\n" + path.read_text(encoding="utf-8")

    new_norm = normalize(new_text)
    missing = sorted(f for f in facts(old_text) if f not in new_norm)
    points = [] if args.facts_only else lost_points(old_text, new_text, args.threshold)

    if missing:
        print(f"Missing {len(missing)} fact(s) from {args.rev}:")
        for fact in missing:
            print(f"  - {fact}")
    else:
        print(f"OK: every fact from {args.rev} is still present.")
    if points:
        print(f"Review {len(points)} old clause(s) whose words no new line holds together: "
              "did each point (reason, condition, exception) survive?")
        for clause, line in points:
            context = "" if clause == line else f"   [in: {line[:120]}]"
            print(f"  - {clause[:160]}{context}")
    elif not args.facts_only:
        print("OK: no old clause lost most of its words.")
    return 1 if missing or points else 0


if __name__ == "__main__":
    sys.exit(main())
