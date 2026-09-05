"""Analysis pipeline combining all engine sub-systems into a unified result."""
from engine.models import UserInput, AnalysisResult
from engine.necessity import IceCreamNecessityEngine
from engine.flavor import FlavorRecommendationEngine
from engine.quantity import QuantityCalculator
from engine.topping import ToppingRecommendationEngine
from engine.explanation import ExplanationEngine


def run_icne_analysis(inp: UserInput) -> AnalysisResult:
    """Executes the full ICNE pipeline deterministically for a given UserInput."""
    # 1. Calculate Necessity Score, Level, and Confidence
    score, level, confidence = IceCreamNecessityEngine.calculate_score(inp)

    # 2. Evaluate Flavors
    top_flavor, runner_ups = FlavorRecommendationEngine.evaluate_flavors(inp)

    # 3. Calculate Quantity and Serving Specs
    quantity = QuantityCalculator.calculate(score, inp)

    # 4. Detect optimal topping
    topping = ToppingRecommendationEngine.evaluate_topping(top_flavor, inp, score)

    # 5. Build preliminary result object
    result = AnalysisResult(
        necessity_score=score,
        level=level,
        dramatic_message=level.dramatic_message,
        top_flavor=top_flavor,
        runner_up_flavors=runner_ups,
        quantity=quantity,
        topping=topping,
        confidence=confidence,
        scientific_explanation="",
        input_snapshot=inp,
    )

    # 6. Generate detailed pseudo-scientific breakdown
    result.scientific_explanation = ExplanationEngine.generate_why_explanation(result, inp)

    return result
