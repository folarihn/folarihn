"""Fetch only public GitHub resources. No private repo or contribution queries."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def api(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "folarihn-profile-stats",
               "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urlopen(Request("https://api.github.com/" + path, headers=headers), timeout=25) as response:
            return json.load(response), response.headers.get("Link", "")
    except HTTPError as exc:
        raise RuntimeError(f"Public GitHub API failed (HTTP {exc.code}); old assets retained.") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Public GitHub API unavailable; old assets retained.") from None


def build_snapshot(profile, repos, events, today: date):
    # Strict positive checks: never treat missing privacy flags as public.
    public = [r for r in repos if r.get("private") is False
              and r.get("owner", {}).get("login", "").lower() == "folarihn"]
    names = {r["full_name"] for r in public}
    start = today - timedelta(days=83)
    counts = Counter()
    for e in events:
        if e.get("public") is not True or e.get("repo", {}).get("name") not in names:
            continue
        try:
            day = date.fromisoformat(e["created_at"][:10])
        except (KeyError, TypeError, ValueError):
            continue
        if start <= day <= today:
            counts[day.isoformat()] += 1
    return {
        "schema_version": 1,
        "owner": "folarihn",
        "public_repositories": len(public),
        "public_stars": sum(int(r.get("stargazers_count", 0)) for r in public),
        "observed_public_events": sum(counts.values()),
        "window_start": start.isoformat(), "window_end": today.isoformat(),
        "daily_public_events": dict(sorted(counts.items())),
        "public_repo_names": sorted(names),
        "note": "Public events observed in the REST API window; not total contributions. "
                "API history is limited to at most 300 recent events and up to 90 days.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-only", action="store_true", help="Use the committed public snapshot without network")
    args = parser.parse_args()
    target = ROOT / "assets/generated/public-stats.json"
    if not args.render_only:
        profile, _ = api("users/folarihn")
        if profile.get("login", "").lower() != "folarihn":
            raise RuntimeError("Unexpected public account; old assets retained.")
        repos = []
        page = 1
        while True:
            batch, links = api(f"users/folarihn/repos?type=owner&per_page=100&page={page}")
            repos.extend(batch)
            if 'rel="next"' not in links:
                break
            page += 1
            if page > 20:
                raise RuntimeError("Unexpected pagination; no partial data written.")
        events = []
        for page in range(1, 4):
            batch, links = api(f"users/folarihn/events/public?per_page=100&page={page}")
            events.extend(batch)
            if 'rel="next"' not in links:
                break
        snapshot = build_snapshot(profile, repos, events, datetime.now(timezone.utc).date())
        old = json.loads(target.read_text()) if target.exists() else {}
        comparison = {k: v for k, v in old.items() if k != "updated_at"}
        if comparison != snapshot:
            snapshot["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(".tmp")
            temporary.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
            temporary.replace(target)
    spec = importlib.util.spec_from_file_location("generate_assets", ROOT / "scripts/generate-assets.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.generate_stats()
    # Keep the critical numbers selectable when images fail.
    snapshot = json.loads(target.read_text())
    readme = ROOT / "README.md"
    value = readme.read_text(encoding="utf-8")
    start, end = "<!-- PUBLIC-STATS:START -->", "<!-- PUBLIC-STATS:END -->"
    summary = (f'**{snapshot["public_repositories"]} public repositories** · '
               f'**{snapshot["public_stars"]} public repository stars** · '
               f'**{snapshot["observed_public_events"]} observed public events** in the API window. '
               f'Snapshot: {snapshot["updated_at"]}. Public data only; not total contributions.')
    if value.count(start) != 1 or value.count(end) != 1:
        raise RuntimeError("README statistics markers must occur exactly once.")
    new_value = value.split(start)[0] + start + "\n" + summary + "\n" + end + value.split(end)[1]
    if new_value != value:
        readme.write_text(new_value, encoding="utf-8")
    print("Public-only GitHub statistics rendered; no private data queried.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
