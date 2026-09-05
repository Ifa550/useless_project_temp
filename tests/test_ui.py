"""Automated UI integration test verifying that all views, buttons, transitions,
and clipboard functions execute without error.
"""
import unittest
import sys
import os
import tkinter as tk

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.app import IceCreamOSApp
from engine.models import UserInput, Mood, TimeOfDay, Weather, FlavorPreference


class TestUIIntegration(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during test
        self.app = IceCreamOSApp(self.root)

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_app_initialization(self):
        """Verify all widgets and views initialize cleanly."""
        self.assertIsNotNone(self.app.input_view)
        self.assertIsNotNone(self.app.analysis_view)
        self.assertIsNotNone(self.app.result_view)
        self.assertIsNotNone(self.app.history_view)

    def test_full_analysis_workflow(self):
        """Simulate user input submission, result display, and history logging."""
        inp = UserInput(
            mood=Mood.STRESSED.value,
            temperature_c=32.0,
            stress_level=85,
            energy_level=35,
            study_hours=7.0,
            sleep_hours=4.5,
            time_of_day=TimeOfDay.NIGHT.value,
            weather=Weather.VERY_HOT.value,
            preference=FlavorPreference.CHOCOLATE.value,
            notes="Testing UI flow",
        )

        # Trigger analysis
        self.app.handle_start_analysis(inp)
        self.assertIsNotNone(self.app.last_result)
        self.assertEqual(self.app.history_mgr.count(), 1)

        # Fast-forward / complete analysis directly
        self.app.handle_analysis_complete(self.app.last_result)
        self.root.update_idletasks()

        # Check result view display
        self.assertIn("CRITICAL", self.app.result_view.status_label.cget("text"))
        self.assertIn("CHOCOLATE", self.app.result_view.fl_name_lbl.cget("text"))

        # Test recalculation
        self.app.handle_recalculate()
        self.assertEqual(self.app.history_mgr.count(), 2)

        # Test History View
        self.app.handle_view_history()
        self.root.update_idletasks()
        self.assertEqual(len(self.app.history_view.tree.get_children()), 2)

        # Test Clear History
        self.app.history_view._clear_history()
        self.assertEqual(len(self.app.history_view.tree.get_children()), 0)
        self.assertEqual(self.app.history_mgr.count(), 0)

        # Test Edit Inputs Navigation
        self.app.handle_edit_inputs()
        self.root.update_idletasks()

    def test_clipboard_copy(self):
        """Verify report copying to clipboard."""
        test_text = "ICECREAM OS TELEMETRY TEST STRING"
        self.app.copy_to_clipboard(test_text)
        clip_content = self.root.clipboard_get()
        self.assertEqual(clip_content, test_text)


if __name__ == "__main__":
    unittest.main()
