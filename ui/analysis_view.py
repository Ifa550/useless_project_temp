"""Analysis view for ICECREAM OS.
Simulates high-tech diagnostic scanning with humorous telemetry messages and smooth progress animation.
"""
import tkinter as tk
from typing import Callable, List
from ui.theme import Theme
from engine.models import AnalysisResult


class AnalysisView(tk.Frame):
    """High-tech loading screen simulating complex neural calculations."""

    MESSAGES: List[str] = [
        "Calibrating emotional dessert sensors...",
        "Analyzing emotional dessert requirements...",
        "Consulting the Ice Cream Database v4.2...",
        "Measuring scoop aerodynamic compatibility...",
        "Calculating chocolate probability index...",
        "Cross-referencing cortisol levels with sugar crystallization...",
        "Running unnecessary quantum cream calculations...",
        "Consulting highly questionable dessert science...",
        "Synthesizing optimal thermodynamic dosage...",
        "Finalizing ICNE recommendation protocol...",
    ]

    def __init__(self, parent, on_complete: Callable[[AnalysisResult], None]):
        super().__init__(parent, bg=Theme.BG_DARK)
        self.on_complete = on_complete
        self.result: AnalysisResult = None
        self.current_step = 0
        self.progress_val = 0.0

        self._build_ui()

    def _build_ui(self):
        # Center container
        center = tk.Frame(self, bg=Theme.BG_DARK)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Futuristic HUD Header
        tk.Label(
            center,
            text="⚡ ICNE NEURAL CORE // DIAGNOSTIC IN PROGRESS",
            font=Theme.FONT_MONO_MED,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_DARK,
        ).pack(pady=(0, 20))

        # Big Animated Icon
        self.icon_lbl = tk.Label(
            center,
            text="🍦",
            font=("Segoe UI Emoji", 48),
            bg=Theme.BG_DARK,
        )
        self.icon_lbl.pack(pady=(0, 10))

        # Status Message Readout
        self.msg_lbl = tk.Label(
            center,
            text="INITIALIZING QUANTUM DESSERT ALGORITHMS...",
            font=Theme.FONT_TITLE_MED,
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_DARK,
            wraplength=600,
        )
        self.msg_lbl.pack(pady=(0, 24))

        # Progress Bar Canvas
        self.bar_w = 480
        self.bar_h = 16
        self.canvas = tk.Canvas(
            center,
            width=self.bar_w,
            height=self.bar_h,
            bg=Theme.BG_INPUT,
            highlightthickness=1,
            highlightbackground=Theme.BORDER_CYAN,
        )
        self.canvas.pack(pady=(0, 12))

        # Percentage Readout
        self.pct_lbl = tk.Label(
            center,
            text="0%",
            font=Theme.FONT_MONO_LARGE,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_DARK,
        )
        self.pct_lbl.pack(pady=(0, 16))

        # Warning / Satirical notice
        tk.Label(
            center,
            text="[ HIGH-PRECISION SATIRICAL COMPUTATION ACTIVE • PLEASE DO NOT PANIC ]",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_DARK,
        ).pack()

    def start_analysis(self, result: AnalysisResult):
        """Starts the simulated calculation sequence."""
        self.result = result
        self.current_step = 0
        self.progress_val = 0.0
        self._step()

    def _step(self):
        total_steps = len(self.MESSAGES)
        if self.current_step < total_steps:
            msg = self.MESSAGES[self.current_step]
            self.msg_lbl.config(text=msg)

            # Smoothly increment progress
            target_pct = ((self.current_step + 1) / total_steps) * 100.0
            self._animate_progress(target_pct)
            self.current_step += 1
            # Step delay (approx 200-250ms per step, ~2 seconds total)
            self.after(220, self._step)
        else:
            # Done! Transition to result view
            self.after(250, lambda: self.on_complete(self.result))

    def _animate_progress(self, target_pct: float):
        if self.progress_val < target_pct:
            self.progress_val += 3.0
            if self.progress_val > target_pct:
                self.progress_val = target_pct

            # Redraw progress bar
            self.canvas.delete("all")
            fill_w = (self.progress_val / 100.0) * self.bar_w
            if fill_w > 0:
                self.canvas.create_rectangle(
                    0, 0, fill_w, self.bar_h, fill=Theme.CYAN_NEON, outline=""
                )
            self.pct_lbl.config(text=f"{int(round(self.progress_val))}%")

            if self.progress_val < target_pct:
                self.after(16, lambda: self._animate_progress(target_pct))
