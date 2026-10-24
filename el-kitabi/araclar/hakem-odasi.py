#!/usr/bin/env python3
"""Judge room: run blind reviewers in an unnamed folder, each in a separate session that knows nothing of the project.

Why (2026-10-24; the session manager's 01:32 and 06:04 notes, Project E's 01:31 finding): blind reviewers and fresh scorers
are Explore agents because Explore doesn't load CLAUDE.md, but a subagent still sees the parent session's working directory
(`...\\_UnityProjects\\Project E`), so a reviewer could read the game's name off the path. The Agent tool can't change a
subagent's folder.

What `run` does:
 1. Copies the evidence into a temporary unnamed room (<temp>/oda-<random>). Strips PNG and JPEG metadata (text, EXIF, XMP,
    timestamps). Leaves out what a reviewer can't open (video, audio, other binaries) and says so.
 2. Leak check: if the game's name (the git folder and remote of the caller's project and of the evidence, --forbid, and the
    optional machine-wide hakem-odasi-forbid.txt beside this script or ~/.hakem-odasi-forbid.txt) appears in a file or folder
    name, a text file or a file's bytes, no reviewer runs (exit 3). It also stops if a key file (a name with "anahtar" or "answer-key") slipped into the evidence. It
    can't see text or logos inside images: whoever prepares the evidence masks those.
 3. Probe: a cheap reviewer (haiku, low effort) lists the names in its own context in the room; if the game's name shows up
    the run stops. This catches a future Claude Code release that loads CLAUDE.md again.
 4. Each reviewer is its own headless session in the room: `claude -p --agent Explore`, the prompt passed verbatim (no
    model in between):
    - CLAUDE.md and auto-memory off (CLAUDE_CODE_DISABLE_CLAUDE_MDS, CLAUDE_CODE_DISABLE_AUTO_MEMORY); the account's settings
      and hooks not loaded (--setting-sources project,local); no MCP; no session transcript; the parent session's links
      (session id, messaging pipe) removed from the environment, the account (CLAUDE_CONFIG_DIR) kept;
    - effort xhigh unless given; max only for the last decision round before a store (measured 2026-10-24 on two real
      rounds: xhigh found what max found, a subtle rewind in the first second included, at ~0.57 of max's cost and half its
      time; one of two high reviewers missed it);
    - tools Read, Glob and Grep only, inside the room only (dontAsk: anything outside is denied and logged);
    - the prompt cache lives 5 minutes, not an hour (CLAUDE_CODE_PROMPT_CACHE_TTL=5m): a reviewer's calls follow each other
      within seconds, and an hour-long cache write costs 8 $/M tokens against 5 (measured 2026-10-24: a reviewer of 103 images
      writes ~219k tokens, its biggest cost).
 5. Each answer goes verbatim to <out>/hakem-<n>.md as soon as its reviewer is done; the log <out>/hakem-odasi-log.md
    records model, time, which evidence files the reviewer opened, denied access and the prompt itself. Then the room and the
    folders the account opened for it are deleted. No answer is lost: if <out> vanished during the run it is created again
    (with a WARNING); if it can't be written, the answer goes to <temp>/hakem-odasi-yedek/ and to stdout. <out> can't be in
    Claude Code's temp tree (<temp>/claude/..., a session's scratchpad): on 2026-10-24 an empty --out in a scratchpad vanished
    during a run and two answers were lost.

Measured 2026-10-24 (Claude Code 2.1.310): a reviewer in the room sees no CLAUDE.md, memory, git or project name; it has only
Read, Glob and Grep; it can't read outside the room (a settings-wide Read allow rule did read outside; the path-scoped rule
and dontAsk refused). One reviewer process peaks at ~240 MB.
Known limit: the account's e-mail (claude.ai login) is in every session's context, so the studio's name is visible; the
only switch that drops it (ANTHROPIC_UNIX_SOCKET) also changes the API connection. Mask the studio's name and logo in the
evidence.

Usage: python hakem-odasi.py run --evidence <dir> --form <form.md> --out <dir> [--judges 2] [--add NAME=PATH]...
         [--forbid "Game Name"]... [--allow WORD]... [--model opus] [--effort low|medium|high|xhigh|max] [--parallel 2]
         [--timeout 30] [--first N] [--prefix hakem] [--lang auto|tr|en] [--cache-ttl 5m|1h] [--no-probe] [--dry-run] [--keep] [--raw]
       python hakem-odasi.py play --package <android package> --form <questions.md> --out <dir> [--evidence <dir>]
         [--serial S] [--adb PATH] [--minutes 10] [--answer-minutes 10] [--clear-data] [--apk FILE] [--model opus] [--effort ...]
         [--first N] [--prefix oyuncu] [--lang auto|tr|en] [--cache-ttl 5m|1h] [--forbid ...] [--allow ...] [--no-probe] [--dry-run]
         [--keep] [--keep-frames] [--raw]
           a fresh player on an Android device or emulator, with tools only for playing (Play mode, below)
       python hakem-odasi.py first-launch --package <android package> [--serial S] [--adb PATH] [--seconds 15] [--out <dir>] [--apk FILE]
           model-free: after Android's full-screen notice the game must draw again (exit 0 passed, 1 black, 3 inconclusive)
       python hakem-odasi.py check <dir> [--forbid ...] [--allow ...]   leak check only (no copy, no reviewer)
       python hakem-odasi.py clean                                     delete rooms whose owner process is gone
Exit: 0 done · 1 a reviewer failed · 2 usage · 3 stopped by the leak check, key file or probe · 4 claude not found.
"""
import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

IMAGE = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
MANY_IMAGES = 100   # above this a run warns: at max effort 126 and 350 files ran past the 30-minute timeout (2026-10-24)
TEXT = {'.md', '.txt', '.csv', '.tsv', '.json', '.html', '.htm', '.xml', '.yaml', '.yml', '.srt', '.vtt', '.log'}
DOC = {'.pdf'}
VIDEO_AUDIO = {'.mp4', '.webm', '.mov', '.mkv', '.avi', '.m4v', '.wav', '.mp3', '.ogg', '.m4a', '.aac', '.flac', '.opus'}
# Variables that tie a child to the parent session: the reviewer is an independent top-level headless session
PARENT_LINKS = ('CLAUDECODE', 'CLAUDE_CODE_CHILD_SESSION', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_PID', 'CLAUDE_CODE_ENTRYPOINT',
                'CLAUDE_CODE_EXECPATH', 'CLAUDE_CODE_MESSAGING_SOCKET', 'CLAUDE_CODE_MESSAGING_TOKEN',
                'CLAUDE_CODE_SESSION_ATTENDED', 'AI_AGENT', 'CLAUDE_CODE_SSE_PORT')
ROOM_PREFIX = 'oda-'
# Machine-wide forbidden names (the studio's and the owner's name: the reviewer sees the account's e-mail and the room's path),
# one per line: beside this script or in the user's home, so every project's copy finds the home one
FORBID_FILES = (Path(__file__).with_name('hakem-odasi-forbid.txt'), Path.home() / '.hakem-odasi-forbid.txt')
KEY_NAMES = ('anahtar', 'answerkey')
# Where an output goes when --out can't be written (one folder per run)
BACKUP_DIR = Path(tempfile.gettempdir()) / 'hakem-odasi-yedek'
RUN_STAMP = f'{time.strftime("%Y%m%d-%H%M%S")}-{os.getpid()}'


def say(*a):
    print(*a, flush=True)


# --- Names and leaks ---

def fold(s):
    """Comparison form: lower case, no accents (ş → s, İ → i), letters and digits only."""
    s = unicodedata.normalize('NFKD', s.casefold())
    return ''.join(c for c in s if c.isalnum() and not unicodedata.combining(c)).replace('ı', 'i')


def split_camel(s):
    """Project E → Project E (for the byte search forms)."""
    return re.sub(r'(?<=[a-zçğıöşü0-9])(?=[A-ZÇĞİÖŞÜ])', ' ', s)


