"""Maintainable GitHub-safe SVG panels and an optimized localized hero animation."""
from __future__ import annotations

import base64
from datetime import date, timedelta
from html import escape
import io
import json
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG, LINE, WHITE, MUTED = "#080b15", "#a659e0", "#f0efff", "#b7b8cd"
GREEN, CYAN = "#64f8a5", "#62e7f0"


def config():
    return json.loads((ROOT / "profile.json").read_text())


def text(x, y, value, size=20, color=WHITE, bold=False):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{700 if bold else 400}">{escape(str(value))}</text>')


def box(x, y, w, h, color=LINE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG}" stroke="{color}"/>'


def svg(name, width, height, title, body):
    value = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
             f'<title>{escape(title)}</title>'
             f'<rect width="100%" height="100%" fill="{BG}"/>'
             '<g font-family="Consolas,DejaVu Sans Mono,monospace">' + body + '</g></svg>\n')
    (ASSETS / name).write_text(value, encoding="utf-8")


def generate_hero():
    source = Image.open(ASSETS / "source/lab-original.png").convert("RGB")
    hero = source.resize((1200, 400), Image.Resampling.NEAREST)
    candidates = [Path("C:/Windows/Fonts/consolab.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")]
    font_path = next((p for p in candidates if p.exists()), None)
    font = lambda size: ImageFont.truetype(str(font_path), size) if font_path else ImageFont.load_default(size=size)
    d = ImageDraw.Draw(hero)
    d.rectangle((19, 18, 239, 128), fill="#070915")
    d.text((28, 24), ">_ FOLARIHN_OS", font=font(18), fill=WHITE)
    d.text((28, 49), "v2.0 / PERSONAL LAB", font=font(12), fill=CYAN)
    for i, label in enumerate(["AI RESEARCH INTERESTS", "AGENT SYSTEMS", "WEB3 EXPERIMENTS"]):
        d.text((28, 72 + 17 * i), "> " + label, font=font(11), fill=WHITE)
    hero.quantize(colors=128).save(ASSETS / "hero-static.png", optimize=True)
    # One fixed palette; animation changes only cursor and a few decorative pixels.
    palette = hero.quantize(colors=128)
    frames = []
    for i in range(16):
        frame = hero.copy()
        draw = ImageDraw.Draw(frame)
        draw.rectangle((219, 115, 225, 120), fill=GREEN if (i // 4) % 2 == 0 else "#070915")
        intensity = [130, 140, 155, 170, 180, 170, 155, 140][i % 8]
        draw.rectangle((793, 267, 798, 268), fill=(25, intensity, 115))
        draw.point((843, 56), fill=(intensity, 95, intensity))
        draw.point((916, 87), fill=(95, intensity, intensity))
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))
    frames[0].save(ASSETS / "hero-animated.gif", save_all=True, append_images=frames[1:],
                   duration=500, loop=0, optimize=True, disposal=1)
    # Original character crop, used as a decorative embedded portrait in a standalone SVG.
    portrait = source.crop((460, 155, 890, 615)).resize((172, 184), Image.Resampling.NEAREST)
    portrait.save(ASSETS / "portrait.png", optimize=True)


