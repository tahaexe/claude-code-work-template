#!/usr/bin/env python3
"""Editor-free previews of Unity prefabs built from FBX models, such as Synty's (unity add-on 1.61): parses the prefab
YAML (old and new formats), the binary FBX meshes it uses and the atlas textures of its materials, and software-renders
a front view and a three-quarter view into a contact sheet.

Usage:  python -I -X utf8 docs/ai/araclar/prefab-onizleme.py [--project DIR] [--yenile] <sheet.png> <prefab> ...
        <prefab>: relative to Assets (Synty/.../SM_Env_Bush_01.prefab), to the project (Assets/...) or absolute
        --project: the Unity project to read (default: the one this file sits in, three folders up)
        --yenile: rebuild the GUID index (cached per project in the system temp folder; a missing GUID or cached
        path refreshes it by itself, re-reading only new or changed .meta files)
        python -I -X utf8 docs/ai/araclar/prefab-onizleme.py --dene    # self-test: a tiny project in a temp folder
Exit:   0 ok · 1 a prefab failed or came back empty (or a self-test check failed) · 2 usage · 4 numpy or Pillow missing

Prints each prefab's bounds in Unity metres (calibrated by the FBX unit scale), its triangle count and its colour mix.
Draws what the editor shows up close: LOD0 of an LOD group (or of a model's _LOD0.._LODn nodes); inactive objects,
disabled renderers and mesh filters without a renderer are left out (the notes count them as hidden). A mesh is
found by its fileID in the model .meta's name table or, when that is empty (2019.3+ imports), by Unity's hash of its
name (see xxh64); FBX pivots are baked into the mesh as Unity's importer does. Writes only the sheet and the index.

Limits: lighting is a flat key and fill and the materials are their atlas colours only (no normal maps, emission,
transparency or HDRP conversion), so judge shape, size and palette here and the look in the editor; binary FBX only
(ASCII FBX and .asset meshes are not read); skinned meshes are drawn as imported (bind pose); prefabs nested inside a
prefab are not drawn (noted); a variant is drawn as its source, a model's variant with its material slot overrides by
slot index (white without them), other overrides ignored. Needs numpy and Pillow.
"""
import argparse
import hashlib
import math
import os
import re
import shutil
import struct
import sys
import tempfile
import zlib

try:
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError:  # python -I hides the user site-packages, where `pip install --user` puts them
    import site
    sys.path.append(site.getusersitepackages())
    try:
        import numpy as np
        from PIL import Image, ImageDraw
    except ImportError as e:
        print("prefab-onizleme needs numpy and Pillow (%s): python -m pip install --user numpy pillow" % e)
        sys.exit(4)

_idx, _fresh, _fbx_cache, _tex_cache = {}, [False], {}, {}  # per run: GUID index, refreshed?, parsed FBX, textures


def use_project(path):
    """Reads that Unity project; its GUID index is cached in the system temp folder under a hash of its path."""
    global PROJECT, ASSETS, INDEX
    PROJECT = os.path.abspath(path)
    ASSETS = os.path.join(PROJECT, "Assets")
    key = hashlib.sha1(os.path.normcase(PROJECT).encode("utf-8")).hexdigest()[:10]
    INDEX = os.path.join(tempfile.gettempdir(), "prefab-onizleme-guids-%s.tsv" % key)
    for cache in (_idx, _fbx_cache, _tex_cache):
        cache.clear()
    _fresh[0] = False


