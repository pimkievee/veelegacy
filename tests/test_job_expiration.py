import datetime as dt
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "update_jobs.py"
spec = importlib.util.spec_from_file_location("career_expiry", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ExpiryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        self.sources = root / "sources.json"
        self.output = root / "jobs.json"
        self.sources.write_text(json.dumps({"sources":[{"id":"x","company":"X","provider":"greenhouse","board_token":"x","permission_reference":"written-approval-reference","approved_for_republication":True}]}))
    def run_import(self, response=None, error=None):
        with patch.object(mod, "SOURCES", self.sources), patch.object(mod, "OUTPUT", self.output):
            with patch.object(mod, "fetch", return_value=response, side_effect=error):
                return mod.main()
    def test_removed_when_absent_from_successful_feed(self):
        self.output.write_text(json.dumps([{"source":"x","url":"https://example.org/old","title":"Old","company":"X","last_seen_at":dt.datetime.now(dt.timezone.utc).isoformat()}]))
        self.assertEqual(self.run_import({"jobs":[]}),0)
        self.assertEqual(json.loads(self.output.read_text()),[])
    def test_failed_feed_keeps_recent_job(self):
        self.output.write_text(json.dumps([{"source":"x","url":"https://example.org/recent","title":"Recent","company":"X","last_seen_at":dt.datetime.now(dt.timezone.utc).isoformat()}]))
        self.assertEqual(self.run_import(error=OSError("offline")),1)
        self.assertEqual(len(json.loads(self.output.read_text())),1)
    def test_failed_feed_removes_old_job(self):
        old=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=4)).isoformat()
        self.output.write_text(json.dumps([{"source":"x","url":"https://example.org/old","title":"Old","company":"X","last_seen_at":old}]))
        self.assertEqual(self.run_import(error=OSError("offline")),1)
        self.assertEqual(json.loads(self.output.read_text()),[])
    def test_expired_at_timestamp(self):
        now=dt.datetime.now(dt.timezone.utc)
        job={"last_seen_at":now.isoformat(),"expires_at":(now-dt.timedelta(minutes=1)).isoformat()}
        self.assertFalse(mod.fresh(job,now))
    def test_unstamped_jobs_are_not_kept(self):
        self.assertFalse(mod.fresh({"url":"https://example.org/job"},dt.datetime.now(dt.timezone.utc)))

if __name__ == "__main__":
    unittest.main()