def git_names(path):
    """The name of the path's git repository folder and its remote's owner and name (github.com/<owner>/<name>)."""
    names = set()
    try:
        path = Path(path)
        d = path if path.is_dir() else path.parent
        top = subprocess.run(['git', '-C', str(d), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, timeout=20)
        if top.returncode != 0 or not top.stdout.strip():
            return names
        names.add(Path(top.stdout.strip()).name)
        remote = subprocess.run(['git', '-C', str(d), 'remote', 'get-url', 'origin'], capture_output=True, text=True, timeout=20)
        m = re.search(r'[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$', remote.stdout.strip()) if remote.returncode == 0 else None
        if m:
            names.update(m.groups())
    except (OSError, subprocess.SubprocessError):
        pass
    return names


def file_names(paths=FORBID_FILES):
    names = set()
    for path in paths:
        if path.is_file():
            for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
                line = line.split('#', 1)[0].strip()
                if line:
                    names.add(line)
    return names


def forbid_set(raw, allow):
    """{folded: shown}; a name shorter than 4 letters is skipped (false alarms), allowed words are removed."""
    allowed = {fold(x) for x in allow}
    out = {}
    for name in raw:
        f = fold(name)
        if len(f) < 4:
            say(f'WARNING: "{name}" not used as a forbidden name (shorter than 4 letters, false alarms)')
            continue
        if f not in allowed:
            out[f] = name
    return out


def byte_forms(name):
    """Forms of a name searched inside files (lower case, UTF-8 and UTF-16): spaced, joined, hyphenated, underscored."""
    bases = {name, split_camel(name)}
    plain = unicodedata.normalize('NFKD', name)
    bases.add(''.join(c for c in plain if not unicodedata.combining(c)).replace('ı', 'i').replace('İ', 'I'))
    forms = set()
    for b in bases:
        for sep in (' ', '', '-', '_', '.'):
            s = re.sub(r'[\s_.-]+', sep, b.strip()).lower()
            if len(fold(s)) >= 4:
                forms.add(s)
    out = set()
    for s in forms:
        for enc in ('utf-8', 'utf-16-le'):
            try:
                out.add(s.encode(enc))
            except UnicodeEncodeError:
                pass
    return out


def leak_scan(root, forbidden):
    """File and folder names, text files and every file's bytes. [(relative path, where, name)]"""
    hits = []
    if not forbidden:
        return hits
    forms = {f: byte_forms(name) for f, name in forbidden.items()}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        for f, name in forbidden.items():
            if f in fold(rel):
                hits.append((rel, 'file or folder name', name))
        if not path.is_file():
            continue
        data = path.read_bytes()
        if path.suffix.lower() in TEXT:
            text = fold(data.decode('utf-8', errors='replace'))
            for f, name in forbidden.items():
                if f in text:
                    hits.append((rel, 'text', name))
        low = data.lower()
        for f, name in forbidden.items():
            if any(b in low for b in forms[f]) and not any(h[0] == rel and h[2] == name for h in hits):
                hits.append((rel, 'inside the file (metadata or embedded text)', name))
    return hits


# --- Metadata stripping (no PIL: python -I doesn't see user site-packages) ---

PNG_SIG = b'\x89PNG\r\n\x1a\n'
PNG_KEEP = {b'IHDR', b'PLTE', b'IDAT', b'IEND', b'tRNS', b'gAMA', b'cHRM', b'sRGB', b'sBIT', b'pHYs', b'bKGD', b'acTL', b'fcTL', b'fdAT'}


def strip_png(data):
    """Chunks that draw the image stay; text (tEXt, zTXt, iTXt), EXIF, time, ICC and unknown ancillary chunks go."""
    if not data.startswith(PNG_SIG):
        return data, 0
    out, i, dropped = [PNG_SIG], 8, 0
    while i + 8 <= len(data):
        length = int.from_bytes(data[i:i + 4], 'big')
        kind = data[i + 4:i + 8]
        end = i + 12 + length
        if end > len(data):
            return data, 0   # damaged: leave it alone
        if kind in PNG_KEEP:
            out.append(data[i:end])
        else:
            dropped += 1
        i = end
        if kind == b'IEND':
            break
    return b''.join(out), dropped


def strip_jpeg(data):
    """APP1-APP15 (EXIF, XMP, IPTC, Photoshop) and comments go; JFIF (APP0), Adobe (APP14, colour transform) and ICC stay."""
    if not data.startswith(b'\xff\xd8'):
        return data, 0
    out, i, dropped = [b'\xff\xd8'], 2, 0
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            return data, 0
        marker = data[i + 1]
        if marker == 0xFF:   # fill byte
            i += 1
            continue
        if marker == 0xDA:   # start of scan: the rest as is
            out.append(data[i:])
            return b''.join(out), dropped
        if 0xD0 <= marker <= 0xD9:
            out.append(data[i:i + 2])
            i += 2
            continue
        length = int.from_bytes(data[i + 2:i + 4], 'big')
        seg = data[i:i + 2 + length]
        keep = not (0xE1 <= marker <= 0xEF or marker == 0xFE) or marker == 0xEE or (marker == 0xE2 and seg[4:16] == b'ICC_PROFILE\x00')
        if keep:
            out.append(seg)
        else:
            dropped += 1
        i += 2 + length
    return data, 0


def strip_metadata(path):
    ext = path.suffix.lower()
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 0
    data = path.read_bytes()
    new, dropped = strip_png(data) if ext == '.png' else strip_jpeg(data)
    if dropped:
        path.write_bytes(new)
    return dropped


# --- Room ---

def project_key(path):
    """Claude Code's project folder name: every character other than a letter or digit becomes '-'."""
    return re.sub(r'[^A-Za-z0-9]', '-', str(path))


def config_dir():
    return Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude')


def remove_room(room):
    """The room, its marker and the folders the account opened for it (project record, subagent info, task output)."""
    key = project_key(room)
    for p in (room, Path(str(room) + '.lock'), Path(str(room) + '.mcp.json'), config_dir() / 'projects' / key,
              Path(tempfile.gettempdir()) / 'claude' / key):
        try:
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.exists():
                p.unlink()
        except OSError:
            pass


def process_alive(pid):
    if os.name == 'nt':
        r = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH', '/FO', 'CSV'], capture_output=True, text=True)
        return f'"{pid}"' in r.stdout
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def clean_old_rooms(root, verbose=False):
    """Rooms whose owner process is gone (or without a marker and older than 6 hours)."""
    removed = 0
    for room in Path(root).glob(ROOM_PREFIX + '*'):
        if not room.is_dir():
            continue
        marker = Path(str(room) + '.lock')
        try:
            info = json.loads(marker.read_text(encoding='utf-8'))
            alive = process_alive(int(info['pid']))
        except (OSError, ValueError, KeyError):
            alive = time.time() - room.stat().st_mtime < 6 * 3600
        if not alive:
            remove_room(room)
            removed += 1
            if verbose:
                say(f'removed: {room}')
    return removed


LEFT_OUT_AV = 'video or audio (a reviewer can\'t open it: Read opens images, text and PDF; add frames or a contact sheet)'
LEFT_OUT_TYPE = 'not a type a reviewer can open'


def copy_evidence(room, evidence, adds):
    """Copies the evidence into the room. (copied files, left out [(path in the room, reason)])."""
    left_out = []

    def copy(src, dst):
        if src.name.startswith('.'):
            return
        if src.is_dir():
            for sub in sorted(src.iterdir()):
                copy(sub, dst / sub.name)
            return
        ext = src.suffix.lower()
        if ext in VIDEO_AUDIO or ext not in IMAGE | TEXT | DOC:
            left_out.append((dst.relative_to(room).as_posix(), LEFT_OUT_AV if ext in VIDEO_AUDIO else LEFT_OUT_TYPE))
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    if evidence:
        e = Path(evidence)
        if not e.is_dir():
            raise SystemExit(f'ERROR: evidence folder not found: {e}')
        for sub in sorted(e.iterdir()):
            copy(sub, room / sub.name)
    for add in adds:
        name, _, src = add.partition('=')
        name, src = name.strip(), Path(src.strip())
        if not name or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9 ._-]*', name) or '..' in name:
            raise SystemExit(f'ERROR: an --add name is letters, digits, spaces, dots, hyphens or underscores: "{name}"')
        if not src.exists():
            raise SystemExit(f'ERROR: --add path not found: {src}')
        if src.is_file() and not Path(name).suffix:
            name += src.suffix.lower()
        copy(src, room / name)
    return sorted(p for p in room.rglob('*') if p.is_file()), left_out


def group_left_out(left_out, limit=8):
    """['<reason>: N file(s): a, b, ...'] (one line per reason)."""
    groups = {}
    for p, why in left_out:
        groups.setdefault(why, []).append(p)
    return [f'{why}: {len(ps)} file(s): {", ".join(ps[:limit])}{" ..." if len(ps) > limit else ""}' for why, ps in groups.items()]


def key_files(files, root):
    return [p.relative_to(root).as_posix() for p in files if any(k in fold(p.name) for k in KEY_NAMES)]


# --- Prompt ---

PREAMBLE = {
    'tr': ('Bağımsız bir hakemsin. Bu klasördeki kanıta bakıp aşağıdaki formu dolduracaksın.\n'
           '- Yalnız bu klasördeki dosyalara bak; klasörün dışına, internete ya da başka bir kaynağa bakma.\n'
           '- Aşağıdaki listedeki her dosyayı aç: görselleri Read ile açıp gerçekten incele, metin dosyalarını baştan sona oku.\n'
           '- Puanı yalnız gördüğüne göre ver. Açamadığın bir dosya olursa cevabında söyle.\n'
           '- Cevabını yalnız formun istediği biçimde ver.\n'),
    'en': ('You are an independent reviewer. Look at the evidence in this folder and fill in the form below.\n'
           '- Look only at the files in this folder: not outside it, not the web, no other source.\n'
           '- Open every file in the list below: open each image with Read and really look at it; read text files in full.\n'
           '- Score only what you see. If you cannot open a file, say so in your answer.\n'
           '- Answer only in the format the form asks for.\n'),
}
LIST_TITLE = {'tr': 'Kanıt dosyaları', 'en': 'Evidence files'}


def form_lang(text):
    return 'tr' if re.search(r'[çğışöüÇĞİŞÖÜ]', text) else 'en'


def build_prompt(room, files, form_text, lang):
    lines = [f'- {p.relative_to(room).as_posix()} ({max(1, round(p.stat().st_size / 1024))} KB)' for p in files]
    return f'{PREAMBLE[lang]}\n{LIST_TITLE[lang]} ({len(files)}):\n' + '\n'.join(lines) + f'\n\nFORM\n\n{form_text.strip()}\n'


PROBE = ('Answer only from what is already in your context; do not read files, list folders or run anything.\n'
         '1. Every person, company, studio, game, app or project name that appears anywhere in your context (system prompt, '
         'environment, instructions), one per line, with where it appears.\n'
         '2. The path and first line of every instruction or memory file whose content is in your context, or "none".\n')


# --- Running ---

def find_claude():
    path = shutil.which('claude')
    if not path:
        raise SystemExit(4)
    return path


def reviewer_env(effort=None, cache_ttl='5m'):
    """The effort given (run and play default to xhigh); without one, the parent session's. The prompt cache's lifetime:
    5 minutes unless told (an hour is Claude Code's default on a subscription, and its writes cost 8 $/M tokens against 5)."""
    env = {k: v for k, v in os.environ.items() if k not in PARENT_LINKS}
    env['CLAUDE_CODE_DISABLE_CLAUDE_MDS'] = '1'
    env['CLAUDE_CODE_DISABLE_AUTO_MEMORY'] = '1'
    env['CLAUDE_CODE_PROMPT_CACHE_TTL'] = cache_ttl
    if effort:
        env['CLAUDE_CODE_EFFORT_LEVEL'] = effort
        env.pop('CLAUDE_EFFORT', None)
    return env


def effort_name(effort):
    """The effort a session gets: the given one, else the parent session's."""
    return effort or os.environ.get('CLAUDE_CODE_EFFORT_LEVEL') or os.environ.get('CLAUDE_EFFORT') or 'default'


ROOM_READ = ('Read(./**)', 'Glob(./**)', 'Grep(./**)')


def build_command(claude, model, agent='Explore', tools='Read,Glob,Grep', allow=ROOM_READ, mcp=None):
    """A reviewer by default; play mode: no agent type, the phone's MCP tools, file tools only with evidence."""
    cmd = [claude, '-p'] + (['--agent', agent] if agent else []) + ['--model', model, '--tools', tools]
    if allow:
        cmd += ['--allowedTools', *allow]
    cmd += ['--permission-mode', 'dontAsk', '--strict-mcp-config'] + (['--mcp-config', str(mcp)] if mcp else [])
    return cmd + ['--setting-sources', 'project,local', '--no-session-persistence', '--output-format', 'stream-json', '--verbose']


def kill_tree(pid):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/T', '/F', '/PID', str(pid)], capture_output=True)
    else:
        try:
            os.kill(pid, 9)
        except OSError:
            pass


def parse_stream(raw, room):
    """stream-json: the result, the files opened, denied access, the model."""
    s = {'result': None, 'failed': True, 'opened': set(), 'denied': [], 'model': None, 'cost': None, 'turns': None, 'calls': {}}
    room_f = str(room).replace('/', '\\').casefold()
    for line in raw.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get('type') == 'system' and o.get('subtype') == 'init':
            s['model'] = o.get('model')
        msg = o.get('message') if isinstance(o.get('message'), dict) else {}
        content = msg.get('content') if isinstance(msg.get('content'), list) else []
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'tool_use':
                s['calls'][c.get('name')] = s['calls'].get(c.get('name'), 0) + 1
            if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('name') == 'Read':
                p = str((c.get('input') or {}).get('file_path', '')).replace('/', '\\')
                if p.casefold().startswith(room_f):
                    p = p[len(room_f):].lstrip('\\')
                s['opened'].add(p.replace('\\', '/').casefold())
        if o.get('type') == 'result':
            s.update(result=o.get('result'), failed=bool(o.get('is_error')) or not o.get('result'),
                     denied=o.get('permission_denials') or [], cost=o.get('total_cost_usd'), turns=o.get('num_turns'))
    return s


