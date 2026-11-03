"""Privacy filtering and exact event accounting, independent of the network."""
from datetime import date
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("stats", ROOT / "scripts/update-stats.py")
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)


class PublicStatsTests(unittest.TestCase):
    def repo(self, name="public", private=False):
        return {"private": private, "owner": {"login": "folarihn"},
                "full_name": "folarihn/" + name, "stargazers_count": 2}

    def event(self, repo="public", public=True, timestamp="2026-11-03T00:00:00Z"):
        return {"public": public, "repo": {"name": "folarihn/" + repo}, "created_at": timestamp}

    def build(self, repos, events):
        return stats.build_snapshot({}, repos, events, date(2026, 11, 3))

    def test_private_repo_and_events_are_excluded(self):
        s = self.build([self.repo(), self.repo("private", True)],
                       [self.event(), self.event("private"), self.event(public=False)])
        self.assertEqual(s["public_repo_names"], ["folarihn/public"])
        self.assertEqual(s["public_stars"], 2)
        self.assertEqual(s["observed_public_events"], 1)

    def test_missing_privacy_flag_is_not_public(self):
        r = self.repo()
        del r["private"]
        s = self.build([r], [self.event()])
        self.assertEqual(s["public_repositories"], 0)
        self.assertEqual(s["observed_public_events"], 0)

    def test_out_of_window_and_malformed_events(self):
        s = self.build([self.repo()], [self.event(timestamp="2025-01-01T00:00:00Z"),
                                      self.event(timestamp="invalid"), {}])
        self.assertEqual(s["daily_public_events"], {})

    def test_exact_daily_counts(self):
        s = self.build([self.repo()], [self.event(), self.event(), self.event(timestamp="2026-11-02T00:00:00Z")])
        self.assertEqual(s["daily_public_events"], {"2026-11-02": 1, "2026-11-03": 2})

    def test_unknown_or_other_owner_repo_is_excluded(self):
        r = self.repo()
        r["owner"]["login"] = "another-owner"
        s = self.build([r], [self.event(), self.event("unlisted")])
        self.assertEqual(s["public_repositories"], 0)
        self.assertEqual(s["observed_public_events"], 0)


if __name__ == "__main__":
    unittest.main()
