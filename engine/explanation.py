"""Pseudo-scientific telemetry and explanation generator for ICECREAM OS.
Produces humorous explanations incorporating the user's exact inputs.
"""
from typing import List
from engine.models import AnalysisResult, UserInput


class ExplanationEngine:
    """Constructs convincing yet completely fictitious NASA-style telemetry explanations."""

    @staticmethod
    def generate_why_explanation(res: AnalysisResult, inp: UserInput) -> str:
        """Generates a detailed, humorous pseudo-scientific breakdown based on user inputs."""
        telemetry_lines: List[str] = []

        # 1. Thermal Telemetry
        if inp.temperature_c >= 30.0:
            telemetry_lines.append(
                f"• THERMAL TELEMETRY: Ambient sensor reads {inp.temperature_c:.1f}°C. Severe atmospheric hyperthermia detected. Internal core cooling required."
            )
        elif inp.temperature_c <= 10.0:
            telemetry_lines.append(
                f"• THERMAL TELEMETRY: Cryogenic ambient reading of {inp.temperature_c:.1f}°C. Cold weather paradox triggered: compensatory emotional warming mandated."
            )
        else:
            telemetry_lines.append(
                f"• THERMAL TELEMETRY: Nominal ambient temperature ({inp.temperature_c:.1f}°C). Baseline thermodynamic intake recommended."
            )

        # 2. Cognitive & Stress Metrics
        if inp.stress_level >= 70:
            telemetry_lines.append(
                f"• CORTISOL SENSORS: Stress load measured at {inp.stress_level}%. Critical nervous system strain requires immediate sucrose-theobromine dampening."
            )
        elif inp.stress_level >= 40:
            telemetry_lines.append(
                f"• CORTISOL SENSORS: Moderate stress level ({inp.stress_level}%). Preemptive dopamine stabilization protocols indicated."
            )
        else:
            telemetry_lines.append(
                f"• CORTISOL SENSORS: Low stress level ({inp.stress_level}%). Dessert protocol designated as celebratory and recreational."
            )

        # 3. Work/Study Fatigue
        if inp.study_hours >= 6.0:
            telemetry_lines.append(
                f"• NEUROLOGICAL WORKLOAD: {inp.study_hours:.1f} hours of study/work detected. Brain glucose reserves critically exhausted. Replenishment vital."
            )
        elif inp.study_hours >= 2.0:
            telemetry_lines.append(
                f"• NEUROLOGICAL WORKLOAD: Standard intellectual burn ({inp.study_hours:.1f} hours). Maintenance glucose payload authorized."
            )

        # 4. Somnological Status
        if inp.sleep_hours <= 4.5:
            telemetry_lines.append(
                f"• SLEEP DEFICIT: Acute somnological deficit recorded ({inp.sleep_hours:.1f} hours of rest). System running on emergency dopamine backup."
            )
        elif inp.sleep_hours <= 6.5:
            telemetry_lines.append(
                f"• SLEEP DEFICIT: Sub-optimal sleep duration ({inp.sleep_hours:.1f} hours). Cognitive recovery enhancement warranted."
            )

        # 5. Emotional Analysis
        telemetry_lines.append(
            f"• AFFECTIVE VECTOR: Subject mood categorized as '{inp.mood}'. Primary neural pathways require '{res.top_flavor.name}' frequency stabilization."
        )

        # 6. Notes integration
        if inp.notes.strip():
            telemetry_lines.append(
                f"• QUALITATIVE TELEMETRY: User stated '{inp.notes.strip()}'. Mission control computers have flagged this as an acute dessert catalyst."
            )

        # 7. Synthesis
        telemetry_block = "\n".join(telemetry_lines)

        explanation = (
            f"DIAGNOSTIC TELEMETRY SUMMARY:\n\n"
            f"{telemetry_block}\n\n"
            f"ICNE SCIENTIFIC SYNTHESIS:\n"
            f"Based on weighted algorithmic fusion of your ambient temperature ({inp.temperature_c:.1f}°C), "
            f"stress telemetry ({inp.stress_level}%), and cognitive workload ({inp.study_hours:.1f}h), "
            f"the ICNE neural core has calculated a Necessity Score of {res.necessity_score}/100 ({res.level.label}).\n\n"
            f"To achieve neuro-gastronomic equilibrium, immediate intake of {res.quantity.scoops_label} "
            f"({res.quantity.grams_estimate}g) of {res.top_flavor.name} topped with {res.topping.name} in a {res.quantity.container} "
            f"is mathematically advised.\n\n"
            f"⚠️ NOTICE: This calculation is powered by 100% humorous, fictional pseudo-science. "
            f"It is created purely for entertainment and does not constitute nutritional or medical guidance."
        )

        return explanation

    @staticmethod
    def generate_clipboard_report(res: AnalysisResult, inp: UserInput) -> str:
        """Produces a clean, futuristic text report suitable for sharing."""
        border = "=" * 62
        divider = "-" * 62
        report = (
            f"{border}\n"
            f"🍦 ICECREAM OS — INTELLIGENT CREAM RECOMMENDATION REPORT\n"
            f"MISSION CONTROL NEURO-DESSERT TELEMETRY CORE v2.0\n"
            f"{border}\n"
            f"TIMESTAMP           : {res.timestamp}\n"
            f"NECESSITY SCORE     : {res.necessity_score} / 100 [{res.level.label}]\n"
            f"SYSTEM STATUS       : {res.dramatic_message}\n"
            f"CONFIDENCE RATING   : {res.confidence}%\n"
            f"{divider}\n"
            f"RECOMMENDED FLAVOR  : {res.top_flavor.emoji} {res.top_flavor.name.upper()} ({res.top_flavor.compatibility}% Match)\n"
            f"FLAVOR RATIONALE    : {res.top_flavor.reason}\n"
            f"RECOMMENDED QUANTITY: {res.quantity.scoops_label}\n"
            f"ESTIMATED AMOUNT    : ~{res.quantity.grams_estimate} g (Non-medical serving estimate)\n"
            f"SERVING ARCHITECTURE: {res.quantity.container}\n"
            f"CONTAINER REASONING : {res.quantity.container_rationale}\n"
            f"TOPPING DETECTED    : {res.topping.emoji} {res.topping.name} ({res.topping.compatibility}% Synergy)\n"
            f"{divider}\n"
            f"ALTERNATIVE OPTIONS : "
            + ", ".join([f"{f.emoji} {f.name} ({f.compatibility}%)" for f in res.runner_up_flavors])
            + f"\n"
            f"{divider}\n"
            f"BIOMETRIC INPUT SNAPSHOT:\n"
            f"• Mood: {inp.mood} | Weather: {inp.weather} | Ambient: {inp.temperature_c:.1f}°C\n"
            f"• Stress: {inp.stress_level}% | Energy: {inp.energy_level}% | Work: {inp.study_hours:.1f}h | Sleep: {inp.sleep_hours:.1f}h\n"
            + (f"• Mission Notes: \"{inp.notes}\"\n" if inp.notes.strip() else "")
            + f"{border}\n"
            f"* DISCLAIMER: Generated by ICECREAM OS purely for entertainment. *\n"
            f"* No actual scientific or medical credibility is claimed or implied. *\n"
            f"{border}"
        )
        return report