use_project(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n")


# ---------- GUID index ----------
def meta_guid(meta):
    try:
        with open(meta, "rb") as fh:
            return re.search(rb"guid: ([0-9a-f]{32})", fh.read(300)).group(1).decode()
    except (OSError, AttributeError):
        return None


def load_index(refresh=False, full=False):
    """Fills the GUID index from its cache file or (refresh) by walking Assets and Packages for .meta files, where one
    whose path and mtime match the cache keeps its cached GUID (full: every .meta is read again)."""
    rows = {}
    try:
        with open(INDEX, encoding="utf-8") as fh:
            rows = {rel: (int(mt), g) for g, mt, rel in (line.rstrip("\n").split("\t") for line in fh)}
    except (OSError, ValueError):
        refresh = True
    if refresh:
        if full or not rows:
            print("indexing the GUIDs of %s (cache: %s)" % (PROJECT, INDEX), file=sys.stderr)
        old, rows, stack = rows, {}, [ASSETS, os.path.join(PROJECT, "Packages")]
        while stack:
            try:
                entries = list(os.scandir(stack.pop()))
            except OSError:
                continue
            for e in entries:
                if e.is_dir(follow_symlinks=False):
                    stack.append(e.path)
                elif e.name.endswith(".meta"):
                    rel, mt = os.path.relpath(e.path[:-5], PROJECT), e.stat().st_mtime_ns
                    was = None if full else old.get(rel)
                    g = was[1] if was and was[0] == mt else meta_guid(e.path)
                    if g:
                        rows[rel] = (mt, g)
        _fresh[0] = True
        try:
            with open("%s.%d" % (INDEX, os.getpid()), "w", encoding="utf-8") as fh:
                fh.writelines("%s\t%d\t%s\n" % (g, mt, rel) for rel, (mt, g) in rows.items())
            os.replace(fh.name, INDEX)
        except OSError:
            pass
    _idx.clear()
    _idx.update((g, os.path.join(PROJECT, rel)) for rel, (mt, g) in rows.items())


def guid_path(guid):
    """Asset path of a GUID; None for built-in resources and missing assets. A cached path is checked against its
    .meta and a miss refreshes the index (once per run), so the cache never serves stale data."""
    if not guid or guid.startswith("0000000000000000"):
        return None
    if not _idx and not _fresh[0]:
        load_index()
    while True:
        p = _idx.get(guid)
        if p and meta_guid(p + ".meta") == guid:
            return p
        if _fresh[0]:
            return None
        load_index(refresh=True)


# ---------- FBX ----------
def xxh64(data):
    """xxHash64 (seed 0) as a signed int64. Unity's model importer (fileIdsGeneration 2, empty internalIDToNameTable)
    gives a mesh the fileID xxh64("Type:Mesh->" + name + n), n counting the earlier meshes of that name."""
    p1, p2, p3, p4, p5 = 0x9E3779B185EBCA87, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9, 0x85EBCA77C2B2AE63, 0x27D4EB2F165667C5
    full = (1 << 64) - 1

    def rotl(x, r):
        return ((x << r) | (x >> (64 - r))) & full

    def rnd(acc, lane):
        return rotl((acc + lane * p2) & full, 31) * p1 & full

    n, i, h = len(data), 0, p5
    if n >= 32:
        v = [(p1 + p2) & full, p2, 0, (-p1) & full]
        while i + 32 <= n:
            v = [rnd(a, lane) for a, lane in zip(v, struct.unpack_from("<4Q", data, i))]
            i += 32
        h = (rotl(v[0], 1) + rotl(v[1], 7) + rotl(v[2], 12) + rotl(v[3], 18)) & full
        for a in v:
            h = ((h ^ rnd(0, a)) * p1 + p4) & full
    h = (h + n) & full
    while i + 8 <= n:
        h = (rotl(h ^ rnd(0, struct.unpack_from("<Q", data, i)[0]), 27) * p1 + p4) & full
        i += 8
    if i + 4 <= n:
        h = (rotl(h ^ (struct.unpack_from("<I", data, i)[0] * p1 & full), 23) * p2 + p3) & full
        i += 4
    for b in data[i:]:
        h = rotl(h ^ (b * p5 & full), 11) * p1 & full
    h = (h ^ (h >> 33)) * p2 & full
    h = (h ^ (h >> 29)) * p3 & full
    h ^= h >> 32
    return h - (1 << 64) if h >> 63 else h


SCALARS = {"Y": "<h", "C": "<B", "I": "<i", "F": "<f", "D": "<d", "L": "<q"}
ARRAYS = {"f": "<f4", "d": "<f8", "l": "<i8", "i": "<i4", "b": "u1"}


def read_fbx(path):
    data = open(path, "rb").read()
    if not data.startswith(b"Kaydara FBX Binary"):
        raise ValueError("not a binary FBX: " + os.path.basename(path))
    head = "<QQQ" if struct.unpack_from("<I", data, 23)[0] >= 7500 else "<III"

    def nodes(pos, end):  # a node list ends at its parent's end or at a null record
        out = []
        while pos < end:
            n, pos = node(pos)
            if n is None:
                break
            out.append(n)
        return out

    def node(pos):
        end, nprops, _ = struct.unpack_from(head, data, pos)
        pos += struct.calcsize(head) + 1
        if end == 0:
            return None, pos
        name, pos = data[pos:pos + data[pos - 1]].decode("latin1"), pos + data[pos - 1]
        props = []
        for _ in range(nprops):
            t, pos = chr(data[pos]), pos + 1
            if t in SCALARS:
                v, pos = struct.unpack_from(SCALARS[t], data, pos)[0], pos + struct.calcsize(SCALARS[t])
            elif t in ARRAYS:
                n, enc, clen = struct.unpack_from("<III", data, pos)
                raw, pos = data[pos + 12:pos + 12 + clen], pos + 12 + clen
                v = np.frombuffer(zlib.decompress(raw) if enc == 1 else raw, dtype=ARRAYS[t], count=n)
            elif t in "SR":
                n = struct.unpack_from("<I", data, pos)[0]
                v, pos = data[pos + 4:pos + 4 + n], pos + 4 + n
                v = v.decode("latin1") if t == "S" else v
            else:
                raise ValueError("unknown property type " + t)
            props.append(v)
        return (name, props, nodes(pos, end)), end

    return nodes(27, len(data))


def child(n, name):
    return next((k for k in n[2] if k[0] == name), None)


def p70(n):
    pr = child(n, "Properties70")
    return {p[1][0]: p[1][4:] for p in pr[2]} if pr else {}


def euler_xyz(r):
    x, y, z = [math.radians(a) for a in r]
    rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return rz @ ry @ rx


class Fbx:
    def __init__(self, path):
        top = read_fbx(path)
        gs = next((n for n in top if n[0] == "GlobalSettings"), None)
        self.unit = float(p70(gs).get("UnitScaleFactor", [1.0])[0]) if gs else 1.0
        objects = next(n for n in top if n[0] == "Objects")
        self.geoms = {o[1][0]: o for o in objects[2] if o[0] == "Geometry"}
        self.models = {o[1][0]: o for o in objects[2] if o[0] == "Model"}
        self.parent, self.geom_of = {}, {}
        for c in next(n for n in top if n[0] == "Connections")[2]:
            if c[1][0] == "OO":
                a, b = c[1][1], c[1][2]
                if a in self.geoms and b in self.models:
                    self.geom_of[b] = a
                elif a in self.models:
                    self.parent[a] = b
        self.names = {mid: m[1][1].split("\x00")[0].encode("latin1").decode("utf-8", "replace")
                      for mid, m in self.models.items()}
        self.hashed, seen = {}, {}
        for mid in self.geom_of:  # Unity's own fileIDs of the meshes (see xxh64), in file order
            name = self.names[mid]
            seen[name] = seen.get(name, -1) + 1
            self.hashed[str(xxh64(("Type:Mesh->%s%d" % (name, seen[name])).encode("utf-8")))] = mid

    def props(self, mid, *keys):
        """The model's Properties70 values as float arrays (missing: 1 for a scaling, else 0)."""
        pr = p70(self.models[mid])
        return [np.array(pr.get(k, [1, 1, 1] if k.endswith("Scaling") else [0, 0, 0]), dtype=float) for k in keys]

    def model_rotation(self, mid):
        pr = p70(self.models[mid])
        return pr.get("PreRotation", [0, 0, 0]), pr.get("Lcl Rotation", [0, 0, 0]), pr.get("Lcl Scaling", [1, 1, 1])

    def model_named(self, name):
        return next((mid for mid in self.geom_of if self.names[mid] == name), None)

    def lod0(self):
        """Models with a mesh the editor shows up close: of _LOD0.._LODn siblings (an LOD group on import) the lowest."""
        lod = {mid: re.search(r"_LOD(\d+)$", self.names[mid], re.I) for mid in self.geom_of}
        low = {}
        for mid, m in lod.items():
            if m:
                low[self.parent.get(mid)] = min(low.get(self.parent.get(mid), 1 << 30), int(m.group(1)))
        return [mid for mid, m in lod.items() if not m or int(m.group(1)) == low[self.parent.get(mid)]]

    def mesh(self, mid, unity=False):
        """Triangles of the model's geometry in the model's own space (geometric offsets applied; unity: also its
        pivots baked, as Unity's importer moves them into the GameObject): verts (n,3), tris (m,3), uvs per corner
        (m,3,2), material index per triangle (m); None without triangles."""
        g = self.geoms[self.geom_of[mid]]
        v = np.array(child(g, "Vertices")[1][0], dtype=float).reshape(-1, 3)
        pvi = np.array(child(g, "PolygonVertexIndex")[1][0], dtype=np.int64)
        last = pvi < 0  # a polygon's last corner is stored as ~index
        poly = np.concatenate([[0], np.cumsum(last)[:-1]]).astype(np.int64)  # each corner's polygon
        first = np.concatenate([[0], np.nonzero(last)[0] + 1])[poly]  # each corner's polygon's first corner
        k = np.nonzero((np.arange(len(pvi)) > first) & ~last)[0]
        k = k[k + 1 < len(pvi)]
        if not len(k):
            return None
        corners = np.stack([first[k], k, k + 1], 1)  # fan triangulation, as Unity's importer
        tris = np.where(last, ~pvi, pvi)[corners]
        tuv, tmat = np.zeros((len(k), 3, 2)), np.zeros(len(k), dtype=np.int64)
        uvl = child(g, "LayerElementUV")
        if uvl:
            uv = np.array(child(uvl, "UV")[1][0], dtype=float).reshape(-1, 2)
            mapping = child(uvl, "MappingInformationType")
            at = tris if mapping and mapping[1][0] in ("ByControlPoint", "ByVertice", "ByVertex") else corners
            direct = child(uvl, "ReferenceInformationType")[1][0] == "Direct"
            tuv = uv[at if direct else np.array(child(uvl, "UVIndex")[1][0], dtype=np.int64)[at]]
        mat = child(g, "LayerElementMaterial")
        mats = np.array(child(mat, "Materials")[1][0], dtype=np.int64) if mat else []
        if len(mats):
            by_poly = len(mats) > 1 and child(mat, "MappingInformationType")[1][0] != "AllSame"
            tmat = mats[poly[k]] if by_poly else np.full(len(k), mats[0])
        gt, gr, gs, rp, so, sp, s = self.props(mid, "GeometricTranslation", "GeometricRotation", "GeometricScaling",
                                               "RotationPivot", "ScalingOffset", "ScalingPivot", "Lcl Scaling")
        v = (euler_xyz(gr) @ (v * gs).T).T + gt
        return v + ((so + sp - rp) / np.where(s == 0, 1, s) - sp if unity else 0), tris, tuv, tmat


def recycled_names(meta):
    """fileID -> name from a model's .meta: internalIDToNameTable (2019.3+) or fileIDToRecycleName (older)."""
    out = dict(re.findall(r"first:\s*\n\s*-?\d+: (-?\d+)\s*\n\s*second: ([^\n]*)", meta))
    m = re.search(r"fileIDToRecycleName:\n((?: {4}-?\d+: [^\n]*\n)+)", meta)
    out.update(re.findall(r"(-?\d+): ([^\n]*)", m.group(1)) if m else [])
    return out


def load_fbx(path):
    """(Fbx, the .meta's fileID -> name table, scale from file units to metres), cached per run."""
    if path not in _fbx_cache:
        meta = read_text(path + ".meta")
        fbx = Fbx(path)
        gsm = re.search(r"globalScale: ([-+\d.eE]+)", meta)
        ufs = re.search(r"useFileScale: (\d)", meta)
        scale = (float(gsm.group(1)) if gsm else 1.0) * ((fbx.unit / 100.0) if (not ufs or ufs.group(1) == "1") else 1.0)
        _fbx_cache[path] = (fbx, recycled_names(meta), scale)
    return _fbx_cache[path]


def fbx_mesh(guid, fid):
    """((Fbx, model id, scale), None) for a mesh reference into a model file, or (None, why not)."""
    path = guid_path(guid)
    if not path or not path.lower().endswith(".fbx"):
        return None, "mesh not an fbx: %s" % (os.path.basename(path) if path else "missing " + guid)
    try:
        fbx, names, scale = load_fbx(path)
    except (OSError, ValueError, StopIteration) as e:
        return None, str(e) or "no Objects in " + os.path.basename(path)
    name = names.get(fid)
    mid = fbx.model_named(name) if name else fbx.hashed.get(fid)
    mid = next(iter(fbx.geom_of)) if mid is None and len(fbx.geom_of) == 1 else mid
    if mid is None:
        return None, "mesh %s not found in %s" % (name or fid, os.path.basename(path))
    return (fbx, mid, scale), None


# ---------- prefab YAML ----------
def ref(body, key):
    m = re.search(key + r": \{fileID: (-?\d+)", body)
    return m.group(1) if m else None


def vec(s, key):
    m = re.search(key + r": \{x: ([-+\d.eE]+), y: ([-+\d.eE]+), z: ([-+\d.eE]+)(?:, w: ([-+\d.eE]+))?\}", s)
    return [float(g) for g in m.groups() if g is not None] if m else None


def quat_matrix(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def material_info(guid):
    path = guid_path(guid)
    if not path or not path.endswith(".mat"):
        return None, (1, 1, 1, 1), path
    s, tex = read_text(path), None
    for key in ("_BaseColorMap", "_MainTex", "_Albedo", "_BaseMap", "_Leaf_Texture", "_LeafTexture", ""):  # "": any
        m = re.search((r"- " + key + r":\s*\n\s*m_Texture: \{fileID: \d+" if key else r"m_Texture: \{fileID: 2800000") +
                      r", guid: ([0-9a-f]{32})", s)
        tex = guid_path(m.group(1)) if m else None
        if tex:
            break
    m = re.search(r"- _(?:BaseColor|Color): \{r: ([-\d.e]+), g: ([-\d.e]+), b: ([-\d.e]+), a: ([-\d.e]+)\}", s)
    return tex, tuple(float(g) for g in m.groups()) if m else (1, 1, 1, 1), path


def texture(path):
    if path not in _tex_cache:
        try:
            _tex_cache[path] = np.asarray(Image.open(path).convert("RGBA"), dtype=float) / 255.0
        except Exception:
            _tex_cache[path] = None
    return _tex_cache[path]


def model_parts(path, overrides):
    """Parts of a model file's own hierarchy (what a model prefab shows), LOD0 nodes only; a model prefab instance's
    material slot overrides apply by slot index (the root renderer's first)."""
    fbx, _, scale = load_fbx(path)
    slots = {}
    for target, slot, guid in re.findall(r"target: \{fileID: (-?\d+),[^}]*\}\s*propertyPath: m_Materials\.Array\.data"
                                         r"\[(\d+)\]\s*value:[^\n]*\n\s*objectReference: \{fileID: -?\d+,\s*guid: "
                                         r"([0-9a-f]{32})", overrides):
        if target in ("-7511558181221131132", "2300000") or int(slot) not in slots:
            slots[int(slot)] = guid
    mats = [material_info(slots.get(i)) for i in range(max(slots) + 1)] if slots else []

    def model_matrix(mid):  # FBX: T * Roff * Rp * Rpre * R * Rpost^-1 * Rp^-1 * Soff * Sp * S * Sp^-1
        t, ro, rp, so, sp, s, pre, r, post = fbx.props(mid, "Lcl Translation", "RotationOffset", "RotationPivot",
                                                       "ScalingOffset", "ScalingPivot", "Lcl Scaling", "PreRotation",
                                                       "Lcl Rotation", "PostRotation")
        m, rot = np.eye(4), euler_xyz(pre) @ euler_xyz(r) @ euler_xyz(post).T
        m[:3, :3], m[:3, 3] = rot @ np.diag(s), t + ro + rp + rot @ (so + sp - rp - s * sp)
        par = fbx.parent.get(mid)
        return (model_matrix(par) @ m) if par in fbx.models else m

    parts = []
    for mid in fbx.lod0():
        got = fbx.mesh(mid)
        if got:
            v, tris, tuv, tmat = got
            w = model_matrix(mid)
            v = ((w[:3, :3] @ v.T).T + w[:3, 3]) * np.array([-1.0, 1.0, 1.0]) * scale
            parts.append((v, tris[:, [0, 2, 1]], tuv[:, [0, 2, 1], :], tmat, mats, fbx.model_rotation(mid), fbx.names[mid]))
    return parts


def prefab_parts(path, depth=0):
    """(parts, notes) for what the editor draws of a prefab up close. A part is (verts in prefab space, tris, uvs per
    corner, material slot per triangle, materials, FBX node rotation, name)."""
    tfs, go_of, active, meshes, rends, hidden, insts = {}, {}, {}, {}, {}, set(), []
    for doc in re.finditer(r"--- !u!(\d+) &(-?\d+)[^\n]*\n(.*?)(?=\n--- !u!|\Z)", read_text(path), re.S):
        cls, fid, body = int(doc.group(1)), doc.group(2), doc.group(3)
        go = ref(body, "m_GameObject")
        if cls == 1:
            active[fid] = "m_IsActive: 0" not in body
        elif cls == 4 and "m_LocalRotation" in body:  # a stripped transform (of a nested prefab) has no pose
            tfs[fid] = (vec(body, "m_LocalPosition"), vec(body, "m_LocalRotation"), vec(body, "m_LocalScale"),
                        ref(body, "m_Father"))
            go_of[fid] = go
        elif cls == 205:  # LODGroup: the first level with renderers is drawn, the other levels' renderers are not
            levels = [re.findall(r"renderer: \{fileID: (-?\d+)\}", lv) for lv in body.split("screenRelativeHeight")[1:]]
            shown = next((lv for lv in levels if any(r != "0" for r in lv)), [])
            hidden.update(r for lv in levels for r in lv if r not in shown)
        elif cls == 1001 and "m_SourcePrefab" in body:  # PrefabInstance (the old format's Prefab doc has none)
            insts.append(body)
        if cls in (33, 137):  # MeshFilter, SkinnedMeshRenderer
            m = re.search(r"m_Mesh: \{fileID: (-?\d+),\s*guid: ([0-9a-f]{32})", body)
            if m and go:
                meshes[go] = (m.group(1), m.group(2))
        if cls in (23, 137) and go:  # renderer: its material slots (an empty slot is None) and whether it's enabled
            sec = body.split("m_Materials:")[1].split("\n  m_")[0] if "m_Materials:" in body else ""
            slots = [g or None for g in re.findall(r"- \{fileID: -?\d+(?:,\s*guid: ([0-9a-f]{32}))?", sec)]
            rends[go] = (fid, slots, "m_Enabled: 0" not in body)
    tf_of = {g: t for t, g in go_of.items()}

    def world(t):
        w = np.eye(4)
        while t in tfs:
            p, q, s, t = tfs[t]
            m = np.eye(4)
            m[:3, :3] = quat_matrix(q or [0, 0, 0, 1]) @ np.diag(s or [1, 1, 1])
            m[:3, 3] = p or [0, 0, 0]
            w = m @ w
        return w

    def shown(t):  # active up the hierarchy; the root's own flag is ignored, so an inactive root still previews
        while t in tfs and tfs[t][3] in tfs:
            if not active.get(go_of[t], True):
                return False
            t = tfs[t][3]
        return True

    parts, notes, lower, off = [], [], 0, 0
    for go, (fid, guid) in meshes.items():
        rend, t = rends.get(go), tf_of.get(go)
        if rend is None or t is None or not rend[2] or not shown(t):
            off += 1
            continue
        if rend[0] in hidden:
            lower += 1
            continue
        got, why = fbx_mesh(guid, fid)
        mesh = got and got[0].mesh(got[1], unity=True)
        if not mesh:
            notes.append(why or "mesh without triangles")
            continue
        (fbx, mid, scale), (v, tris, tuv, tmat) = got, mesh
        v = v * np.array([-1.0, 1.0, 1.0]) * scale  # FBX (right-handed, file units) -> Unity: x mirrored, metres
        w = world(t)
        parts.append(((w[:3, :3] @ v.T).T + w[:3, 3], tris[:, [0, 2, 1]], tuv[:, [0, 2, 1], :], tmat,
                      [material_info(g) for g in rend[1]], fbx.model_rotation(mid), fbx.names[mid]))
    for body in insts:
        m = re.search(r"m_SourcePrefab: \{fileID: -?\d+,\s*guid: ([0-9a-f]{32})", body)
        src = guid_path(m.group(1)) if m else None
        name = os.path.basename(src) if src else "a missing source"
        if ref(body, "m_TransformParent") != "0":
            notes.append("nested prefab not drawn: " + name)
        elif src and src.lower().endswith(".fbx"):
            parts += model_parts(src, body)
            notes.append("model prefab")
        elif src and src.endswith(".prefab") and depth < 8:
            more, why = prefab_parts(src, depth + 1)
            parts += more
            notes += why + ["variant of " + name]
        else:
            notes.append("source not drawn: " + name)
    left = ["%d lower-LOD" % lower] * bool(lower) + ["%d hidden" % off] * bool(off)
    return parts, list(dict.fromkeys(notes)) + ["left out: " + ", ".join(left)] * bool(left)


# ---------- render ----------
def render(parts, view, size=300):
    yaw, pitch = math.radians(view[0]), math.radians(view[1])  # Unity: yaw about +y from +z, pitch down
    fwd = np.array([math.sin(yaw) * math.cos(pitch), -math.sin(pitch), math.cos(yaw) * math.cos(pitch)])
    right = np.array([math.cos(yaw), 0.0, -math.sin(yaw)])
    up = np.cross(fwd, right)
    up = -up if up[1] < 0 else up
    allv = np.concatenate([p[0] for p in parts])
    pts = [(p[0] - (allv.min(0) + allv.max(0)) / 2) @ np.stack([right, up, fwd]).T for p in parts]
    every = np.concatenate(pts)
    ext = max(np.abs(every[:, 0]).max(), np.abs(every[:, 1]).max()) * 1.08 + 1e-6
    img, zb = np.ones((size, size, 3)) * np.array([0.80, 0.84, 0.88]), np.full((size, size), np.inf)
    light = -fwd * 0.6 + up * 0.6 + right * -0.4
    light /= np.linalg.norm(light)
    for (v, tris, tuv, tmat, mats, _, _), q in zip(parts, pts):
        sx, sy = (q[:, 0] / ext * 0.5 + 0.5) * (size - 1), (0.5 - q[:, 1] / ext * 0.5) * (size - 1)
        for t, (a, b, c) in enumerate(tris):
            xs, ys, zs = sx[[a, b, c]], sy[[a, b, c]], q[[a, b, c], 2]
            x0, x1 = int(max(0, math.floor(xs.min()))), int(min(size - 1, math.ceil(xs.max())))
            y0, y1 = int(max(0, math.floor(ys.min()))), int(min(size - 1, math.ceil(ys.max())))
            den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
            if x1 < x0 or y1 < y0 or abs(den) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
            l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
            l2 = 1 - l0 - l1
            inside = (l0 >= -1e-4) & (l1 >= -1e-4) & (l2 >= -1e-4)
            if not inside.any():
                continue
            n = np.cross(v[b] - v[a], v[c] - v[a])
            nn = np.linalg.norm(n)
            shade = 0.55 + 0.45 * abs(np.dot(n / nn, light)) if nn > 0 else 0.8
            mi = int(tmat[t]) if len(tmat) else 0
            tex, col, _ = mats[mi] if mi < len(mats) else (None, (1, 1, 1, 1), None)
            arr = texture(tex) if tex else None
            rgb = np.ones(gx.shape + (3,)) * np.array(col[:3])
            if arr is not None:  # the texel under each pixel; its alpha cuts out leaf cards
                u, w = (l0 * tuv[t, 0, i] + l1 * tuv[t, 1, i] + l2 * tuv[t, 2, i] for i in (0, 1))
                h, wd = arr.shape[:2]
                texel = arr[np.clip(((1 - (w % 1.0)) * h).astype(int), 0, h - 1), np.clip(((u % 1.0) * wd).astype(int), 0, wd - 1)]
                rgb, inside = texel[..., :3] * np.array(col[:3]), inside & (texel[..., 3] > 0.35)
            z, sub = l0 * zs[0] + l1 * zs[1] + l2 * zs[2], zb[y0:y1 + 1, x0:x1 + 1]
            mask = inside & (z < sub)
            sub[mask] = z[mask]
            img[y0:y1 + 1, x0:x1 + 1][mask] = np.clip(rgb[mask] * shade, 0, 1)
    return Image.fromarray((img * 255).astype(np.uint8))


def colour_mix(parts):
    """Share of triangle area by a coarse colour name, from each triangle's texel at its UV centroid."""
    names = {}
    for v, tris, tuv, tmat, mats, _, _ in parts:
        area = np.linalg.norm(np.cross(v[tris[:, 1]] - v[tris[:, 0]], v[tris[:, 2]] - v[tris[:, 0]]), axis=1) / 2
        rgb = np.ones((len(tris), 3))
        for mi in set(tmat.tolist()):
            tex, col, _ = mats[mi] if mi < len(mats) else (None, (1, 1, 1, 1), None)
            arr, sel = texture(tex) if tex else None, tmat == mi
            if arr is not None:
                uv, (h, w) = tuv[sel].mean(1), arr.shape[:2]
                rgb[sel] = arr[np.clip(((1 - uv[:, 1] % 1.0) * h).astype(int), 0, h - 1),
                               np.clip(((uv[:, 0] % 1.0) * w).astype(int), 0, w - 1), :3]
            rgb[sel] *= np.array(col[:3])
        for key, a in zip(("#%02x%02x%02x" % tuple(c) for c in (rgb * 255).astype(int) // 32 * 32), area):
            names[key] = names.get(key, 0) + a
    tot = sum(names.values()) or 1
    return ", ".join("%s %d%%" % (k, 100 * a / tot) for k, a in sorted(names.items(), key=lambda kv: -kv[1])[:5])


def main(out, prefabs):
    tiles, bad = [], 0
    for rel in prefabs:
        path = next((p for p in (os.path.join(ASSETS, rel), os.path.join(PROJECT, rel), rel) if os.path.isfile(p)), None)
        try:
            if not path:
                raise FileNotFoundError("no such prefab in " + PROJECT)
            parts, notes = prefab_parts(path)
        except Exception as e:
            print("FAIL", rel, e)
            bad += 1
            continue
        if not parts:
            print("EMPTY", rel, notes)
            bad += 1
            continue
        allv = np.concatenate([p[0] for p in parts])
        lo, hi = allv.min(0), allv.max(0)
        print("%s size (%.2f, %.2f, %.2f) min (%.2f, %.2f, %.2f) tris %d rot %s | %s %s" % (
            rel, *(hi - lo), *lo, sum(len(p[1]) for p in parts), parts[0][5], colour_mix(parts), " ".join(notes)))
        tile = Image.new("RGB", (600, 330), (40, 40, 40))
        tile.paste(render(parts, (180, 8)), (0, 0))
        tile.paste(render(parts, (215, 28)), (300, 0))
        d = ImageDraw.Draw(tile)
        d.text((4, 302), os.path.basename(rel).replace(".prefab", ""), fill=(255, 255, 255))
        d.text((4, 316), "%.2f x %.2f x %.2f m" % tuple(hi - lo), fill=(200, 200, 200))
        tiles.append(tile)
    if tiles:
        sheet = Image.new("RGB", (3 * 600, (len(tiles) + 2) // 3 * 330), (20, 20, 20))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % 3) * 600, (i // 3) * 330))
        sheet.save(out)
        print("sheet", out, len(tiles))
    return 1 if bad else 0


# ---------- self-test ----------
def fbx_bytes(geoms, models, links):
    """A minimal binary FBX 7.4 for --dene, in centimetres: geoms (id, verts, quads), models (id, name, kind, pivot),
    links (child, parent)."""
    def prop(x):
        if isinstance(x, str):
            return b"S" + struct.pack("<I", len(x)) + x.encode()
        if not isinstance(x, list):
            return b"L" + struct.pack("<q", x) if isinstance(x, int) else b"D" + struct.pack("<d", x)
        a = np.array(x, dtype="<f8" if isinstance(x[0], float) else "<i4")
        return (b"d" if a.dtype.kind == "f" else b"i") + struct.pack("<III", len(a), 0, a.nbytes) + a.tobytes()

    def node(name, props, kids, off):
        p, body = b"".join(map(prop, props)), b""
        for k in kids:
            body += node(*k, off + 13 + len(name) + len(p) + len(body))
        body += b"\0" * 13 * bool(kids)
        return struct.pack("<IIIB", off + 13 + len(name) + len(p) + len(body), len(props), len(p), len(name)) + \
            name.encode() + p + body

    objects = [("Model", [i, name + "\x00\x01Model", kind], [("Properties70", [], [("P", [k, "Vector3D", "Vector", ""] +
                [float(c) for c in pivot], []) for k in ("RotationPivot", "ScalingPivot")])]) for i, name, kind, pivot in models] + [
        ("Geometry", [gid, "\x00\x01Geometry", "Mesh"], [("Vertices", [[float(c) for v in verts for c in v]], []),
         ("PolygonVertexIndex", [[i if j < 3 else ~i for q in quads for j, i in enumerate(q)]], []), ("LayerElementUV",
          [0], [("ReferenceInformationType", ["Direct"], []), ("UV", [[0.5, 0.5] * 4 * len(quads)], [])])])
        for gid, verts, quads in geoms]
    data = b"Kaydara FBX Binary  \x00\x1a\x00" + struct.pack("<I", 7400)
    for n in (("Objects", [], objects), ("Connections", [], [("C", ["OO", a, b], []) for a, b in links])):
        data += node(*n, len(data))
    return data + b"\0" * 13


def test_prefab(old, fbx_guid, mesh_ids, mat_guid):
    """A prefab's YAML: an LOD group on the root, children LOD0 and LOD1, and an inactive copy of LOD0 5 m away."""
    s = "%YAML 1.1\n" + ("--- !u!1001 &100100000\nPrefab:\n  m_RootGameObject: {fileID: 10}\n" if old else "")
    for n, name, father, mesh, act, x in ((1, "Bush", 0, None, 1, 0), (2, "Bush_LOD0", 11, mesh_ids[0], 1, 0),
                                         (3, "Bush_LOD1", 11, mesh_ids[1], 1, 0), (4, "Spare", 11, mesh_ids[0], 0, 5)):
        s += ("--- !u!1 &%d0\nGameObject:\n  m_Name: %s\n  m_IsActive: %d\n--- !u!4 &%d1\nTransform:\n  m_GameObject: "
              "{fileID: %d0}\n  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n  m_LocalPosition: {x: %d, y: 0, z: 0}\n"
              "  m_LocalScale: {x: 1, y: 1, z: 1}\n  m_Father: {fileID: %d}\n") % (n, name, act, n, n, x, father)
        s += ("--- !u!33 &%d2\nMeshFilter:\n  m_GameObject: {fileID: %d0}\n  m_Mesh: {fileID: %s, guid: %s, type: 3}\n"
              "--- !u!23 &%d3\nMeshRenderer:\n  m_GameObject: {fileID: %d0}\n  m_Enabled: 1\n  m_Materials:\n  - {fileID: "
              "2100000, guid: %s, type: 2}\n") % (n, n, mesh, fbx_guid, n, n, mat_guid) if mesh else ""
    return s + ("--- !u!205 &19\nLODGroup:\n  m_LODs:\n  - screenRelativeHeight: 0.25\n    renderers:\n    - renderer: "
                "{fileID: 23}\n  - screenRelativeHeight: 0.01\n    renderers:\n    - renderer: {fileID: 33}\n")


def dene():
    """Self-test: a tiny project in a temp folder (a binary FBX with _LOD0/_LOD1 meshes, new- and old-format prefabs
    with an LOD group, a model prefab variant, a material and its texture), previewed and checked, then deleted."""
    checks, full, root = [], (1 << 64) - 1, tempfile.mkdtemp(prefix="prefab-onizleme-dene-")

    def case(what, ok):
        checks.append(bool(ok))
        print("ok  " if ok else "FAIL", what)

    case("xxHash64 test vectors; Unity's fileID of a Synty import's mesh SM_Env_Bush_01_LOD0",
         xxh64(b"abc") & full == 0x44BC2CF5AD770999 and xxh64(b"Type:Mesh->SM_Env_Bush_01_LOD00") == -5738406403296023646
         and xxh64(b"Nobody inspects the spammish repetition") & full == 0xFBCEA83C8A378BF1)
    case(".meta name tables, old and new", recycled_names("  fileIDToRecycleName:\n    100000: //RootNode\n    4300000: "
         "Leaf\n  materials:\n") == {"100000": "//RootNode", "4300000": "Leaf"} and recycled_names(
         "  internalIDToNameTable:\n  - first:\n      43: -42\n    second: Leaf\n  externalObjects: {}\n") == {"-42": "Leaf"})
    use_project(root)
    try:
        g = {k: hashlib.md5(k.encode()).hexdigest() for k in ("fbx", "old", "mat", "tex", "late")}
        fbx = fbx_bytes([(12, [(x, y, z) for x in (0, 100) for y in (0, 100) for z in (-50, 50)],  # a 1 m cube whose
                          [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]),  # pivot is
                         (13, [(-150, 0, -150), (150, 0, -150), (150, 0, 150), (-150, 0, 150)], [(0, 1, 2, 3)])],  # its
                        [(1, "Bush", "Null", (0, 0, 0)), (2, "Bush_LOD0", "Mesh", (50, 0, 0)),  # centre, a 3 m card
                         (3, "Bush_LOD1", "Mesh", (0, 0, 0))], [(1, 0), (2, 1), (3, 1), (12, 2), (13, 3)])
        meta = "guid: %s\nModelImporter:\n%s  meshes:\n    globalScale: 1\n    useFileScale: 1\n"
        files = {"Bush.fbx": fbx, "Old.fbx": fbx, "Bush.fbx.meta": meta % (g["fbx"], "  internalIDToNameTable: []\n"),
                 "Old.fbx.meta": meta % (g["old"], "  fileIDToRecycleName:\n    4300000: Bush_LOD0\n    4300002: Bush_LOD1\n"),
                 "Red.mat": "    - _BaseMap:\n        m_Texture: {fileID: 2800000, guid: %s, type: 3}\n    - _BaseColor: "
                            "{r: 1, g: 1, b: 1, a: 1}\n" % g["tex"], "Red.mat.meta": "guid: %s\n" % g["mat"],
                 "Red.png.meta": "guid: %s\n" % g["tex"],
                 "New.prefab": test_prefab(False, g["fbx"], [str(xxh64(b"Type:Mesh->Bush_LOD%d0" % i)) for i in (0, 1)], g["mat"]),
                 "Old.prefab": test_prefab(True, g["old"], ["4300000", "4300002"], g["mat"]),
                 "Variant.prefab": "--- !u!1001 &5\nPrefabInstance:\n  m_Modification:\n    m_TransformParent: {fileID: 0}\n"
                                   "    m_Modifications:\n    - target: {fileID: -7511558181221131132, guid: %s,\n        type: "
                                   "3}\n      propertyPath: m_Materials.Array.data[0]\n      value: \n      objectReference: "
                                   "{fileID: 2100000, guid: %s, type: 2}\n  m_SourcePrefab: {fileID: 100100000, guid: %s, type: "
                                   "3}\n" % (g["fbx"], g["mat"], g["fbx"])}
        os.makedirs(os.path.join(ASSETS, "Moved"))
        for name, content in files.items():
            with open(os.path.join(ASSETS, name), "wb") as fh:
                fh.write(content if isinstance(content, bytes) else content.encode("utf-8"))
        Image.new("RGB", (4, 4), (255, 0, 0)).save(os.path.join(ASSETS, "Red.png"))
        for name, note, low in (("New.prefab", "left out: 1 lower-LOD, 1 hidden", -0.5),  # its pivot baked
                                ("Old.prefab", "left out: 1 lower-LOD, 1 hidden", -0.5),
                                ("Variant.prefab", "model prefab", -1)):  # the node's own place in the model
            parts, notes = prefab_parts(os.path.join(ASSETS, name))
            allv = np.concatenate([p[0] for p in parts]) if parts else np.zeros((1, 3))
            lo, hi, ntri = allv.min(0), allv.max(0), sum(len(p[1]) for p in parts)
            case("%s: the LOD0 cube alone, red, in place (%d tris, min %s, max %s, %s; %s)" % (
                name, ntri, np.round(lo, 2), np.round(hi, 2), colour_mix(parts), "; ".join(notes)), ntri == 12 and
                np.allclose(lo, (low, 0, -0.5)) and np.allclose(hi - lo, 1) and note in notes and colour_mix(parts) == "#e00000 100%")
        img = np.asarray(render(parts, (180, 8), size=64))
        case("renderer: the red cube in the centre, the background in the corner",
             img[32, 32, 0] > 120 and img[32, 32, 1] < 60 and tuple(img[1, 1]) == (204, 214, 224))
        sheet = os.path.join(root, "sheet.png")
        case("a sheet from three path forms", main(sheet, ["New.prefab", "Assets/Old.prefab", os.path.join(
             ASSETS, "Variant.prefab")]) == 0 and Image.open(sheet).size == (1800, 330))
        case("the index cached per project in the temp folder",
             os.path.isfile(INDEX) and hashlib.sha1(os.path.normcase(root).encode()).hexdigest()[:10] in INDEX)
        for name in ("Red.mat", "Red.mat.meta"):  # move one asset and add another
            os.replace(os.path.join(ASSETS, name), os.path.join(ASSETS, "Moved", name))
        for name, content in (("Late.mat", ""), ("Late.mat.meta", "guid: %s\n" % g["late"])):
            with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
                fh.write(content)
        use_project(root)  # a new run: its cache holds the moved asset's old path and lacks the new one
        case("the index finds a moved asset and a new one", guid_path(g["tex"]) and guid_path(g["mat"]) == os.path.join(
             ASSETS, "Moved", "Red.mat") and guid_path(g["late"]) == os.path.join(ASSETS, "Late.mat"))
    finally:
        try:
            os.remove(INDEX)
        except OSError:
            pass
        shutil.rmtree(root, ignore_errors=True)
    print("dene: %d/%d ok" % (sum(checks), len(checks)))
    return 0 if all(checks) else 1


def cli():
    parser = argparse.ArgumentParser(description="Editor-free previews of Unity prefabs built from FBX models.")
    parser.add_argument("sheet", nargs="?", help="the contact sheet to write (.png)")
    parser.add_argument("prefabs", nargs="*", help="prefab paths: relative to Assets, to the project, or absolute")
    parser.add_argument("--project", help="the Unity project (default: three folders up from this file)")
    parser.add_argument("--yenile", action="store_true", help="rebuild the project's GUID index first")
    parser.add_argument("--dene", action="store_true", help="self-test in a temp folder, then exit")
    args = parser.parse_args()
    if args.dene:
        return dene()
    use_project(args.project or PROJECT)
    if not os.path.isdir(ASSETS) or not args.prefabs:
        parser.error("no Assets folder in %s (pass --project)" % PROJECT if args.prefabs else "give a sheet and prefabs")
    if args.yenile:
        load_index(refresh=True, full=True)
    return main(args.sheet, args.prefabs)


if __name__ == "__main__":
    sys.exit(cli())
