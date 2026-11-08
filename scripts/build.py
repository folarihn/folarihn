"""Render the animated SVG panels for the GitHub profile README from profile.json.

Usage:  python scripts/build.py
Edit profile.json (builds, boot lines, stack) and re-run; README.md is regenerated too.
SVGs use only inline CSS animation (no scripts, no external fonts or images), which
GitHub renders inside <img>.
"""
from __future__ import annotations

import json
import random
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))

BG = "#05080b"
PANEL = "#0a1117"
LINE = "#14303a"
GREEN = "#3dff9a"
CYAN = "#22d3ee"
AMBER = "#ffb020"
PINK = "#ff3d7f"
TEXT = "#d4e1ea"
DIM = "#6b8495"
MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Code',Consolas,'Liberation Mono',monospace"
STATUS = {"LIVE": GREEN, "BETA": AMBER, "R&D": CYAN}


def x(s: str) -> str:
    return escape(s, quote=True)


def svg(w: int, h: int, body: str, css: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{x(title)}">\n<title>{x(title)}</title>\n'
        f"<style>\ntext{{font-family:{MONO};}}\n{css}\n"
        "@media (prefers-reduced-motion: reduce){*{animation:none!important;opacity:1!important}}\n"
        f"</style>\n{body}\n</svg>\n"
    )


def grid_defs(pid: str, step: int = 32) -> str:
    return (
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<path d="M {step} 0 L 0 0 0 {step}" fill="none" stroke="{LINE}" stroke-width="0.6" opacity="0.55"/></pattern>'
    )


