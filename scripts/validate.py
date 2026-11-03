"""Validate README paths, safe SVGs, assets, snapshots and workflow structure."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(online=False):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    refs = re.findall(r'(?:src|srcset)="([^"]+)"', readme)
    refs += re.findall(r'\]\(([^)]+)\)', readme)
    for ref in refs:
        if ref.startswith("https://"):
            continue
        assert not ref.startswith(("http:", "file:", "javascript:")), "Unsafe README reference"
        assert (ROOT / ref.split("#")[0]).is_file(), f"Missing asset/link: {ref}"
    for image in re.findall(r'<img\s[^>]+>', readme):
        alt = re.search(r'alt="([^"]+)"', image)
        assert alt and len(alt[1]) > 20, "Image needs meaningful alt text"
    for path in (ROOT / "assets").rglob("*.svg"):
        doc = ET.fromstring(path.read_text(encoding="utf-8"))
        assert doc.attrib.get("viewBox") and doc.find("{*}title") is not None
        for node in doc.iter():
            assert node.tag.split("}")[-1] not in {"script", "foreignObject", "animate", "set"}
            for k, value in node.attrib.items():
                assert not k.lower().startswith("on"), "SVG event handler"
                if k.split("}")[-1] == "href":
                    assert value.startswith("data:image/png;base64,"), "SVG external image reference"
    for name in ["hero-static.png", "hero-animated.gif"]:
        image = Image.open(ROOT / "assets" / name)
        assert image.size == (1200, 400)
        assert (ROOT / "assets" / name).stat().st_size < 750_000, "Hero exceeds bandwidth budget"
        if name.endswith("gif"):
            duration = 0
            for i in range(image.n_frames):
                image.seek(i)
                duration += image.info.get("duration", 0)
            assert 6000 <= duration <= 10000
    snapshot = json.loads((ROOT / "assets/generated/public-stats.json").read_text())
    assert snapshot["owner"] == "folarihn"
    assert snapshot["public_repositories"] == len(snapshot["public_repo_names"])
    assert snapshot["observed_public_events"] == sum(snapshot["daily_public_events"].values())
    assert "not total contributions" in readme.lower()
    assert "private" not in snapshot and "token" not in snapshot
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        assert workflow["permissions"]["contents"] == "read"
        assert "jobs" in workflow and "on" in workflow
        for job in workflow["jobs"].values():
            for step in job["steps"]:
                if "uses" in step:
                    assert re.fullmatch(r'[\w-]+/[\w-]+@[a-f0-9]{40}', step["uses"]), "Action must be SHA pinned"
        if path.name == "update-stats.yml":
            assert "pull_request" not in workflow["on"]
            assert workflow["jobs"]["refresh"]["permissions"]["contents"] == "write"
            assert "schedule" in workflow["on"]
    if online:
        for url in ["https://github.com/folarihn", "https://github.com/folarihn/Universal-Agent-Minter",
                    "https://github.com/folarihn/topclaw-agent", "https://folarihnport.vercel.app/"]:
            # No token: a private repository must not pass this check.
            with urlopen(Request(url, headers={"User-Agent": "profile-link-check"}), timeout=25) as response:
                assert response.status == 200, "Public link not available"
    print("PASS: README paths/alt text, standalone SVG safety, hero budgets/loop, public snapshot and pinned workflows" +
          ("; public links returned HTTP 200" if online else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    validate(parser.parse_args().online)
