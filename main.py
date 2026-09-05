"""Entry point for ICECREAM OS — Intelligent Cream Recommendation & Quantity Engine."""
import sys
import os
import tkinter as tk

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import IceCreamOSApp


def set_windows_dpi_awareness():
    """Enables Windows Per-Monitor DPI awareness for crisp font and UI rendering."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            # Shcore SetProcessDpiAwareness: 2 = PROCESS_PER_MONITOR_DPI_AWARE
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                # Fallback to user32 SetProcessDPIAware
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def main():
    """Launches ICECREAM OS desktop application."""
    set_windows_dpi_awareness()
    root = tk.Tk()
    app = IceCreamOSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
