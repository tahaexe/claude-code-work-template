#!/usr/bin/env python3
"""How similar this game's store listing texts are to the studio's other listings.

Apple publishes no threshold for look-alike metadata, but texts reused across a studio's
apps read as "one template fired repeatedly" (4.3). The portfolio rule (handbook
kalite-kapisi.md, Portfolio rules) keeps every listing text of a game (description,
promotional text, what's new) at most 25 % similar to any other studio listing; the 25 %
is a heuristic. Two measures from 0 to 1, both reported for every pair:
- difflib: SequenceMatcher ratio on the two word sequences (shared wording in order);
- 5-gram:  Jaccard index of the two sets of word 5-grams (shared phrases anywhere).
Before comparing, Markdown loses HTML comments, heading lines, code-fence lines and link
targets; JSON gives its string values; URLs go. Words are lower-cased runs of letters and
digits in any script. A pair is the same file given on both sides only once: it's skipped.

Usage:  python metin-benzerlik.py [--threshold 0.25] [--top 10] THIS [THIS ...] -- OTHER [OTHER ...]
        THIS:  this game's listing files, or folders (their .md, .txt and .json files)
        OTHER: the other games' listing files, folders or globs (quote globs; "**" recurses)
        python metin-benzerlik.py --dene        # self-test in memory
Exit:   0 every pair at or below the threshold · 1 a pair above it (either measure) · 2 usage error
Read-only: it reads the given files and writes nothing.
"""
import argparse
import difflib
import glob
import json
import os
import pathlib
import re
import sys

TEXT_SUFFIXES = {".md", ".txt", ".json"}
WORD = re.compile(r"[^\W_]+")
COMMENT = re.compile(r"<!--.*?-->", re.S)
LINK_TARGET = re.compile(r"\]\([^)]*\)")
URL = re.compile(r"https?://\S+|www\.\S+")
GLOB_CHARS = set("*?[")
N = 5