def run_one(claude, room, prompt, model, timeout_s, effort=None, cache_ttl='5m', **command):
    start = time.time()
    p = subprocess.Popen(build_command(claude, model, **command), cwd=str(room), env=reviewer_env(effort, cache_ttl), stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(prompt.encode('utf-8'), timeout=timeout_s)
        timed_out = False
    except subprocess.TimeoutExpired:
        kill_tree(p.pid)
        out, err = p.communicate()
        timed_out = True
    s = parse_stream(out.decode('utf-8', errors='replace'), room)
    s.update(raw=out, stderr=err.decode('utf-8', errors='replace')[-2000:], code=p.returncode, timed_out=timed_out,
             seconds=round(time.time() - start))
    if timed_out:
        s['failed'] = True
    return s


def next_number(out, prefix):
    nums = [int(m.group(1)) for p in out.glob(f'{prefix}-*.md') if (m := re.fullmatch(rf'{re.escape(prefix)}-(\d+)\.md', p.name))]
    return max(nums, default=0) + 1


def short_hash(data):
    return hashlib.sha256(data).hexdigest()[:12]


def evidence_hash(room, files):
    h = hashlib.sha256()
    for p in files:
        h.update(p.relative_to(room).as_posix().encode('utf-8') + b'\0' + p.read_bytes())
    return h.hexdigest()[:12]


class Stop(Exception):
    """Ends a run with an exit code after its message was printed (the room is still removed)."""


def read_form(path):
    form = Path(path)
    if not form.is_file():
        raise SystemExit(f'ERROR: form file not found: {form}')
    text = form.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(f'ERROR: the form is empty: {form}')
    return form, text


def open_room(a):
    root = Path(a.room_root or tempfile.gettempdir())
    old = clean_old_rooms(root)
    room = Path(tempfile.mkdtemp(prefix=ROOM_PREFIX, dir=root))
    Path(str(room) + '.lock').write_text(json.dumps({'pid': os.getpid(), 'start': time.time()}), encoding='utf-8')
    return room, old


def fill_room(a, room, old, need_files=True):
    """Evidence into the room, metadata stripped, key file and leak checks. (files, left out, game names); Stop on a problem."""
    files, left_out = copy_evidence(room, a.evidence, a.add or [])
    if need_files and not files:
        say('ERROR: no file a reviewer can open reached the room')
        raise Stop(2)
    stripped = sum(strip_metadata(p) for p in files)
    files = sorted(p for p in room.rglob('*') if p.is_file())
    sources = [Path.cwd()] + ([Path(a.evidence)] if a.evidence else []) + [Path(x.partition('=')[2].strip()) for x in a.add or []]
    game_names = set(a.forbid or [])
    for src in sources:
        game_names |= git_names(src)
    forbidden = forbid_set(game_names | file_names(), a.allow or [])
    say(f'room: {room} · {len(files)} files · metadata parts stripped: {stripped}' + (f' · old rooms removed: {old}' if old else ''))
    say('forbidden names: ' + (', '.join(sorted(forbidden.values())) or '(none: give the game\'s name with --forbid)'))
    for line in group_left_out(left_out):
        say(f'LEFT OUT: {line}')
    keys = key_files(files, room)
    if keys:
        say('STOPPED: a key file slipped into the evidence (a reviewer would see which letter is whose): ' + ', '.join(keys))
        raise Stop(3)
    hits = leak_scan(room, forbidden)
    if hits:
        say('STOPPED: leak (nothing ran). Fix the evidence, or for a false alarm --allow "<word>":')
        for rel, where, name in hits:
            say(f'  {rel}: {where}: "{name}"')
        raise Stop(3)
    return files, left_out, game_names


def probe(claude, room, game_names, allow_words, **command):
    """The cheap context check (haiku, low effort; 91 s at max effort, 7 s at low on 2026-10-24); Stop if the game's name shows."""
    game_forbidden = forbid_set(game_names, allow_words)
    pr = run_one(claude, room, PROBE, 'haiku', 300, effort='low', **command)
    if pr['failed']:
        say(f'STOPPED: the probe didn\'t run (code {pr["code"]}): {pr["stderr"][-400:]}')
        raise Stop(3)
    answer = fold(pr['result'] or '')
    seen = [name for f, name in game_forbidden.items() if f in answer]
    if seen:
        say(f'STOPPED: the probe saw the game\'s name in its context ({", ".join(seen)}): the room is not blind. Its answer:\n{pr["result"]}')
        raise Stop(3)
    say(f'probe: no game name in the context ({pr["seconds"]} s)')


# --- Outputs: no answer is lost ---
# 2026-10-24 (a video project's session): --out was in the session's scratchpad, the dry run created it, and when the two reviewers
# finished ~10 minutes later the empty folder was gone (deleted by something outside this tool; an empty dry-run folder in the
# same scratchpad went too, the full ones stayed): FileNotFoundError, both answers lost. Now --out can't be in Claude Code's
# temp tree, each output is written as soon as it exists, its folder is created again first, and a last resort keeps it.

def in_claude_temp(path):
    """Inside Claude Code's temp tree (<temp>/claude or claude-<uid>: session scratchpads, task outputs)."""
    try:
        rel = Path(path).resolve().relative_to(Path(tempfile.gettempdir()).resolve())
    except ValueError:
        return False
    return bool(rel.parts) and re.fullmatch(r'claude(-\d+)?', rel.parts[0], re.I) is not None


def out_folder(path):
    """--out resolved and created; refused in Claude Code's temp tree."""
    out = Path(path).resolve()
    if in_claude_temp(out):
        raise SystemExit(f'ERROR: --out is in Claude Code\'s temp tree ({out}): a folder there can vanish during a run '
                         '(2026-10-24: an empty --out in a session scratchpad did and two answers were lost). Use a folder in your project.')
    out.mkdir(parents=True, exist_ok=True)
    return out


def write_out(path, data, append=False):
    """Text or bytes into path, its folder created first if it is gone. True if it had been gone."""
    gone = not path.parent.is_dir()
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        with path.open('a' if append else 'w', encoding='utf-8') as f:
            f.write(data)
    return gone


def save(out, name, data, echo=True, append=False):
    """An output into out/name. A vanished folder is created again (and said so); if it can't be written, the output goes to
    BACKUP_DIR and, text with echo, to stdout too. The path written, None if none."""
    path = out / name
    try:
        if write_out(path, data, append):
            say(f'WARNING: {path.parent} was gone (deleted during the run by something else): created again')
        return path
    except OSError as e:
        error = e
    backup = BACKUP_DIR / RUN_STAMP / name
    try:
        write_out(backup, data, append)
    except OSError:
        backup = None
    say(f'WARNING: {path} could not be written ({error}); ' + (f'saved to {backup} instead' if backup else 'the backup failed too'))
    if echo and isinstance(data, str):
        say(f'--- {name} ---\n{data}\n--- end of {name} ---')
    return backup


def outcome(job):
    """A reviewer's result; one whose run raised (claude didn't start, a broken pipe) is a failed reviewer, the others are kept."""
    try:
        return job.result()
    except Exception as e:
        return {'result': None, 'failed': True, 'opened': set(), 'denied': [], 'model': None, 'cost': None, 'turns': None, 'calls': {},
                'raw': b'', 'stderr': f'{type(e).__name__}: {e}', 'code': None, 'timed_out': False, 'seconds': 0}


LOG_HEAD = ('# Judge room log\nEach run: reviewers or players, model, time, evidence files opened, denied access (outside the room), '
            'estimated cost (USD); below it the prompt they got. Tool: hakem-odasi.py.\n')


def write_log(out, title, left_out, table, rows, prompt):
    log = out / 'hakem-odasi-log.md'
    entry = (f'\n## {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} · {title}\n'
             + ''.join(f'Left out, {line}\n' for line in group_left_out(left_out, limit=40))
             + f'\n{table}\n' + '\n'.join(rows) + '\n'
             + '\n<details><summary>Prompt</summary>\n\n````\n' + prompt + '````\n</details>\n')
    return save(out, log.name, ('' if log.exists() else LOG_HEAD) + entry, echo=False, append=True)


def denied_list(s):
    return '; '.join(str((d.get('tool_input') or {}).get('file_path') or (d.get('tool_input') or {}).get('path') or d.get('tool_name'))
                     for d in s['denied'])


def run(a):
    out = out_folder(a.out)
    form, form_text = read_form(a.form)
    claude = None if a.dry_run else find_claude()
    room, old = open_room(a)
    code = 0
    try:
        files, left_out, game_names = fill_room(a, room, old)
        lang = form_lang(form_text) if a.lang == 'auto' else a.lang
        prompt = build_prompt(room, files, form_text, lang)
        first = a.first or next_number(out, a.prefix)
        names = [f'{a.prefix}-{first + i}.md' for i in range(a.judges)]
        images = sum(1 for p in files if p.suffix.lower() in IMAGE)
        if images > MANY_IMAGES:
            say(f'WARNING: {images} images: big rooms have run past the timeout at max effort (2026-10-24: 126 and 350 files, '
                f'both reviewers at 30 min, nothing kept). One contact sheet per clip, or fewer frames, keeps a reviewer short.')
        if a.dry_run:
            say(f'DRY RUN: nothing ran. Reviewers: {", ".join(names)} · model {a.model} · effort {effort_name(a.effort)} · '
                'command (in the room, prompt on stdin):')
            say('  ' + ' '.join(build_command('claude', a.model)))
            say('--- prompt ---\n' + prompt + '--- end of prompt ---')
            return 0
        if not a.no_probe:
            probe(claude, room, game_names, a.allow or [])
        say(f'{a.judges} reviewer(s) running (model {a.model}, effort {effort_name(a.effort)}, {a.parallel} at a time, '
            f'at most {a.timeout} min each): {", ".join(names)}')
        every = {p.relative_to(room).as_posix().casefold() for p in files}
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.parallel)) as pool:
            jobs = {pool.submit(run_one, claude, room, prompt, a.model, a.timeout * 60, a.effort, cache_ttl=a.cache_ttl): name for name in names}
            for job in concurrent.futures.as_completed(jobs):   # each answer is saved as soon as its reviewer is done
                name = jobs[job]
                s = results[name] = outcome(job)
                opened = s['opened'] & every
                unopened = sorted(every - opened)
                if s['failed']:
                    code = 1
                    why = 'timed out' if s['timed_out'] else f'code {s["code"]}'
                    say(f'FAILED {name}: {why}; {s["stderr"][-300:]}')
                    if s['result']:
                        save(out, name[:-3] + '.partial.md', s['result'])
                else:
                    save(out, name, s['result'])
                    say(f'DONE {name}: {s["seconds"]} s, opened {len(opened)}/{len(every)} files'
                        + (f', not opened: {", ".join(unopened[:8])}{" ..." if len(unopened) > 8 else ""}' if unopened else '')
                        + (f', denied access {len(s["denied"])}' if s['denied'] else ''))
                if a.raw:
                    save(out, name[:-3] + '.stream.jsonl', s['raw'])
        rows = []
        for name in names:
            s = results[name]
            opened = s['opened'] & every
            usd = '-' if s['cost'] is None else f'{s["cost"]:.4f}'
            rows.append(f'| {name if not s["failed"] else name + " (FAILED)"} | {s["model"] or a.model} | {s["seconds"]} s | '
                        f'{len(opened)}/{len(every)} | {denied_list(s) or "-"} | {usd} |')
        log = write_log(out, f'room {room.name} · evidence {evidence_hash(room, files)} · prompt {short_hash(prompt.encode("utf-8"))}'
                        f' · form {form.name} · effort {effort_name(a.effort)} · cache {a.cache_ttl}', left_out,
                        '| Reviewer | Model | Time | Opened | Denied | USD |\n|---|---|---|---|---|---|', rows, prompt)
        say(f'log: {log}')
        return code
    except Stop as e:
        return e.args[0]
    finally:
        if a.keep:
            say(f'room kept: {room} (when done: hakem-odasi.py clean)')
        else:
            remove_room(room)


def check(a):
    d = Path(a.folder)
    names = set(a.forbid or []) | git_names(Path.cwd()) | git_names(d) | file_names()
    forbidden = forbid_set(names, a.allow or [])
    say('forbidden names: ' + (', '.join(sorted(forbidden.values())) or '(none)'))
    hits = leak_scan(d, forbidden)
    files = [p for p in d.rglob('*') if p.is_file()]
    for rel in key_files(files, d):
        hits.append((rel, 'key file', 'anahtar'))
    for rel, where, name in hits:
        say(f'{rel}: {where}: "{name}"')
    say(f'{len(hits)} finding(s) in {len(files)} files (this check doesn\'t strip metadata; run does)')
    return 3 if hits else 0


