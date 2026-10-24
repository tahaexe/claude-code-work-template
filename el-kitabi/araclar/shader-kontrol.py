#!/usr/bin/env python3
"""Editor-free shader check: each code shader's HLSLPROGRAM compiled by the Windows SDK's fxc (SM 5) and dxc (SM 6).

From a game session's tool (2026-10-24, the studio's shared lesson U57): no editor and no heavy-job slot, about a second a
shader. The URP include is swapped for a stub of the core names the game's shaders use (`shader-kontrol-stub.hlsl` beside
this file: half as float, texture macros, the transform functions, built-in globals), so it catches syntax, type and
undeclared-name errors in the game's own code before a Unity run spends minutes on them. It doesn't replace Unity's compile
(URP's real library, the mobile back ends, variants): a step is still verified by a Unity run that logs no shader error.
A name missing from the stub fails as undeclared: add it to the stub (a project's copy keeps its own lines on a template
update) or give a project stub with --stub.
Usage: python -I -B shader-kontrol.py [--cost] [--stub FILE] <file.shader | folder> ...   (a folder: every *.shader under it)
       python -I -B shader-kontrol.py --dene    self-test on two tiny shaders, one with a planted error (needs the SDK)
       --cost also prints fxc's instruction slots a stage: a desktop proxy for comparing two versions of a shader (no Mali
       Offline Compiler needed), not a device's cycles.
       The SDK: WINDOWS_SDK_BIN (the folder holding fxc.exe and dxc.exe), else the newest Windows Kits 10 bin\\<version>\\x64.
Exit: 0 every stage compiles · 1 a stage failed · 2 usage · 4 no Windows SDK (fxc.exe) found.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

STUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shader-kontrol-stub.hlsl")
KITS = "C:/Program Files (x86)/Windows Kits/10/bin"
# fxc's performance hints on integer division and its save notes, not errors.
QUIET = re.compile(r"integer (divides|modulus) may be much slower|compilation (object|code) save succeeded")
SLOTS = re.compile(r"Approximately (\d+) instruction slots used")
# Stand-ins a URP include brings that a game's own shaders often define themselves (Vert, Varyings): only for a program
# that includes that file.
BY_INCLUDE = {"Blit.hlsl": ("struct Attributes { uint vertexID : SV_VertexID; };\n"
                            "struct Varyings { float4 positionCS : SV_POSITION; float2 texcoord : TEXCOORD0; };\n"
                            "Varyings Vert(Attributes input) { Varyings o; o.texcoord = float2((input.vertexID << 1) & 2, input.vertexID & 2);"
                            " o.positionCS = float4(o.texcoord * 2.0 - 1.0, 0.0, 1.0); return o; }\n")}


def find_sdk():
    """The folder holding fxc.exe (and dxc.exe where it has one): WINDOWS_SDK_BIN, else the newest Windows Kits 10 version."""
    given = os.environ.get("WINDOWS_SDK_BIN")
    if given:
        return given if os.path.isfile(os.path.join(given, "fxc.exe")) else None
    found = glob.glob(os.path.join(KITS, "10.*", "x64", "fxc.exe"))
    found.sort(key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(os.path.dirname(os.path.dirname(p))))])
    return os.path.dirname(found[-1]) if found else None


INCLUDE = re.compile(r'^\s*#include(?:_with_pragmas)?\s+"([^"]+)"')


def project_root(path):
    """The Unity project holding the file (the first folder up with Assets and ProjectSettings), or None."""
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.isdir(os.path.join(d, "Assets")) and os.path.isdir(os.path.join(d, "ProjectSettings")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def resolve(include, shader):
    """A project include's file (beside the shader, else from the project root); None for Packages/ (the stub stands in)."""
    if include.startswith("Packages/"):
        return None
    for base in (os.path.dirname(shader), project_root(shader)):
        if base and os.path.isfile(os.path.join(base, include)):
            return os.path.normpath(os.path.join(base, include))
    return None


