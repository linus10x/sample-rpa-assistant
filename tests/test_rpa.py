import unittest

from rpa.app import AppError, Desk
from rpa.assistant import next_action, run
from rpa.robot import apply_action


class DeskTests(unittest.TestCase):
    def test_notice_blocks_intake_until_dismissed(self):
        desk = Desk()
        with self.assertRaises(AppError):
            desk.click("open_intake")
        desk.click("dismiss_notice")
        desk.click("open_intake")
        self.assertEqual(desk.screen, "intake")

    def test_submit_requires_both_fields(self):
        desk = Desk()
        desk.click("dismiss_notice")
        desk.click("open_intake")
        desk.type("applicant", "Sample Person")
        result = apply_action(desk, {"op": "click", "button": "submit"})
        self.assertFalse(result["ok"])
        self.assertIn("case_id", result["error"])
        self.assertFalse(desk.submitted)


class AssistantTests(unittest.TestCase):
    def test_files_intake_and_clears_the_notice_first(self):
        result = run(Desk(), "file_intake", {"applicant": "Sample Person", "case_id": "C-1001"})
        self.assertTrue(result["submitted"])
        self.assertEqual(
            result["log"],
            ["click dismiss_notice", "click open_intake", "type applicant", "type case_id", "click submit"],
        )

    def test_stops_when_the_packet_is_missing_a_field(self):
        result = run(Desk(), "file_intake", {"applicant": "Sample Person"})
        self.assertFalse(result["submitted"])
        self.assertIn("packet missing case_id", result["transcript"][-1]["error"])

    def test_unknown_goal_stops(self):
        action = next_action("delete_all", Desk().observe(), {})
        self.assertEqual(action["op"], "stop")

    def test_robot_rejects_an_unknown_op(self):
        result = apply_action(Desk(), {"op": "paint"})
        self.assertFalse(result["ok"])
        self.assertIn("unknown op", result["error"])


if __name__ == "__main__":
    unittest.main()
