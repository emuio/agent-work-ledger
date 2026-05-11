import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectSkillTest(unittest.TestCase):
    def test_project_skill_registry_points_to_valid_skill(self):
        registry_path = ROOT / ".codex" / "project-skills.json"
        self.assertTrue(registry_path.exists(), "missing .codex/project-skills.json")

        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        skills = registry.get("skills", [])
        self.assertTrue(skills, "registry should declare at least one project skill")

        declared = {item["name"]: item for item in skills}
        self.assertIn("agent-work-ledger", declared)

        skill_path = ROOT / declared["agent-work-ledger"]["path"] / "SKILL.md"
        self.assertTrue(skill_path.exists(), "registered skill must contain SKILL.md")

        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertIn("name: agent-work-ledger", skill_text)
        self.assertIn("description:", skill_text)
        self.assertIn("events.jsonl", skill_text)
        self.assertIn("human_checkpoint", skill_text)
        self.assertIn("default Agent GTD operating loop", skill_text)
        self.assertIn(".agent-work-ledger/events.jsonl", skill_text)
        self.assertIn("simple question", skill_text)

    def test_example_org_projection_is_stable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "agent-agenda.org"
            subprocess.check_call(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render-org-agenda.py"),
                    str(ROOT / "examples" / "events.example.jsonl"),
                    str(output_path),
                ],
                cwd=str(ROOT),
            )

            expected = (ROOT / "examples" / "org-mode" / "agent-agenda.example.org").read_text(encoding="utf-8")
            actual = output_path.read_text(encoding="utf-8")
            self.assertEqual(expected, actual)

    def test_dogfood_skill_smoke_task_projects_to_review(self):
        events_path = ROOT / "examples" / "dogfood" / "skill-smoke.events.jsonl"
        self.assertTrue(events_path.exists(), "missing dogfood smoke event log")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "skill-smoke.org"
            subprocess.check_call(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render-org-agenda.py"),
                    str(events_path),
                    str(output_path),
                ],
                cwd=str(ROOT),
            )

            org_text = output_path.read_text(encoding="utf-8")
            self.assertIn("* REVIEW [#B] Agent: Test project-local Agent Work Ledger skill", org_text)
            self.assertIn(":TASK_ID: awl-skill-smoke-001", org_text)
            self.assertIn(":NEXT_ACTION: Decide whether to promote the project-local skill to global installation.", org_text)
            self.assertIn("[[file:skills/agent-work-ledger/SKILL.md][Project-local Agent Work Ledger skill]]", org_text)
            self.assertIn("[open]", org_text)

    def test_task_done_clears_next_action_projection(self):
        events = "\n".join(
            [
                '{"ts":"2026-05-12T10:00:00+08:00","task_id":"done-001","event":"task_created","title":"Finish a small fix","outcome":"Fix verified."}',
                '{"ts":"2026-05-12T10:01:00+08:00","task_id":"done-001","event":"next_action_set","next_action":"Run the final verification command."}',
                '{"ts":"2026-05-12T10:02:00+08:00","task_id":"done-001","event":"task_done","message":"Verification passed."}',
            ]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            events_path = Path(tmpdir) / "events.jsonl"
            output_path = Path(tmpdir) / "done.org"
            events_path.write_text(events + "\n", encoding="utf-8")

            subprocess.check_call(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render-org-agenda.py"),
                    str(events_path),
                    str(output_path),
                ],
                cwd=str(ROOT),
            )

            org_text = output_path.read_text(encoding="utf-8")
            self.assertIn("* DONE [#B] Agent: Finish a small fix", org_text)
            self.assertIn(":NEXT_ACTION:", org_text)
            self.assertNotIn(":NEXT_ACTION: Run the final verification command.", org_text)
            self.assertIn("No further action; task is DONE.", org_text)

    def test_runtime_ledger_directory_is_gitignored(self):
        gitignore_text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".agent-work-ledger/", gitignore_text)


if __name__ == "__main__":
    unittest.main()
