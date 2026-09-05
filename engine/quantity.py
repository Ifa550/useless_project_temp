"""Quantity Calculator for ICECREAM OS.
Computes scoop dosage, gram estimation, and structural container (Cup vs Cone).
"""
from engine.models import QuantityRecommendation, UserInput


class QuantityCalculator:
    """Determines precise physiological scoop dosage and structural serving architecture."""

    GRAMS_PER_SCOOP = 70
    TOPPING_WEIGHT = 25

    @classmethod
    def calculate(cls, necessity_score: int, inp: UserInput) -> QuantityRecommendation:
        """Computes quantity recommendation based on necessity score and biometrics."""
        if necessity_score <= 20:
            scoops = 1
            label = "1 Scoop (Maintenance Dose)"
            has_topping_bonus = False
        elif necessity_score <= 40:
            scoops = 1
            label = "1 Scoop (Preventative Intake)"
            has_topping_bonus = False
        elif necessity_score <= 60:
            scoops = 2
            label = "2 Scoops (Thermodynamic Equilibrium)"
            has_topping_bonus = False
        elif necessity_score <= 80:
            scoops = 3
            label = "3 Scoops (Cognitive Rejuvenation)"
            has_topping_bonus = False
        else: # 81 - 100
            scoops = 3
            label = "3 Scoops + Emergency Topping Payload"
            has_topping_bonus = True

        grams = scoops * cls.GRAMS_PER_SCOOP
        if has_topping_bonus:
            grams += cls.TOPPING_WEIGHT

        # Structural Container Logic (Cup vs Cone)
        # If hot, or scoops >= 3, cone poses acute drip hazard
        if inp.temperature_c >= 28.0 or scoops >= 3:
            container = "Insulated Thermal Cup"
            rationale = (
                f"Atmospheric temperature ({inp.temperature_c:.1f}°C) and volume ({scoops} scoops) "
                "risk rapid thermodynamic melting. Reinforced cup containment mandated."
            )
        elif inp.weather == "Rainy" or inp.time_of_day == "Night":
            container = "Heavy-Duty Waffle Cup"
            rationale = "Ambient moisture and late-hour conditions indicate seated cup consumption protocol."
        elif inp.energy_level >= 60 and inp.temperature_c < 26.0:
            container = "Crispy Waffle Cone"
            rationale = "Low melt coefficient and elevated kinetic energy favor mobile handheld cone aerodynamics."
        else:
            container = "Sugar Cone"
            rationale = "Standard baseline stability supports structural sugar cone consumption."

        return QuantityRecommendation(
            scoops=scoops,
            scoops_label=label,
            grams_estimate=grams,
            container=container,
            container_rationale=rationale,
        )
