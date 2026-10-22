#!/usr/bin/env python3
"""Find art and audio files this game shares with the studio's other games, by content hash.

Apple's 4.3(a) names the same source code or assets across apps as a spam signal, and Poki
and CrazyGames refuse asset flips. The portfolio rule (handbook kalite-kapisi.md, Portfolio
rules) allows 0 shared gameplay art or audio files between the studio's games. This script
takes the sha256 of every audio, image and model file under each project's Assets/ (a folder
without Assets/ is scanned whole, minus Library, Packages, Temp, Logs, obj, bin and
node_modules) and lists the files of THIS project whose exact bytes appear in another
project, grouped by folder. Skipped: *.meta, hidden folders, "name~" folders, and SDK and
editor folders at any depth (SKIP below: player-invisible or third-party technical files).
Only files whose byte size occurs on both sides are hashed, so big projects take seconds.
Asset packs count like any other file: two games built from the same pack share files.

Deliberate shared parts go into an allow list (--allow FILE), one per line: a path glob
relative to THIS project's scanned folder (e.g. "Art/Brand/logo*.png"; * also crosses /)
or a sha256, then "# reason". A line without a reason is an error.

Usage:  python varlik-cakisma.py [--allow FILE] [--all] THIS -- OTHER [OTHER ...]
        THIS, OTHER: project folders; OTHER may be a quoted glob (only folders with Assets/)
        --all lists every shared file (default: 5 per folder)
        python varlik-cakisma.py --dene         # self-test in memory
Exit:   0 nothing shared outside the allow list · 1 shared gameplay art or audio · 2 usage error
Read-only: it reads files and writes nothing.
"""
import argparse
import collections
import fnmatch
import glob
import hashlib
import io
import os
import pathlib
import re
import sys

AUDIO = {".wav", ".mp3", ".ogg", ".aif", ".aiff", ".flac", ".m4a", ".aac", ".opus", ".mod", ".it", ".s3m", ".xm"}
IMAGE = {".png", ".jpg", ".jpeg", ".tga", ".psd", ".tif", ".tiff", ".bmp", ".gif", ".exr", ".hdr", ".webp",
         ".svg", ".dds", ".ktx", ".ktx2", ".iff", ".pict"}
MODEL = {".fbx", ".obj", ".blend", ".dae", ".3ds", ".max", ".ma", ".mb", ".glb", ".gltf", ".ply", ".stl",
         ".usd", ".usda", ".usdc", ".usdz", ".abc", ".skp"}
KINDS = AUDIO | IMAGE | MODEL
# Folders (any depth, any case) whose files players never see or that belong to an SDK.
SKIP = {"editor", "editor default resources", "gizmos", "plugins", "externaldependencymanager", "firebase",
        "googlemobileads", "googleplayplugins", "googleplaygames", "generatedlocalrepo", "textmesh pro",
        "tutorialinfo", "samples"}
# Never source in a project folder scanned whole.
OUTSIDE_ASSETS = {"library", "packages", "temp", "logs", "obj", "bin", "node_modules", "usersettings"}
SHA256 = re.compile(r"[0-9a-fA-F]{64}")

Entry = collections.namedtuple("Entry", "project rel size path")


def scan_root(folder):
    assets = folder / "Assets"
    return (assets, True) if assets.is_dir() else (folder, False)


def folder_rule(name, top_of_whole_folder):
    """'scan', 'ignore' (hidden, Unity-hidden or never source) or 'skip' (SDK or editor: counted, not compared)."""
    low = name.lower()
    if name.startswith(".") or name.endswith("~") or (top_of_whole_folder and low in OUTSIDE_ASSETS):
        return "ignore"
    return "skip" if low in SKIP else "scan"


