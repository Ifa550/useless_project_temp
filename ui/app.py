"""Main Application Coordinator for ICECREAM OS."""
import tkinter as tk
from tkinter import messagebox
from typing import Optional
from ui.theme import Theme
from ui.input_view import InputView
from ui.analysis_view import AnalysisView
from ui.result_view import ResultView
from ui.history_view import HistoryView
from engine.models import UserInput, AnalysisResult
from engine.pipeline import run_icne_analysis
from storage.history import HistoryManager


class IceCreamOSApp:
    """Main application manager handling view transitions, state, and clipboard interactions."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ICECREAM OS — Intelligent Cream Recommendation & Quantity Engine")
        self.root.geometry("1060x780")
        self.root.minsize(920, 660)
        self.root.configure(bg=Theme.BG_DARK)

        # Center window on screen
        self._center_window(1060, 780)

        # Application state
        self.history_mgr = HistoryManager()
        self.last_input: Optional[UserInput] = None
        self.last_result: Optional[AnalysisResult] = None

        # Container for swappable views
        self.container = tk.Frame(self.root, bg=Theme.BG_DARK)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize Views
        self.input_view = InputView(self.container, on_analyze=self.handle_start_analysis)
        self.analysis_view = AnalysisView(self.container, on_complete=self.handle_analysis_complete)
        self.result_view = ResultView(
            self.container,
            on_recalculate=self.handle_recalculate,
            on_edit_inputs=self.handle_edit_inputs,
            on_view_history=self.handle_view_history,
            on_copy_report=self.copy_to_clipboard,
        )
        self.history_view = HistoryView(
            self.container,
            history_mgr=self.history_mgr,
            on_back=self.handle_back_from_history,
            on_view_result=self.handle_view_historical_result,
        )

        for v in (self.input_view, self.analysis_view, self.result_view, self.history_view):
            v.grid(row=0, column=0, sticky="nsew")

        # Start on Input View
        self.show_view(self.input_view)

    def _center_window(self, width: int, height: int):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, int((sw - width) / 2))
        y = max(0, int((sh - height) / 2) - 20)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_view(self, view: tk.Frame):
        """Raises a view to the top."""
        view.tkraise()

    def handle_start_analysis(self, inp: UserInput):
        """Processes user biometrics, triggers diagnostic animation, then presents results."""
        try:
            self.last_input = inp
            result = run_icne_analysis(inp)
            self.last_result = result
            self.history_mgr.add_record(result, inp)

            # Switch to loading/analysis view
            self.show_view(self.analysis_view)
            self.analysis_view.start_analysis(result)
        except Exception as ex:
            messagebox.showerror("Sensor Computation Fault", f"An unexpected computational error occurred:\n{ex}")

    def handle_analysis_complete(self, result: AnalysisResult):
        """Invoked when the simulated scanning sequence completes."""
        self.result_view.display_result(result)
        self.show_view(self.result_view)

    def handle_recalculate(self):
        """Recalculates the recommendation based on the most recent inputs."""
        if self.last_input:
            self.handle_start_analysis(self.last_input)
        else:
            self.show_view(self.input_view)

    def handle_edit_inputs(self):
        """Returns to the input cockpit."""
        self.show_view(self.input_view)

    def handle_view_history(self):
        """Opens the telemetry history log."""
        self.history_view.refresh_data()
        self.show_view(self.history_view)

    def handle_back_from_history(self):
        """Returns to the result view if available, otherwise input view."""
        if self.last_result:
            self.show_view(self.result_view)
        else:
            self.show_view(self.input_view)

    def handle_view_historical_result(self, result: AnalysisResult):
        """Inspects a historical analysis result."""
        self.last_result = result
        self.result_view.display_result(result)
        self.show_view(self.result_view)

    def copy_to_clipboard(self, text: str):
        """Safely writes text to the operating system clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()  # Required on Windows to ensure clipboard persists
        except Exception as ex:
            messagebox.showwarning("Clipboard Warning", f"Could not access OS clipboard:\n{ex}")