def generate_panels():
    p = config()
    encoded = base64.b64encode((ASSETS / "portrait.png").read_bytes()).decode()
    b = box(22, 24, 182, 194)
    b += f'<image x="27" y="29" width="172" height="184" href="data:image/png;base64,{encoded}"/>'
    b += text(228, 65, "FOLARIHN_", 42, WHITE, True)
    b += text(230, 100, "Builder / agent systems / experiments", 18)
    for n, value in enumerate(["Building with AI agents.", "Exploring reliable autonomous systems.", "Learning through implementation", "and honest evaluation."]):
        b += text(230, 140 + n * 23, value, 17, MUTED)
    b += box(677, 25, 500, 192)
    for x, color in [(696, "#ff5c8c"), (716, "#ffc873"), (736, GREEN)]:
        b += f'<circle cx="{x}" cy="44" r="5" fill="{color}"/>'
    b += text(758, 50, "system@folarihn:~$ status", 16, GREEN)
    for n, (k, v) in enumerate([("OS", "FOLARIHN_OS v2.0"), ("Focus", "Agents / tool use"), ("Location", "Earth"), ("Mode", "Building + experimenting")]):
        b += text(701, 87 + n * 31, k + " ....", 17, GREEN)
        b += text(847, 87 + n * 31, v, 17)
    svg("identity-panel.svg", 1200, 240, "Folarihn, builder exploring agents; system status: Earth, building and experimenting", b)
    mobile = text(24, 49, "FOLARIHN_", 37, WHITE, True)
    mobile += text(25, 86, "Builder / agent systems", 22, CYAN)
    mobile += text(25, 121, "Building with AI agents.", 20)
    mobile += text(25, 153, "Exploring reliable systems.", 20, MUTED)
    mobile += box(20, 179, 440, 132)
    mobile += text(37, 211, "system@folarihn:~$ status", 20, GREEN)
    mobile += text(37, 248, "Location: Earth", 21)
    mobile += text(37, 282, "Mode: Building + experimenting", 20)
    svg("identity-mobile.svg", 480, 330, "Folarihn; builder exploring reliable agents, based on Earth", mobile)

    b = text(25, 35, "/projects", 27, WHITE, True)
    b += '<path d="M205 29H780" stroke="#656986"/>'
    for i, project in enumerate(p["projects"]):
        x, y = 24 + (i % 2) * 392, 58 + (i // 2) * 143
        private = "url" not in project
        b += box(x, y, 368, 124, GREEN if private else "#858bff")
        b += text(x + 15, y + 29, project["name"], 19, GREEN if private else WHITE, True)
        for n, line in enumerate(textwrap.wrap(project["description"], 34)):
            b += text(x + 15, y + 54 + 18*n, line, 15, MUTED)
        b += text(x + 15, y + 92, " / ".join(project["tags"]), 14, WHITE)
        b += text(x + 15, y + 112, project["status"], 13, GREEN if private else "#b3b7ff")
    svg("projects-panel.svg", 800, 346, "Four projects: Hermes and Quorum in development; Universal-Agent-Minter and topclaw-agent public source", b)

    b = text(20, 35, "/research-interests", 23, WHITE, True)
    for i, item in enumerate(p["research"]):
        y = 76 + i * 31
        b += f'<rect x="22" y="{y-10}" width="7" height="7" fill="{GREEN}"/>'
        b += text(42, y, item, 16)
    skyline = Image.open(ASSETS / "source/lab-original.png").crop((1250, 15, 2040, 260)).resize((356, 98), Image.Resampling.NEAREST)
    data = io.BytesIO()
    skyline.save(data, format="PNG", optimize=True)
    b += box(20, 230, 360, 102, "#485a96")
    b += f'<image x="22" y="232" width="356" height="98" href="data:image/png;base64,{base64.b64encode(data.getvalue()).decode()}"/>'
    svg("research-panel.svg", 400, 346, "Research interests in reliable agents, tool use, safety and evaluation", b)
    # Nested self-contained SVGs keep the desktop reference composition without HTML tables.
    projects = (ASSETS / "projects-panel.svg").read_text()
    research = (ASSETS / "research-panel.svg").read_text().replace('width="400"', 'x="800" width="400"', 1)
    svg("directory-panel.svg", 1200, 346, "Project directory and research interests; selectable links follow", projects + research)
    mobile = text(24, 40, "/projects", 26, WHITE, True)
    for i, project in enumerate(p["projects"]):
        y = 64 + i * 164
        private = "url" not in project
        mobile += box(20, y, 440, 148, GREEN if private else "#858bff")
        mobile += text(36, y + 31, project["name"], 23, GREEN if private else WHITE, True)
        for n, line in enumerate(textwrap.wrap(project["description"], 34)):
            mobile += text(36, y + 61 + n * 23, line, 19, MUTED)
        mobile += text(36, y + 111, " / ".join(project["tags"]), 16)
        mobile += text(36, y + 135, project["status"], 15, GREEN if private else "#b3b7ff")
    mobile += text(24, 768, "/research-interests", 25, WHITE, True)
    for i, item in enumerate(p["research"]):
        mobile += text(25, 810 + 35 * i, "> " + item, 18, MUTED)
    svg("directory-mobile.svg", 480, 980, "Mobile project directory and research interests; links follow", mobile)
    b = text(25, 33, "/verified-stack", 25, WHITE, True)
    b += box(25, 54, 1150, 62)
    for i, item in enumerate(p["stack"]):
        b += text(45 + i * 163, 93, item, 22, CYAN if i % 2 else WHITE, True)
    b += text(27, 145, "Source evidence: Quorum code + public project manifests. No proficiency rating implied.", 17, MUTED)
    svg("stack-panel.svg", 1200, 166, "Verified source technologies: Python, TypeScript, JavaScript, React, Next.js, Node.js and Docker", b)
    mobile = text(24, 37, "/verified-stack", 26, WHITE, True)
    for i, item in enumerate(p["stack"]):
        mobile += text(28 + (i % 2)*230, 81 + (i//2)*38, item, 23, CYAN if i%2 else WHITE)
    svg("stack-mobile.svg", 480, 224, "Verified technologies; selectable stack follows", mobile)
    b = box(24, 16, 1152, 66)
    b += text(44, 57, "root@folarihn:~$", 22, GREEN, True)
    b += text(273, 57, "connect --all", 22, WHITE)
    b += text(565, 56, "github.com/folarihn", 20)
    b += text(875, 56, "portfolio / online", 20, CYAN)
    svg("footer.svg", 1200, 100, "Connect with Folarihn on GitHub and the portfolio website; links follow in selectable text", b)
    mobile = box(18, 14, 444, 104)
    mobile += text(33, 49, "root@folarihn:~$ connect", 23, GREEN)
    mobile += text(33, 88, "GitHub / portfolio", 23)
    svg("footer-mobile.svg", 480, 132, "Connect with Folarihn; working links follow", mobile)


def generate_stats():
    s = json.loads((ASSETS / "generated/public-stats.json").read_text())
    b = ""
    metrics = [(s["public_repositories"], "Public repositories"),
               (s["observed_public_events"], "Observed public events"),
               (s["public_stars"], "Public repository stars"),
               (sum(p.get("url", "").removeprefix("https://github.com/") in s["public_repo_names"] for p in config()["projects"]), "Linked public projects")]
    for i, (value, label) in enumerate(metrics):
        x = 24 + i * 294
        b += box(x, 12, 270, 88)
        b += text(x + 18, 51, value, 32, WHITE, True)
        b += text(x + 18, 80, label, 16, MUTED)
    svg("generated/github-metrics.svg", 1200, 112, "Public repository, observed event, star and linked-project counts", b)
    mobile = ""
    for i, (value, label) in enumerate(metrics):
        x, y = 16 + (i % 2) * 236, 10 + (i // 2) * 100
        mobile += box(x, y, 220, 88)
        mobile += text(x + 14, y + 35, value, 30, WHITE, True)
        for n, line in enumerate(textwrap.wrap(label, 21)):
            mobile += text(x + 14, y + 58 + n*17, line, 15, MUTED)
    svg("generated/github-metrics-mobile.svg", 480, 214, "Public GitHub metrics", mobile)
    b = text(25, 135, "/github-activity", 25, WHITE, True)
    b += text(25, 162, "Observed PUBLIC events / 84-day view / API-limited", 18, GREEN)
    start = date.fromisoformat(s["window_start"])
    colors = ["#151d2a", "#124e35", "#1b8751", "#2dbd68", "#64f8a5"]
    for i in range(84):
        day = start + timedelta(days=i)
        count = s["daily_public_events"].get(day.isoformat(), 0)
        x, y = 28 + (i // 7) * 39, 182 + (i % 7) * 18
        b += f'<rect x="{x}" y="{y}" width="31" height="13" rx="1" fill="{colors[min(count,4)]}"><title>{day.isoformat()}: {count} observed public events</title></rect>'
    b += text(540, 200, f'{s["window_start"]} to {s["window_end"]}', 19)
    b += text(540, 234, "Not a total contribution graph.", 20, CYAN)
    b += text(540, 267, "No private repository activity queried.", 18, MUTED)
    b += text(540, 300, "Daily refresh after publication.", 18, MUTED)
    b += text(26, 342, 'Snapshot: ' + s.get("updated_at", "unknown") + ' / GitHub REST API', 16, MUTED)
    svg("generated/github-stats.svg", 1200, 260, "Public-only GitHub statistics and observed activity; not total contributions", '<g transform="translate(0,-105)">' + b + '</g>')
    mobile = text(22, 34, "/github-activity", 25, WHITE, True)
    mobile += text(22, 67, "Observed public events / API-limited", 18, GREEN)
    for i in range(84):
        day = start + timedelta(days=i)
        count = s["daily_public_events"].get(day.isoformat(), 0)
        x, y = 23 + (i // 7)*36, 90 + (i % 7)*20
        mobile += f'<rect x="{x}" y="{y}" width="28" height="14" fill="{colors[min(count,4)]}"><title>{day.isoformat()}: {count} events</title></rect>'
    mobile += text(22, 260, s["window_start"] + " to " + s["window_end"], 18)
    mobile += text(22, 293, "Not a total contribution calendar.", 18, CYAN)
    mobile += text(22, 325, "Snapshot: " + s["updated_at"], 15, MUTED)
    svg("generated/github-stats-mobile.svg", 480, 350, "Observed public events; not complete contributions", mobile)


if __name__ == "__main__":
    generate_hero()
    generate_panels()
    if (ASSETS / "generated/public-stats.json").exists():
        generate_stats()
    print("Static assets generated. Hero motion is localized; all critical text also belongs in README.")