def placeholders(files, work, root, seen):
    """Empty stand-ins for the Packages/ includes the project's own include files pull in (the stub has their names)."""
    for f in files:
        if f in seen:
            continue
        seen.add(f)
        nested = []
        for line in open(f, encoding="utf-8", errors="replace").read().splitlines():
            m = INCLUDE.match(line)
            if not m:
                continue
            if m.group(1).startswith("Packages/"):
                stand_in = os.path.join(work, *m.group(1).split("/"))
                os.makedirs(os.path.dirname(stand_in), exist_ok=True)
                open(stand_in, "a").close()
            else:
                for base in (os.path.dirname(f), root):
                    if base and os.path.isfile(os.path.join(base, m.group(1))):
                        nested.append(os.path.normpath(os.path.join(base, m.group(1))))
                        break
        placeholders(nested, work, root, seen)


def programs(source):
    """Each HLSLPROGRAM block: its first line in the file, its vertex and fragment entry points, and its lines with the
    pragmas blanked (lines kept, so errors point at the file's own lines; includes are handled by check)."""
    for match in re.finditer(r"HLSLPROGRAM(.*?)ENDHLSL", source, re.S):
        block = match.group(1)
        vertex = re.search(r"#pragma\s+vertex\s+(\w+)", block)
        fragment = re.search(r"#pragma\s+fragment\s+(\w+)", block)
        lines = ["" if line.strip().startswith("#pragma") else line for line in block.split("\n")]
        first_line = source.count("\n", 0, match.start(1)) + 1
        yield first_line, (vertex.group(1) if vertex else None), (fragment.group(1) if fragment else None), lines


def compile_stage(sdk, tool, args, path):
    result = subprocess.run([os.path.join(sdk, tool)] + args + [path], capture_output=True, encoding="utf-8", errors="replace")
    lines = [line for line in (result.stdout + result.stderr).splitlines() if line.strip() and not QUIET.search(line)]
    return result.returncode == 0, lines


def check(shader, sdk, stubs, cost, out=print):
    """Compiles every program of one shader; True when every stage compiles. Errors print with the shader's own lines."""
    source = open(shader, encoding="utf-8", errors="replace").read()
    tools = [("fxc.exe", "5_0", "/")] + ([("dxc.exe", "6_0", "-")] if os.path.isfile(os.path.join(sdk, "dxc.exe")) else [])
    root = project_root(shader)
    ok, count = True, 0
    with tempfile.TemporaryDirectory() as work:
        for number, (first_line, vertex, fragment, lines) in enumerate(programs(source)):
            count += 1
            kept, extra = [], ""
            for i, line in enumerate(lines):   # Packages/ includes → the stub; the project's own includes stay, by full path
                m = INCLUDE.match(line)
                if m:
                    found = resolve(m.group(1), shader)
                    lines[i] = f'#include "{found.replace(os.sep, "/")}"' if found else ""
                    kept += [found] if found else []
                    extra += BY_INCLUDE.get(m.group(1).rsplit("/", 1)[-1], "") if not found else ""
            placeholders(kept, work, root, set())
            path = os.path.join(work, f"program{number}.hlsl")
            includes = "".join(f'#include "{s}"\n' for s in stubs)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f'{includes}{extra}#line {first_line} "{os.path.basename(shader)}"\n' + "\n".join(lines))
            dirs = [work] + ([root] if root else [])
            for stage, entry in (("vs", vertex), ("ps", fragment)):
                if entry is None:
                    continue
                output, listing = os.path.join(work, f"{stage}{number}.bin"), os.path.join(work, f"{stage}{number}.asm")
                for tool, model, dash in tools:
                    args = [f"{dash}nologo", f"{dash}T", f"{stage}_{model}", f"{dash}E", entry, f"{dash}Fo", output]
                    args += [a for d in dirs for a in (f"{dash}I", d)]
                    passed, lines = compile_stage(sdk, tool, args + ([f"{dash}Fc", listing] if tool == "fxc.exe" else []), path)
                    ok = ok and passed
                    for line in lines:
                        out(f"  {tool[:3]} {stage}: {line}")
                if cost and os.path.exists(listing):
                    slots = SLOTS.search(open(listing, encoding="utf-8", errors="replace").read())
                    out(f"  cost {stage} {entry}: {slots.group(1) if slots else '?'} instruction slots (fxc)")
    out(f"{shader}: {'compiles' if ok else 'FAILED'}" + ("" if count else " (no HLSLPROGRAM)"))
    return ok


