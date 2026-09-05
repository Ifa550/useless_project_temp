"""Comprehensive automated test suite for ICECREAM OS engine and storage."""
import unittest
import sys
import os

# Add parent directory to path so engine and storage can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.models import UserInput, NecessityLevel, Mood, Weather, TimeOfDay, FlavorPreference
from engine.necessity import IceCreamNecessityEngine
from engine.flavor import FlavorRecommendationEngine
from engine.quantity import QuantityCalculator
from engine.topping import ToppingRecommendationEngine
from engine.explanation import ExplanationEngine
from engine.pipeline import run_icne_analysis
from storage.history import HistoryManager


class TestIceCreamEngine(unittest.TestCase):

    def test_score_determinism(self):
        """Verify that identical inputs produce identical scores and confidence ratings."""
        inp1 = UserInput(
            mood=Mood.STRESSED.value,
            temperature_c=31.5,
            stress_level=80,
            energy_level=30,
            study_hours=6.0,
            sleep_hours=4.5,
            time_of_day=TimeOfDay.NIGHT.value,
            weather=Weather.VERY_HOT.value,
            preference=FlavorPreference.CHOCOLATE.value,
            notes="Deadline approaching",
        )
        inp2 = UserInput(
            mood=Mood.STRESSED.value,
            temperature_c=31.5,
            stress_level=80,
            energy_level=30,
            study_hours=6.0,
            sleep_hours=4.5,
            time_of_day=TimeOfDay.NIGHT.value,
            weather=Weather.VERY_HOT.value,
            preference=FlavorPreference.CHOCOLATE.value,
            notes="Deadline approaching",
        )
        score1, level1, conf1 = IceCreamNecessityEngine.calculate_score(inp1)
        score2, level2, conf2 = IceCreamNecessityEngine.calculate_score(inp2)

        self.assertEqual(score1, score2)
        self.assertEqual(level1, level2)
        self.assertEqual(conf1, conf2)
        self.assertGreaterEqual(score1, 80)
        self.assertEqual(level1, NecessityLevel.CRITICAL)

    def test_score_clamping(self):
        """Verify score never exceeds 100 or drops below 0 even under extreme conditions."""
        # Maximum possible overload
        extreme_high = UserInput(
            mood=Mood.STRESSED.value,
            temperature_c=45.0,
            stress_level=100,
            energy_level=0,
            study_hours=20.0,
            sleep_hours=0.0,
            time_of_day=TimeOfDay.NIGHT.value,
            weather=Weather.VERY_HOT.value,
            notes="deadline urgent crying exam boss",
        )
        score_high, _, _ = IceCreamNecessityEngine.calculate_score(extreme_high)
        self.assertLessEqual(score_high, 100)
        self.assertGreaterEqual(score_high, 85)

        # Minimum possible demand
        extreme_low = UserInput(
            mood=Mood.NORMAL.value,
            temperature_c=-15.0,
            stress_level=0,
            energy_level=60,
            study_hours=0.0,
            sleep_hours=10.0,
            time_of_day=TimeOfDay.MORNING.value,
            weather=Weather.COLD.value,
            notes="",
        )
        score_low, _, _ = IceCreamNecessityEngine.calculate_score(extreme_low)
        self.assertGreaterEqual(score_low, 0)
        self.assertLessEqual(score_low, 25)

    def test_necessity_levels(self):
        """Verify mapping of score categories to NecessityLevel enums."""
        self.assertEqual(NecessityLevel.from_score(15), NecessityLevel.NOT_REQUIRED)
        self.assertEqual(NecessityLevel.from_score(30), NecessityLevel.MILD)
        self.assertEqual(NecessityLevel.from_score(50), NecessityLevel.MODERATE)
        self.assertEqual(NecessityLevel.from_score(75), NecessityLevel.HIGH)
        self.assertEqual(NecessityLevel.from_score(90), NecessityLevel.CRITICAL)

    def test_flavor_recommendation_logic(self):
        """Verify situational flavor pairing heuristics."""
        # 1. Stressed + Tired -> Chocolate
        inp_stress = UserInput(mood=Mood.STRESSED.value, stress_level=90, sleep_hours=3.0)
        top_flavor, runner_ups = FlavorRecommendationEngine.evaluate_flavors(inp_stress)
        self.assertEqual(top_flavor.name, "Chocolate")
        self.assertEqual(len(runner_ups), 2)

        # 2. Happy + Energetic -> Strawberry or Mango
        inp_happy = UserInput(mood=Mood.HAPPY.value, energy_level=95, weather=Weather.SUNNY.value)
        top_happy, _ = FlavorRecommendationEngine.evaluate_flavors(inp_happy)
        self.assertIn(top_happy.name, ["Strawberry", "Mango"])

        # 3. Very Hot Temperature -> Mango
        inp_hot = UserInput(temperature_c=39.0, weather=Weather.VERY_HOT.value)
        top_hot, _ = FlavorRecommendationEngine.evaluate_flavors(inp_hot)
        self.assertEqual(top_hot.name, "Mango")

        # 4. Bored -> Cookies & Cream
        inp_bored = UserInput(mood=Mood.BORED.value)
        top_bored, _ = FlavorRecommendationEngine.evaluate_flavors(inp_bored)
        self.assertEqual(top_bored.name, "Cookies & Cream")

        # 5. Rainy Weather -> Butterscotch
        inp_rain = UserInput(weather=Weather.RAINY.value, temperature_c=18.0)
        top_rain, _ = FlavorRecommendationEngine.evaluate_flavors(inp_rain)
        self.assertEqual(top_rain.name, "Butterscotch")

        # 6. Confused -> Vanilla
        inp_confused = UserInput(mood=Mood.CONFUSED.value)
        top_confused, _ = FlavorRecommendationEngine.evaluate_flavors(inp_confused)
        self.assertEqual(top_confused.name, "Vanilla")

    def test_quantity_calculator(self):
        """Verify scoops, grams estimation, and container selection."""
        inp_hot = UserInput(temperature_c=35.0)
        q_critical = QuantityCalculator.calculate(88, inp_hot)
        self.assertEqual(q_critical.scoops, 3)
        self.assertEqual(q_critical.grams_estimate, 3 * 70 + 25)  # 235g with emergency topping
        self.assertEqual(q_critical.container, "Insulated Thermal Cup")

        inp_cool = UserInput(temperature_c=20.0, energy_level=70)
        q_mod = QuantityCalculator.calculate(50, inp_cool)
        self.assertEqual(q_mod.scoops, 2)
        self.assertEqual(q_mod.grams_estimate, 140)
        self.assertEqual(q_mod.container, "Crispy Waffle Cone")

        inp_low = UserInput(temperature_c=18.0)
        q_low = QuantityCalculator.calculate(15, inp_low)
        self.assertEqual(q_low.scoops, 1)
        self.assertEqual(q_low.grams_estimate, 70)

    def test_topping_engine(self):
        """Verify topping synergy selection."""
        inp = UserInput(stress_level=85, mood=Mood.STRESSED.value)
        top_fl, _ = FlavorRecommendationEngine.evaluate_flavors(inp)
        topping = ToppingRecommendationEngine.evaluate_topping(top_fl, inp, 85)
        self.assertIn("Chocolate", topping.name)
        self.assertGreaterEqual(topping.compatibility, 75)

    def test_pipeline_and_explanation(self):
        """Verify complete pipeline execution and explanation generation."""
        inp = UserInput(
            mood=Mood.STRESSED.value,
            temperature_c=31.0,
            stress_level=78,
            study_hours=5.0,
            sleep_hours=5.0,
            notes="Working on physics paper",
        )
        res = run_icne_analysis(inp)
        self.assertIsNotNone(res)
        self.assertIn("31.0°C", res.scientific_explanation)
        self.assertIn("78%", res.scientific_explanation)
        self.assertIn("5.0", res.scientific_explanation)
        self.assertIn("physics paper", res.scientific_explanation)
        self.assertIn("entertainment", res.scientific_explanation.lower())

        # Test clipboard report
        report = ExplanationEngine.generate_clipboard_report(res, inp)
        self.assertIn("ICECREAM OS", report)
        self.assertIn("NECESSITY SCORE", report)
        self.assertIn("Chocolate", report)

    def test_history_manager(self):
        """Verify history storage, retrieval, and clearing."""
        hist = HistoryManager()
        self.assertEqual(hist.count(), 0)

        inp = UserInput(mood=Mood.HAPPY.value)
        res = run_icne_analysis(inp)
        record = hist.add_record(res, inp)

        self.assertEqual(hist.count(), 1)
        self.assertEqual(record.mood, Mood.HAPPY.value)
        self.assertEqual(hist.get_records()[0].score, res.necessity_score)

        hist.clear()
        self.assertEqual(hist.count(), 0)

    def test_edge_case_robustness(self):
        """Verify that unusual or extreme boundary inputs do not crash the engine."""
        weird_inputs = [
            UserInput(temperature_c=-50.0, stress_level=0, energy_level=0, study_hours=0.0, sleep_hours=0.0, notes=""),
            UserInput(temperature_c=100.0, stress_level=100, energy_level=100, study_hours=24.0, sleep_hours=24.0, notes="!@#$%^&*()_+"),
            UserInput(notes="A" * 2000),  # Very long notes string
        ]
        for inp in weird_inputs:
            res = run_icne_analysis(inp)
            self.assertIsNotNone(res)
            self.assertTrue(0 <= res.necessity_score <= 100)
            self.assertIsNotNone(res.top_flavor)
            self.assertIsNotNone(res.quantity)
            self.assertIsNotNone(res.topping)
            self.assertTrue(len(res.scientific_explanation) > 0)


if __name__ == "__main__":
    unittest.main()

