import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InterviewHandoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interview = (ROOT / "docs" / "interview.md").read_text(encoding="utf-8")

    def test_sixty_second_pitch_exists(self):
        self.assertIn("## 1. 60-second pitch", self.interview)

    def test_ten_questions_are_present(self):
        count = sum(1 for line in self.interview.splitlines() if line.startswith("### Q") and ". " in line)
        self.assertEqual(count, 10)

    def test_hardest_problem_story_exists(self):
        self.assertIn("300+ short FAQs", self.interview)
        self.assertIn("STAR format", self.interview)

    def test_date_rules_are_deterministic(self):
        self.assertIn("deterministic", self.interview.lower())
        self.assertIn("date-dependent", self.interview)

    def test_form_version_conflict_is_covered(self):
        self.assertIn("Composite Claim Form", self.interview)
        self.assertIn("outdated", self.interview.lower())

    def test_demo_walkthrough_has_seven_steps(self):
        section = self.interview.split("## 4. Demo walkthrough", 1)[1].split("## 5.", 1)[0]
        steps = [line for line in section.splitlines() if line[:1].isdigit() and ". **" in line]
        self.assertEqual(len(steps), 7)

    def test_two_automated_rehearsals_and_manual_demo_limit_are_disclosed(self):
        self.assertIn("Automated API rehearsal 1", self.interview)
        self.assertIn("Automated API rehearsal 2", self.interview)
        self.assertIn("not two human-operated browser demos", self.interview)
        self.assertTrue((ROOT / "scripts" / "rehearse_demo.py").is_file())

    def test_faq_sample_records_import(self):
        namespace = runpy.run_path(str(ROOT / "data" / "sample_records.py"))
        records = namespace["sample_records"]
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)
        for record in records:
            self.assertIn("question", record)
            self.assertIn("answer", record)
            self.assertIn("source_url", record)

    def test_expanded_faq_corpus_has_explicit_provenance(self):
        namespace = runpy.run_path(str(ROOT / "data" / "sample_records.py"))
        records = namespace["sample_records"]
        self.assertEqual(len(records), 320)
        supplied = [r for r in records if r.get("source_type") == "user_supplied_epfo_faq"]
        generated = [r for r in records if r.get("source_type") == "model_generated_from_general_epfo_scheme_knowledge"]
        self.assertEqual(len(supplied), 20)
        self.assertEqual(len(generated), 300)
        self.assertTrue(all(r.get("verification_status") == "draft_requires_official_review" for r in generated))

    def test_readme_and_progress_exist(self):
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "PROGRESS.md").is_file())


if __name__ == "__main__":
    unittest.main()
