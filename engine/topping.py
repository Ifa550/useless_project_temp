"""Topping Recommendation Engine for ICECREAM OS.
Matches optimal topping particulates and sauces to the selected flavor and situation.
"""
from typing import Dict
from engine.models import ToppingScore, FlavorScore, UserInput, Mood


class ToppingRecommendationEngine:
    """Calculates molecular topping compatibility."""

    TOPPING_DATA = {
        "Chocolate Syrup": {"emoji": "🍫", "base": 65},
        "Chocolate Chips": {"emoji": "🍪", "base": 62},
        "Sprinkles": {"emoji": "✨", "base": 58},
        "Oreo-Style Cookie Pieces": {"emoji": "🍘", "base": 64},
        "Caramel Drizzle": {"emoji": "🍯", "base": 60},
        "Roasted Nuts": {"emoji": "🥜", "base": 55},
        "Fresh Strawberry Pieces": {"emoji": "🍓", "base": 59},
        "Whipped Cream Cloud": {"emoji": "☁️", "base": 63},
    }

    @classmethod
    def evaluate_topping(cls, flavor: FlavorScore, inp: UserInput, necessity_score: int) -> ToppingScore:
        """Determines the single most compatible topping based on flavor and biometrics."""
        scores: Dict[str, float] = {k: v["base"] for k, v in cls.TOPPING_DATA.items()}
        reasons: Dict[str, str] = {}

        # Flavor-specific pairings
        fl_name = flavor.name.lower()
        if "chocolate" in fl_name:
            scores["Chocolate Syrup"] += 28.0
            scores["Chocolate Chips"] += 20.0
            scores["Whipped Cream Cloud"] += 15.0
            reasons["Chocolate Syrup"] = "Dual-layer cocoa saturation required to suppress cortisol spikes."
        elif "vanilla" in fl_name:
            scores["Caramel Drizzle"] += 24.0
            scores["Sprinkles"] += 20.0
            scores["Roasted Nuts"] += 18.0
            reasons["Caramel Drizzle"] = "Golden buttery ribbons elevate neutral vanilla baseline to gourmet status."
        elif "strawberry" in fl_name:
            scores["Fresh Strawberry Pieces"] += 28.0
            scores["Sprinkles"] += 22.0
            scores["Whipped Cream Cloud"] += 18.0
            reasons["Fresh Strawberry Pieces"] = "Reinforces natural berry flavonoids and visual vibrancy spectrum."
        elif "butterscotch" in fl_name:
            scores["Caramel Drizzle"] += 26.0
            scores["Roasted Nuts"] += 24.0
            reasons["Caramel Drizzle"] = "Complementary sugar caramelization amplifies comforting lipid density."
        elif "mango" in fl_name:
            scores["Whipped Cream Cloud"] += 26.0
            scores["Fresh Strawberry Pieces"] += 22.0
            reasons["Whipped Cream Cloud"] = "Aerated dairy lipid cloud tempers intense tropical mango acidity."
        elif "cookies" in fl_name:
            scores["Oreo-Style Cookie Pieces"] += 30.0
            scores["Chocolate Syrup"] += 20.0
            reasons["Oreo-Style Cookie Pieces"] = "High-impact particulate crunch provides maximum sensory dopamine feedback."

        # Situational modifiers
        if inp.stress_level >= 75:
            scores["Chocolate Syrup"] += 15.0
            scores["Whipped Cream Cloud"] += 12.0
        if inp.mood in [Mood.HAPPY.value, Mood.EXCITED.value]:
            scores["Sprinkles"] += 20.0
            reasons["Sprinkles"] = "Chromatically saturated sucrose cylinders align with elevated euphoric state."
        if inp.mood == Mood.BORED.value:
            scores["Oreo-Style Cookie Pieces"] += 18.0
        if necessity_score >= 80:
            scores["Chocolate Syrup"] += 12.0
            scores["Whipped Cream Cloud"] += 14.0

        # Find topping with highest score
        best_name = max(scores, key=lambda k: scores[k])
        compat = int(round(max(70.0, min(99.0, scores[best_name]))))
        reason = reasons.get(best_name, "Optimal textural and flavor synergy verified by algorithmic sensor matrix.")

        return ToppingScore(
            name=best_name,
            emoji=cls.TOPPING_DATA[best_name]["emoji"],
            compatibility=compat,
            reason=reason,
        )