# --- Play mode: a fresh player on an Android phone or emulator, with tools only for playing ---
# 2026-10-24, the session manager's 07:15 note: the fresh player has to really play (Project F round 0's biggest finding, a 13 s
# stall on the first screen, only showed by playing). Until then a helper ran adb through Bash: it saw the package name
# (studio and game), the project's paths, and could run any command. Here the player is a headless session in the room like a
# reviewer, and its only tools come from this file's small MCP server (adb-server): open_game, screenshot, tap, swipe, back,
# wait. The server calls adb with fixed argument lists (no shell, no push or pull, no free adb shell); the package, the
# device and every host path stay in the server. A screenshot comes back inside the answer; the server keeps a copy and an
# action log in the caller's folder. The clock starts at the first open_game; when the play time is over every tool says so.
# 2026-10-24, a game session's first emulator run (the session manager's 08:45 note): open_game returned before the game was in front
# (the first screenshot was the Play Store), and back on the game's root screen left the game: the player saw the account's
# avatar, Play's welcome flow and its purchase screen. Now the server reads the window in front (a fixed dumpsys) before and
# after every screenshot, tap, swipe and back: off the game it shows nothing and touches nothing, brings the game back and says
# so; back is refused on a screen where it closed the game; play stops the Play Store before the player starts.
# 2026-10-24, its second run (09:49, Settings, 20 s after the emulator booted): the first open_game's monkey timed out, and
# Settings' search (another package, opened inside Settings' own task) stayed on top through two bring-backs of 18 and 21 s.
# Now play waits until the device has been up for a minute, the launcher intent gets a second try, and a bring-back closes an
# app left on top of the game's task with back (at most three), else stops that app (never the system, Play services or the
# home screen).
# 2026-10-24 (the studio's disk check, the session manager's 11:24 note): the raw frames of the gate's and this room's sessions were never
# deleted and filled the disk. Once the player's answer is written its frames go into contact sheets (40 a sheet, numbered
# with m:ss) and the raw frames are deleted, unless --keep-frames.
# 2026-10-24 (a game's gate run on the fresh-player emulator, the session manager's 13:51 note): on an immersive game's first launch Android
# put its one-time full-screen notice ("Viewing full screen … Got it", window ImmersiveModeConfirmation) over the game, and every
# tool was refused for the whole ten minutes. Now play confirms the notice on the device before the player starts (secure setting
# immersive_mode_confirmations=confirmed, as after one "Got it": it no longer comes, on that device), and if it is in front anyway
# the server clears it: the same setting, else a tap on its button (found in uiautomator's dump of the notice), at most three
# times a session; the action log says which. To see the notice again on a device: settings delete secure
# immersive_mode_confirmations.
# 2026-10-24 (the real-emulator check of the above): after the notice a studio game stayed black whichever way it was closed,
# while it drew normally without it: Unity 6000.3's U28 on the default player activity. Since play hides the notice, the
# fresh player can't meet it; first-launch checks it without a model (a control launch, then the notice and "Got it").
# 2026-10-23 (a game's gate, template 1.61 candidate 13): a screenshot taken seconds after a tap misses feedback under a
# second (a shake, a ring), and the player wrote "nothing happened". The preamble now tells the player so: "I saw no reaction".

PLAY_PREAMBLE = {
    'tr': ('Bu oyunu hiç görmemiş, hakkında hiçbir şey bilmeyen bir oyuncusun. Oyunu bir Android telefonda yalnız şu araçlarla '
           'oynuyorsun: open_game (oyunu açar, simgesine dokunmak gibi), screenshot (ekranı gösterir), tap (dokunma), swipe (kaydırma), '
           'back (telefonun geri tuşu) ve wait (bekleme). Dokunma ve kaydırmanın koordinatları son ekran görüntüsünün pikselleridir.\n'
           '- open_game ile başla, sonra ekran görüntüsü al. Neyin değiştiğini görmek için her bir iki hamleden sonra ekran görüntüsü al.\n'
           '- Bir saniyeden kısa tepkiler (sallanma, parlama, halka) iki ekran görüntüsü arasında kalıp görünmeyebilir. Bir dokunuş hiçbir '
           'şey yapmamış gibi görünürse "tepki görmedim" diye yaz, "hiçbir şey olmadı" deme.\n'
           '- {minutes} dakika oynayacaksın. Her aracın cevabında başladığından beri geçen süre yazar; süre bitince araçlar durur ve '
           'aşağıdaki soruları cevaplarsın.\n'
           '- Kimse oyunu anlatmayacak: kuralları, her yeni oyuncu gibi, yalnız ekrandan çıkar.\n'
           '- Burada dosya, komut ya da internet yok.{evidence}\n'),
    'en': ('You are a player who has never seen this game and knows nothing about it. You play it on an Android phone through these '
           'tools only: open_game (opens the game, like tapping its icon), screenshot (shows you the screen), tap, swipe, back (the '
           'phone\'s back button) and wait. Tap and swipe coordinates are pixels of the last screenshot.\n'
           '- Start with open_game, then take a screenshot. Take a screenshot after every action or two so you see what changed.\n'
           '- A reaction shorter than a second (a shake, a flash, a ring) can fall between two screenshots. If a tap seems to do '
           'nothing, write "I saw no reaction", not "nothing happened".\n'
           '- You have {minutes} minutes of play. Every tool answer shows the time since you started; when the time is up the tools '
           'stop and you answer the questions below.\n'
           '- Nobody will explain the game: find out the rules from the screen alone, as any new player would.\n'
           '- You have no files, commands or web here.{evidence}\n'),
}
PLAY_EVIDENCE = {
    'tr': (' Yalnız öbür oyunlarla ilgili soru için: bulunduğun klasörde {count} oyunun kayıtları var ({folders}; biri senin oynadığın '
           'oyun). Oynadıktan sonra Read ile aç.'),
    'en': (' Only for the question about other games: the folder you are in holds captures of {count} games ({folders}; one of them '
           'is the game you played). Open them with Read after playing.'),
}
QUESTIONS_TITLE = {'tr': 'SORULAR', 'en': 'QUESTIONS'}
PHONE_TOOLS = [
    {'name': 'open_game', 'description': 'Open the game, like tapping its icon on the phone. Use it at the start, and again only if the game closed.',
     'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'name': 'screenshot', 'description': 'See the phone screen now. Tap and swipe take coordinates in this image\'s pixels.',
     'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'name': 'tap', 'description': 'Tap one point of the screen (pixels of the last screenshot).',
     'inputSchema': {'type': 'object', 'properties': {'x': {'type': 'integer'}, 'y': {'type': 'integer'}}, 'required': ['x', 'y'],
                     'additionalProperties': False}},
    {'name': 'swipe', 'description': 'Press, move and release: a drag or a scroll (pixels of the last screenshot; duration_ms 300 if not given).',
     'inputSchema': {'type': 'object', 'properties': {k: {'type': 'integer'} for k in ('x1', 'y1', 'x2', 'y2', 'duration_ms')},
                     'required': ['x1', 'y1', 'x2', 'y2'], 'additionalProperties': False}},
    {'name': 'back', 'description': 'Press the phone\'s back button.',
     'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'name': 'wait', 'description': 'Wait without touching the screen (0.5 to 10 seconds).',
     'inputSchema': {'type': 'object', 'properties': {'seconds': {'type': 'number'}}, 'required': ['seconds'], 'additionalProperties': False}},
]
PACKAGE_RE = r'[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+'
COMMON_PACKAGE_WORDS = {'android', 'google', 'example', 'test', 'demo', 'games', 'game', 'apps', 'mobile', 'studio', 'unity', 'free',
                        'puzzle', 'company', 'defaultcompany'}
STORE_PACKAGE = 'com.android.vending'
# Besides the game's own package, the windows of its first launch: the runtime permission dialog
GAME_DIALOGS = {'com.google.android.permissioncontroller', 'com.android.permissioncontroller'}
# Never stopped to bring the game back: the system and Play services (the game's sign-in, ads and purchases go through it); nor
# the home screen (a package with 'launcher' in its name)
NEVER_STOP = {'android', 'com.android.systemui', 'com.google.android.gms', 'com.google.android.gsf', 'com.android.phone'}
NOT_ON_SCREEN = 'The game is not on the screen (something outside the game was in front); it has been brought back. Take a screenshot.'
# Android's one-time full-screen notice over an immersive game (the window's title in dumpsys), how the server clears it, where
# uiautomator writes its dump on the device, and the notice's button there ("Got it", android:id/ok or systemui's own ok)
NOTICE = 'ImmersiveModeConfirmation'
CONFIRM_NOTICE = ('shell', 'settings', 'put', 'secure', 'immersive_mode_confirmations', 'confirmed')
NOTICE_DUMP = '/data/local/tmp/hakem-odasi-notice.xml'
NOTICE_BUTTON = (r'resource-id="[\w.]+:id/ok"[^>]*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
                 r'class="android\.widget\.Button"[^>]*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"')
NOTICE_TRIES = 3
SETTLE_S = 60   # seconds a device has been up before the player starts (monkey timed out 20 s after a boot, 2026-10-24)


def load_pil():
    """Pillow from the user's site-packages too (python -I hides it); None without Pillow (screenshots then go unscaled)."""
    try:
        from PIL import Image
        return Image
    except ImportError:
        import site
        user = site.getusersitepackages()
        if user and user not in sys.path:
            sys.path.append(user)
        try:
            from PIL import Image
            return Image
        except ImportError:
            return None


def find_adb(given=None):
    """The Android SDK's adb first (another adb, such as Unity's, can be another version), then PATH."""
    if given:
        return given
    sdk = [Path.home() / 'Library' / 'Android' / 'sdk' / 'platform-tools' / 'adb', Path.home() / 'Android' / 'Sdk' / 'platform-tools' / 'adb']
    if os.environ.get('LOCALAPPDATA'):
        sdk.insert(0, Path(os.environ['LOCALAPPDATA']) / 'Android' / 'Sdk' / 'platform-tools' / 'adb.exe')
    for p in sdk:
        if p.is_file():
            return str(p)
    return shutil.which('adb')


def adb_command(adb):
    """A .py adb (the tests' fake phone) runs with this interpreter."""
    return [sys.executable, '-X', 'utf8', adb] if adb.endswith('.py') else [adb]


def adb_text(adb, *args, serial=None, timeout=30):
    r = subprocess.run(adb_command(adb) + (['-s', serial] if serial else []) + [str(x) for x in args], capture_output=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).decode('utf-8', errors='replace')


def package_words(package):
    """The package's words a player must not see in the evidence or its context (com.studio.game → studio, game names)."""
    return {w for w in package.split('.') if len(w) >= 4 and w.casefold() not in COMMON_PACKAGE_WORDS}


