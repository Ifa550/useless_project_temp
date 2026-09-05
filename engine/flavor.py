"""Flavor Recommendation Engine for ICECREAM OS.
Evaluates multi-factor compatibility across all flavors and generates scientific rationales.
"""
from typing import List, Tuple
from engine.models import (
    UserInput,
    FlavorScore,
    FlavorPreference,
    Mood,
    Weather,
    TimeOfDay,
)


class FlavorRecommendationEngine:
    """Calculates compatibility indices for all flavors and produces top recommendations."""

    FLAVORS = [
        {"name": "Chocolate", "emoji": "🍫"},
        {"name": "Vanilla", "emoji": "🍦"},
        {"name": "Strawberry", "emoji": "🍓"},
        {"name": "Butterscotch", "emoji": "🍯"},
        {"name": "Mango", "emoji": "🥭"},
        {"name": "Cookies & Cream", "emoji": "🍪"},
    ]

    @classmethod
    def evaluate_flavors(cls, inp: UserInput) -> Tuple[FlavorScore, List[FlavorScore]]:
        """Calculates compatibility for all flavors, returns (top_flavor, runner_ups)."""
        scores = {}
        reasons = {}

        # 1. Base scores for all flavors
        for f in cls.FLAVORS:
            scores[f["name"]] = 45.0

        # 2. Mood Influences
        if inp.mood in [Mood.STRESSED.value, Mood.SAD.value, Mood.ANGRY.value]:
            scores["Chocolate"] += 28.0
            reasons["Chocolate"] = f"Elevated {inp.mood.lower()} metrics demand dense cocoa-theobromine neurological stabilization."
        elif inp.mood in [Mood.HAPPY.value, Mood.EXCITED.value]:
            scores["Strawberry"] += 24.0
            scores["Mango"] += 18.0
            reasons["Strawberry"] = "Positive neurotransmitter surge harmonizes with berry sucrose vibration frequencies."
            reasons["Mango"] = "High dopamine baseline synergizes perfectly with tropical fruit esters."
        elif inp.mood == Mood.BORED.value:
            scores["Cookies & Cream"] += 28.0
            reasons["Cookies & Cream"] = "Textural cookie particulates required to stimulate dormant sensory neural pathways."
        elif inp.mood == Mood.CONFUSED.value:
            scores["Vanilla"] += 28.0
            reasons["Vanilla"] = "High cognitive disorientation requires the comforting baseline clarity of pure bourbon vanilla."
        elif inp.mood == Mood.TIRED.value:
            scores["Chocolate"] += 18.0
            scores["Cookies & Cream"] += 16.0
            reasons["Chocolate"] = "Fatigue signals trigger urgent cocoa lipid energy deployment protocols."
        else: # Normal
            scores["Vanilla"] += 14.0
            scores["Butterscotch"] += 12.0
            reasons["Vanilla"] = "Equilibrium biometrics pair smoothly with classic culinary baseline architecture."

        # 3. Ambient Temperature Influences
        temp = inp.temperature_c
        if temp >= 32.0:
            scores["Mango"] += 26.0
            scores["Strawberry"] += 16.0
            reasons["Mango"] = f"Extreme thermal load ({temp:.1f}°C) triggers automatic tropical cooling protocols."
        elif temp >= 24.0:
            scores["Mango"] += 14.0
            scores["Strawberry"] += 10.0
        elif temp <= 10.0:
            scores["Butterscotch"] += 22.0
            scores["Chocolate"] += 14.0
            reasons["Butterscotch"] = f"Sub-ambient thermal reading ({temp:.1f}°C) warrants warm caramelized butter lipid comfort."
        else:
            scores["Cookies & Cream"] += 8.0

        # 4. Weather Influences
        if inp.weather == Weather.RAINY.value:
            scores["Butterscotch"] += 24.0
            scores["Chocolate"] += 12.0
            if "Butterscotch" not in reasons:
                reasons["Butterscotch"] = "Precipitation and atmospheric pressure drop create an acute caramelization craving."
        elif inp.weather == Weather.VERY_HOT.value:
            scores["Mango"] += 20.0
            scores["Strawberry"] += 15.0
        elif inp.weather == Weather.COLD.value:
            scores["Butterscotch"] += 18.0
            scores["Chocolate"] += 15.0

        # 5. Stress and Sleep Influences
        if inp.stress_level >= 70:
            scores["Chocolate"] += 20.0
            reasons["Chocolate"] = f"Critical stress telemetry ({inp.stress_level}%) activated emergency cocoa-endorphin synthesis."
        if inp.sleep_hours < 5.0:
            scores["Cookies & Cream"] += 14.0
            scores["Chocolate"] += 12.0

        # 6. Energy Influences
        if inp.energy_level >= 75 and inp.mood in [Mood.HAPPY.value, Mood.EXCITED.value]:
            scores["Strawberry"] += 16.0
        elif inp.energy_level <= 25:
            scores["Chocolate"] += 12.0
            scores["Butterscotch"] += 10.0

        # 7. Time of Day
        if inp.time_of_day == TimeOfDay.NIGHT.value:
            scores["Chocolate"] += 10.0
            scores["Cookies & Cream"] += 10.0
        elif inp.time_of_day == TimeOfDay.MORNING.value:
            scores["Strawberry"] += 12.0
            scores["Vanilla"] += 10.0

        # 8. User Preference Bonus
        pref = inp.preference
        if pref != FlavorPreference.NO_PREFERENCE.value:
            for fname in scores:
                if fname.lower() == pref.lower():
                    scores[fname] += 25.0
                    if fname not in reasons:
                        reasons[fname] = f"Direct subject preference calibration corroborated by biometrics."

        # Compile and clamp scores
        compiled_list: List[FlavorScore] = []
        for f in cls.FLAVORS:
            name = f["name"]
            raw = scores[name]
            clamped = int(round(max(40.0, min(99.0, raw))))
            reason = reasons.get(name, f"Calculated algorithmic synergy based on current ambient and physiological matrix.")
            compiled_list.append(FlavorScore(name=name, emoji=f["emoji"], compatibility=clamped, reason=reason))

        # Sort descending by compatibility
        compiled_list.sort(key=lambda x: x.compatibility, reverse=True)

        top_flavor = compiled_list[0]
        runner_ups = compiled_list[1:3]
        return top_flavor, runner_ups