def json_strings(value):
    """Every string value in a JSON document (keys are field names, not listing text)."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from json_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from json_strings(item)


def words(text, suffix=".txt"):
    if suffix == ".json":
        text = "\n".join(json_strings(json.loads(text)))
    elif suffix == ".md":
        text = COMMENT.sub(" ", text)
        text = LINK_TARGET.sub("] ", text)
        text = "\n".join(line for line in text.splitlines()
                         if not line.lstrip().startswith(("#", "```", "~~~")))
    text = URL.sub(" ", text)
    return WORD.findall(text.lower().replace("̇", ""))  # "İ".lower() leaves a combining dot


def shingles(seq):
    if len(seq) < N:
        return {tuple(seq)} if seq else set()
    return {tuple(seq[i:i + N]) for i in range(len(seq) - N + 1)}


def similarity(a, b):
    """(difflib ratio, 5-gram Jaccard) of two word lists."""
    ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a or b else 0.0
    sa, sb = shingles(a), shingles(b)
    union = sa | sb
    return ratio, (len(sa & sb) / len(union) if union else 0.0)


def expand(args, take_globs):
    """Files from file, folder and (for OTHER) glob arguments, in order, without repeats."""
    found, missing = [], []
    for arg in args:
        if take_globs and GLOB_CHARS & set(arg):
            hits = sorted(glob.glob(arg, recursive=True))
        else:
            hits = [arg]
        paths = []
        for hit in hits:
            path = pathlib.Path(hit)
            if path.is_dir():
                paths += sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
            elif path.is_file():
                paths.append(path)
        if not paths:
            missing.append(arg)
        found += paths
    unique, seen = [], set()
    for path in found:
        key = os.path.normcase(str(path.resolve()))
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique, missing


def load(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        return words(text, path.suffix.lower())
    except json.JSONDecodeError:
        return words(text)


def compare(these, others):
    """[(difflib, 5-gram, this name, other name)] for every pair; texts are {name: words}."""
    pairs = []
    for this_name, this_words in these.items():
        for other_name, other_words in others.items():
            if this_name != other_name:
                pairs.append((*similarity(this_words, other_words), this_name, other_name))
    return pairs


def verdict(pairs, threshold):
    return 1 if any(max(d, j) > threshold for d, j, _, _ in pairs) else 0


def shown(path):
    try:
        return os.path.relpath(path)
    except ValueError:  # another drive
        return str(path)


def report(pairs, threshold, top, these):
    best = {}
    for pair in pairs:
        if pair[2] not in best or max(pair[:2]) > max(best[pair[2]][:2]):
            best[pair[2]] = pair
    print("Closest other listing per file here (difflib · 5-gram):")
    for name in these:
        if name in best:
            d, j, _, other = best[name]
            flag = "  ABOVE" if max(d, j) > threshold else ""
            print(f"  {d:4.2f} · {j:4.2f}  {name}  ~  {other}{flag}")
    ranked = sorted(pairs, key=lambda p: max(p[:2]), reverse=True)[:top]
    print(f"Top {len(ranked)} pairs:")
    for d, j, this_name, other in ranked:
        print(f"  {d:4.2f} · {j:4.2f}  {this_name}  ~  {other}")
    max_d = max(p[0] for p in pairs)
    max_j = max(p[1] for p in pairs)
    code = verdict(pairs, threshold)
    word = "above" if code else "at or below"
    print(f"Result: max difflib {max_d:.2f}, max 5-gram {max_j:.2f}: {word} the threshold {threshold:.2f}"
          + (" -> rewrite the texts named ABOVE in this game's own words." if code else "."))
    return code


def dene():
    """Self-test on texts in memory; writes nothing."""
    base = ("Slide the colored blocks into their gates and clear the board one move at a time. "
            "Every level adds a new idea: frozen blocks, keys, one-way gates and moving walls. "
            "Plan ahead, undo a step whenever you like and use a hint when you are stuck. "
            "No timers and no lives, so you can relax and think. "
            "Collect stars on every board and unlock calm new worlds at your own pace.")
    other = ("Grow a tiny garden on a floating island and help sleepy animals wake up for spring. "
             "Water seedlings, trade fruit with travelling merchants and decorate cosy cottages. "
             "Seasons change the weather, and every visitor brings a small story to finish. "
             "Build bridges to new islands and find rare flowers hidden in the fog.")
    half = " ".join(other.split()[:30] + base.split()[-30:])
    markdown = "<!-- notes for the store tool -->\n## full\n```text\n" + base + "\n```\n[More](https://example.com)\n"
    js = json.dumps({"title": "Block Gates", "full": base})
    checks = []

    def check(name, ok):
        checks.append((name, ok))
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")

    d, j = similarity(words(base), words(base))
    check(f"identical text: difflib {d:.2f}, 5-gram {j:.2f} (both 1.00)", d == 1.0 and j == 1.0)
    d, j = similarity(words(base), words(other))
    check(f"another game's text: difflib {d:.2f}, 5-gram {j:.2f} (both <= 0.25)", d <= 0.25 and j <= 0.25)
    d, j = similarity(words(base), words(half))
    check(f"half shared: difflib {d:.2f}, 5-gram {j:.2f} (both > 0.25)", d > 0.25 and j > 0.25)
    check("Markdown comment, heading, fence and link target dropped", words(markdown, ".md") == words(base + " More"))
    check("JSON string values read, keys skipped", words(js, ".json") == words("Block Gates " + base))
    check("short titles: equal 5-gram 1.00, different 0.00",
          similarity(words("Block Gates"), words("Block Gates"))[1] == 1.0
          and similarity(words("Block Gates"), words("Island Garden"))[1] == 0.0)
    check("dotted capital I folds like i", words("İSTANBUL") == words("istanbul"))
    pairs = compare({"this": words(base)}, {"a": words(other), "b": words(half)})
    check("exit 1 when a pair is above 0.25, 0 when none is",
          verdict(pairs, 0.25) == 1 and verdict(pairs[:1], 0.25) == 0)
    passed = sum(ok for _, ok in checks)
    print(f"dene: {passed}/{len(checks)} ok")
    return 0 if passed == len(checks) else 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--dene" in sys.argv[1:]:
        return dene()
    argv = sys.argv[1:]
    if "--" not in argv:
        print("Give this game's files, then --, then the other games' files (see the usage above).\n" + __doc__)
        return 2
    cut = argv.index("--")
    parser = argparse.ArgumentParser(description="Listing text similarity against the studio's other games.")
    parser.add_argument("--threshold", type=float, default=0.25, help="highest allowed similarity (default 0.25)")
    parser.add_argument("--top", type=int, default=10, help="pairs to list (default 10)")
    parser.add_argument("this", nargs="+")
    args = parser.parse_args(argv[:cut])
    other_args = argv[cut + 1:]
    these, missing_here = expand(args.this, take_globs=False)
    others, missing_there = expand(other_args, take_globs=True)
    for arg in missing_here + missing_there:
        print(f"No listing file at: {arg}", file=sys.stderr)
    if not these or not others:
        print("Nothing to compare: both sides need at least one .md, .txt or .json file.", file=sys.stderr)
        return 2
    this_texts = {shown(p): load(p) for p in these}
    this_keys = {os.path.normcase(str(p.resolve())) for p in these}
    other_texts = {shown(p): load(p) for p in others if os.path.normcase(str(p.resolve())) not in this_keys}
    if not other_texts:
        print("The other side holds only this game's own files.", file=sys.stderr)
        return 2
    print(f"metin-benzerlik: {len(this_texts)} file(s) here, {len(other_texts)} there · threshold "
          f"{args.threshold:.2f} on difflib (word sequence ratio) and 5-gram (word 5-gram Jaccard)")
    return report(compare(this_texts, other_texts), args.threshold, args.top, this_texts)


if __name__ == "__main__":
    sys.exit(main())