# ---------------------------------------------------------------- hero
def hero() -> str:
    W, H = 1200, 440
    rnd = random.Random(7)
    css = f"""
.grid{{animation:drift 14s linear infinite}}
@keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-32px,-32px)}}}}
.scan{{animation:scan 6s linear infinite}}
@keyframes scan{{from{{transform:translateY(-120px)}}to{{transform:translateY({H}px)}}}}
.line{{opacity:0;animation:type .35s steps(1) forwards}}
.ok{{opacity:0;animation:pop .3s ease-out forwards}}
@keyframes type{{to{{opacity:1}}}}
@keyframes pop{{0%{{opacity:0}}60%{{opacity:1;fill:#fff}}100%{{opacity:1}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.g1{{animation:g1 4s steps(1) infinite}}
.g2{{animation:g2 4s steps(1) infinite}}
@keyframes g1{{0%,88%,100%{{transform:translate(0,0);opacity:0}}89%{{transform:translate(-5px,2px);opacity:.85}}92%{{transform:translate(4px,-1px);opacity:.85}}95%{{opacity:0}}}}
@keyframes g2{{0%,88%,100%{{transform:translate(0,0);opacity:0}}90%{{transform:translate(5px,-2px);opacity:.85}}93%{{transform:translate(-3px,1px);opacity:.85}}96%{{opacity:0}}}}
.node{{animation:pulse 3s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.edge{{stroke-dasharray:4 6;animation:flow 2.4s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-40}}}}
.pkt{{animation:pkt 3.2s linear infinite}}
.bar{{animation:bar 2.8s ease-in-out infinite alternate}}
@keyframes bar{{from{{transform:scaleX(.25)}}to{{transform:scaleX(1)}}}}
.fade{{opacity:0;animation:type .6s ease-out forwards}}
"""
    b = [
        f"<defs>{grid_defs('g')}"
        f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{GREEN}" stop-opacity=".09"/></linearGradient>'
        f'<radialGradient id="glow" cx=".78" cy=".45" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>',
        f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<rect class="grid" x="0" y="0" width="{W + 64}" height="{H + 64}" fill="url(#g)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
    ]

    # --- network graph (right side)
    nodes = [(rnd.randint(985, 1160), rnd.randint(40, 400)) for _ in range(14)]
    edges = set()
    for i, (ax, ay) in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - ax) ** 2 + (nodes[j][1] - ay) ** 2)[1:3]
        for j in near:
            edges.add(tuple(sorted((i, j))))
    for k, (i, j) in enumerate(sorted(edges)):
        (ax, ay), (bx, by) = nodes[i], nodes[j]
        col = CYAN if k % 3 else GREEN
        b.append(
            f'<line class="edge" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{col}" stroke-width="1" '
            f'opacity=".45" style="animation-delay:-{k * 0.3:.1f}s"/>'
        )
    for k, (i, j) in enumerate(sorted(edges)[:7]):
        (ax, ay), (bx, by) = nodes[i], nodes[j]
        b.append(
            f'<circle r="2.6" fill="{GREEN}"><animateMotion dur="{2.4 + k * 0.4:.1f}s" repeatCount="indefinite" '
            f'path="M{ax},{ay} L{bx},{by}"/></circle>'
        )
    for k, (nx, ny) in enumerate(nodes):
        r = 3 + (k % 3)
        col = GREEN if k % 4 == 0 else CYAN
        b.append(
            f'<circle class="node" cx="{nx}" cy="{ny}" r="{r + 6}" fill="{col}" opacity=".12" style="animation-delay:-{k * 0.37:.2f}s"/>'
            f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="{BG}" stroke="{col}" stroke-width="1.5"/>'
        )

    # --- name block
    name = DATA["name"]
    b.append(f'<text x="56" y="76" fill="{DIM}" font-size="15" letter-spacing="3">// {x(DATA["handle"])}@agent-systems:~</text>')
    for cls, col in (("g1", PINK), ("g2", CYAN)):
        b.append(f'<text class="{cls}" x="52" y="150" fill="{col}" font-size="78" font-weight="800" letter-spacing="6">{x(name)}</text>')
    b.append(f'<text x="52" y="150" fill="{TEXT}" font-size="78" font-weight="800" letter-spacing="6">{x(name)}</text>')
    b.append(f'<rect class="cur" x="{52 + len(name) * 53}" y="96" width="30" height="58" fill="{GREEN}"/>')
    b.append(f'<text x="56" y="188" fill="{GREEN}" font-size="18" letter-spacing="1.5">&gt; {x(DATA["role"])}</text>')

    # --- boot terminal
    tx, ty, tw, th = 56, 214, 640, 190
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="{PANEL}" fill-opacity=".92" stroke="{LINE}"/>')
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="28" rx="10" fill="#0e1820"/>')
    for k, c in enumerate((PINK, AMBER, GREEN)):
        b.append(f'<circle cx="{tx + 18 + k * 18}" cy="{ty + 14}" r="5" fill="{c}" opacity=".85"/>')
    b.append(f'<text x="{tx + 82}" y="{ty + 19}" fill="{DIM}" font-size="12">boot.log — live</text>')
    for k, (verb, target, st) in enumerate(DATA["boot"]):
        y = ty + 54 + k * 22
        d = 0.4 + k * 0.45
        label = f"[{verb:<5}] {target}"
        dots = "." * max(3, 44 - len(label))
        col = GREEN if st == "OK" else CYAN
        b.append(
            f'<text class="line" x="{tx + 18}" y="{y}" font-size="14" style="animation-delay:{d:.2f}s">'
            f'<tspan fill="{DIM}">$ </tspan><tspan fill="{TEXT}">{x(label)}</tspan><tspan fill="#2a4350"> {dots}</tspan></text>'
        )
        b.append(
            f'<text class="ok" x="{tx + tw - 24}" y="{y}" text-anchor="end" font-size="14" font-weight="700" fill="{col}" '
            f'style="animation-delay:{d + 0.3:.2f}s">[{st}]</text>'
        )

    # --- side metrics (activity bars)
    mx = 730
    b.append(f'<text class="fade" x="{mx}" y="{ty + 16}" fill="{DIM}" font-size="12" style="animation-delay:3.2s">SYSTEM LOAD</text>')
    for k, lab in enumerate(("agents", "chains", "builds")):
        y = ty + 40 + k * 30
        b.append(f'<text class="fade" x="{mx}" y="{y + 9}" fill="{TEXT}" font-size="12" style="animation-delay:{3.3 + k * .15:.2f}s">{lab}</text>')
        b.append(f'<rect x="{mx + 64}" y="{y}" width="150" height="10" rx="2" fill="#0f1c24"/>')
        b.append(
            f'<rect class="bar" x="{mx + 64}" y="{y}" width="150" height="10" rx="2" fill="{GREEN if k != 1 else CYAN}" '
            f'style="transform-origin:{mx + 64}px {y}px;animation-delay:-{k * 0.9:.1f}s"/>'
        )

    b.append(f'<rect class="scan" x="0" y="0" width="{W}" height="120" fill="url(#scanG)"/>')
    # CRT lines
    b.append('<g opacity=".06">' + "".join(f'<rect x="0" y="{yy}" width="{W}" height="1" fill="#fff"/>' for yy in range(0, H, 4)) + "</g>")
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/></g>')
    return svg(W, H, "\n".join(b), css, f"{name}: {DATA['role']}. Boot log shows SETTLE and ZecOne live.")


