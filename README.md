# 🍦 ICECREAM OS — Intelligent Cream Recommendation & Quantity Engine

> **"An extremely sophisticated solution to a problem that absolutely nobody needed solved."**

```
  ___ ____ _____ ____ ____  _____    _    __  __     ___  ____  
 |_ _/ ___| ____/ ___|  _ \| ____|  / \  |  \/  |   / _ \/ ___| 
  | | |   |  _|| |   | |_) |  _|   / _ \ | |\/| |  | | | \___ \ 
  | | |___| |__| |___|  _ <| |___ / ___ \| |  | |  | |_| |___) |
 |___\____|_____\____|_| \_\_____/_/   \_\_|  |_|   \___/|____/ 
                                                                
     Intelligent Cream Recommendation & Quantity Engine v2.0
```

---

## ⚡ Mission Overview

**ICECREAM OS** is a fully functional desktop application featuring a serious, futuristic, NASA-level AI-powered mission control command center—built entirely for the purpose of analyzing whether you need ice cream, how much, what flavor, and what topping.

It features custom multi-factor calculation engines, interactive telemetry sliders, an animated circular score gauge, a simulated quantum diagnostic scan, an interactive pseudo-scientific telemetry breakdown (*"Why Do I Need This?"*), one-click clipboard report sharing, and volatile session calculation logs.

> [!IMPORTANT]
> **DISCLAIMER: ENTERTAINMENT PROTOCOL**
> ICECREAM OS and the ICNE algorithms are created strictly for entertainment and humorous purposes. None of the recommendations, scores, or rationales constitute medical, nutritional, or psychological advice.

---

## 🚀 Quick Start

### Requirements
- **Python 3.8+** (Standard installation on Windows, macOS, or Linux)
- **Zero External Dependencies**: Built 100% on Python's standard library (`tkinter`), ensuring instant launch and total offline operation.

### Running the Application

Double-click `run.bat` or run via terminal:

```bash
python main.py
```

### Running Automated Test Suite

```bash
python -m unittest discover tests
```

---

## 🧠 The ICNE Computational Matrix

### 1. ICNE — Ice Cream Necessity Engine
Computes a mathematically weighted score from **0 to 100** based on real biometric and environmental inputs:
- **Cortisol Stress Load (0–100%)**: Scales linearly to demand emergency theobromine stabilization.
- **Cognitive Workload (Study/Work Duration)**: Hours of intellectual burn deplete cerebral glucose reserves.
- **Somnological Deficit (Sleep Hours)**: Sleep deprivation triggers compensatory dopamine synthesis.
- **Ambient Thermal Environment (°C)**: Extreme temperatures (>32°C) spike cooling necessity; sub-zero conditions shift demand toward warm comfort profiles.
- **Atmospheric Conditions & Chronobiology**: Weather (Sunny, Rainy, Very Hot, Cold) and Time of Day (Morning, Afternoon, Evening, Night).
- **Affective State Vector (Mood)**: Happy, Sad, Stressed, Bored, Angry, Tired, Excited, Confused, Normal.
- **Qualitative Mission Telemetry**: Keyword scanning in the notes field ("deadline", "exam", "boss", "breakup", "birthday").

### 2. Necessity Categories & Emergency Protocols
- **0–20**: `ICE CREAM NOT REQUIRED` *(System in baseline state. Ingestion optional.)*
- **21–40**: `MILD ICE CREAM REQUIREMENT` *(Minor neuro-dessert craving detected. Preventative intake suggested.)*
- **41–60**: `MODERATE ICE CREAM REQUIREMENT` *(Elevated thermal & mental load. Standard cooling protocol advised.)*
- **61–80**: `HIGH ICE CREAM REQUIREMENT` *(Significant cognitive strain. Immediate dessert intervention strongly recommended.)*
- **81–100**: `CRITICAL ICE CREAM SITUATION` *(EMERGENCY DESSERT PROTOCOLS RECOMMENDED. IMMEDIATE GLUCOSE-LIPID STABILIZATION MANDATED.)*

