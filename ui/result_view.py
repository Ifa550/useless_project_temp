"""Result dashboard view for ICECREAM OS.
Presents the Ice Cream Necessity Score, flavor recommendations, quantity dosage, toppings,
and interactive pseudo-scientific 'Why?' analysis modal.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ui.theme import Theme
from ui.widgets import HUDCard, CircularScoreGauge, CyberButton
from engine.models import AnalysisResult, UserInput
from engine.explanation import ExplanationEngine


class ResultView(tk.Frame):
    """Futuristic Mission Control Dashboard displaying all calculated recommendations."""

    def __init__(
        self,
        parent,
        on_recalculate: Callable[[], None],
        on_edit_inputs: Callable[[], None],
        on_view_history: Callable[[], None],
        on_copy_report: Callable[[str], None],
    ):
        super().__init__(parent, bg=Theme.BG_DARK)
        self.on_recalculate = on_recalculate
        self.on_edit_inputs = on_edit_inputs
        self.on_view_history = on_view_history
        self.on_copy_report = on_copy_report

        self.current_result: Optional[AnalysisResult] = None
        self._build_ui()

    def _build_ui(self):
        # Top Header Bar
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
            text=" // NEURO-DESSERT TELEMETRY COMPLETE",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PANEL,
        ).pack(side="left", padx=8)

        # Quick Action Buttons in Header
        header_actions = tk.Frame(top_inner, bg=Theme.BG_PANEL)
        header_actions.pack(side="right")

        self.btn_history = CyberButton(
            header_actions,
            text="HISTORY",
            icon="📜",
            width=110,
            height=34,
            command=self.on_view_history,
            color=Theme.BLUE_ELECTRIC,
            font=Theme.FONT_SMALL_BOLD,
        )
        self.btn_history.pack(side="left", padx=4)

        self.btn_edit = CyberButton(
            header_actions,
            text="EDIT INPUTS",
            icon="⬅",
            width=120,
            height=34,
            command=self.on_edit_inputs,
            color=Theme.TEXT_SECONDARY,
            font=Theme.FONT_SMALL_BOLD,
        )
        self.btn_edit.pack(side="left", padx=4)

        # Scrollable Dashboard Area
        self.canvas = tk.Canvas(self, bg=Theme.BG_DARK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=Theme.BG_DARK)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_mousewheel(self)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Dashboard Grid Container
        self.dash_content = tk.Frame(self.scroll_frame, bg=Theme.BG_DARK)
        self.dash_content.pack(fill="both", expand=True, padx=24, pady=16)

        # ====================================================
        # ROW 1: HERO METRIC PANEL (Score Gauge + Status Banner)
        # ====================================================
        self.hero_card = HUDCard(self.dash_content, title="Quantum Ice Cream Necessity Index", subtitle="TELEMETRY CORE")
        self.hero_card.pack(fill="x", pady=(0, 16))

        hero_inner = tk.Frame(self.hero_card, bg=Theme.BG_PANEL, padx=20, pady=16)
        hero_inner.pack(fill="x")

        # Left: Circular Gauge
        gauge_box = tk.Frame(hero_inner, bg=Theme.BG_PANEL)
        gauge_box.pack(side="left", padx=(10, 30))

        self.gauge = CircularScoreGauge(gauge_box, size=180, bg=Theme.BG_PANEL)
        self.gauge.pack()

        # Right: Status Banner & Dramatic Readout
        status_box = tk.Frame(hero_inner, bg=Theme.BG_PANEL)
        status_box.pack(side="left", fill="both", expand=True)

        tk.Label(
            status_box,
            text="OPERATIONAL STATUS",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_PANEL,
        ).pack(anchor="w")

        self.status_label = tk.Label(
            status_box,
            text="ANALYZING...",
            font=Theme.FONT_TITLE_HERO,
            fg=Theme.RED_CRITICAL,
            bg=Theme.BG_PANEL,
            anchor="w",
        )
        self.status_label.pack(anchor="w", pady=(2, 6))

        # Dramatic Message Callout
        self.dramatic_box = tk.Frame(status_box, bg=Theme.BG_INPUT, padx=12, pady=10, highlightthickness=1, highlightbackground=Theme.BORDER_CYAN)
        self.dramatic_box.pack(fill="x", pady=(0, 10))

        self.dramatic_msg_label = tk.Label(
            self.dramatic_box,
            text="",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_INPUT,
            wraplength=620,
            justify="left",
        )
        self.dramatic_msg_label.pack(anchor="w")

        # Telemetry Metadata row (Confidence, Timestamp, Algorithm version)
        meta_row = tk.Frame(status_box, bg=Theme.BG_PANEL)
        meta_row.pack(fill="x")

        self.confidence_lbl = tk.Label(
            meta_row,
            text="CONFIDENCE: 94.5%",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        )
        self.confidence_lbl.pack(side="left", padx=(0, 16))

        self.time_lbl = tk.Label(
            meta_row,
            text="TIME: --",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_PANEL,
        )
        self.time_lbl.pack(side="left")

        # ====================================================
        # ROW 2: 3-COLUMN METRICS (Flavor, Quantity, Topping)
        # ====================================================
        cards_grid = tk.Frame(self.dash_content, bg=Theme.BG_DARK)
        cards_grid.pack(fill="x", pady=(0, 16))
        cards_grid.grid_columnconfigure(0, weight=4)
        cards_grid.grid_columnconfigure(1, weight=3)
        cards_grid.grid_columnconfigure(2, weight=3)

        # 1. FLAVOR CARD
        card_flavor = HUDCard(cards_grid, title="Recommended Flavor", subtitle="PRIMARY PAYLOAD")
        card_flavor.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        fl_inner = tk.Frame(card_flavor, bg=Theme.BG_PANEL, padx=16, pady=14)
        fl_inner.pack(fill="both", expand=True)

        self.fl_name_lbl = tk.Label(
            fl_inner,
            text="🍫 CHOCOLATE",
            font=Theme.FONT_TITLE_LARGE,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        )
        self.fl_name_lbl.pack(anchor="w")

        self.fl_compat_lbl = tk.Label(
            fl_inner,
            text="COMPATIBILITY: 94%",
            font=Theme.FONT_MONO_MED,
            fg=Theme.GREEN_SUCCESS,
            bg=Theme.BG_PANEL,
        )
        self.fl_compat_lbl.pack(anchor="w", pady=(2, 6))

        self.fl_reason_lbl = tk.Label(
            fl_inner,
            text="",
            font=Theme.FONT_BODY,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PANEL,
            wraplength=280,
            justify="left",
        )
        self.fl_reason_lbl.pack(anchor="w", pady=(0, 10))

        # Runner-up alternatives bar
        tk.Label(fl_inner, text="ALTERNATIVE VARIANTS:", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w")
        self.fl_alts_lbl = tk.Label(
            fl_inner,
            text="",
            font=Theme.FONT_SMALL_BOLD,
            fg=Theme.TEXT_CYAN,
            bg=Theme.BG_PANEL,
        )
        self.fl_alts_lbl.pack(anchor="w", pady=(2, 0))

        # 2. QUANTITY & DOSAGE CARD
        card_qty = HUDCard(cards_grid, title="Recommended Quantity", subtitle="DOSAGE SPECS")
        card_qty.grid(row=0, column=1, sticky="nsew", padx=4)

        qty_inner = tk.Frame(card_qty, bg=Theme.BG_PANEL, padx=16, pady=14)
        qty_inner.pack(fill="both", expand=True)

        self.qty_scoops_lbl = tk.Label(
            qty_inner,
            text="2 Scoops",
            font=Theme.FONT_TITLE_LARGE,
            fg=Theme.TEXT_PRIMARY,
            bg=Theme.BG_PANEL,
        )
        self.qty_scoops_lbl.pack(anchor="w")

        self.qty_grams_lbl = tk.Label(
            qty_inner,
            text="~140 g (Serving Estimate)",
            font=Theme.FONT_MONO_MED,
            fg=Theme.AMBER_WARN,
            bg=Theme.BG_PANEL,
        )
        self.qty_grams_lbl.pack(anchor="w", pady=(2, 8))

        tk.Label(qty_inner, text="CONTAINER ARCHITECTURE:", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w")
        self.container_lbl = tk.Label(
            qty_inner,
            text="Insulated Cup",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        )
        self.container_lbl.pack(anchor="w")

        self.container_reason_lbl = tk.Label(
            qty_inner,
            text="",
            font=Theme.FONT_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_PANEL,
            wraplength=220,
            justify="left",
        )
        self.container_reason_lbl.pack(anchor="w", pady=(4, 0))

        # 3. TOPPING CARD
        card_top = HUDCard(cards_grid, title="Topping Detected", subtitle="MOLECULAR SYNERGY")
        card_top.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        top_inner = tk.Frame(card_top, bg=Theme.BG_PANEL, padx=16, pady=14)
        top_inner.pack(fill="both", expand=True)

        self.top_name_lbl = tk.Label(
            top_inner,
            text="🍫 Chocolate Syrup",
            font=Theme.FONT_TITLE_LARGE,
            fg=Theme.PINK_NEON,
            bg=Theme.BG_PANEL,
        )
        self.top_name_lbl.pack(anchor="w")

        self.top_compat_lbl = tk.Label(
            top_inner,
            text="COMPATIBILITY: 91%",
            font=Theme.FONT_MONO_MED,
            fg=Theme.GREEN_SUCCESS,
            bg=Theme.BG_PANEL,
        )
        self.top_compat_lbl.pack(anchor="w", pady=(2, 8))

        self.top_reason_lbl = tk.Label(
            top_inner,
            text="",
            font=Theme.FONT_BODY,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PANEL,
            wraplength=220,
            justify="left",
        )
        self.top_reason_lbl.pack(anchor="w")

        # ====================================================
        # ROW 3: COMMAND ACTION BUTTONS
        # ====================================================
        actions_frame = tk.Frame(self.dash_content, bg=Theme.BG_DARK)
        actions_frame.pack(fill="x", pady=(8, 16))

        # Center cluster of buttons
        btn_cluster = tk.Frame(actions_frame, bg=Theme.BG_DARK)
        btn_cluster.pack(anchor="center")

        self.btn_why = CyberButton(
            btn_cluster,
            text="WHY DO I NEED THIS?",
            icon="🔬",
            width=240,
            height=46,
            command=self._show_why_modal,
            color=Theme.PURPLE_NEON,
            font=Theme.FONT_BODY_BOLD,
        )
        self.btn_why.pack(side="left", padx=8)

        self.btn_recalc = CyberButton(
            btn_cluster,
            text="RECALCULATE DESTINY",
            icon="🔄",
            width=250,
            height=46,
            command=self.on_recalculate,
            color=Theme.CYAN_NEON,
            font=Theme.FONT_BODY_BOLD,
        )
        self.btn_recalc.pack(side="left", padx=8)

        self.btn_copy = CyberButton(
            btn_cluster,
            text="COPY MY ICE CREAM REPORT",
            icon="📋",
            width=260,
            height=46,
            command=self._copy_report,
            color=Theme.GREEN_SUCCESS,
            font=Theme.FONT_BODY_BOLD,
        )
        self.btn_copy.pack(side="left", padx=8)

        # Toast / confirmation banner
        self.toast_lbl = tk.Label(
            actions_frame,
            text="",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.GREEN_SUCCESS,
            bg=Theme.BG_DARK,
        )
        self.toast_lbl.pack(anchor="center", pady=(6, 0))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame_id, width=event.width)

    def bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def display_result(self, res: AnalysisResult):
        """Updates the dashboard with newly calculated analysis data."""
        self.current_result = res

        # Update Gauge & Status
        self.gauge.set_score(res.necessity_score, res.level.label, res.level.color, animate=True)
        self.status_label.config(text=f"STATUS: {res.level.label}", fg=res.level.color)
        self.dramatic_msg_label.config(text=res.dramatic_message)
        self.dramatic_box.config(highlightbackground=res.level.color)

        self.confidence_lbl.config(text=f"ALGORITHMIC CONFIDENCE: {res.confidence}%")
        self.time_lbl.config(text=f"TIMESTAMP: {res.timestamp}")

        # Update Flavor
        fl = res.top_flavor
        self.fl_name_lbl.config(text=f"{fl.emoji} {fl.name.upper()}")
        self.fl_compat_lbl.config(text=f"COMPATIBILITY: {fl.compatibility}%")
        self.fl_reason_lbl.config(text=fl.reason)

        alts_text = " | ".join([f"{a.emoji} {a.name} ({a.compatibility}%)" for a in res.runner_up_flavors])
        self.fl_alts_lbl.config(text=alts_text)

        # Update Quantity
        q = res.quantity
        self.qty_scoops_lbl.config(text=q.scoops_label)
        self.qty_grams_lbl.config(text=f"~{q.grams_estimate} g (Serving Estimate)")
        self.container_lbl.config(text=q.container)
        self.container_reason_lbl.config(text=q.container_rationale)

        # Update Topping
        top = res.topping
        self.top_name_lbl.config(text=f"{top.emoji} {top.name}")
        self.top_compat_lbl.config(text=f"COMPATIBILITY: {top.compatibility}%")
        self.top_reason_lbl.config(text=top.reason)

        # Reset toast
        self.toast_lbl.config(text="")

    def _copy_report(self):
        if not self.current_result:
            return
        report = ExplanationEngine.generate_clipboard_report(
            self.current_result, self.current_result.input_snapshot
        )
        self.on_copy_report(report)
        self.toast_lbl.config(text="✓ REPORT COPIED TO CLIPBOARD! READY TO TRANSMIT.", fg=Theme.GREEN_SUCCESS)
        self.after(3500, lambda: self.toast_lbl.config(text=""))

    def _show_why_modal(self):
        """Displays the 'Why Do I Need This?' interactive pseudo-scientific telemetry modal."""
        if not self.current_result:
            return

        modal = tk.Toplevel(self)
        modal.title("ICECREAM OS // DIAGNOSTIC TELEMETRY BREAKDOWN")
        modal.geometry("720x540")
        modal.configure(bg=Theme.BG_DARK)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        # Modal Header
        hdr = tk.Frame(modal, bg=Theme.BG_PANEL, height=54, highlightthickness=1, highlightbackground=Theme.BORDER_CYAN)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="🔬 WHY DO I NEED THIS? // ICNE DIAGNOSTIC BREAKDOWN",
            font=Theme.FONT_TITLE_MED,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        ).pack(side="left", padx=16, pady=12)

        # Content Area with Text Readout
        text_frame = tk.Frame(modal, bg=Theme.BG_DARK, padx=16, pady=14)
        text_frame.pack(fill="both", expand=True)

        txt = tk.Text(
            text_frame,
            bg=Theme.BG_PANEL,
            fg=Theme.TEXT_PRIMARY,
            insertbackground=Theme.CYAN_NEON,
            relief="flat",
            bd=0,
            padx=16,
            pady=16,
            font=Theme.FONT_MONO_BODY,
            wrap="word",
        )
        scroll = tk.Scrollbar(text_frame, command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        txt.insert("1.0", self.current_result.scientific_explanation)
        txt.configure(state="disabled")

        # Modal Footer
        ftr = tk.Frame(modal, bg=Theme.BG_PANEL, height=50)
        ftr.pack(fill="x")
        ftr.pack_propagate(False)

        close_btn = CyberButton(
            ftr,
            text="ACKNOWLEDGE TELEMETRY",
            icon="✓",
            width=220,
            height=36,
            command=modal.destroy,
            color=Theme.CYAN_NEON,
            font=Theme.FONT_BODY_BOLD,
        )
        close_btn.pack(side="right", padx=16, pady=7)