# ---------------------------------------------------------------- build cards
def card(p: dict, idx: int) -> str:
    W, H = 590, 236
    col = STATUS.get(p["status"], CYAN)
    css = f"""
.led{{animation:led 1.6s ease-in-out infinite}}
@keyframes led{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.sweep{{animation:sweep 5s linear infinite;animation-delay:-{idx * 0.6:.1f}s}}
@keyframes sweep{{from{{transform:translateX(-260px)}}to{{transform:translateX({W + 40}px)}}}}
.corner{{animation:cn 3s ease-in-out infinite}}
@keyframes cn{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
"""
    b = [
        f'<defs><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
        f'{grid_defs("cg", 24)}<clipPath id="cc"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
        f'<g clip-path="url(#cc)"><rect width="{W}" height="{H}" fill="{PANEL}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#cg)" opacity=".5"/>',
        f'<rect class="sweep" x="0" y="0" width="220" height="2" fill="url(#sw)"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{LINE}"/>',
    ]
    # corner brackets
    for cx, cy, dx, dy in ((10, 10, 1, 1), (W - 10, 10, -1, 1), (10, H - 10, 1, -1), (W - 10, H - 10, -1, -1)):
        b.append(
            f'<path class="corner" d="M{cx} {cy + 14 * dy} V{cy} H{cx + 14 * dx}" fill="none" stroke="{col}" stroke-width="2"/>'
        )
    b.append(f'<text x="30" y="44" fill="{DIM}" font-size="12" letter-spacing="2">{idx + 1:02d} // {x(p["kind"].upper())}</text>')
    # status pill
    sw = 22 + len(p["status"]) * 9
    b.append(f'<rect x="{W - 30 - sw - 14}" y="27" width="{sw + 14}" height="24" rx="12" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".5"/>')
    b.append(f'<circle class="led" cx="{W - 30 - sw + 2}" cy="39" r="4" fill="{col}"/>')
    b.append(f'<text x="{W - 36}" y="44" text-anchor="end" fill="{col}" font-size="12" font-weight="700">{x(p["status"])}</text>')
    b.append(f'<text x="28" y="86" fill="{TEXT}" font-size="30" font-weight="800">{x(p["name"])}</text>')
    for k, ln in enumerate(textwrap.wrap(p["desc"], 62)[:3]):
        b.append(f'<text x="30" y="{118 + k * 20}" fill="#9fb3c1" font-size="13.5">{x(ln)}</text>')
    cx = 30
    for t in p["stack"]:
        w = 18 + len(t) * 7.6
        b.append(f'<rect x="{cx}" y="182" width="{w:.0f}" height="24" rx="5" fill="#0f1c24" stroke="{LINE}"/>')
        b.append(f'<text x="{cx + w / 2:.0f}" y="198" text-anchor="middle" fill="{CYAN}" font-size="12">{x(t)}</text>')
        cx += w + 8
    foot = ("↗ " + p["url"].split("//")[1]) if p.get("url") else "◆ private build"
    b.append(f'<text x="{W - 30}" y="198" text-anchor="end" fill="{GREEN if p.get("url") else DIM}" font-size="12">{x(foot)}</text>')
    b.append("</g>")
    alt = f"{p['name']} ({p['status']}): {p['desc']} Stack: {', '.join(p['stack'])}."
    return svg(W, H, "\n".join(b), css, alt)


