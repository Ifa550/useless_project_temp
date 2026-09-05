"""Custom futuristic HUD widgets for ICECREAM OS built on standard Tkinter."""
import tkinter as tk
from tkinter import ttk
import math
from typing import Callable, List, Optional, Any
from ui.theme import Theme


class CyberButton(tk.Canvas):
    """Futuristic styled button with hover glow and high-tech borders."""

    def __init__(
        self,
        parent,
        text: str,
        command: Optional[Callable] = None,
        color: str = Theme.CYAN_NEON,
        bg_color: str = Theme.BG_PANEL_ALT,
        text_color: str = Theme.TEXT_PRIMARY,
        font=Theme.FONT_BODY_BOLD,
        width: int = 200,
        height: int = 40,
        icon: str = "",
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"] if "bg" in parent.keys() else Theme.BG_DARK,
            highlightthickness=0,
            cursor="hand2",
        )
        self.text = text
        self.command = command
        self.primary_color = color
        self.base_bg = bg_color
        self.text_color = text_color
        self.font = font
        self.w = width
        self.h = height
        self.icon = icon
        self.is_hovered = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.draw()

    def draw(self):
        self.delete("all")
        pad = 2
        bg = self.primary_color if self.is_hovered else self.base_bg
        border_col = self.primary_color if self.is_hovered else Theme.BORDER_CYAN
        txt_col = Theme.BG_DARK if self.is_hovered else self.primary_color

        # High-tech chamfered polygon
        cut = 8
        coords = [
            pad + cut, pad,
            self.w - pad - cut, pad,
            self.w - pad, pad + cut,
            self.w - pad, self.h - pad - cut,
            self.w - pad - cut, self.h - pad,
            pad + cut, self.h - pad,
            pad, self.h - pad - cut,
            pad, pad + cut,
        ]

        self.create_polygon(coords, fill=bg, outline=border_col, width=2)

        # Tech accent corners
        if not self.is_hovered:
            self.create_line(pad + cut, pad, pad, pad + cut, fill=self.primary_color, width=2)
            self.create_line(self.w - pad - cut, self.h - pad, self.w - pad, self.h - pad - cut, fill=self.primary_color, width=2)

        display_text = f"{self.icon} {self.text}".strip()
        self.create_text(
            self.w // 2,
            self.h // 2,
            text=display_text,
            fill=txt_col,
            font=self.font,
        )

    def _on_enter(self, _):
        self.is_hovered = True
        self.draw()

    def _on_leave(self, _):
        self.is_hovered = False
        self.draw()

    def _on_click(self, _):
        if self.command:
            self.command()


class CircularScoreGauge(tk.Canvas):
    """High-tech animated circular arc gauge displaying score (0-100)."""

    def __init__(self, parent, size: int = 180, bg: str = Theme.BG_PANEL):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=bg,
            highlightthickness=0,
        )
        self.size = size
        self.current_score = 0.0
        self.target_score = 0.0
        self.level_label = ""
        self.glow_color = Theme.CYAN_NEON
        self.animating = False
        self.draw_gauge(0)

    def set_score(self, score: int, level_label: str = "", glow_color: str = Theme.CYAN_NEON, animate: bool = True):
        self.target_score = float(score)
        self.level_label = level_label
        self.glow_color = glow_color

        if animate:
            self.current_score = 0.0
            self._animate_tick()
        else:
            self.current_score = self.target_score
            self.draw_gauge(self.current_score)

    def _animate_tick(self):
        diff = self.target_score - self.current_score
        if abs(diff) > 0.5:
            step = max(1.0, diff * 0.18)
            self.current_score += step
            self.draw_gauge(self.current_score)
            self.after(16, self._animate_tick)
        else:
            self.current_score = self.target_score
            self.draw_gauge(self.current_score)

    def draw_gauge(self, score: float):
        self.delete("all")
        cx = self.size / 2
        cy = self.size / 2
        r = (self.size / 2) - 16

        # Draw outer tick marks
        for deg in range(140, 400, 15):
            rad = math.radians(deg)
            x1 = cx + (r + 4) * math.cos(rad)
            y1 = cy + (r + 4) * math.sin(rad)
            x2 = cx + (r + 10) * math.cos(rad)
            y2 = cy + (r + 10) * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill=Theme.BG_INPUT, width=1)

        # Background Track Arc (240 degrees sweep from 150 to 390)
        start_angle = 150
        extent_total = 240
        self.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=start_angle,
            extent=-extent_total,
            style="arc",
            outline=Theme.BG_INPUT,
            width=10,
        )

        # Active Fill Arc
        fraction = max(0.0, min(1.0, score / 100.0))
        active_extent = -(extent_total * fraction)
        if fraction > 0.01:
            self.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start_angle,
                extent=active_extent,
                style="arc",
                outline=self.glow_color,
                width=10,
            )

        # Center Numeric Display
        self.create_text(
            cx,
            cy - 12,
            text=f"{int(round(score))}",
            font=Theme.FONT_MONO_HERO,
            fill=Theme.TEXT_PRIMARY,
        )
        self.create_text(
            cx,
            cy + 18,
            text="/ 100",
            font=Theme.FONT_MONO_SMALL,
            fill=Theme.TEXT_MUTED,
        )
        self.create_text(
            cx,
            cy + 34,
            text="ICNE INDEX",
            font=Theme.FONT_SMALL_BOLD,
            fill=self.glow_color,
        )