GOOD = """Shader "Test/Good" { SubShader { Pass {
HLSLPROGRAM
#pragma vertex vert
#pragma fragment frag
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
CBUFFER_START(UnityPerMaterial)
half4 _Tint;
CBUFFER_END
struct A { float4 p : POSITION; };
struct V { float4 p : SV_POSITION; };
V vert(A a) { V v; v.p = TransformObjectToHClip(a.p.xyz); return v; }
half4 frag(V v) : SV_Target { return _Tint * (0.5 + 0.5 * sin(_Time.y)); }
ENDHLSL
} } }
"""
BAD_LINE = 12   # frag uses a name nobody declared, on this line of the shader file


def dene(sdk):
    """Self-test: the good shader compiles, the same with an undeclared name fails and the error names the file's own line."""
    results = []
    with tempfile.TemporaryDirectory() as work:
        good, bad = os.path.join(work, "good.shader"), os.path.join(work, "bad.shader")
        with open(good, "w", encoding="utf-8") as f:
            f.write(GOOD)
        with open(bad, "w", encoding="utf-8") as f:
            f.write(GOOD.replace("return _Tint *", "return _Missing *"))
        lines = []
        results.append(("good shader compiles", check(good, sdk, [STUB], True, out=lines.append)))
        results.append(("its cost line", any("instruction slots" in line for line in lines)))
        lines = []
        results.append(("planted error fails", not check(bad, sdk, [STUB], False, out=lines.append)))
        results.append((f"the error points at bad.shader line {BAD_LINE}", any(f"bad.shader({BAD_LINE}," in line for line in lines)))
    for name, passed in results:
        print(f"{'OK  ' if passed else 'FAIL'} {name}")
    print(f"dene: {sum(p for _, p in results)}/{len(results)}")
    return 0 if all(p for _, p in results) else 1


def main(argv):
    sdk = find_sdk()
    if "--dene" in argv:
        if not sdk:
            print("no Windows SDK found (fxc.exe): set WINDOWS_SDK_BIN or install the Windows 10/11 SDK")
            return 4
        return dene(sdk)
    cost, stubs, paths, i = False, [STUB], [], 0
    while i < len(argv):
        if argv[i] == "--cost":
            cost = True
        elif argv[i] == "--stub" and i + 1 < len(argv):
            stubs.append(os.path.abspath(argv[i + 1]))
            i += 1
        elif argv[i].startswith("-"):
            print(__doc__)
            return 2
        else:
            paths.append(argv[i])
        i += 1
    if not paths:
        print(__doc__)
        return 2
    if not sdk:
        print("no Windows SDK found (fxc.exe): set WINDOWS_SDK_BIN or install the Windows 10/11 SDK")
        return 4
    shaders = []
    for p in paths:
        shaders += sorted(glob.glob(os.path.join(p, "**", "*.shader"), recursive=True)) if os.path.isdir(p) else [p]
    if not shaders:
        print("no .shader file in the given paths")
        return 2
    results = [check(os.path.abspath(s), sdk, stubs, cost) for s in shaders]
    print(f"{sum(results)}/{len(results)} shaders compile (fxc SM 5" + (", dxc SM 6" if os.path.isfile(os.path.join(sdk, "dxc.exe")) else "") + ")")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
