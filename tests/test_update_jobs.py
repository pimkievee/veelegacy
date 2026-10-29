"""Offline tests for the job importer; no employer API calls required."""
import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "update_jobs.py"
spec = importlib.util.spec_from_file_location("career_jobs", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ImportTests(unittest.TestCase):
    def test_greenhouse_normalization(self):
        source = {"id":"example", "company":"Example", "region":"Canada"}
        raw = {"id":42,"title":"Personal Support Worker","absolute_url":"https://example.org/job/42","location":{"name":"Toronto, ON"}}
        job = mod.normalize(raw, source)
        self.assertEqual(job["category"], "Healthcare")
        self.assertEqual(job["eligibility"], "unknown")
        self.assertEqual(job["location"], "Toronto, ON")

    def test_lever_normalization(self):
        source = {"id":"example", "company":"Example"}
        raw = {"id":"a","text":"Social Worker","hostedUrl":"https://example.org/jobs/a","categories":{"location":"Ottawa"}}
        job = mod.normalize(raw, source)
        self.assertEqual(job["category"], "Social Services")
        self.assertEqual(job["eligibilityLabel"], "Eligibility not confirmed")

    def test_rejects_non_https_links(self):
        source = {"id":"example", "company":"Example"}
        self.assertIsNone(mod.normalize({"title":"Job","absolute_url":"javascript:alert(1)"}, source))
        self.assertIsNone(mod.normalize({"title":"Job","absolute_url":"https:///bad"}, source))

    def test_no_sources_preserves_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp)
            sources=root/"sources.json"
            output=root/"jobs.json"
            sources.write_text('{"sources":[]}',encoding="utf-8")
            output.write_text('[{"existing":true}]',encoding="utf-8")
            with patch.object(mod,"SOURCES",sources), patch.object(mod,"OUTPUT",output):
                self.assertEqual(mod.main(),0)
            self.assertEqual(output.read_text(encoding="utf-8"),'[{"existing":true}]')

    def test_approved_source_requires_permission_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp)
            sources=root/"sources.json"
            sources.write_text('{"sources":[{"id":"x","company":"X","provider":"greenhouse","board_token":"x","approved_for_republication":true}]}',encoding="utf-8")
            with patch.object(mod,"SOURCES",sources):
                self.assertEqual(mod.main(),1)

if __name__=="__main__":
    unittest.main()