### 3. Multi-Factor Flavor Recommendation Engine
Calculates compatibility percentages (0–100%) across all major flavors and outputs the #1 payload alongside the top 2 alternatives:
- **🍫 Chocolate**: Stress, fatigue, late night, sadness, anger.
- **🍦 Vanilla**: Confusion, baseline clarity, thermal moderation, versatile stability.
- **🍓 Strawberry**: Euphoria, high kinetic energy, morning/afternoon sunshine.
- **🍯 Butterscotch**: Precipitation, sub-ambient temperatures, evening study fatigue.
- **🥭 Mango**: Hyperthermic atmospheric load (>32°C), intense solar radiation.
- **🍪 Cookies & Cream**: Boredom, sensory deprivation, afternoon slump.

### 4. Quantity & Structural Architecture Engine
- **Scoop Dosage**:
  - Score 0–40: `1 Scoop` (~70 g)
  - Score 41–60: `2 Scoops` (~140 g)
  - Score 61–80: `3 Scoops` (~210 g)
  - Score 81–100: `3 Scoops + Emergency Topping Payload` (~235 g)
- **Serving Architecture (Cup vs Cone)**:
  - High ambient temps (>28°C) or 3 scoops: `Insulated Thermal Cup` *(prevents thermodynamic melting failure)*.
  - Active energy & moderate temps: `Crispy Waffle Cone` *(optimal handheld aerodynamics)*.

### 5. Topping Synergy Engine
Detects optimal topping from:
- Chocolate Syrup
- Chocolate Chips
- Sprinkles
- Oreo-Style Cookie Pieces
- Caramel Drizzle
- Roasted Nuts
- Fresh Strawberry Pieces
- Whipped Cream Cloud

---

## 🖥️ Feature Tour

| Feature | Description |
| :--- | :--- |
| **Cockpit Input View** | Interactive sliders, selectable chip grids for mood, weather, time, and flavor preference, and a mission notes text area. |
| **Diagnostic Animation** | Simulated scanning sequence with humorous status tickers ("Measuring scoop aerodynamic compatibility...", "Consulting highly questionable dessert science..."). |
| **Mission Control Dashboard** | Glowing circular gauge, color-coded emergency status badge, flavor card with compatibility % and runner-ups, dosage specs, and topping readout. |
| **🔬 "Why Do I Need This?"** | Modal dialog detailing a humorous pseudo-scientific breakdown referencing the user's exact temperature, stress, workload, and sleep inputs. |
| **🔄 Recalculate Destiny** | Re-triggers quantum analysis and refreshes telemetry indicators. |
| **📋 Copy Report** | Copies a formatted ASCII telemetry report to the clipboard with real-time feedback. |
| **📜 Result History** | Tracks all calculations during the session with column sorting, double-click inspection, and clear history. |

---

## 📁 Project Architecture

```
icecream_os/
├── main.py                     # Primary launcher and DPI awareness setup
├── run.bat                     # Windows double-click runner
├── README.md                   # System documentation
├── engine/
│   ├── __init__.py
│   ├── models.py               # Typed dataclasses (UserInput, AnalysisResult, etc.)
│   ├── necessity.py            # ICNE weighted scoring and confidence calculation
│   ├── flavor.py               # Multi-factor flavor compatibility calculator
│   ├── quantity.py             # Dosage (scoops, grams, Cup/Cone container)
│   ├── topping.py              # Molecular topping pairing engine
│   ├── explanation.py          # Pseudo-scientific telemetry explanation & report generator
│   └── pipeline.py             # Unified analysis execution runner
├── storage/
│   ├── __init__.py
│   └── history.py              # Session calculation history manager
├── ui/
│   ├── __init__.py
│   ├── theme.py                # Sci-fi color palette, fonts, styling constants
│   ├── widgets.py              # Custom HUD cards, circular gauge, cyber sliders, chips, buttons
│   ├── input_view.py           # Cockpit input screen
│   ├── analysis_view.py        # Diagnostic scanning animation screen
│   ├── result_view.py          # Mission control dashboard
│   ├── history_view.py         # Session history table
│   └── app.py                  # Main Tkinter application coordinator
└── tests/
    ├── __init__.py
    └── test_engine.py          # Unit test suite verifying math, determinism, clamping, and edge cases
```

---

## 🧪 Verification & Testing

Run the automated test suite:
```bash
python -m unittest discover tests
```
Result:
```
Ran 8 tests in 0.005s
OK
```
All scoring matrices, clamping constraints, flavor heuristics, quantity bounds, topping matching, and clipboard reports are verified.