# ---------------------------------------------------------------- section header
def header(slug: str, label: str, sub: str) -> str:
    W, H = 1200, 64
    css = f"""
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.run{{stroke-dasharray:6 10;animation:run 1.8s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-32}}}}
"""
    lw = 70 + len(label) * 15
    b = [
        f'<text x="4" y="40" font-size="24" font-weight="800"><tspan fill="{GREEN}">~/</tspan><tspan fill="{TEXT}">{x(label)}</tspan></text>',
        f'<rect class="cur" x="{lw - 18}" y="20" width="12" height="24" fill="{GREEN}"/>',
        f'<line class="run" x1="{lw + 10}" y1="32" x2="{W - 280}" y2="32" stroke="{LINE}" stroke-width="2"/>',
        f'<text x="{W - 4}" y="38" text-anchor="end" fill="{DIM}" font-size="13">{x(sub)}</text>',
    ]
    return svg(W, H, "\n".join(b), css, f"{label}: {sub}")


# ---------------------------------------------------------------- stack marquee
def stack() -> str:
    W, H = 1200, 76
    items = DATA["stack"]
    css = """
.mq{animation:mq 26s linear infinite}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
"""
    chips, cx = [], 0
    for _ in range(2):
        for k, t in enumerate(items):
            w = 34 + len(t) * 10
            col = GREEN if k % 2 == 0 else CYAN
            chips.append(
                f'<rect x="{cx}" y="16" width="{w}" height="40" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                f'<circle cx="{cx + 16}" cy="36" r="3.5" fill="{col}"/>'
                f'<text x="{cx + 28}" y="41" fill="{TEXT}" font-size="15">{x(t)}</text>'
            )
            cx += w + 12
    total = cx
    css = css.replace("-50%", f"-{total // 2}px")
    b = [
        f'<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".06" stop-color="{BG}" stop-opacity="0"/>'
        f'<stop offset=".94" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
        f'<g clip-path="url(#sc)"><rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<g class="mq">{"".join(chips)}</g>',
        f'<rect width="{W}" height="{H}" fill="url(#fade)"/></g>',
    ]
    return svg(W, H, "\n".join(b), css, "Stack: " + ", ".join(items))


# ---------------------------------------------------------------- footer
def footer() -> str:
    W, H = 1200, 120
    cmd = "connect --portfolio --x --github"
    css = f"""
.ty{{animation:ty 2.4s steps({len(cmd)}) .4s both}}
@keyframes ty{{from{{width:0}}to{{width:{len(cmd) * 9.6 + 4:.0f}px}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.res{{opacity:0;animation:in .4s ease-out 3s forwards}}
@keyframes in{{to{{opacity:1}}}}
"""
    b = [
        f'<defs><clipPath id="tc"><rect class="ty" x="200" y="20" width="0" height="34"/></clipPath></defs>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>',
        f'<text x="28" y="44" font-size="16"><tspan fill="{GREEN}">folarihn@build</tspan><tspan fill="{DIM}">:~$ </tspan></text>',
        f'<text x="200" y="44" fill="{TEXT}" font-size="16" clip-path="url(#tc)">{x(cmd)}</text>',
        f'<rect class="cur" x="{200 + len(cmd) * 9.6 + 8:.0f}" y="30" width="10" height="18" fill="{GREEN}"/>',
        f'<text class="res" x="28" y="86" font-size="15"><tspan fill="{GREEN}">✓ </tspan><tspan fill="{TEXT}">3 channels open </tspan>'
        f'<tspan fill="{DIM}">— links below. open to collabs, audits and agent builds.</tspan></text>',
    ]
    return svg(W, H, "\n".join(b), css, "Terminal: connect with Folarihn. Links follow.")


