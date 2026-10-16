"""Pairwise colour differences (CIEDE2000) of game palettes under normal vision and simulated dichromacy.

CVD simulation: Machado, Oliveira, Fernandes 2009, severity 1.0 matrices, applied to linear sRGB (as DaltonLens and the
colour library do). Usage: python -I cvd_palette.py
"""
import math

MACHADO = {
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def hex_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def simulate(rgb, kind):
    lin = [to_linear(c) for c in rgb]
    if kind == "normal":
        return lin
    m = MACHADO[kind]
    return [min(1, max(0, sum(m[r][k] * lin[k] for k in range(3)))) for r in range(3)]


def lab(lin):
    r, g, b = lin
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de2000(lab1, lab2):
    # Sharma, Wu, Dalal 2005 formulation.
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if C1p else 0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if C2p else 0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def report(name, palette, background=None):
    print(f"== {name}")
    names = list(palette)
    for kind in ("normal", "protan", "deutan", "tritan"):
        labs = {n: lab(simulate(hex_rgb(palette[n]), kind)) for n in names}
        pairs = sorted(((de2000(labs[a], labs[b]), a, b) for i, a in enumerate(names) for b in names[i + 1:]))
        worst = ", ".join(f"{a}/{b} {d:.1f}" for d, a, b in pairs[:3])
        line = f"  {kind:7} min dE00 {pairs[0][0]:5.1f}  closest: {worst}"
        if background:
            bg = lab(simulate(hex_rgb(background), kind))
            near = min((de2000(labs[n], bg), n) for n in names)
            line += f"  | nearest to background: {near[1]} {near[0]:.1f}"
        print(line)


STONE = "#3E3833"  # dark stone floor (night): every proposal-B colour stays >= 22 dE00 away under all three CVD types

# A tower-defense game's element colours (EffectColor), for reference.
report("Tower defense (EffectColor)", {"Fire": "#EC4D34", "Ice": "#99E8F7", "Lightning": "#E0B649", "BlueFire": "#6D28FF",
                              "Plasma": "#FFD98C", "Aqua": "#31D1EF"}, STONE)
# Proposal A: the GDD's hues as first picked.
report("A (GDD hues)", {"Fire": "#E8452C", "Ice": "#8FDDF2", "Lightning": "#F6C21B", "BlueFire": "#24349E",
                        "Plasma": "#9B4DDB", "Aqua": "#16B3A3"}, STONE)
# Proposal B: lightness spread so each pair also differs in brightness (helps every CVD type).
report("B (lightness spread)", {"Fire": "#D9381E", "Ice": "#BDEFFF", "Lightning": "#FFD21F", "BlueFire": "#1B2A80",
                                "Plasma": "#B05CE6", "Aqua": "#0E8F7E"}, STONE)
# Proposal C: B with Fire pushed to orange and Plasma to magenta (away from blue for protan/deutan).
report("C (orange fire, magenta plasma)", {"Fire": "#F06A1D", "Ice": "#BDEFFF", "Lightning": "#FFD21F", "BlueFire": "#1B2A80",
                                           "Plasma": "#C2409E", "Aqua": "#0E8F7E"}, STONE)
