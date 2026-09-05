"""Input cockpit view for ICECREAM OS.
Collects mood, temperature, stress, energy, duration, sleep, weather, time, and preferences.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ui.theme import Theme
from ui.widgets import HUDCard, CyberSlider, ChipSelector, CyberButton
from engine.models import UserInput, Mood, TimeOfDay, Weather, FlavorPreference


class InputView(tk.Frame):
    """Cockpit input screen where the user enters biometrics and telemetry."""

    def __init__(self, parent, on_analyze: Callable[[UserInput], None]):
        super().__init__(parent, bg=Theme.BG_DARK)
        self.on_analyze = on_analyze
        self._build_ui()

    def _build_ui(self):
        # Top Header Bar
        header = tk.Frame(self, bg=Theme.BG_PANEL, height=72, highlightthickness=1, highlightbackground=Theme.BORDER_CYAN)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        top_inner = tk.Frame(header, bg=Theme.BG_PANEL)
        top_inner.pack(fill="both", expand=True, padx=20, pady=10)

        title_box = tk.Frame(top_inner, bg=Theme.BG_PANEL)
        title_box.pack(side="left")

        title_lbl = tk.Label(
            title_box,
            text="🍦 ICECREAM OS",
            font=Theme.FONT_TITLE_LARGE,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        )
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(
            title_box,
            text=" // INTELLIGENT CREAM RECOMMENDATION & QUANTITY ENGINE",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.TEXT_SECONDARY,
            bg=Theme.BG_PANEL,
        )
        sub_lbl.pack(side="left", padx=8)

        disclaimer_lbl = tk.Label(
            top_inner,
            text="[ ENTERTAINMENT PROTOCOL • NOT MEDICAL SCIENCE ]",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.AMBER_WARN,
            bg=Theme.BG_PANEL,
        )
        disclaimer_lbl.pack(side="right")

        # Scrollable Canvas Container for Cockpit Cards
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

        # 2-Column Grid inside scroll_frame
        grid_container = tk.Frame(self.scroll_frame, bg=Theme.BG_DARK)
        grid_container.pack(fill="both", expand=True, padx=24, pady=16)
        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)

        # ==========================================
        # LEFT COLUMN
        # ==========================================
        left_col = tk.Frame(grid_container, bg=Theme.BG_DARK)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # CARD 1: Emotional & Biometric Telemetry
        card_mood = HUDCard(left_col, title="Affective State & Biometrics", subtitle="SENSOR BANK A-1")
        card_mood.pack(fill="x", pady=(0, 14))

        mood_content = tk.Frame(card_mood, bg=Theme.BG_PANEL, padx=14, pady=12)
        mood_content.pack(fill="x")

        tk.Label(mood_content, text="PRIMARY EMOTIONAL VECTOR (MOOD)", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(0, 6))

        mood_icons = {
            "Happy": "😊", "Sad": "😢", "Stressed": "⚡",
            "Bored": "🥱", "Angry": "😠", "Tired": "😴",
            "Excited": "🎉", "Confused": "🌀", "Normal": "😐"
        }
        self.mood_selector = ChipSelector(
            mood_content,
            options=[m.value for m in Mood],
            default=Mood.NORMAL.value,
            columns=3,
            icons=mood_icons,
        )
        self.mood_selector.pack(fill="x", pady=(0, 14))

        # Stress Slider
        self.stress_slider = CyberSlider(mood_content, label="CORTISOL STRESS LOAD", from_=0, to=100, default=45, unit="%")
        self.stress_slider.pack(fill="x", pady=(0, 12))

        # Energy Slider
        self.energy_slider = CyberSlider(mood_content, label="PHYSICAL ENERGY LEVEL", from_=0, to=100, default=60, unit="%")
        self.energy_slider.pack(fill="x", pady=(0, 4))

        # CARD 2: Cognitive Load & Rest
        card_work = HUDCard(left_col, title="Cognitive Workload & Somnology", subtitle="SENSOR BANK A-2")
        card_work.pack(fill="x", pady=(0, 14))

        work_content = tk.Frame(card_work, bg=Theme.BG_PANEL, padx=14, pady=12)
        work_content.pack(fill="x")

        self.study_slider = CyberSlider(work_content, label="STUDY / WORK HOURS TODAY", from_=0.0, to=16.0, default=4.5, unit=" hrs", is_integer=False)
        self.study_slider.pack(fill="x", pady=(0, 12))

        self.sleep_slider = CyberSlider(work_content, label="REST DURATION LAST NIGHT", from_=0.0, to=14.0, default=7.0, unit=" hrs", is_integer=False)
        self.sleep_slider.pack(fill="x", pady=(0, 4))

        # ==========================================
        # RIGHT COLUMN
        # ==========================================
        right_col = tk.Frame(grid_container, bg=Theme.BG_DARK)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # CARD 3: Atmospheric & Chronological Factors
        card_env = HUDCard(right_col, title="Environmental & Chrono Sensors", subtitle="SENSOR BANK B-1")
        card_env.pack(fill="x", pady=(0, 14))

        env_content = tk.Frame(card_env, bg=Theme.BG_PANEL, padx=14, pady=12)
        env_content.pack(fill="x")

        # Temperature Slider
        self.temp_slider = CyberSlider(env_content, label="AMBIENT TEMPERATURE", from_=-10.0, to=45.0, default=26.0, unit="°C", is_integer=False)
        self.temp_slider.pack(fill="x", pady=(0, 14))

        # Weather selector
        tk.Label(env_content, text="METEOROLOGICAL CONDITIONS", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(0, 6))
        weather_icons = {"Sunny": "☀️", "Cloudy": "☁️", "Rainy": "🌧️", "Very Hot": "🔥", "Cold": "❄️"}
        self.weather_selector = ChipSelector(
            env_content,
            options=[w.value for w in Weather],
            default=Weather.SUNNY.value,
            columns=5,
            icons=weather_icons,
        )
        self.weather_selector.pack(fill="x", pady=(0, 14))

        # Time of Day selector
        tk.Label(env_content, text="CHRONOLOGICAL TIME OF DAY", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(0, 6))
        tod_icons = {"Morning": "🌅", "Afternoon": "☀️", "Evening": "🌆", "Night": "🌙"}
        self.tod_selector = ChipSelector(
            env_content,
            options=[t.value for t in TimeOfDay],
            default=TimeOfDay.AFTERNOON.value,
            columns=4,
            icons=tod_icons,
        )
        self.tod_selector.pack(fill="x", pady=(0, 4))

        # CARD 4: Subject Preference & Mission Notes
        card_pref = HUDCard(right_col, title="Flavor Preference & Mission Log", subtitle="SENSOR BANK B-2")
        card_pref.pack(fill="x", pady=(0, 14))

        pref_content = tk.Frame(card_pref, bg=Theme.BG_PANEL, padx=14, pady=12)
        pref_content.pack(fill="x")

        tk.Label(pref_content, text="EXPLICIT FLAVOR BIAS (OPTIONAL)", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(0, 6))
        flavor_icons = {
            "Chocolate": "🍫", "Vanilla": "🍦", "Strawberry": "🍓",
            "Butterscotch": "🍯", "Mango": "🥭", "Cookies & Cream": "🍪",
            "No Preference": "⚖️"
        }
        self.pref_selector = ChipSelector(
            pref_content,
            options=[f.value for f in FlavorPreference],
            default=FlavorPreference.NO_PREFERENCE.value,
            columns=4,
            icons=flavor_icons,
        )
        self.pref_selector.pack(fill="x", pady=(0, 12))

        # Notes Box
        tk.Label(pref_content, text="QUALITATIVE TELEMETRY (ANYTHING ELSE?)", font=Theme.FONT_MONO_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(0, 6))
        self.notes_entry = tk.Text(
            pref_content,
            height=3,
            bg=Theme.BG_INPUT,
            fg=Theme.TEXT_PRIMARY,
            insertbackground=Theme.CYAN_NEON,
            relief="flat",
            bd=0,
            padx=8,
            pady=6,
            font=Theme.FONT_MONO_BODY,
        )
        self.notes_entry.pack(fill="x", pady=(0, 4))

        # ==========================================
        # BOTTOM ACTION BAR
        # ==========================================
        action_bar = tk.Frame(self.scroll_frame, bg=Theme.BG_DARK, pady=12)
        action_bar.pack(fill="x", padx=24)

        analyze_btn = CyberButton(
            action_bar,
            text="INITIALIZE ICNE ANALYSIS PROTOCOL",
            icon="🚀",
            command=self._on_submit,
            color=Theme.CYAN_NEON,
            bg_color=Theme.BG_PANEL_ALT,
            width=360,
            height=46,
            font=Theme.FONT_TITLE_MED,
        )
        analyze_btn.pack(side="top")

        ticker_lbl = tk.Label(
            action_bar,
            text="⚡ ICNE ENGINE ONLINE • QUANTUM CREAM TELEMETRY READY",
            font=Theme.FONT_MONO_SMALL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_DARK,
        )
        ticker_lbl.pack(side="top", pady=(8, 12))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame_id, width=event.width)

    def bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_submit(self):
        # Collect values safely
        notes_text = self.notes_entry.get("1.0", "end-1c").strip()
        inp = UserInput(
            mood=self.mood_selector.get(),
            temperature_c=float(self.temp_slider.get()),
            stress_level=int(round(self.stress_slider.get())),
            energy_level=int(round(self.energy_slider.get())),
            study_hours=float(self.study_slider.get()),
            sleep_hours=float(self.sleep_slider.get()),
            time_of_day=self.tod_selector.get(),
            weather=self.weather_selector.get(),
            preference=self.pref_selector.get(),
            notes=notes_text,
        )
        self.on_analyze(inp)
