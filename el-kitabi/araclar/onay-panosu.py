#!/usr/bin/env python3
"""Approval board: the options of one decision side by side, each in its own frame, the way the owner asked (2026-10-23 18:0x).

The rule (handbook, visual work; the studio's NASIL-kalite › "Onay panosu net olsun"): each option in its own framed area with
space between; a large, clear "A: <short name>" on top (the same letter and name as the card's button) with one line of what
differs under it, and a "recommended" badge on the recommended one; the current state, before and after, and the internal
reference carry their own headers ("CURRENT: …") and stand apart from the options; no text over an image (the game's counter
or button stays visible); at most 4 options, all in the same frame and at the same scale.

What it does:
- Every image of the board is drawn at one height (never more than 2x its own size), so two screens compare 1:1; options
  share one frame size; a recommended option gets a green frame and badge; options made with AI get the internal reference
  tag line ("reference": true).
- Picks the layout: all options in one row (context frames on the left, a separator, then the options) unless that would
  shrink the images below 70 % of what a grid allows; then a grid with the context frames on top. --columns forces it.
- Wraps text inside its frame; a title or difference that needs more than two lines stops the tool (shorten it) instead of
  being cut (the 24 Oct gate board cut its reference tag at the frame's edge).
- Checks every board after layout: text inside its frame and clear of every image, option frames equal, images at one
  height, nothing overlapping or off the canvas.

Input: a JSON spec (preferred; paths relative to the spec's folder) or flags.
  {"title": "...", "subtitle": "...", "lang": "tr", "captions": ["Lanes", "Win"], "reference": true, "recommend": "A",
   "context": [{"kind": "current", "name": "Today", "note": "dark lanes, thin beam", "images": ["now-play.png", "now-win.png"]}],
   "options": [{"letter": "A", "name": "Sandstone lanes", "diff": "carved edge, gold dust burst", "images": ["a1.png", "a2.png"]}]}
  kind: current | before | after | reference. lang: tr (default) | en, for the fixed labels. Optional per frame "reference"
  and per option "recommended": true. "font" and "font_bold": TTF paths (e.g. the game's own font).
Usage: python onay-panosu.py --spec board.json --out board.png [--columns N] [--image-height PX] [--max-width 4000]
       python onay-panosu.py --out board.png --title "..." [--subtitle "..."] [--lang tr|en] [--captions C1 C2 ...]
           [--reference] [--recommend A] --option A "Short name" "What differs" img1.png [img2.png ...] [--option B ...]
           [--context current "Today" "One line" now1.png ...]
       python onay-panosu.py --dene        # self-test in memory
Output by extension: .png, .jpg, .webp. Needs Pillow (found in the user's site-packages even under python -I).
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path


def load_pil():
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError:
        import site
        user = site.getusersitepackages()
        if user and user not in sys.path:
            sys.path.append(user)
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageOps
        except ImportError:
            raise SystemExit("ERROR: Pillow is needed: python -m pip install --user Pillow")
    return Image, ImageDraw, ImageFont, ImageOps


Image, ImageDraw, ImageFont, ImageOps = load_pil()

LABELS = {
    "tr": {"current": "ŞİMDİKİ", "before": "ÖNCE", "after": "SONRA", "reference": "İÇ REFERANS", "recommended": "önerim",
           "options": "SEÇENEKLER", "tag": "İÇ REFERANS · yapay zekâ · yayımlanmaz"},
    "en": {"current": "CURRENT", "before": "BEFORE", "after": "AFTER", "reference": "INTERNAL REFERENCE", "recommended": "recommended",
           "options": "OPTIONS", "tag": "INTERNAL REFERENCE · AI · not for publishing"},
}
SIZES = {"title": 64, "subtitle": 32, "head": 52, "diff": 30, "tag": 24, "badge": 26, "caption": 26, "group": 26}
MARGIN, GAP, PAD, IMG_GAP, HEAD_GAP, SEP, RADIUS = 56, 40, 28, 20, 22, 30, 18
MIN_INNER = 420                     # the narrowest frame's inside: a short title and a line of difference fit
H_DEFAULT, H_MIN = 960, 300         # image height on the board
ROW_KEEP = 0.7                      # one row of options unless that shrinks the images below 70 % of a grid's
COLOURS = {"bg": (245, 240, 230), "frame": (255, 255, 255), "option": (205, 191, 166), "context": (140, 140, 140),
           "recommended": (76, 175, 106), "badge_text": (255, 255, 255), "title": (43, 38, 34), "body": (74, 68, 61),
           "tag": (138, 111, 85), "caption": (90, 84, 76), "group": (110, 100, 90), "sep": (200, 190, 175), "outline": (225, 220, 210)}
FONTS = {
    "bold": ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
             "/Library/Fonts/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"],
    "regular": ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf"],
}
MAX_OPTIONS = 4


class BoardError(Exception):
    pass


def warn(msg):
    print(f"WARNING: {msg}", flush=True)


class Fonts:
    def __init__(self, regular=None, bold=None):
        self.paths = {"regular": self.pick(regular, FONTS["regular"]), "bold": self.pick(bold, FONTS["bold"])}
        self.cache = {}

    @staticmethod
    def pick(given, candidates):
        for p in ([given] if given else []) + candidates:
            if p and Path(p).is_file():
                return p
        if given:
            raise BoardError(f"font not found: {given}")
        return None

    def get(self, role, scale=1.0):
        bold = role in ("title", "head", "badge", "group")
        size = max(10, round(SIZES[role] * scale))
        key = (bold, size)
        if key not in self.cache:
            path = self.paths["bold" if bold else "regular"]
            self.cache[key] = ImageFont.truetype(path, size) if path else ImageFont.load_default(size=size)
        return self.cache[key]


def line_height(font):
    ascent, descent = font.getmetrics()
    return ascent + descent


def text_width(font, text):
    return font.getlength(text)


def wrap(font, text, width):
    """Greedy word wrap; a word wider than the width stays on its own line (the caller widens the frame first)."""
    words, lines, line = text.split(), [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if line and text_width(font, test) > width:
            lines.append(line)
            line = w
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def fit(fonts, role, text, width, max_lines, what):
    """Lines of text inside the width: the full size, then 90 % and 80 %; more than max_lines stops the tool."""
    if not text:
        return [], fonts.get(role)
    for scale in (1.0, 0.9, 0.8):
        font = fonts.get(role, scale)
        lines = wrap(font, text, width)
        if len(lines) <= max_lines and all(text_width(font, ln) <= width for ln in lines):
            return lines, font
    raise BoardError(f"{what} needs more than {max_lines} line(s) in a {int(width)} px frame: shorten it: \"{text}\"")


# --- Spec ---

def load_spec(a):
    if a.spec:
        p = Path(a.spec)
        spec = json.loads(p.read_text(encoding="utf-8"))
        base = p.parent
    else:
        spec = {"title": a.title, "subtitle": a.subtitle, "lang": a.lang, "captions": a.captions, "reference": a.reference,
                "recommend": a.recommend, "options": [], "context": []}
        for o in a.option or []:
            if len(o) < 4:
                raise BoardError("--option LETTER NAME DIFF IMAGE [IMAGE ...]")
            spec["options"].append({"letter": o[0], "name": o[1], "diff": o[2], "images": o[3:]})
        for c in a.context or []:
            if len(c) < 4:
                raise BoardError("--context KIND NAME NOTE IMAGE [IMAGE ...]")
            spec["context"].append({"kind": c[0], "name": c[1], "note": c[2], "images": c[3:]})
        base = Path.cwd()
    spec.setdefault("lang", "tr")
    if spec["lang"] not in LABELS:
        raise BoardError(f"lang is tr or en, not {spec['lang']}")
    options, context = spec.get("options") or [], spec.get("context") or []
    if len(options) > MAX_OPTIONS:
        raise BoardError(f"at most {MAX_OPTIONS} options on a board (the owner's rule); this has {len(options)}")
    if not options and not context:
        raise BoardError("nothing to show: give options or context frames")
    letters = []
    for i, o in enumerate(options):
        o.setdefault("letter", "ABCD"[i])
        if not (isinstance(o["letter"], str) and len(o["letter"]) == 1 and o["letter"].isalpha() and o["letter"].isupper()):
            raise BoardError(f"an option letter is one capital letter, not {o['letter']!r}")
        letters.append(o["letter"])
    if len(set(letters)) != len(letters):
        raise BoardError(f"option letters repeat: {letters}")
    rec = spec.get("recommend")
    if rec and rec not in letters:
        raise BoardError(f"recommend {rec} is not one of the options ({', '.join(letters)})")
    for o in options:
        o["recommended"] = bool(o.get("recommended")) or o["letter"] == rec
        o.setdefault("reference", bool(spec.get("reference")))
    for c in context:
        if c.get("kind") not in ("current", "before", "after", "reference"):
            raise BoardError(f"a context kind is current, before, after or reference, not {c.get('kind')!r}")
    for f in options + context:
        if not str(f.get("name") or "").strip():
            raise BoardError("every option and context frame needs a short name")
        if not f.get("images"):
            raise BoardError(f"{f.get('name')}: no images")
        f["paths"] = [Path(x) if Path(x).is_absolute() else base / x for x in f["images"]]
        for p in f["paths"]:
            if not p.is_file():
                raise BoardError(f"image not found: {p}")
    counts = {len(o["paths"]) for o in options}
    if len(counts) > 1:
        warn("the options have different numbers of images; frames stay the same size")
    return spec


# --- Layout ---

def open_image(path):
    im = ImageOps.exif_transpose(Image.open(path))
    return im.convert("RGBA")


def frame_texts(fonts, spec, f, inner, labels, is_option):
    """(header lines with fonts, badge?) for one frame at an inner width."""
    head = f"{f['letter']}: {f['name']}" if is_option else f"{labels[f['kind']]}: {f['name']}"
    head_lines, head_font = fit(fonts, "head", head, inner, 2, "a title")
    body = f.get("diff") if is_option else f.get("note")
    body_lines, body_font = fit(fonts, "diff", (body or "").strip(), inner, 2, "a difference line")
    tag_lines, tag_font = fit(fonts, "tag", labels["tag"], inner, 2, "the reference tag") if f.get("reference") else ([], fonts.get("tag"))
    badge = labels["recommended"] if is_option and f.get("recommended") else None
    return {"head": (head_lines, head_font), "body": (body_lines, body_font), "tag": (tag_lines, tag_font), "badge": badge}


def header_height(fonts, t, inner):
    lines, font = t["head"]
    h = len(lines) * round(line_height(font) * 1.1)
    if t["badge"]:
        bf = fonts.get("badge")
        bw = text_width(bf, t["badge"]) + 32
        if text_width(font, lines[-1]) + 16 + bw > inner:   # the badge on its own line
            h += line_height(bf) + 16
    for key, gap in (("body", 10), ("tag", 8)):
        ls, fo = t[key]
        if ls:
            h += gap + len(ls) * round(line_height(fo) * 1.15)
    return h


def caption_height(fonts, captions, widths):
    if not captions:
        return 0
    lines = 1
    for c, w in zip(captions, widths):
        ls, _ = fit(fonts, "caption", c, w, 2, "a caption")
        lines = max(lines, len(ls))
    return 12 + lines * round(line_height(fonts.get("caption")) * 1.15)


def measure(spec, fonts, images, H, cols):
    """Sizes of every frame and the board at image height H and option columns cols."""
    labels = LABELS[spec["lang"]]
    caps = spec.get("captions") or []
    options, context = spec.get("options") or [], spec.get("context") or []

    def row_width(f):
        return sum(round(im.width * H / im.height) for im in images[id(f)]) + IMG_GAP * (len(images[id(f)]) - 1)

    def longest_word(f, is_option):
        head = f"{f['letter']}: {f['name']}" if is_option else f"{labels[f['kind']]}: {f['name']}"
        words = head.split() + str(f.get("diff") or f.get("note") or "").split()
        return max([text_width(fonts.get("head"), w) for w in head.split()] + [text_width(fonts.get("diff"), w) for w in words] + [0])

    inner_opt = max([MIN_INNER] + [row_width(o) for o in options] + [longest_word(o, True) for o in options]) if options else 0
    frames = []
    for f in context:
        inner = max(MIN_INNER, row_width(f), longest_word(f, False))
        frames.append({"f": f, "option": False, "inner": inner, "t": frame_texts(fonts, spec, f, inner, labels, False)})
    for o in options:
        frames.append({"f": o, "option": True, "inner": inner_opt, "t": frame_texts(fonts, spec, o, inner_opt, labels, True)})
    head_h = max(header_height(fonts, fr["t"], fr["inner"]) for fr in frames)
    cap_h = 0
    for fr in frames:
        widths = [round(im.width * H / im.height) for im in images[id(fr["f"])]]
        cap_h = max(cap_h, caption_height(fonts, caps[:len(widths)], widths))
    frame_h = PAD + head_h + HEAD_GAP + H + cap_h + PAD
    for fr in frames:
        fr["w"], fr["h"] = fr["inner"] + 2 * PAD, frame_h
    ctx = [fr for fr in frames if not fr["option"]]
    opt = [fr for fr in frames if fr["option"]]
    cols = max(1, min(cols, len(opt))) if opt else 1
    one_row = not opt or cols >= len(opt)
    ctx_w = sum(fr["w"] for fr in ctx) + GAP * max(0, len(ctx) - 1)
    opt_w = (opt[0]["w"] * cols + GAP * (cols - 1)) if opt else 0
    rows = -(-len(opt) // cols) if opt else 0
    group_h = round(line_height(fonts.get("group")) * 1.2) + 10 if ctx and opt else 0
    if one_row:
        width = ctx_w + (2 * SEP + 2 if ctx and opt else 0) + opt_w
        body_h = group_h + frame_h
    else:
        width = max(ctx_w, opt_w)
        body_h = (frame_h + 2 * SEP + 2 if ctx else 0) + group_h + rows * frame_h + GAP * (rows - 1)
    board_w = round(width) + 2 * MARGIN
    title_lines, title_font = (wrap(fonts.get("title"), spec["title"], board_w - 2 * MARGIN) if spec.get("title") else []), fonts.get("title")
    sub_lines, sub_font = (wrap(fonts.get("subtitle"), spec["subtitle"], board_w - 2 * MARGIN) if spec.get("subtitle") else []), fonts.get("subtitle")
    title_h = (len(title_lines) * round(line_height(title_font) * 1.1) + (8 + len(sub_lines) * round(line_height(sub_font) * 1.2) if sub_lines else 0)
               + 36) if (title_lines or sub_lines) else 0
    board_h = MARGIN + title_h + body_h + MARGIN
    return {"frames": frames, "ctx": ctx, "opt": opt, "cols": cols, "one_row": one_row, "w": board_w, "h": round(board_h), "H": H,
            "head_h": head_h, "cap_h": cap_h, "title": (title_lines, title_font, sub_lines, sub_font, title_h), "group_h": group_h}


def choose(spec, fonts, images, max_w, max_h, force_cols=None, force_h=None):
    """The largest image height for each column count that fits; one row unless it costs more than 30 % of the image size."""
    all_imgs = [im for f in (spec.get("options") or []) + (spec.get("context") or []) for im in images[id(f)]]
    h_max = force_h or min(H_DEFAULT, max(min(im.height for im in all_imgs), 480))
    n_opt = len(spec.get("options") or [])
    candidates = [force_cols] if force_cols else list(range(max(1, n_opt), 0, -1))
    best = {}
    for cols in candidates:
        if force_h:
            best[cols] = measure(spec, fonts, images, force_h, cols)
            continue
        lo, hi, found = H_MIN, h_max, None
        while lo <= hi:
            mid = (lo + hi) // 2
            m = measure(spec, fonts, images, mid, cols)
            if m["w"] <= max_w and m["h"] <= max_h:
                found, lo = m, mid + 1
            else:
                hi = mid - 1
        if found:
            best[cols] = found
    if not best:
        m = measure(spec, fonts, images, H_MIN, 1)
        raise BoardError(f"the board doesn't fit {max_w}x{max_h} even at {H_MIN} px images ({m['w']}x{m['h']}): fewer images or a larger --max-width")
    top = max(m["H"] for m in best.values())
    for cols in sorted(best, reverse=True):
        if best[cols]["H"] >= ROW_KEEP * top:
            return best[cols]
    return best[max(best)]


# --- Drawing ---

def draw_board(spec, fonts, images, m):
    canvas = Image.new("RGB", (m["w"], m["h"]), COLOURS["bg"])
    d = ImageDraw.Draw(canvas)
    boxes = {"text": [], "image": [], "frame": []}

    def text(x, y, s, font, colour, frame=None):
        d.text((x, y), s, font=font, fill=colour, anchor="la")
        x0, y0, x1, y1 = d.textbbox((x, y), s, font=font, anchor="la")
        boxes["text"].append({"box": (x0, y0, x1, y1), "frame": frame, "s": s})

    y = MARGIN
    title_lines, title_font, sub_lines, sub_font, title_h = m["title"]
    for ln in title_lines:
        text(MARGIN, y, ln, title_font, COLOURS["title"])
        y += round(line_height(title_font) * 1.1)
    if sub_lines:
        y += 8
        for ln in sub_lines:
            text(MARGIN, y, ln, sub_font, COLOURS["body"])
            y += round(line_height(sub_font) * 1.2)
    y = MARGIN + title_h
    labels = LABELS[spec["lang"]]
    gf = fonts.get("group")

    def place(fr, x, fy):
        fr["x"], fr["y"] = round(x), round(fy)

    ctx, opt = m["ctx"], m["opt"]
    if m["one_row"]:
        x = MARGIN
        fy = y + m["group_h"]
        for fr in ctx:
            place(fr, x, fy)
            x += fr["w"] + GAP
        if ctx and opt:
            x += SEP - GAP
            d.line((x, fy, x, fy + m["frames"][0]["h"]), fill=COLOURS["sep"], width=2)
            x += 2 + SEP
            text(x, y, labels["options"], gf, COLOURS["group"])
        for fr in opt:
            place(fr, x, fy)
            x += fr["w"] + GAP
    else:
        x = MARGIN
        for fr in ctx:
            place(fr, x, y)
            x += fr["w"] + GAP
        if ctx:
            y += m["frames"][0]["h"] + SEP
            d.line((MARGIN, y, m["w"] - MARGIN, y), fill=COLOURS["sep"], width=2)
            y += 2 + SEP
        if ctx and opt:
            text(MARGIN, y, labels["options"], gf, COLOURS["group"])
        y += m["group_h"]
        cols = m["cols"]
        for i, fr in enumerate(opt):
            r, c = divmod(i, cols)
            in_row = min(cols, len(opt) - r * cols)
            row_w = in_row * fr["w"] + (in_row - 1) * GAP
            x0 = MARGIN + (m["w"] - 2 * MARGIN - row_w) / 2   # an incomplete last row is centred
            place(fr, x0 + c * (fr["w"] + GAP), y + r * (fr["h"] + GAP))

    caps = spec.get("captions") or []
    for i, fr in enumerate(m["frames"]):
        f, t = fr["f"], fr["t"]
        rec = fr["option"] and f.get("recommended")
        border = COLOURS["recommended"] if rec else (COLOURS["option"] if fr["option"] else COLOURS["context"])
        x0, y0, x1, y1 = fr["x"], fr["y"], fr["x"] + fr["w"], fr["y"] + fr["h"]
        d.rounded_rectangle((x0, y0, x1, y1), RADIUS, fill=COLOURS["frame"], outline=border, width=6 if rec else 3)
        boxes["frame"].append({"box": (x0, y0, x1, y1), "option": fr["option"], "i": i})
        tx, ty, inner = x0 + PAD, y0 + PAD, fr["inner"]
        lines, font = t["head"]
        for k, ln in enumerate(lines):
            text(tx, ty, ln, font, COLOURS["title"], i)
            last_y = ty
            ty += round(line_height(font) * 1.1)
        if t["badge"]:
            bf = fonts.get("badge")
            bw, bh = text_width(bf, t["badge"]) + 32, line_height(bf) + 12
            bx = tx + text_width(font, lines[-1]) + 16
            by = last_y + (line_height(font) - bh) / 2
            if bx + bw > tx + inner:
                bx, by = tx, ty + 4
                ty += line_height(bf) + 16
            d.rounded_rectangle((bx, by, bx + bw, by + bh), bh / 2, fill=COLOURS["recommended"])
            text(bx + 16, by + 6, t["badge"], bf, COLOURS["badge_text"], i)
        for key, gap, colour in (("body", 10, COLOURS["body"]), ("tag", 8, COLOURS["tag"])):
            ls, fo = t[key]
            if ls:
                ty += gap
                for ln in ls:
                    text(tx, ty, ln, fo, colour, i)
                    ty += round(line_height(fo) * 1.15)
        iy = y0 + PAD + m["head_h"] + HEAD_GAP
        ims = images[id(f)]
        widths = [round(im.width * m["H"] / im.height) for im in ims]
        ix = tx + (inner - (sum(widths) + IMG_GAP * (len(widths) - 1))) / 2
        for k, (im, w) in enumerate(zip(ims, widths)):
            small = im.resize((w, m["H"]), Image.LANCZOS)
            px = round(ix)
            canvas.paste(small, (px, iy), small)
            d.rectangle((px - 1, iy - 1, px + w, iy + m["H"]), outline=COLOURS["outline"], width=1)
            boxes["image"].append({"box": (px, iy, px + w, iy + m["H"]), "frame": i})
            if k < len(caps) and caps[k]:
                cl, cf = fit(fonts, "caption", caps[k], w, 2, "a caption")
                cy = iy + m["H"] + 12
                for ln in cl:
                    text(px + (w - text_width(cf, ln)) / 2, cy, ln, cf, COLOURS["caption"], i)
                    cy += round(line_height(cf) * 1.15)
            ix += w + IMG_GAP
    return canvas, boxes


def verify(m, boxes):
    """The rule, measured on the drawn board. Returns the problems (an empty list is a pass)."""
    problems = []
    W, H = m["w"], m["h"]

    def inside(b, c, slack=0):
        return b[0] >= c[0] - slack and b[1] >= c[1] - slack and b[2] <= c[2] + slack and b[3] <= c[3] + slack

    def overlap(b, c):
        return b[0] < c[2] and c[0] < b[2] and b[1] < c[3] and c[1] < b[3]

    frames = {fb["i"]: fb["box"] for fb in boxes["frame"]}
    for t in boxes["text"]:
        if not inside(t["box"], (0, 0, W, H)):
            problems.append(f"text off the board: {t['s']}")
        if t["frame"] is not None:
            f = frames[t["frame"]]
            if not inside(t["box"], (f[0] + 3, f[1] + 3, f[2] - 3, f[3] - 3), slack=1):
                problems.append(f"text out of its frame: {t['s']}")
        for im in boxes["image"]:
            if overlap(t["box"], im["box"]):
                problems.append(f"text over an image: {t['s']}")
    for im in boxes["image"]:
        if not inside(im["box"], frames[im["frame"]]):
            problems.append("an image out of its frame")
        if im["box"][3] - im["box"][1] != m["H"]:
            problems.append("images at different heights")
    sizes = {(fb["box"][2] - fb["box"][0], fb["box"][3] - fb["box"][1]) for fb in boxes["frame"] if fb["option"]}
    if len(sizes) > 1:
        problems.append(f"option frames differ: {sizes}")
    fl = [fb["box"] for fb in boxes["frame"]]
    for i in range(len(fl)):
        if not inside(fl[i], (0, 0, W, H)):
            problems.append("a frame off the board")
        for j in range(i + 1, len(fl)):
            if overlap(fl[i], fl[j]):
                problems.append("frames overlap")
    return problems


def build(spec, out, fonts, max_w=4000, max_h=4000, columns=None, image_height=None, quiet=False):
    images = {}
    for f in (spec.get("options") or []) + (spec.get("context") or []):
        images[id(f)] = [open_image(p) for p in f["paths"]]
    m = choose(spec, fonts, images, max_w, max_h, columns, image_height)
    for f in (spec.get("options") or []) + (spec.get("context") or []):
        for p, im in zip(f["paths"], images[id(f)]):
            if m["H"] / im.height > 1.5:
                warn(f"{p.name} drawn at {m['H'] / im.height:.1f}x its size (blurry): a larger capture is better")
    canvas, boxes = draw_board(spec, fonts, images, m)
    problems = verify(m, boxes)
    if problems:
        raise BoardError("the layout broke the rule (a bug in this tool): " + "; ".join(sorted(set(problems))[:6]))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ext = out.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        canvas.save(out, "JPEG", quality=92)
    elif ext == ".webp":
        canvas.save(out, "WEBP", quality=92)
    elif ext == ".png":
        canvas.save(out, "PNG")
    else:
        raise BoardError(f"output is .png, .jpg or .webp, not {ext or 'no extension'}")
    if not quiet:
        opts = spec.get("options") or []
        print(f"board: {out} ({m['w']}x{m['h']}) · {len(opts)} option(s){', ' + str(m['cols']) + ' a row' if opts else ''}"
              f" · {len(spec.get('context') or [])} context frame(s) · images {m['H']} px high"
              + (f" · recommended {[o['letter'] for o in opts if o.get('recommended')]}" if any(o.get("recommended") for o in opts) else ""), flush=True)
    return m, boxes


# --- Self-test ---

def selftest():
    passed = total = 0

    def check(name, cond, extra=""):
        nonlocal passed, total
        total += 1
        passed += bool(cond)
        print(f"{'ok  ' if cond else 'FAIL'} {name}{'' if cond else ' | ' + str(extra)[:300]}", flush=True)

    with tempfile.TemporaryDirectory(prefix="onay-panosu-") as tmp:
        t = Path(tmp)

        def shot(name, size, colour):
            im = Image.new("RGB", size, colour)
            dr = ImageDraw.Draw(im)
            dr.rectangle((0, 0, size[0], size[1] // 12), fill=(30, 30, 30))       # a HUD bar: text must stay clear of it
            dr.ellipse((size[0] // 4, size[1] // 3, 3 * size[0] // 4, size[1] // 3 + size[0] // 2), fill=(240, 240, 240))
            p = t / name
            im.save(p)
            return str(p)

        fonts = Fonts()
        portrait = {k: shot(f"{k}.png", (564, 1414), c) for k, c in (("now1", (120, 110, 160)), ("now2", (60, 50, 80)),
                    ("a1", (200, 150, 110)), ("a2", (180, 120, 90)), ("b1", (150, 200, 210)), ("b2", (120, 160, 180)),
                    ("c1", (170, 90, 80)), ("c2", (140, 70, 60)), ("d1", (90, 120, 200)), ("d2", (70, 90, 160)))}
        spec = {"title": "Kapı 2. tur: şeritler ve kazanma", "subtitle": "Gerçek bir kareden; şeritlerin zemini ve kenarı, kazanma kutlaması",
                "lang": "tr", "captions": ["Şeritler", "Kazanma"], "reference": True, "recommend": "A",
                "context": [{"kind": "current", "name": "Bugün", "note": "koyu şeritler, ince ışın, küçük parıltı", "images": [portrait["now1"], portrait["now2"]]}],
                "options": [{"letter": L, "name": n, "diff": dd, "images": [portrait[f"{L.lower()}1"], portrait[f"{L.lower()}2"]]}
                            for L, n, dd in (("A", "Kumtaşı şeritler", "oymalı kenar ve küçük meşale yuvaları; altın toz patlaması; sevinen ruhlar"),
                                             ("B", "Açık zemin, çini kenar", "krem zemin, turkuaz çini kenar; yıldız halkalı patlama"),
                                             ("C", "Kervan kilimi", "desenli kilim şeritler, püsküllü uçlar; yükselen kum girdabı"),
                                             ("D", "Ay ışığı", "gümüş mavi ay ışığı, kehribar meşaleler"))]}

        def run(sp, name, **kw):
            return build(load_spec_from(sp), t / name, fonts, quiet=True, **kw)

        m, boxes = run(spec, "a.png")
        check("4 options with 2 screens and a context frame: one row, rule verified", m["one_row"] and not verify(m, boxes), (m["cols"], verify(m, boxes)))
        check("option frames equal, images one height", len({(b["box"][2] - b["box"][0]) for b in boxes["frame"] if b["option"]}) == 1
              and len({b["box"][3] - b["box"][1] for b in boxes["image"]}) == 1)
        check("no text over an image", not any(tb["box"][0] < ib["box"][2] and ib["box"][0] < tb["box"][2] and tb["box"][1] < ib["box"][3]
                                               and ib["box"][1] < tb["box"][3] for tb in boxes["text"] for ib in boxes["image"]))
        check("the board fits 4000 px", m["w"] <= 4000 and m["h"] <= 4000, (m["w"], m["h"]))
        check("badge and reference tag drawn", any(tb["s"] == "önerim" for tb in boxes["text"])
              and any(tb["s"].startswith("İÇ REFERANS") for tb in boxes["text"]))
        land = {k: shot(f"{k}.png", (1640, 624), c) for k, c in (("x", (20, 30, 60)), ("y", (30, 60, 90)), ("z", (60, 40, 30)))}
        spec2 = {"title": "Facebook kapağı", "lang": "tr", "recommend": "B",
                 "options": [{"letter": L, "name": n, "diff": dd, "images": [land[k]]} for L, n, dd, k in
                             (("A", "Beş oyun", "mağaza görselleri, adlarıyla", "x"), ("B", "Simge şeridi", "on simge, iki sıra", "y"),
                              ("C", "Kolaj", "beş oyunun görseli şerit şerit", "z"))]}
        m2, b2 = run(spec2, "b.jpg")
        check("3 landscape options: verified, no upscaling", not verify(m2, b2) and m2["H"] <= 624, (m2["H"], verify(m2, b2)))
        spec3 = {"title": "Önce ve sonra", "lang": "tr",
                 "context": [{"kind": "before", "name": "Dün", "note": "eski ışık", "images": [portrait["now1"]]},
                             {"kind": "after", "name": "Bugün", "note": "yeni ışık", "images": [portrait["a1"]]}]}
        m3, b3 = run(spec3, "c.webp")
        check("before and after only", not verify(m3, b3) and not m3["opt"], verify(m3, b3))
        m4, b4 = run(spec, "d.png", columns=2)
        check("--columns 2: a grid, context on top, verified", not m4["one_row"] and not verify(m4, b4), verify(m4, b4))
        too_many = json.loads(json.dumps(spec))
        too_many["options"].append(dict(too_many["options"][0], letter="E"))
        try:
            load_spec_from(too_many)
            check("5 options refused", False)
        except BoardError as e:
            check("5 options refused", "at most 4" in str(e), e)
        long_diff = json.loads(json.dumps(spec))
        long_diff["options"][1]["diff"] = " ".join(["çok uzun bir fark satırı"] * 20)
        try:
            run(long_diff, "e.png")
            check("a difference longer than two lines stops the tool", False)
        except BoardError as e:
            check("a difference longer than two lines stops the tool", "shorten it" in str(e), e)
        dup = json.loads(json.dumps(spec))
        dup["options"][1]["letter"] = "A"
        try:
            load_spec_from(dup)
            check("repeated letters refused", False)
        except BoardError as e:
            check("repeated letters refused", "repeat" in str(e), e)
        bad = {"title": "x", "options": [{"letter": "A", "name": "n", "diff": "d", "images": [str(t / "missing.png")]}]}
        try:
            load_spec_from(bad)
            check("missing image refused", False)
        except BoardError as e:
            check("missing image refused", "not found" in str(e), e)
    print(f"self-test: {passed}/{total} passed", flush=True)
    return 0 if passed == total else 1


def load_spec_from(spec):
    """load_spec for a dict (the self-test): the JSON goes through a temporary file."""
    with tempfile.TemporaryDirectory(prefix="onay-spec-") as tmp:
        p = Path(tmp) / "spec.json"
        p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        return load_spec(argparse.Namespace(spec=str(p)))


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    argv = sys.argv[1:] if argv is None else argv
    if "--dene" in argv:
        return selftest()
    ap = argparse.ArgumentParser(description="An approval board by the owner's rule (see the top of the file).")
    ap.add_argument("--spec", help="JSON spec (paths relative to its folder)")
    ap.add_argument("--out", required=True, help="output image (.png, .jpg or .webp)")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--lang", default="tr", choices=("tr", "en"), help="the fixed labels' language (tr)")
    ap.add_argument("--captions", nargs="+", help="a caption under each image position (e.g. Lanes Win)")
    ap.add_argument("--reference", action="store_true", help="the options are AI internal references (tag line)")
    ap.add_argument("--recommend", help="the recommended option's letter")
    ap.add_argument("--option", nargs="+", action="append", metavar="X", help="LETTER NAME DIFF IMAGE [IMAGE ...]")
    ap.add_argument("--context", nargs="+", action="append", metavar="X", help="KIND NAME NOTE IMAGE [IMAGE ...] (current, before, after, reference)")
    ap.add_argument("--columns", type=int, help="options a row (default: chosen)")
    ap.add_argument("--image-height", type=int, help="image height on the board (default: chosen, at most 960)")
    ap.add_argument("--max-width", type=int, default=4000)
    ap.add_argument("--max-height", type=int, default=4000)
    ap.add_argument("--font", help="regular TTF (default: Arial or DejaVu Sans)")
    ap.add_argument("--font-bold", help="bold TTF")
    a = ap.parse_args(argv)
    try:
        if not a.spec and not a.option and not a.context:
            raise BoardError("give --spec, or --option/--context")
        spec = load_spec(a)
        fonts = Fonts(spec.get("font") or a.font, spec.get("font_bold") or a.font_bold)
        if not fonts.paths["regular"] or not fonts.paths["bold"]:
            warn("no TTF font found: Pillow's default font (give --font and --font-bold)")
        build(spec, a.out, fonts, a.max_width, a.max_height, a.columns, a.image_height)
        return 0
    except BoardError as e:
        print(f"ERROR: {e}", flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