def scan(folder, project):
    """(entries, skipped count): art and audio files under the project's Assets/ (or the folder)."""
    root, in_assets = scan_root(folder)
    entries, skipped = [], 0
    for current, dirs, files in os.walk(root):
        rel_dir = pathlib.Path(current).relative_to(root)
        kept = []
        for name in dirs:
            rule = folder_rule(name, not in_assets and rel_dir == pathlib.Path("."))
            if rule == "skip":
                skipped += sum(1 for _, _, fs in os.walk(os.path.join(current, name))
                               for f in fs if pathlib.Path(f).suffix.lower() in KINDS)
            elif rule == "scan":
                kept.append(name)
        dirs[:] = kept
        for name in files:
            if pathlib.Path(name).suffix.lower() in KINDS:
                path = os.path.join(current, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                if size:
                    entries.append(Entry(project, (rel_dir / name).as_posix(), size, path))
    return entries, skipped


def file_digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def read_allow(text):
    """[(pattern, reason)]; raises ValueError naming a line without a reason."""
    rules = []
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pattern, _, reason = line.partition("#")
        if not reason.strip():
            raise ValueError(f"line {number} has no '# reason': {line}")
        rules.append((pattern.strip(), reason.strip()))
    return rules


def allowed_by(entry, digest, rules):
    for pattern, reason in rules:
        if SHA256.fullmatch(pattern):
            if pattern.lower() == digest:
                return reason
        elif fnmatch.fnmatchcase(entry.rel.lower(), pattern.lower()):
            return reason
    return None


def shared_files(ours, theirs, rules, digest=file_digest):
    """({folder: [(entry, places)]} shared, {folder: [(entry, reason)]} allowed, files hashed)."""
    sizes = {e.size for e in ours} & {e.size for e in theirs}
    index = collections.defaultdict(list)
    hashed = 0
    for entry in theirs:
        if entry.size in sizes:
            index[digest(entry.path)].append(entry)
            hashed += 1
    shared, allowed = collections.defaultdict(list), collections.defaultdict(list)
    for entry in ours:
        if entry.size not in sizes:
            continue
        hashed += 1
        key = digest(entry.path)
        if key in index:
            folder = os.path.dirname(entry.rel) + "/" if "/" in entry.rel else "./"
            reason = allowed_by(entry, key, rules)
            if reason:
                allowed[folder].append((entry, reason))
            else:
                shared[folder].append((entry, index[key]))
    return shared, allowed, hashed


def kb(size):
    return f"{size / 1024:,.1f} KB" if size < 1 << 20 else f"{size / (1 << 20):,.1f} MB"


def report(shared, allowed, show_all):
    count = sum(len(v) for v in shared.values())
    print(f"Shared gameplay art, audio or models: {count} file(s) in {len(shared)} folder(s)")
    for folder in sorted(shared, key=lambda f: (-len(shared[f]), f)):
        items = sorted(shared[folder], key=lambda item: item[0].rel)
        print(f"  {folder}  ({len(items)})")
        for entry, places in items if show_all else items[:5]:
            first = places[0]
            more = f" +{len(places) - 1} more" if len(places) > 1 else ""
            print(f"    {pathlib.PurePosixPath(entry.rel).name}  {kb(entry.size)}  = {first.project}: {first.rel}{more}")
        if not show_all and len(items) > 5:
            print(f"    ... {len(items) - 5} more (--all lists every file)")
    if allowed:
        total = sum(len(v) for v in allowed.values())
        print(f"Allowed by the list: {total} file(s) in {len(allowed)} folder(s)")
        for folder in sorted(allowed):
            reasons = sorted({reason for _, reason in allowed[folder]})
            print(f"  {folder}  ({len(allowed[folder])}): {'; '.join(reasons)}")
    return 1 if count else 0


def dene():
    """Self-test on files in memory; writes nothing."""
    blobs = {"click": b"click sound", "hero": b"hero texture", "frame": b"ui frame", "same-size": b"hero texturf",
             "logo": b"studio logo", "music": b"a long music loop", "tree": b"tree model"}
    ours = [Entry("this", "Audio/click.wav", 11, "click"), Entry("this", "Art/hero.png", 12, "hero"),
            Entry("this", "UI/Kit/frame.png", 8, "frame"), Entry("this", "Brand/logo.png", 11, "logo"),
            Entry("this", "Audio/music.ogg", 17, "music")]
    theirs = [Entry("other", "Sfx/tap.wav", 11, "click"), Entry("other", "Art/villain.png", 12, "same-size"),
              Entry("other", "Kit/frame.png", 8, "frame"), Entry("other", "Splash/logo.png", 11, "logo"),
              Entry("other", "Props/tree.fbx", 10, "tree")]
    seen = []

    def digest(key):
        seen.append(key)
        return hashlib.sha256(blobs[key]).hexdigest()

    logo_hash = hashlib.sha256(blobs["logo"]).hexdigest()
    rules = read_allow(f"# deliberate shared parts\nUI/Kit/*  # kit frames, tinted per game\n{logo_hash}  # studio logo\n")
    shared, allowed, hashed = shared_files(ours, theirs, rules, digest)
    checks = []

    def check(name, ok):
        checks.append((name, ok))
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")

    flat = [entry.rel for items in shared.values() for entry, _ in items]
    check("the same sound under another name is shared", flat == ["Audio/click.wav"])
    check("same size, other bytes: not shared", "Art/hero.png" not in flat)
    check("allowed by path glob and by sha256, with reasons",
          sorted(e.rel for items in allowed.values() for e, _ in items) == ["Brand/logo.png", "UI/Kit/frame.png"])
    check(f"only files whose size occurs on both sides are hashed ({hashed} of 10)",
          hashed == 8 and "music" not in seen and "tree" not in seen)
    try:
        read_allow("Art/*.png\n")
        check("an allow line without a reason is refused", False)
    except ValueError:
        check("an allow line without a reason is refused", True)
    rules_seen = [folder_rule(n, False) for n in ("Editor", "Plugins", "TextMesh Pro", "Samples~", ".git", "Art")]
    check("Editor, Plugins and TextMesh Pro skipped, Samples~ and .git ignored, Art scanned",
          rules_seen == ["skip", "skip", "skip", "ignore", "ignore", "scan"]
          and folder_rule("Library", True) == "ignore" and folder_rule("Library", False) == "scan")
    with io.StringIO() as buffer:
        stdout, sys.stdout = sys.stdout, buffer
        try:
            code = report(shared, allowed, False)
            clean = report({}, allowed, False)
        finally:
            sys.stdout = stdout
    check("exit 1 with a shared gameplay file, 0 when only allowed ones are shared", code == 1 and clean == 0)
    passed = sum(ok for _, ok in checks)
    print(f"dene: {passed}/{len(checks)} ok")
    return 0 if passed == len(checks) else 1


def folders(args, this):
    picked, notes = [], []
    for arg in args:
        hits = sorted(glob.glob(arg)) if set("*?[") & set(arg) else [arg]
        for hit in hits:
            path = pathlib.Path(hit)
            if not path.is_dir():
                notes.append(f"Not a folder: {hit}")
            elif os.path.normcase(str(path.resolve())) == os.path.normcase(str(this.resolve())):
                continue
            elif hit != arg and not (path / "Assets").is_dir():
                notes.append(f"Skipped (no Assets/): {hit}")
            else:
                picked.append(path)
    return picked, notes


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--dene" in sys.argv[1:]:
        return dene()
    argv = sys.argv[1:]
    if "--" not in argv:
        print("Give this project, then --, then the other projects (see the usage above).\n" + __doc__)
        return 2
    cut = argv.index("--")
    parser = argparse.ArgumentParser(description="Art and audio this game shares with other studio games.")
    parser.add_argument("--allow", type=pathlib.Path, help="allow list: path glob or sha256, then # reason")
    parser.add_argument("--all", action="store_true", help="list every shared file")
    parser.add_argument("this", type=pathlib.Path)
    args = parser.parse_args(argv[:cut])
    if not args.this.is_dir():
        print(f"Not a folder: {args.this}", file=sys.stderr)
        return 2
    others, notes = folders(argv[cut + 1:], args.this)
    for note in notes:
        print(note, file=sys.stderr)
    if not others:
        print("No other project to compare with.", file=sys.stderr)
        return 2
    try:
        rules = read_allow(args.allow.read_text(encoding="utf-8")) if args.allow else []
    except (OSError, ValueError) as error:
        print(f"Allow list {args.allow}: {error}", file=sys.stderr)
        return 2
    ours, skipped = scan(args.this, args.this.resolve().name)
    theirs, skipped_there = [], 0
    for folder in others:
        entries, skip = scan(folder, folder.resolve().name)
        theirs += entries
        skipped_there += skip
    root, _ = scan_root(args.this)
    print(f"varlik-cakisma: {root} vs {len(others)} project(s): {', '.join(f.resolve().name for f in others)}")
    print(f"  here {len(ours):,} art, audio and model files ({skipped:,} more in SDK and editor folders, not compared)"
          f" · there {len(theirs):,} ({skipped_there:,} skipped)")
    shared, allowed, hashed = shared_files(ours, theirs, rules)
    print(f"  {hashed:,} files hashed (their size occurs on both sides)")
    code = report(shared, allowed, args.all)
    print("Result: " + ("shared gameplay files -> replace them with this game's own, or allow deliberate ones "
                        "with a reason (--allow)." if code else "no shared gameplay art or audio."))
    return code


if __name__ == "__main__":
    sys.exit(main())