# ---------------------------------------------------------------- README
def readme(builds: list[dict]) -> str:
    L = DATA["links"]
    rows = []
    for i in range(0, len(builds), 2):
        cells = []
        for p in builds[i : i + 2]:
            img = f'<img src="assets/build-{p["id"]}.svg" width="100%" alt="{x(p["name"])}: {x(p["desc"])}">'
            href = p.get("url") or p.get("repo")
            cells.append(f'    <td width="50%">{f"<a href={chr(34)}{href}{chr(34)}>{img}</a>" if href else img}</td>')
        rows.append("  <tr>\n" + "\n".join(cells) + "\n  </tr>")
    more = "\n".join(f"- {m}" for m in DATA["more"])
    links = " ".join(
        [
            f'<a href="{L["portfolio"]}"><img src="https://img.shields.io/badge/portfolio-folarihnport-3dff9a?style=for-the-badge&labelColor=05080b" alt="Portfolio"></a>',
            f'<a href="{L["x"]}"><img src="https://img.shields.io/badge/X-@folarihn-22d3ee?style=for-the-badge&labelColor=05080b" alt="X @folarihn"></a>',
        ]
    )
    return f"""<!-- Generated by scripts/build.py from profile.json. Edit those, not this file. -->
<a href="{L["portfolio"]}"><img src="assets/hero.svg" width="100%" alt="FOLARIHN — {x(DATA["role"])}"></a>

<p align="center"><b>{x(DATA["tagline"])}</b><br>
<sub>Agents · guardrails · escrow · private payments · on-chain intelligence — shipped from {x(DATA["location"])}</sub></p>

<p align="center">{links}</p>

<img src="assets/h-builds.svg" width="100%" alt="Builds">

<table>
{chr(10).join(rows)}
</table>

<details>
<summary><b>More builds</b></summary>

{more}

</details>

<img src="assets/h-stack.svg" width="100%" alt="Stack">
<img src="assets/stack.svg" width="100%" alt="Stack: {x(", ".join(DATA["stack"]))}">

<img src="assets/h-activity.svg" width="100%" alt="Activity">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/folarihn/folarihn/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/folarihn/folarihn/output/snake.svg">
  <img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/folarihn/folarihn/output/snake-dark.svg" width="100%">
</picture>

<a href="{L["portfolio"]}"><img src="assets/footer.svg" width="100%" alt="Connect with Folarihn"></a>

<p align="center"><a href="{L["portfolio"]}">portfolio</a> · <a href="{L["x"]}">x.com/folarihn</a> · <a href="https://settlenear.xyz">settlenear.xyz</a> · <a href="https://zecone.xyz">zecone.xyz</a></p>
"""


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    out = {
        "hero.svg": hero(),
        "stack.svg": stack(),
        "footer.svg": footer(),
        "h-builds.svg": header("builds", "builds", f"{len(DATA['builds'])} systems · live + private"),
        "h-stack.svg": header("stack", "stack", "what I ship with"),
        "h-activity.svg": header("activity", "activity", "commits, eaten daily"),
    }
    for i, p in enumerate(DATA["builds"]):
        out[f"build-{p['id']}.svg"] = card(p, i)
    for name, body in out.items():
        (ASSETS / name).write_text(body, encoding="utf-8", newline="\n")
    (ROOT / "README.md").write_text(readme(DATA["builds"]), encoding="utf-8", newline="\n")
    print(f"wrote {len(out)} svgs + README.md")


if __name__ == "__main__":
    main()