class HUDCard(tk.Frame):
    """Futuristic framed card with subtle border and optional header badge."""

    def __init__(self, parent, title: str = "", subtitle: str = "", border_color: str = Theme.BORDER_CYAN, **kwargs):
        super().__init__(parent, bg=Theme.BG_PANEL, highlightthickness=1, highlightbackground=border_color, **kwargs)
        self.title = title
        self.border_color = border_color

        if title:
            header = tk.Frame(self, bg=Theme.BG_PANEL_ALT, height=28)
            header.pack(fill="x", side="top")
            header.pack_propagate(False)

            # Left indicator bar
            indicator = tk.Frame(header, bg=border_color, width=4)
            indicator.pack(side="left", fill="y")

            title_lbl = tk.Label(
                header,
                text=f" // {title.upper()}",
                font=Theme.FONT_MONO_SMALL,
                bg=Theme.BG_PANEL_ALT,
                fg=Theme.TEXT_CYAN,
            )
            title_lbl.pack(side="left", padx=6)

            if subtitle:
                sub_lbl = tk.Label(
                    header,
                    text=subtitle,
                    font=Theme.FONT_SMALL,
                    bg=Theme.BG_PANEL_ALT,
                    fg=Theme.TEXT_MUTED,
                )
                sub_lbl.pack(side="right", padx=8)


class CyberSlider(tk.Frame):
    """Custom slider with live digital readout and sci-fi aesthetic."""

    def __init__(
        self,
        parent,
        label: str,
        from_: float,
        to: float,
        default: float,
        unit: str = "",
        is_integer: bool = True,
        on_change: Optional[Callable[[float], None]] = None,
    ):
        super().__init__(parent, bg=Theme.BG_PANEL)
        self.is_integer = is_integer
        self.unit = unit
        self.on_change = on_change

        # Label Row
        top_row = tk.Frame(self, bg=Theme.BG_PANEL)
        top_row.pack(fill="x", pady=(0, 2))

        lbl = tk.Label(top_row, text=label, font=Theme.FONT_BODY_BOLD, fg=Theme.TEXT_SECONDARY, bg=Theme.BG_PANEL)
        lbl.pack(side="left")

        self.val_var = tk.DoubleVar(value=default)
        self.readout = tk.Label(
            top_row,
            text=self._format_value(default),
            font=Theme.FONT_MONO_MED,
            fg=Theme.CYAN_NEON,
            bg=Theme.BG_PANEL,
        )
        self.readout.pack(side="right")

        # Scale slider
        self.scale = tk.Scale(
            self,
            from_=from_,
            to=to,
            orient="horizontal",
            variable=self.val_var,
            showvalue=0,
            command=self._on_slide,
            bg=Theme.BG_PANEL,
            troughcolor=Theme.BG_INPUT,
            activebackground=Theme.CYAN_NEON,
            highlightthickness=0,
            sliderrelief="flat",
            bd=0,
            resolution=1 if is_integer else 0.5,
        )
        self.scale.pack(fill="x")

    def _format_value(self, val: float) -> str:
        if self.is_integer:
            return f"{int(round(float(val)))}{self.unit}"
        return f"{float(val):.1f}{self.unit}"

    def _on_slide(self, val):
        fval = float(val)
        self.readout.config(text=self._format_value(fval))
        if self.on_change:
            self.on_change(int(round(fval)) if self.is_integer else fval)

    def get(self) -> float:
        return self.val_var.get()

    def set(self, val: float):
        self.val_var.set(val)
        self.readout.config(text=self._format_value(val))


class ChipSelector(tk.Frame):
    """Grid of futuristic selectable chips/buttons with active highlight."""

    def __init__(
        self,
        parent,
        options: List[str],
        default: str,
        columns: int = 3,
        icons: Optional[dict] = None,
        on_select: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(parent, bg=Theme.BG_PANEL)
        self.options = options
        self.selected_var = tk.StringVar(value=default)
        self.on_select = on_select
        self.buttons = {}
        self.icons = icons or {}

        for i, opt in enumerate(options):
            r = i // columns
            c = i % columns
            icon = self.icons.get(opt, "")
            text = f"{icon} {opt}".strip()

            btn = tk.Button(
                self,
                text=text,
                font=Theme.FONT_SMALL_BOLD,
                relief="flat",
                bd=0,
                padx=8,
                pady=6,
                cursor="hand2",
                command=lambda o=opt: self._select(o),
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            self.buttons[opt] = btn
            self.grid_columnconfigure(c, weight=1)

        self._refresh_styles()

    def _select(self, opt: str):
        self.selected_var.set(opt)
        self._refresh_styles()
        if self.on_select:
            self.on_select(opt)

    def _refresh_styles(self):
        current = self.selected_var.get()
        for opt, btn in self.buttons.items():
            if opt == current:
                btn.config(
                    bg=Theme.BORDER_CYAN,
                    fg=Theme.TEXT_PRIMARY,
                    activebackground=Theme.CYAN_NEON,
                    activeforeground=Theme.BG_DARK,
                )
            else:
                btn.config(
                    bg=Theme.BG_INPUT,
                    fg=Theme.TEXT_SECONDARY,
                    activebackground=Theme.BG_INPUT_ACTIVE,
                    activeforeground=Theme.TEXT_PRIMARY,
                )

    def get(self) -> str:
        return self.selected_var.get()

    def set(self, opt: str):
        self.selected_var.set(opt)
        self._refresh_styles()
