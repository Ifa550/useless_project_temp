"""Theme definitions, color palette, and visual styling constants for ICECREAM OS."""

class Theme:
    # Futuristic Dark Cyber Palette
    BG_DARK = "#080C14"            # Deep cosmos dark background
    BG_PANEL = "#0F172A"           # Surface panel / card background
    BG_PANEL_ALT = "#162038"       # Slightly lighter card accent
    BG_INPUT = "#1E293B"           # Input field / chip background
    BG_INPUT_ACTIVE = "#253450"    # Hover / active input

    # High-Tech Neon Accents
    CYAN_NEON = "#00F2FE"          # Primary glowing cyan
    BLUE_ELECTRIC = "#4FACFE"      # Secondary electric blue
    PURPLE_NEON = "#9B51E0"        # Accent purple
    PINK_NEON = "#FF007F"          # Dramatic alert / critical
    AMBER_WARN = "#FFB703"         # Moderate warning
    GREEN_SUCCESS = "#00F5A0"      # Mild / Nominal state
    RED_CRITICAL = "#FF3366"       # Critical alert

    # Text Colors
    TEXT_PRIMARY = "#F8FAFC"       # Crisp white
    TEXT_SECONDARY = "#94A3B8"     # Muted telemetry gray
    TEXT_MUTED = "#64748B"         # Darker label gray
    TEXT_CYAN = "#38BDF8"          # High-tech readout blue
    TEXT_GLOW = "#E0F2FE"

    # Borders & Dividers
    BORDER_DEFAULT = "#1E293B"
    BORDER_CYAN = "#0284C7"
    BORDER_GLOW = "#00F2FE"

    # Font Families
    FONT_FAMILY_HEAD = "Segoe UI"
    FONT_FAMILY_MONO = "Consolas"

    # Pre-built Font Tuples for Tkinter
    FONT_TITLE_HERO = ("Segoe UI", 22, "bold")
    FONT_TITLE_LARGE = ("Segoe UI", 16, "bold")
    FONT_TITLE_MED = ("Segoe UI", 12, "bold")
    FONT_BODY_BOLD = ("Segoe UI", 10, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_SMALL_BOLD = ("Segoe UI", 8, "bold")

    FONT_MONO_HERO = ("Consolas", 28, "bold")
    FONT_MONO_LARGE = ("Consolas", 14, "bold")
    FONT_MONO_MED = ("Consolas", 11, "bold")
    FONT_MONO_BODY = ("Consolas", 10)
    FONT_MONO_SMALL = ("Consolas", 8)
