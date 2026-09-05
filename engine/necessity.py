"""ICNE — Ice Cream Necessity Engine.
Computes a scientifically unnecessary yet mathematically weighted Ice Cream Necessity Score (0-100).
"""
import hashlib
from typing import Tuple
from engine.models import (
    UserInput,
    NecessityLevel,
    Mood,
    Weather,
    TimeOfDay,
)


class IceCreamNecessityEngine:
    """The central computational core of ICECREAM OS."""

    @staticmethod
    def calculate_score(inp: UserInput) -> Tuple[int, NecessityLevel, float]:
        """Calculates the Ice Cream Necessity Score (0-100), NecessityLevel, and confidence %."""
        # 1. Base metabolic expectation
        score = 8.0

        # 2. Stress impact (0 - 100%) -> up to +28 points
        stress_contribution = (inp.stress_level / 100.0) * 28.0
        score += stress_contribution

        # 3. Work/Study cognitive fatigue (hours) -> up to +20 points
        if inp.study_hours >= 10:
            score += 20.0
        elif inp.study_hours >= 7:
            score += 16.0
        elif inp.study_hours >= 5:
            score += 12.0
        elif inp.study_hours >= 3:
            score += 7.0
        elif inp.study_hours >= 1:
            score += 3.0

        # 4. Sleep deprivation factor (hours) -> up to +14 points
        if inp.sleep_hours <= 3:
            score += 14.0
        elif inp.sleep_hours <= 5:
            score += 10.0
        elif inp.sleep_hours <= 6.5:
            score += 5.0
        elif inp.sleep_hours >= 9:
            score -= 3.0  # Well-rested reduces cortisol craving

        # 5. Energy interaction (inverted U or exhaustion boost)
        # Low energy induces glucose-seeking; high energy with excitement triggers celebration
        if inp.energy_level < 30:
            score += 10.0 * (1.0 - (inp.energy_level / 30.0))
        elif inp.energy_level > 80 and inp.mood in [Mood.EXCITED.value, Mood.HAPPY.value]:
            score += 8.0

        # 6. Thermal environment (°C)
        temp = inp.temperature_c
        if temp >= 38:
            score += 24.0
        elif temp >= 32:
            score += 18.0
        elif temp >= 26:
            score += 12.0
        elif temp >= 20:
            score += 5.0
        elif temp >= 10:
            score += 0.0
        elif temp >= 0:
            score -= 6.0
        else:
            # Below 0°C: dampens pure cooling demand, but if stress is high, comfort eating still applies
            score -= 12.0

        # 7. Weather factor
        weather_adjustments = {
            Weather.VERY_HOT.value: 12.0,
            Weather.SUNNY.value: 6.0,
            Weather.RAINY.value: 8.0,   # High comfort dessert quotient
            Weather.CLOUDY.value: 3.0,
            Weather.COLD.value: -5.0,
        }
        score += weather_adjustments.get(inp.weather, 0.0)

        # 8. Time of day chronobiology
        tod_adjustments = {
            TimeOfDay.NIGHT.value: 10.0,
            TimeOfDay.EVENING.value: 7.0,
            TimeOfDay.AFTERNOON.value: 5.0,
            TimeOfDay.MORNING.value: 1.0,
        }
        score += tod_adjustments.get(inp.time_of_day, 0.0)

        # 9. Emotional state matrix
        mood_multipliers = {
            Mood.STRESSED.value: 15.0,
            Mood.SAD.value: 16.0,
            Mood.ANGRY.value: 13.0,
            Mood.TIRED.value: 12.0,
            Mood.BORED.value: 10.0,
            Mood.EXCITED.value: 9.0,
            Mood.HAPPY.value: 7.0,
            Mood.CONFUSED.value: 8.0,
            Mood.NORMAL.value: 2.0,
        }
        score += mood_multipliers.get(inp.mood, 0.0)

        # 10. Qualitative Notes Semantic Scan
        notes_lower = inp.notes.lower().strip()
        urgent_keywords = ["deadline", "boss", "exam", "crying", "urgent", "tired", "burned", "breakup", "help", "pain"]
        positive_keywords = ["birthday", "won", "passed", "celebrate", "party", "gym", "friday", "weekend"]

        for kw in urgent_keywords:
            if kw in notes_lower:
                score += 4.0
                break

        for kw in positive_keywords:
            if kw in notes_lower:
                score += 3.0
                break

        # Final score clamping to 0 - 100
        final_score = int(round(max(0.0, min(100.0, score))))
        level = NecessityLevel.from_score(final_score)

        # Confidence calculation:
        # Confidence is mathematically deterministic: ranges from 88.0% to 98.9%
        # Stronger input signals yield higher algorithmic confidence
        input_vector = f"{inp.mood}:{inp.temperature_c}:{inp.stress_level}:{inp.study_hours}:{inp.sleep_hours}"
        hash_val = int(hashlib.md5(input_vector.encode("utf-8")).hexdigest()[:4], 16)
        variance = (hash_val % 50) / 10.0  # 0.0 to 4.9
        confidence = round(92.0 + (final_score / 100.0) * 4.0 + (variance * 0.5), 1)
        confidence = min(99.4, max(88.0, confidence))

        return final_score, level, confidence