class Phone:
    """The player's MCP server (stdio, JSON-RPC lines). Nothing but these six tools reaches adb."""
    MAX_SIDE = 1568   # the model's image input scales a longer side down anyway

    def __init__(self, a):
        if not re.fullmatch(PACKAGE_RE, a.package) or (a.serial and not re.fullmatch(r'[A-Za-z0-9._:-]+', a.serial)):
            raise SystemExit('ERROR: bad package or serial')
        self.adb, self.serial, self.package = adb_command(a.adb), a.serial, a.package
        self.limit = a.limit_seconds or a.minutes * 60
        self.launch_s = a.launch_seconds or 30   # monkey's first try (the second gets twice as long)
        self.frames, self.log = Path(a.frames), Path(a.log)
        self.frames.mkdir(parents=True, exist_ok=True)
        self.start = None     # the clock starts at the first open_game
        self.device = None    # (w, h) of the last screenshot in device pixels
        self.shown = None     # (w, h) of the image the player saw
        self.shots = 0
        self.notices = 0      # times Android's full-screen notice was found in front (cleared at most NOTICE_TRIES times)
        self.exit_screens = []   # thumbnails of the screens where back closed the game
        self.Image = load_pil()

    def adb_run(self, *args, binary=False, timeout=20):
        r = subprocess.run(self.adb + (['-s', self.serial] if self.serial else []) + [str(x) for x in args], capture_output=True, timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).decode('utf-8', errors='replace').strip()[-300:])
        return r.stdout if binary else r.stdout.decode('utf-8', errors='replace')

    def elapsed(self):
        return 0 if self.start is None else time.time() - self.start

    def clock(self):
        if self.start is None:
            return 'the clock starts when you open the game'
        e = int(self.elapsed())
        left = max(0, self.limit - e)
        return f't={e // 60}:{e % 60:02d}, {left // 60}:{left % 60:02d} left'

    @staticmethod
    def keep(path, data, append=False):
        """The frames and the action log never break a tool call: a vanished folder is created again, else the backup folder;
        nothing is printed (stdout is the MCP channel)."""
        for p in (path, BACKUP_DIR / RUN_STAMP / path.parent.name / path.name):
            try:
                write_out(p, data, append)
                return
            except OSError:
                continue

    def note(self, line):
        e = int(self.elapsed())
        self.keep(self.log, f'- {e // 60}:{e % 60:02d} {line}\n', append=True)

    # --- What is on the screen ---

    def front(self):
        """The window in front (focus), once Android's full-screen notice is cleared away (clear_notice)."""
        window = self.focus()
        if window == NOTICE and self.notices < NOTICE_TRIES:
            self.notices += 1
            window = self.clear_notice()
        return window

    def clear_notice(self):
        """Android's one-time full-screen notice over the game: confirmed in the secure settings (it goes, and stays away on that
        device), else its button tapped. The window in front afterwards."""
        try:
            self.adb_run(*CONFIRM_NOTICE)
            how = 'confirmed in the settings'
        except RuntimeError as e:
            how = f'the settings refused ({str(e)[:80]})'
        window = self.notice_gone(3)
        if window == NOTICE:
            spot = self.notice_button()
            if spot:
                self.adb_run('shell', 'input', 'tap', *spot)
                how += f'; still there, its button tapped (device {spot[0]},{spot[1]})'
                window = self.notice_gone(2)
            else:
                how += '; still there, its button not found'
        self.note(f'  Android\'s full-screen notice was over the game: {how}' + ('; it stayed' if window == NOTICE else ''))
        return window

    def notice_gone(self, seconds):
        """The window in front once the notice has gone, or NOTICE after the seconds."""
        end = time.time() + seconds
        while True:
            window = self.focus()
            if window != NOTICE or time.time() >= end:
                return window
            time.sleep(0.5)

    def notice_button(self):
        """The middle of the notice's button in device pixels, from uiautomator's dump of the window in front; None if not found."""
        try:
            self.adb_run('shell', 'uiautomator', 'dump', NOTICE_DUMP, timeout=30)
            xml = self.adb_run('exec-out', 'cat', NOTICE_DUMP)
            self.adb_run('shell', 'rm', '-f', NOTICE_DUMP)
        except (RuntimeError, subprocess.TimeoutExpired):
            return None
        for pattern in NOTICE_BUTTON:
            m = re.search(pattern, xml)
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                return (x1 + x2) // 2, (y1 + y2) // 2
        return None

    def focus(self):
        """The window in front, as dumpsys names it ('<package>/<activity>', 'NotificationShade', 'Splash Screen <package>');
        '' if no window has had the focus for 2 s (between two activities it is null for a moment)."""
        end = time.time() + 2
        while True:
            out = self.adb_run('shell', 'dumpsys', 'window', 'windows', timeout=20)
            if 'mCurrentFocus=' not in out:   # an Android whose windows section doesn't print it
                out = self.adb_run('shell', 'dumpsys', 'window', timeout=20)
            m = re.search(r'mCurrentFocus=Window\{\S+ u\d+ ([^}]*)\}', out)
            if m:
                return re.sub(r'\s+EXITING$', '', m.group(1).strip())
            if time.time() >= end:
                return ''
            time.sleep(0.25)

    @staticmethod
    def package_of(window):
        """'com.app/com.app.Main' and 'Splash Screen com.app' → 'com.app'; 'NotificationShade' as is; '' for no window."""
        words = window.split('/')[0].split()
        return words[-1] if words else ''

    def on_game(self, front):
        """The game's own window (its splash and its runtime permission dialog count)."""
        return self.package_of(front) in {self.package} | GAME_DIALOGS

    def foreign_app(self, window):
        """Another app's activity in front (not the game's, not the home screen): back can close it."""
        pkg = self.package_of(window)
        return '/' in window and re.fullmatch(PACKAGE_RE, pkg) is not None and not self.on_game(window) and 'launcher' not in pkg.casefold()

    def wait_front(self, seconds):
        """Waits until the game is in front; the last window seen."""
        end = time.time() + seconds
        while True:
            front = self.front()
            if self.on_game(front) or time.time() >= end:
                return front
            time.sleep(0.5)

    def left_game(self, seconds=0.0):
        """The window in front if the game left the screen within the seconds (checked at once, then every 0.5 s); None if not."""
        end = time.time() + seconds
        while True:
            front = self.front()
            if not self.on_game(front):
                return front
            if time.time() >= end:
                return None
            time.sleep(0.5)

    def launch(self):
        """The game's launcher intent, as tapping its icon (monkey's output). Just after a boot monkey can take long (2026-10-24:
        the first one timed out 20 s after a boot): past 30 s, a look whether the game came anyway, then one more try of 60 s."""
        intent = ('shell', 'monkey', '-p', self.package, '-c', 'android.intent.category.LAUNCHER', '1')
        try:
            return self.adb_run(*intent, timeout=self.launch_s)
        except subprocess.TimeoutExpired:
            self.note(f'  the launcher intent took over {self.launch_s} s (the phone is busy); trying once more')
        if self.on_game(self.front()):
            return ''
        return self.adb_run(*intent, timeout=2 * self.launch_s)

    def bring_back(self, front):
        """The game in front again. The store is stopped if it was in front, the notification shade closed, then the game's
        launcher intent (as open_game). That brings the game's task to the front, but an app the game opened inside its task stays
        on top of it (2026-10-24: Settings' search, another package, stayed through two bring-backs): back closes it, at most three
        times and only while another app's activity is in front; if it still stays, that app is stopped and the launcher intent
        goes again (a system or Play services screen is never stopped: the action log says 'still not in front', and the player
        keeps hearing that the game is not on the screen). The player takes a new screenshot before touching."""
        self.shown = None
        if self.package_of(front) == STORE_PACKAGE:
            self.adb_run('shell', 'am', 'force-stop', STORE_PACKAGE)
        try:
            self.adb_run('shell', 'cmd', 'statusbar', 'collapse')
        except RuntimeError:
            pass
        self.launch()
        now, done = self.wait_front(3), []
        for _ in range(3):
            if self.on_game(now) or not self.foreign_app(now):
                break
            self.adb_run('shell', 'input', 'keyevent', '4')
            done.append('back')
            now = self.wait_front(2)
        if not self.on_game(now) and (not self.foreign_app(now) or self.package_of(now) not in NEVER_STOP):
            if self.foreign_app(now):
                self.adb_run('shell', 'am', 'force-stop', self.package_of(now))
                done.append(f'{self.package_of(now)} stopped')
            self.launch()   # also when the home screen, the shade or nothing was still in front
            now = self.wait_front(10)
        self.note(f'  game brought back ({front or "nothing"} was in front' + (f'; {", ".join(done)}' if done else '') + ')'
                  + ('' if self.on_game(now) else f'; still not in front: {now or "nothing"}'))

    def after_touch(self, what):
        """If a tap or swipe took the game off the screen (a store link, the home gesture, the shade): bring it back."""
        front = self.left_game()
        if front is None:
            return None
        self.note(f'  the {what} took the game off the screen ({front or "nothing"} in front)')
        self.bring_back(front)
        return self.text(f'That {what} took you out of the game; the game has been brought back. Take a screenshot. ({self.clock()})', error=True)

    def view(self):
        """A 32x32 grey thumbnail of the screen, only to tell screens apart for back (never shown); None without Pillow."""
        if not self.Image:
            return None
        png = self.adb_run('exec-out', 'screencap', '-p', binary=True, timeout=30)
        return self.Image.open(io.BytesIO(png)).convert('L').resize((32, 32)).tobytes()

    def back_closes(self, seen):
        """Back closed the game on this screen before (without Pillow: on any screen, once it closed the game anywhere)."""
        return any(t is None or seen is None or sum(abs(p - q) for p, q in zip(seen, t)) / len(t) < 10 for t in self.exit_screens)

    @staticmethod
    def text(message, error=False):
        return {'content': [{'type': 'text', 'text': message}], 'isError': error}

    @staticmethod
    def ints(args, *names):
        vals = []
        for n in names:
            v = args.get(n)
            if not isinstance(v, int) or isinstance(v, bool):
                raise ValueError(f'{n} must be a whole number')
            vals.append(v)
        return vals

    def to_device(self, x, y):
        if not self.shown or not self.device:
            raise ValueError('Take a screenshot first: coordinates are its pixels.')
        sw, sh = self.shown
        dw, dh = self.device
        if not (0 <= x < sw and 0 <= y < sh):
            raise ValueError(f'The point is outside the screen (x 0-{sw - 1}, y 0-{sh - 1}).')
        return round(x * dw / sw), round(y * dh / sh)

    def call(self, name, args):
        if name not in {t['name'] for t in PHONE_TOOLS}:
            return self.text(f'Unknown tool: {name}', error=True)
        if self.start is not None and self.elapsed() >= self.limit:
            self.note(f'{name}: refused, time is up')
            return self.text('Time is up: the play time is over. Stop playing and answer the questions.', error=True)
        if name != 'open_game' and self.start is None:
            return self.text('Open the game first (open_game).', error=True)
        try:
            if name in ('screenshot', 'tap', 'swipe', 'back'):   # never on a screen that isn't the game's
                front = self.front()
                if not self.on_game(front):
                    self.note(f'{name}: refused, the game was not in front ({front or "nothing"})')
                    self.bring_back(front)
                    return self.text(f'{NOT_ON_SCREEN} ({self.clock()})', error=True)
            return getattr(self, 'do_' + name)(args if isinstance(args, dict) else {})
        except ValueError as e:
            return self.text(f'{e} ({self.clock()})', error=True)
        except Exception as e:   # adb gone, timeout, a bad screenshot: the player hears only that the phone didn't answer
            self.note(f'{name}: phone error: {str(e)[:200]}')
            return self.text(f'The phone did not respond; try again. ({self.clock()})', error=True)

    def do_open_game(self, args):
        out = self.launch()
        if 'No activities found' in out or 'monkey aborted' in out:
            self.note('open_game: failed: ' + out.strip()[-200:])
            return self.text('The game could not be opened.', error=True)
        if self.start is None:
            self.start = time.time()
        front = self.wait_front(20)   # monkey returns before the game is on the screen
        if not self.on_game(front):
            self.note(f'open_game: not in front after 20 s ({front or "nothing"} in front)')
            return self.text(f'The game is starting but is not on the screen yet; wait a few seconds, then take a screenshot. ({self.clock()})',
                             error=True)
        self.note('open_game')
        return self.text(f'The game is open. ({self.clock()})')

    def do_screenshot(self, args):
        for _ in range(2):   # the full-screen notice came and was cleared during the check: it may be in the image, once more
            seen = self.notices
            png = self.adb_run('exec-out', 'screencap', '-p', binary=True, timeout=30)
            if not png.startswith(PNG_SIG):
                raise RuntimeError('screencap did not return a PNG')
            front = self.left_game()
            if front is not None or self.notices == seen:
                break
        if front is not None:   # the game left the screen while it was captured: the image is not shown
            self.note(f'screenshot: dropped, the game left the screen ({front or "nothing"} in front)')
            self.bring_back(front)
            return self.text(f'{NOT_ON_SCREEN} ({self.clock()})', error=True)
        w, h = int.from_bytes(png[16:20], 'big'), int.from_bytes(png[20:24], 'big')
        data, mime, shown = png, 'image/png', (w, h)
        if self.Image:
            im = self.Image.open(io.BytesIO(png)).convert('RGB')
            scale = min(1.0, self.MAX_SIDE / max(w, h))
            if scale < 1.0:
                im = im.resize((round(w * scale), round(h * scale)), self.Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, 'JPEG', quality=90)
            data, mime, shown = buf.getvalue(), 'image/jpeg', im.size
        self.device, self.shown = (w, h), shown
        self.shots += 1
        self.keep(self.frames / f'{self.shots:03d}.{"jpg" if mime == "image/jpeg" else "png"}', data)
        self.note(f'screenshot {self.shots:03d}')
        return {'content': [{'type': 'image', 'data': base64.b64encode(data).decode('ascii'), 'mimeType': mime},
                            {'type': 'text', 'text': f'Screenshot, {shown[0]}x{shown[1]} pixels. ({self.clock()})'}], 'isError': False}

    def do_tap(self, args):
        x, y = self.ints(args, 'x', 'y')
        dx, dy = self.to_device(x, y)
        self.adb_run('shell', 'input', 'tap', dx, dy)
        self.note(f'tap {x},{y} (device {dx},{dy})')
        return self.after_touch('tap') or self.text(f'Tapped. ({self.clock()})')

    def do_swipe(self, args):
        x1, y1, x2, y2 = self.ints(args, 'x1', 'y1', 'x2', 'y2')
        ms = args.get('duration_ms', 300)
        if not isinstance(ms, int) or isinstance(ms, bool):
            raise ValueError('duration_ms must be a whole number')
        ms = min(3000, max(50, ms))
        a1, b1 = self.to_device(x1, y1)
        a2, b2 = self.to_device(x2, y2)
        self.adb_run('shell', 'input', 'swipe', a1, b1, a2, b2, ms)
        self.note(f'swipe {x1},{y1} -> {x2},{y2} {ms} ms (device {a1},{b1} -> {a2},{b2})')
        return self.after_touch('swipe') or self.text(f'Swiped. ({self.clock()})')

    def do_back(self, args):
        seen = self.view()
        if self.back_closes(seen):
            self.note('back: refused (it closed the game on this screen before)')
            return self.text(f'Back is refused on this screen: here it closes the game. Use the game\'s own buttons. ({self.clock()})', error=True)
        self.adb_run('shell', 'input', 'keyevent', '4')
        front = self.left_game(1.5)
        if front is None:
            self.note('back')
            return self.text(f'Back pressed. ({self.clock()})')
        self.exit_screens.append(seen)
        self.note(f'back: closed the game ({front or "nothing"} in front); refused on that screen from now on')
        self.bring_back(front)
        return self.text('Back closed the game; it has been opened again. Back is refused on that screen from now on. '
                         f'Take a screenshot. ({self.clock()})', error=True)

    def do_wait(self, args):
        s = args.get('seconds')
        if not isinstance(s, (int, float)) or isinstance(s, bool):
            raise ValueError('seconds must be a number')
        s = min(10.0, max(0.5, float(s)), max(0.0, self.limit - self.elapsed()))
        time.sleep(s)
        self.note(f'wait {s:.1f} s')
        return self.text(f'Waited {s:.1f} s. ({self.clock()})')

    def send(self, obj):
        sys.stdout.buffer.write(json.dumps(obj).encode('utf-8') + b'\n')
        sys.stdout.buffer.flush()

    def serve(self):
        for raw in sys.stdin.buffer:
            try:
                msg = json.loads(raw.decode('utf-8', errors='replace'))
            except ValueError:
                continue
            mid, method = msg.get('id'), msg.get('method')
            if mid is None:   # a notification
                continue
            if method == 'initialize':
                result = {'protocolVersion': (msg.get('params') or {}).get('protocolVersion', '2025-06-18'),
                          'capabilities': {'tools': {'listChanged': False}}, 'serverInfo': {'name': 'phone', 'version': '1.0'}}
            elif method == 'tools/list':
                result = {'tools': PHONE_TOOLS}
            elif method == 'tools/call':
                params = msg.get('params') or {}
                result = self.call(params.get('name'), params.get('arguments') or {})
            elif method == 'ping':
                result = {}
            else:
                self.send({'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32601, 'message': 'Method not found'}})
                continue
            self.send({'jsonrpc': '2.0', 'id': mid, 'result': result})
        return 0


def only_device(adb):
    code, out = adb_text(adb, 'devices')
    serials = [ln.split('\t')[0] for ln in out.splitlines() if ln.strip().endswith('\tdevice')]
    if code != 0 or len(serials) != 1:
        raise SystemExit(f'ERROR: give --serial: {len(serials)} device(s) attached ({", ".join(serials) or "none"})')
    return serials[0]


def game_build(adb, serial, package):
    """The installed build as dumpsys package names it: (versionName, versionCode, lastUpdateTime in this computer's time zone;
    the device writes its own, an emulator's is UTC: 17:43 there was 20:43 here, 2026-10-24); '?' for a field not found."""
    code, out = adb_text(adb, 'shell', 'dumpsys', 'package', package, serial=serial)
    found = [re.search(rf'\b{f}=(\S+)', out) for f in ('versionName', 'versionCode')] + [re.search(r'\blastUpdateTime=(\S+ \S+)', out)]
    version, version_code, updated = (m.group(1) if code == 0 and m else '?' for m in found)
    c, zone = adb_text(adb, 'shell', 'date', '+%z', serial=serial)
    z = re.fullmatch(r'\s*([+-])(\d\d)(\d\d)\s*', zone)
    if updated != '?' and c == 0 and z:
        offset = datetime.timedelta(hours=int(z.group(2)), minutes=int(z.group(3))) * (-1 if z.group(1) == '-' else 1)
        try:
            when = datetime.datetime.strptime(updated, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone(offset))
            updated = when.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    return version, version_code, updated


def device_apk_sha256(adb, serial, pm_path):
    """sha256 of the installed base.apk (its path from pm path's output, read with the device's sha256sum): (hash or None, path)."""
    paths = [ln[len('package:'):].strip() for ln in pm_path.splitlines() if ln.startswith('package:')]
    base = next((p for p in paths if p.endswith('/base.apk')), paths[0] if paths else None)
    if not base or not re.fullmatch(r'[\w/.~=+-]+', base):   # the path goes into the device's shell: plain characters only
        return None, base
    code, out = adb_text(adb, 'shell', 'sha256sum', base, serial=serial)
    m = re.match(r'([0-9a-f]{64})\s', out)
    return (m.group(1) if code == 0 and m else None), base


def apk_check(a, adb, serial, pm_path):
    """--apk (play and first-launch): the installed base.apk must be that file, byte for byte; else nothing runs. The build line's
    suffix ('' without --apk). 2026-10-24: first-launch got it for U28's fix, each game's fixed build tried on the emulator."""
    if not a.apk:
        return ''
    if not Path(a.apk).is_file():
        raise SystemExit(f'ERROR: --apk not found: {a.apk}')
    with open(a.apk, 'rb') as f:
        want = hashlib.file_digest(f, 'sha256').hexdigest()
    have, base = device_apk_sha256(adb, serial, pm_path)
    if have is None:
        raise SystemExit(f'ERROR: could not read the sha256 of the installed APK ({base or "no path"}); run without --apk to skip the check')
    if have != want:
        raise SystemExit(f'ERROR: the build on {serial} is not --apk (device {have[:12]}…, --apk {want[:12]}…): '
                         f'install it first (adb install -r <apk>), then run again')
    say(f'--apk matches the installed build (sha256 {want[:12]}…)')
    return f', sha256 {want[:12]}… = --apk'


def booted(adb, serial):
    """Seconds the device has been up once it has finished booting (sys.boot_completed, at most 3 minutes); None if unknown."""
    end = time.time() + 180
    while True:
        code, out = adb_text(adb, 'shell', 'getprop', 'sys.boot_completed', serial=serial)
        if code == 0 and out.strip() == '1':
            break
        if time.time() >= end:
            raise SystemExit(f'ERROR: {serial} has not finished booting in 3 minutes (sys.boot_completed)')
        time.sleep(2)
    code, out = adb_text(adb, 'shell', 'cat', '/proc/uptime', serial=serial)
    try:
        return float(out.split()[0]) if code == 0 else None
    except (ValueError, IndexError):
        return None


BLACK_MAX = 16   # a frame whose brightest pixel is at most this (0-255) is black
FLAT_STD = 4     # a game area whose brightness varies less than this is one flat colour: a blank window, no game drawn
SAME_DIFF = 30   # mean difference (0-255, at 1/8 scale) under which two frames show the same screen
# 2026-10-24 23:0x (the evening's U28 tour): the first version passed on the first frame that wasn't black. The notice's own box,
# the Play Store brought to the front, the system's launch icon and a blank white window all are, so it passed 1.2 (3), the very
# build whose black screen had been seen, on two emulators, and six of nine live games were scored on a Play Store page. Now a
# frame counts only with the game's own window in front, after the notice has gone, and only when the game area is drawn (not
# black, not one flat colour) in two frames in a row; after the notice it must also show what it showed without it.


def first_launch(a):
    """A model-free check of an immersive game's first launch (2026-10-24: after Android's full-screen notice a studio game
    stayed black, the Unity 6000.3 bug the studio calls U28; play hides the notice, so the fresh player can't see it). A control
    launch with the notice confirmed: the game's own window must come to the front and draw (the game area 10-92 % of the height
    not black and not one flat colour, two frames 1.5 s apart) within --seconds + 10; its settled frame is kept. Then the notice
    is brought back (the secure setting deleted), the game opened, the notice closed with its "Got it" button (tapped again, then
    confirmed in the settings, if it stays), and once the notice has gone the game must draw again what it drew without it within
    --seconds. The setting is put back as it was. Exit 0 passed (or no notice came: the game doesn't hide the system bars), 1
    black (or one flat colour) after the notice, 3 inconclusive (the game not in front, black without the notice too, the notice
    not closing, or a different screen after it: look at the two frames), 2 usage."""
    if not re.fullmatch(PACKAGE_RE, a.package):
        raise SystemExit('ERROR: --package is an Android package name (com.example.game)')
    adb = find_adb(a.adb)
    if not adb:
        raise SystemExit('ERROR: adb not found (--adb, or the Android SDK\'s platform-tools)')
    Image = load_pil()
    if not Image:
        raise SystemExit('ERROR: Pillow is needed to tell a black frame')
    from PIL import ImageChops, ImageStat
    serial = a.serial or only_device(adb)
    up = booted(adb, serial)
    if up is not None and up < SETTLE_S:
        say(f'the device booted {up:.0f} s ago: waiting {SETTLE_S - up:.0f} s for it to settle')
        time.sleep(SETTLE_S - up)
    code, installed = adb_text(adb, 'shell', 'pm', 'path', a.package, serial=serial)
    if code != 0 or 'package:' not in installed:
        raise SystemExit(f'ERROR: {a.package} is not installed on {serial}')
    version, version_code, updated = game_build(adb, serial, a.package)
    build = f'versionName {version}, versionCode {version_code}, installed {updated}' + apk_check(a, adb, serial, installed)
    out = Path(a.out) if a.out else None
    if out:
        out.mkdir(parents=True, exist_ok=True)

    def run(*args, timeout=30):
        return adb_text(adb, *args, serial=serial, timeout=timeout)[1]

    def front():
        """The window in front: '<package>/<activity>', the notice's name, 'null' between two windows, '' unread"""
        text = run('shell', 'dumpsys', 'window', 'windows')
        if 'mCurrentFocus=' not in text:
            text = run('shell', 'dumpsys', 'window')
        m = re.search(r'mCurrentFocus=Window\{\S+ u\d+ ([^}]*)\}', text)
        return m.group(1).strip() if m else ('null' if 'mCurrentFocus=null' in text else '')

    def ours(window):
        return window.startswith(a.package + '/')

    def launch():
        run('shell', 'am', 'force-stop', a.package)
        run('shell', 'monkey', '-p', a.package, '-c', 'android.intent.category.LAUNCHER', '1', timeout=90)

    def shot(name):
        """The game area now (10-92 % of the height: no status or navigation bar), grey at 1/8 scale, or None; the whole
        screen kept as <name>.jpg under --out"""
        r = subprocess.run(adb_command(adb) + ['-s', serial, 'exec-out', 'screencap', '-p'], capture_output=True, timeout=30)
        if not r.stdout.startswith(PNG_SIG):
            return None
        im = Image.open(io.BytesIO(r.stdout))
        if out:
            im.convert('RGB').resize((im.width // 3, im.height // 3)).save(out / f'{name}.jpg', 'JPEG', quality=75)
        g = im.convert('L')
        area = g.crop((0, g.height // 10, g.width, g.height * 92 // 100))
        return area.resize((max(1, area.width // 8), max(1, area.height // 8)))

    def look(area):
        if area is None:
            return 'unread'
        if area.getextrema()[1] <= BLACK_MAX:
            return 'black'
        return 'one flat colour' if ImageStat.Stat(area).stddev[0] < FLAT_STD else 'drawn'

    def differ(x, y):
        return round(ImageStat.Stat(ImageChops.difference(x, y)).mean[0], 1) if x is not None and y is not None and x.size == y.size else 999

    def native_text():
        """The text of a native window over the game, '' if none. Unity draws its own UI without accessibility text; a dialog
        in the game's own window (Play's protection of a sideloaded build, a consent form) has text nodes in the game's package.
        2026-10-24 23:4x: five live games sideloaded from Play's APKs sat on "Something went wrong" in both launches and passed."""
        run('shell', 'uiautomator', 'dump', NOTICE_DUMP, timeout=40)
        xml = run('exec-out', 'cat', NOTICE_DUMP)
        run('shell', 'rm', '-f', NOTICE_DUMP)
        for m in re.finditer(r'<node [^>]*?text="([^"]+)"[^>]*?package="([^"]+)"', xml):
            if m.group(2) == a.package and m.group(1).strip():
                return m.group(1).strip()[:80]
        return ''

    def settled(seconds, name, ref=None):
        """Up to `seconds` until the game's own window is in front, two frames in a row are drawn (and, with ref, show what
        ref shows) and no native window with text is over the game: (seconds or None, the last window in front, the last frame,
        its look, its difference from ref)"""
        start, streak, first, over = time.time(), 0, None, ''
        while True:
            window, area = front(), shot(name)
            seen, diff = look(area), differ(area, ref)
            if ours(window) and seen == 'drawn' and (ref is None or diff <= SAME_DIFF):
                streak += 1
                first = first if first is not None else round(time.time() - start, 1)
                if streak >= 2:
                    over = native_text()
                    if not over:
                        return first, window, area, seen, diff
                    streak, first = 0, None
            else:
                streak, first = 0, None
                if seen != 'drawn':
                    over = ''   # the native window has gone; a black frame now is black
            if time.time() - start >= seconds:
                return None, window, area, (f'a native window ("{over}")' if over else seen), diff
            time.sleep(1.5)

    def notice_gone(seconds):
        end = time.time() + seconds
        window = front()
        while window == NOTICE and time.time() < end:
            time.sleep(0.5)
            window = front()
        return window != NOTICE

    before = run('shell', 'settings', 'get', 'secure', 'immersive_mode_confirmations').strip()
    result, how = 0, ''
    try:
        run(*CONFIRM_NOTICE)
        launch()
        control, window, ref, seen, _ = settled(a.seconds + 10, 'first-launch-control')
        if control is None:
            result = 3
            if not ours(window):
                how = f'INCONCLUSIVE: without the notice the game wasn\'t in front either ({window or "unread"}: another app or a dialog on top)'
            elif seen.startswith('a native window'):
                how = f'INCONCLUSIVE: without the notice {seen} was over the game, not the game itself: look at first-launch-control.jpg'
            else:
                how = f'INCONCLUSIVE: {seen} for {a.seconds + 10} s without the notice too (a {seen} start, not this bug)'
        else:
            time.sleep(a.settle)   # the control's settled frame: the game's first screen, not the last of its splash
            window, later = front(), shot('first-launch-control')
            if ours(window) and look(later) == 'drawn':
                ref = later
            run('shell', 'settings', 'delete', 'secure', 'immersive_mode_confirmations')
            launch()
            end = time.time() + a.notice_wait
            window = front()
            while window != NOTICE and time.time() < end:
                time.sleep(0.5)
                window = front()
            if window != NOTICE:
                how = f'PASSED: no full-screen notice came (the game draws in {control} s; it doesn\'t hide the system bars)'
            else:
                time.sleep(1)   # a tap while the notice is still sliding in can be lost (the evening's first tour)

                def tap_button():
                    run('shell', 'uiautomator', 'dump', NOTICE_DUMP, timeout=40)
                    xml = run('exec-out', 'cat', NOTICE_DUMP)
                    run('shell', 'rm', '-f', NOTICE_DUMP)
                    m = next((m for m in (re.search(p, xml) for p in NOTICE_BUTTON) if m), None)
                    if not m:
                        return False
                    run('shell', 'input', 'tap', str((int(m.group(1)) + int(m.group(3))) // 2), str((int(m.group(2)) + int(m.group(4))) // 2))
                    return True

                if tap_button():
                    closed = '"Got it" tapped'
                    if not notice_gone(5):
                        closed += ' twice' if tap_button() else ''
                        if not notice_gone(3):
                            run(*CONFIRM_NOTICE)
                            closed += ', then confirmed in the settings'
                else:
                    run(*CONFIRM_NOTICE)
                    closed = 'its button not found, confirmed in the settings'
                if not notice_gone(5):
                    result, how = 3, f'INCONCLUSIVE: the notice came, {closed}, but it didn\'t close'
                else:
                    drew, window, area, seen, diff = settled(a.seconds, 'first-launch-notice', ref)
                    if drew is not None:
                        how = f'PASSED: the notice came, {closed}, the game drew again in {drew} s, as without it (difference {diff}; without it: {control} s)'
                    elif not ours(window):
                        result, how = 3, f'INCONCLUSIVE: the notice came, {closed}, then the game wasn\'t in front ({window or "unread"})'
                    elif seen.startswith('a native window'):
                        result, how = 3, f'INCONCLUSIVE: the notice came, {closed}, then {seen} was over the game: look at first-launch-notice.jpg'
                    elif seen != 'drawn':
                        result, how = 1, f'BLACK: the notice came, {closed}, then the game stayed {seen} for {a.seconds} s (draws in {control} s without it)'
                    else:
                        result, how = 3, (f'INCONCLUSIVE: the notice came, {closed}, then the game drew another screen than without it '
                                          f'(difference {diff}, same is ≤ {SAME_DIFF}): look at first-launch-control.jpg and first-launch-notice.jpg')
    finally:
        if before in ('', 'null'):
            run('shell', 'settings', 'delete', 'secure', 'immersive_mode_confirmations')
        else:
            run('shell', 'settings', 'put', 'secure', 'immersive_mode_confirmations', before)
        run('shell', 'am', 'force-stop', a.package)
    say(f'first launch · {a.package} · {build} · {how}')
    return result


SHEET_COLS, SHEET_ROWS, TILE_W = 8, 5, 180   # 40 frames a contact sheet, each tile 180 px wide


def pack_frames(frames, actions, keep=False):
    """A player's frames, once its answer is written: contact sheets beside them (<frames>-1.jpg …, 40 a sheet, each tile with
    its number and m:ss from the action log), then the raw frames deleted unless keep. 2026-10-24 (the session manager's 11:24 note): the
    gate's and the judge room's raw session frames were never deleted and filled the disk. Without Pillow nothing is deleted.
    Returns the line to print."""
    shots = sorted((p for p in frames.iterdir() if p.stem.isdigit() and p.suffix.lower() in ('.jpg', '.png')),
                   key=lambda p: int(p.stem)) if frames.is_dir() else []
    if not shots:
        if not keep:   # the server makes the folder at its start: a player who saw no screenshot left it empty (2026-10-24)
            try:
                frames.rmdir()
            except OSError:
                pass
        return 'frames: none'
    Image = load_pil()
    if not Image:
        return f'frames: {len(shots)} kept in {frames} (no Pillow for the contact sheets)'
    from PIL import ImageDraw, ImageFont
    try:
        font = ImageFont.truetype('arial.ttf', 18)
    except OSError:
        font = ImageFont.load_default()
    when = {}
    if actions.is_file():
        for m in re.finditer(r'^- (\d+:\d\d) screenshot (\d{3,})$', actions.read_text(encoding='utf-8', errors='replace'), re.M):
            when[m.group(2)] = m.group(1)
    per = SHEET_COLS * SHEET_ROWS
    sheets = []
    try:
        for k in range(0, len(shots), per):
            tiles = []
            for p in shots[k:k + per]:
                with Image.open(p) as im:
                    im = im.convert('RGB')
                    tiles.append((p.stem, im.resize((TILE_W, max(1, round(TILE_W * im.height / im.width))), Image.LANCZOS)))
            th = max(t.height for _, t in tiles) + 26
            cols = min(SHEET_COLS, len(tiles))
            sheet = Image.new('RGB', (cols * (TILE_W + 6) + 6, -(-len(tiles) // SHEET_COLS) * (th + 6) + 6), (24, 24, 28))
            draw = ImageDraw.Draw(sheet)
            for i, (stem, t) in enumerate(tiles):
                x, y = 6 + (i % SHEET_COLS) * (TILE_W + 6), 6 + (i // SHEET_COLS) * (th + 6)
                sheet.paste(t, (x, y))
                draw.text((x + 2, y + t.height + 3), f'{stem}' + (f' · {when[stem]}' if stem in when else ''), font=font, fill=(230, 230, 230))
            path = frames.with_name(f'{frames.name}-{len(sheets) + 1}.jpg')
            buf = io.BytesIO()
            sheet.save(buf, 'JPEG', quality=80)
            write_out(path, buf.getvalue())
            sheets.append(path)
    except OSError as e:
        return f'frames: {len(shots)} kept in {frames} (a contact sheet failed: {e})'
    if keep:
        return f'frames: {len(sheets)} contact sheet(s) ({sheets[0].name} …); {len(shots)} raw frames kept (--keep-frames)'
    shutil.rmtree(frames, ignore_errors=True)
    left = len(list(frames.glob('*'))) if frames.exists() else 0
    return (f'frames: {len(sheets)} contact sheet(s) ({sheets[0].name} …); {len(shots) - left} raw frames deleted'
            + (f', {left} could not be' if left else '') + ' (--keep-frames keeps them)')


def build_play_prompt(lang, minutes, form_text, folders):
    evidence = PLAY_EVIDENCE[lang].format(count=len(folders), folders=', '.join(folders)) if folders else ''
    return PLAY_PREAMBLE[lang].format(minutes=minutes, evidence=evidence) + f'\n{QUESTIONS_TITLE[lang]}\n\n{form_text.strip()}\n'


def play(a):
    out = out_folder(a.out)
    form, form_text = read_form(a.form)
    if not re.fullmatch(PACKAGE_RE, a.package):
        raise SystemExit('ERROR: --package is an Android package name (com.example.game)')
    adb = find_adb(a.adb)
    if not adb:
        raise SystemExit('ERROR: adb not found (--adb, or the Android SDK\'s platform-tools)')
    serial = a.serial or only_device(adb)
    up = booted(adb, serial)
    settled = time.time() + (max(0.0, SETTLE_S - up) if up is not None else 0.0)
    code, installed = adb_text(adb, 'shell', 'pm', 'path', a.package, serial=serial)
    if code != 0 or 'package:' not in installed:
        raise SystemExit(f'ERROR: {a.package} is not installed on {serial}')
    # 2026-10-24 (a game session, the session manager's 16:04 answer): a gate's fresh player played the morning's APK, the new install had
    # failed silently. The build on the device is printed and logged; with --apk it must be that file, byte for byte.
    version, version_code, updated = game_build(adb, serial, a.package)
    build = f'versionName {version}, versionCode {version_code}, installed {updated}'
    say(f'game build on the device: {build}')
    build += apk_check(a, adb, serial, installed)
    claude = None if a.dry_run else find_claude()
    room, old = open_room(a)
    try:
        a.forbid = (a.forbid or []) + sorted(package_words(a.package))
        files, left_out, game_names = fill_room(a, room, old, need_files=False)
        folders = sorted({p.relative_to(room).parts[0] for p in files if len(p.relative_to(room).parts) > 1})
        lang = form_lang(form_text) if a.lang == 'auto' else a.lang
        prompt = build_play_prompt(lang, a.minutes, form_text, folders if files else [])
        n = a.first or next_number(out, a.prefix)
        name, frames, actions = f'{a.prefix}-{n}.md', out / f'{a.prefix}-{n}-frames', out / f'{a.prefix}-{n}-actions.md'
        mcp = Path(str(room) + '.mcp.json')
        server = [str(Path(__file__).resolve()), 'adb-server', '--adb', adb, '--serial', serial, '--package', a.package,
                  '--minutes', str(a.minutes), '--frames', str(frames), '--log', str(actions)]
        mcp.write_text(json.dumps({'mcpServers': {'phone': {'type': 'stdio', 'command': sys.executable, 'args': ['-X', 'utf8'] + server}}}),
                       encoding='utf-8')
        tools = 'Read,Glob,Grep' if files else ''
        command = {'agent': None, 'tools': tools, 'allow': ('mcp__phone',) + (ROOM_READ if files else ()), 'mcp': mcp}
        if a.dry_run:
            say(f'DRY RUN: nothing ran. Player: {name} on {serial} · model {a.model} · {a.minutes} min of play · command (in the room, prompt on stdin):')
            say('  ' + ' '.join(build_command('claude', a.model, **command)))
            if settled > time.time():
                say(f'the device booted {up:.0f} s ago: a run would first wait {settled - time.time():.0f} s for it to settle')
            say('--- prompt ---\n' + prompt + '--- end of prompt ---')
            return 0
        if not a.no_probe:
            probe(claude, room, game_names, a.allow or [], agent=None, tools=tools, allow=ROOM_READ if files else ())
        if settled > time.time():   # a device that has just booted is busy: monkey timed out 20 s after a boot (2026-10-24)
            say(f'the device booted {up:.0f} s ago: waiting {settled - time.time():.0f} s for it to settle')
            time.sleep(max(0.0, settled - time.time()))
        if a.clear_data:
            c, o = adb_text(adb, 'shell', 'pm', 'clear', a.package, serial=serial)
            say(f'game data cleared: {o.strip()[:60]}' if c == 0 else f'WARNING: pm clear failed: {o.strip()[:200]}')
        if a.package != STORE_PACKAGE:   # nothing behind the game leads into the store (back left a game for it, 2026-10-24)
            c, o = adb_text(adb, 'shell', 'am', 'force-stop', STORE_PACKAGE, serial=serial)
            say('Play Store stopped' if c == 0 else f'WARNING: could not stop the Play Store: {o.strip()[:200]}')
        c, o = adb_text(adb, *CONFIRM_NOTICE, serial=serial)   # the full-screen notice never comes over the game (as after "Got it")
        say('Android\'s full-screen notice confirmed on the device' if c == 0
            else f'WARNING: could not confirm Android\'s full-screen notice (the player\'s server clears it if it comes): {o.strip()[:200]}')
        save(out, actions.name, f'# {name[:-3]}: actions (m:ss since open_game; tap and swipe in screenshot pixels, then device pixels)\n')
        say(f'player running: {name} (model {a.model}, {a.minutes} min of play + at most {a.answer_minutes} min for the answers)')
        s = run_one(claude, room, prompt, a.model, (a.minutes + a.answer_minutes) * 60 + 60, a.effort, cache_ttl=a.cache_ttl, **command)
        calls = {k.split('__')[-1]: v for k, v in s['calls'].items() if k.startswith('mcp__phone__')}
        every = {p.relative_to(room).as_posix().casefold() for p in files}
        opened = s['opened'] & every
        if s['failed']:
            why = 'timed out' if s['timed_out'] else f'code {s["code"]}'
            say(f'FAILED {name}: {why}; {s["stderr"][-300:]}')
            if s['result']:
                save(out, name[:-3] + '.partial.md', s['result'])
        else:
            save(out, name, s['result'])
            say(f'DONE {name}: {s["seconds"]} s; ' + ', '.join(f'{k} {v}' for k, v in sorted(calls.items()))
                + (f'; evidence opened {len(opened)}/{len(every)}' if every else '') + (f'; denied access {len(s["denied"])}' if s['denied'] else ''))
        say(f'actions: {actions} · frames: {frames}')
        if not s['failed']:   # the answer is written: the frames go into contact sheets, the raw ones are deleted
            say(pack_frames(frames, actions, a.keep_frames))
        if a.raw:
            save(out, name[:-3] + '.stream.jsonl', s['raw'])
        usd = '-' if s['cost'] is None else f'{s["cost"]:.4f}'
        row = (f'| {name if not s["failed"] else name + " (FAILED)"} | {s["model"] or a.model} | {s["seconds"]} s | '
               + (', '.join(f'{k} {v}' for k, v in sorted(calls.items())) or '-') + f' | {f"{len(opened)}/{len(every)}" if every else "-"} | '
               f'{denied_list(s) or "-"} | {usd} |')
        log = write_log(out, f'play · room {room.name} · device {serial} · build {build} · {a.minutes} min · prompt {short_hash(prompt.encode("utf-8"))}'
                        f' · form {form.name} · effort {effort_name(a.effort)} · cache {a.cache_ttl}',
                        left_out, '| Player | Model | Time | Tools used | Evidence opened | Denied | USD |\n|---|---|---|---|---|---|---|', [row], prompt)
        say(f'log: {log}')
        return 1 if s['failed'] else 0
    except Stop as e:
        return e.args[0]
    finally:
        if a.keep:
            say(f'room kept: {room} (when done: hakem-odasi.py clean)')
        else:
            remove_room(room)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(prog='hakem-odasi.py', description='Blind reviewers in an unnamed room (see the top of the file).')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run', help='copy the evidence into a room, check it, run the reviewers')
    r.add_argument('--evidence', help='evidence folder (its content goes to the room\'s root, e.g. kor/)')
    r.add_argument('--add', action='append', metavar='NAME=PATH', help='add one file or folder as NAME (e.g. A=cut1-frames)')
    r.add_argument('--form', required=True, help='the reviewer\'s form or question (markdown), appended to the prompt as is')
    r.add_argument('--out', required=True, help='where hakem-<n>.md and the log go (outside the room)')
    r.add_argument('--judges', type=int, default=2, help='number of reviewers (2)')
    r.add_argument('--model', default='opus', help='reviewer model (opus: the same as the Explore reviewers in agent sessions)')
    r.add_argument('--effort', choices=('low', 'medium', 'high', 'xhigh', 'max'), default='xhigh',
                   help='reviewer effort (xhigh; max only for the last decision round before a store)')
    r.add_argument('--parallel', type=int, default=2, help='reviewers at a time (2; ~240 MB each)')
    r.add_argument('--timeout', type=int, default=30, help='minutes a reviewer may take (30)')
    r.add_argument('--first', type=int, help='first reviewer number (default: one past the highest in --out)')
    r.add_argument('--prefix', default='hakem', help='output name prefix (hakem → hakem-<n>.md)')
    r.add_argument('--lang', choices=('auto', 'tr', 'en'), default='auto', help='preamble language (auto: Turkish letters in the form → tr)')
    r.add_argument('--cache-ttl', choices=('5m', '1h'), default='5m', help='prompt cache lifetime of the sessions (5m: cheaper writes)')
    r.add_argument('--forbid', action='append', metavar='NAME', help='a name that must not appear in the evidence (store name, rivals\' names)')
    r.add_argument('--allow', action='append', metavar='WORD', help='drop from the forbidden names (a false alarm)')
    r.add_argument('--no-probe', action='store_true', help='skip the probe reviewer')
    r.add_argument('--dry-run', action='store_true', help='build and check the room, show the prompt; run no reviewer')
    r.add_argument('--keep', action='store_true', help='don\'t delete the room (for inspection)')
    r.add_argument('--raw', action='store_true', help='also write each reviewer\'s raw stream (<name>.stream.jsonl)')
    r.add_argument('--room-root', help=argparse.SUPPRESS)   # tests only
    c = sub.add_parser('check', help='leak check only')
    c.add_argument('folder')
    c.add_argument('--forbid', action='append', metavar='NAME')
    c.add_argument('--allow', action='append', metavar='WORD')
    k = sub.add_parser('clean', help='delete rooms whose owner process is gone')
    k.add_argument('--room-root', help=argparse.SUPPRESS)
    p = sub.add_parser('play', help='a fresh player plays the game on an Android device, with tools only for playing')
    p.add_argument('--package', required=True, help='the game\'s Android package (never shown to the player)')
    p.add_argument('--form', required=True, help='the questions the player answers after playing (markdown)')
    p.add_argument('--out', required=True, help='where oyuncu-<n>.md, its actions, frames and the log go (outside the room)')
    p.add_argument('--serial', help='adb device (default: the only one attached)')
    p.add_argument('--adb', help='adb to use (default: the Android SDK\'s platform-tools, else PATH)')
    p.add_argument('--minutes', type=int, default=10, help='minutes of play (10)')
    p.add_argument('--answer-minutes', type=int, default=10, help='minutes for the answers after play (10)')
    p.add_argument('--evidence', help='captures for the question about other games (into the room; opened with Read after play)')
    p.add_argument('--add', action='append', metavar='NAME=PATH', help='add one file or folder as NAME')
    p.add_argument('--clear-data', action='store_true', help='clear the game\'s data first (pm clear): a first launch')
    p.add_argument('--apk', help='the APK that must be the installed build (sha256 of the device\'s base.apk); else nobody plays')
    p.add_argument('--model', default='opus', help='player model (opus)')
    p.add_argument('--effort', choices=('low', 'medium', 'high', 'xhigh', 'max'), default='xhigh', help='player effort (xhigh)')
    p.add_argument('--first', type=int, help='player number (default: one past the highest in --out)')
    p.add_argument('--prefix', default='oyuncu', help='output name prefix (oyuncu → oyuncu-<n>.md)')
    p.add_argument('--lang', choices=('auto', 'tr', 'en'), default='auto', help='preamble language (auto: Turkish letters in the form → tr)')
    p.add_argument('--cache-ttl', choices=('5m', '1h'), default='5m', help='prompt cache lifetime of the sessions (5m: cheaper writes)')
    p.add_argument('--forbid', action='append', metavar='NAME', help='a name that must not appear in the evidence or the context')
    p.add_argument('--allow', action='append', metavar='WORD', help='drop from the forbidden names (a false alarm)')
    p.add_argument('--no-probe', action='store_true', help='skip the probe')
    p.add_argument('--dry-run', action='store_true', help='check the device and the room, show the prompt; nobody plays')
    p.add_argument('--keep', action='store_true', help='don\'t delete the room (for inspection)')
    p.add_argument('--keep-frames', action='store_true', help='keep the raw frames after the answer (contact sheets are made anyway)')
    p.add_argument('--raw', action='store_true', help='also write the player\'s raw stream (<name>.stream.jsonl)')
    p.add_argument('--room-root', help=argparse.SUPPRESS)
    f = sub.add_parser('first-launch', help='model-free: after Android\'s full-screen notice the game must draw again (U28)')
    f.add_argument('--package', required=True, help='the game\'s Android package')
    f.add_argument('--serial', help='adb device (default: the only one attached)')
    f.add_argument('--adb', help='adb to use (default: the Android SDK\'s platform-tools, else PATH)')
    f.add_argument('--seconds', type=int, default=15, help='seconds the game has to draw again after the notice (15)')
    f.add_argument('--out', help='folder for the last frame of each run (first-launch-control.jpg, first-launch-notice.jpg)')
    f.add_argument('--apk', help='the APK that must be the installed build (sha256 of the device\'s base.apk); else nothing runs')
    f.add_argument('--notice-wait', type=float, default=20, help=argparse.SUPPRESS)   # tests only
    f.add_argument('--settle', type=float, default=4, help=argparse.SUPPRESS)   # tests only: seconds before the control's settled frame
    s = sub.add_parser('adb-server', help='internal: the player\'s MCP server (play starts it)')
    s.add_argument('--adb', required=True)
    s.add_argument('--serial')
    s.add_argument('--package', required=True)
    s.add_argument('--minutes', type=int, default=10)
    s.add_argument('--frames', required=True)
    s.add_argument('--log', required=True)
    s.add_argument('--limit-seconds', type=int, help=argparse.SUPPRESS)   # tests only
    s.add_argument('--launch-seconds', type=float, help=argparse.SUPPRESS)   # tests only
    a = ap.parse_args(argv)
    if a.cmd == 'adb-server':
        return Phone(a).serve()
    if a.cmd == 'first-launch':
        return first_launch(a)
    if a.cmd in ('run', 'play'):
        if a.cmd == 'run' and a.judges < 1:
            ap.error('--judges must be at least 1')
        if a.cmd == 'run' and not a.evidence and not a.add:
            ap.error('--evidence or --add is required')
        if a.cmd == 'play' and (a.minutes < 1 or a.answer_minutes < 1):
            ap.error('--minutes and --answer-minutes must be at least 1')
        try:
            return run(a) if a.cmd == 'run' else play(a)
        except SystemExit as e:
            if e.code == 4:
                say('ERROR: claude not found (PATH)')
                return 4
            raise
    if a.cmd == 'check':
        return check(a)
    n = clean_old_rooms(Path(a.room_root or tempfile.gettempdir()), verbose=True)
    say(f'{n} old room(s) removed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
