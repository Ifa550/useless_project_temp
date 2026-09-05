"""History view for ICECREAM OS.
Displays all previous calculations performed during the session with clear action.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ui.theme import Theme
from ui.widgets import HUDCard, CyberButton
from storage.history import HistoryManager, HistoryRecord
from engine.models import AnalysisResult


class HistoryView(tk.Frame):
    """Session history viewer with formatted table and clear functionality."""

    def __init__(
        self,
        parent,
        history_mgr: HistoryManager,
        on_back: Callable[[], None],
        on_view_result: Callable[[AnalysisResult], None],
    ):
        super().__init__(parent, bg=Theme.BG_DARK)
        self.history_mgr = history_mgr
        self.on_back = on_back
        self.on_view_result = on_view_result
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=Theme.BG_PANEL, height=72, highlightthickness=1, highlightbackground=Theme.BORDER_CYAN)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        top_inner = tk.Frame(header, bg=Theme.BG_PANEL)
        top_inner.pack(fill="both", expand=True, padx=20, pady=10)

        left_title = tk.Frame(top_inner, bg=Theme.BG_PANEL)
        left_title.pack(side="left")

        tk.Label(
            left_title,
            text="🍦 ICECREAM OS",
            font=Theme.FONT_TITLE_LARGE,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        ).pack(side="left")

        tk.Label(
            left_title,
            text=" // SESSION CALCULATION LOGS",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PANEL,
        ).pack(side="left", padx=8)

        # Right Action Buttons in Header
        right_actions = tk.Frame(top_inner, bg=Theme.BG_PANEL)
        right_actions.pack(side="right")

        self.btn_clear = CyberButton(
            right_actions,
            text="CLEAR HISTORY",
            icon="🗑️",
            width=150,
            height=34,
            command=self._clear_history,
            color=Theme.RED_CRITICAL,
            font=Theme.FONT_SMALL_BOLD,
        )
        self.btn_clear.pack(side="left", padx=4)

        self.btn_back = CyberButton(
            right_actions,
            text="BACK TO DASHBOARD",
            icon="⬅",
            width=170,
            height=34,
            command=self.on_back,
            color=Theme.CYAN_NEON,
            font=Theme.FONT_SMALL_BOLD,
        )
        self.btn_back.pack(side="left", padx=4)

        # Main Table Container
        content = tk.Frame(self, bg=Theme.BG_DARK, padx=24, pady=16)
        content.pack(fill="both", expand=True)

        card = HUDCard(content, title="Telemetric Session Archive", subtitle="LOCAL VOLATILE MEMORY")
        card.pack(fill="both", expand=True)

        table_frame = tk.Frame(card, bg=Theme.BG_PANEL, padx=12, pady=12)
        table_frame.pack(fill="both", expand=True)

        # Treeview Styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=Theme.BG_INPUT,
            foreground=Theme.TEXT_PRIMARY,
            rowheight=32,
            fieldbackground=Theme.BG_INPUT,
            font=Theme.FONT_BODY,
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=Theme.BG_PANEL_ALT,
            foreground=Theme.CYAN_NEON,
            font=Theme.FONT_MONO_SMALL,
            relief="flat",
        )
        style.map("Treeview", background=[("selected", Theme.BORDER_CYAN)])

        columns = ("time", "mood", "temp", "score", "level", "flavor", "quantity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("time", text="TIMESTAMP")
        self.tree.heading("mood", text="MOOD")
        self.tree.heading("temp", text="TEMP (°C)")
        self.tree.heading("score", text="SCORE")
        self.tree.heading("level", text="NECESSITY STATUS")
        self.tree.heading("flavor", text="RECOMMENDED FLAVOR")
        self.tree.heading("quantity", text="DOSAGE")

        self.tree.column("time", width=140, anchor="center")
        self.tree.column("mood", width=100, anchor="center")
        self.tree.column("temp", width=90, anchor="center")
        self.tree.column("score", width=70, anchor="center")
        self.tree.column("level", width=220, anchor="w")
        self.tree.column("flavor", width=160, anchor="w")
        self.tree.column("quantity", width=140, anchor="center")

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", self._on_row_double_click)

        # Footer info
        tk.Label(
            table_frame,
            text="Tip: Double-click any row to view full telemetry result for that session entry.",
            font=Theme.FONT_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_PANEL,
        ).pack(side="bottom", anchor="w", pady=(8, 0))

    def refresh_data(self):
        """Reloads records from HistoryManager into Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.history_mgr.get_records()
        for idx, rec in enumerate(records):
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(
                    rec.timestamp,
                    rec.mood,
                    f"{rec.temperature_c:.1f}°C",
                    f"{rec.score}/100",
                    rec.level_label,
                    rec.flavor,
                    rec.quantity,
                ),
            )

    def _clear_history(self):
        self.history_mgr.clear()
        self.refresh_data()

    def _on_row_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        records = self.history_mgr.get_records()
        if 0 <= idx < len(records):
            self.on_view_result(records[idx].result)
