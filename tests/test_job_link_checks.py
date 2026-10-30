import importlib.util
import pathlib
import unittest

path=pathlib.Path(__file__).resolve().parents[1]/'scripts/check_job_links.py'
spec=importlib.util.spec_from_file_location('links',path)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class LinkChecks(unittest.TestCase):
    def test_network_and_blocking_errors_do_not_hide_jobs(self):
        for code in (403,429,500,503):
            self.assertEqual(mod.classify(code,'https://example.org/job',''),'unknown')
    def test_removed_postings_are_closed(self):
        self.assertEqual(mod.classify(404,'https://example.org/job',''),'closed')
        self.assertEqual(mod.classify(200,'https://job-boards.greenhouse.io/company?error=true',''),'closed')
        self.assertEqual(mod.classify(200,'https://example.org/job','The job you are trying to apply for has been filled'),'closed')
    def test_reachable_is_not_claimed_as_verified(self):
        self.assertEqual(mod.classify(200,'https://example.org/job','Apply today'),'reachable')
    def test_extracts_json_arrays_without_executing_javascript(self):
        data='const x=[{"title":"Admin","company":"X","url":"https://example.org/job"}].filter(x=>true);'
        self.assertEqual(len(mod.extract_jobs(data)),1)
