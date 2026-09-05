"""Data models and type definitions for ICECREAM OS."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class Mood(str, Enum):
    HAPPY = "Happy"
    SAD = "Sad"
    STRESSED = "Stressed"
    BORED = "Bored"
    ANGRY = "Angry"
    TIRED = "Tired"
    EXCITED = "Excited"
    CONFUSED = "Confused"
    NORMAL = "Normal"


class TimeOfDay(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"


class Weather(str, Enum):
    SUNNY = "Sunny"
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    VERY_HOT = "Very Hot"
    COLD = "Cold"


class FlavorPreference(str, Enum):
    CHOCOLATE = "Chocolate"
    VANILLA = "Vanilla"
    STRAWBERRY = "Strawberry"
    BUTTERSCOTCH = "Butterscotch"
    MANGO = "Mango"
    COOKIES_AND_CREAM = "Cookies & Cream"
    NO_PREFERENCE = "No Preference"


class NecessityLevel(Enum):
    NOT_REQUIRED = (0, 20, "ICE CREAM NOT REQUIRED", "#4facfe", "System in baseline state. Ingestion optional.")
    MILD = (21, 40, "MILD ICE CREAM REQUIREMENT", "#00f5a0", "Minor neuro-dessert craving detected. Preventative intake suggested.")
    MODERATE = (41, 60, "MODERATE ICE CREAM REQUIREMENT", "#ffb703", "Elevated thermal & mental load. Standard cooling protocol advised.")
    HIGH = (61, 80, "HIGH ICE CREAM REQUIREMENT", "#ff7b00", "Significant cognitive strain. Immediate dessert intervention strongly recommended.")
    CRITICAL = (81, 100, "CRITICAL ICE CREAM SITUATION", "#ff3366", "EMERGENCY DESSERT PROTOCOLS RECOMMENDED. IMMEDIATE GLUCOSE-LIPID STABILIZATION MANDATED.")

    def __init__(self, min_score: int, max_score: int, label: str, color: str, dramatic_message: str):
        self.min_score = min_score
        self.max_score = max_score
        self.label = label
        self.color = color
        self.dramatic_message = dramatic_message

    @classmethod
    def from_score(cls, score: int) -> "NecessityLevel":
        clamped = max(0, min(100, score))
        for level in cls:
            if level.min_score <= clamped <= level.max_score:
                return level
        return cls.CRITICAL


@dataclass
class UserInput:
    mood: str = Mood.NORMAL.value
    temperature_c: float = 24.0
    stress_level: int = 50          # 0-100%
    energy_level: int = 50          # 0-100%
    study_hours: float = 4.0        # Hours
    sleep_hours: float = 7.0        # Hours
    time_of_day: str = TimeOfDay.AFTERNOON.value
    weather: str = Weather.SUNNY.value
    preference: str = FlavorPreference.NO_PREFERENCE.value
    notes: str = ""


@dataclass
class FlavorScore:
    name: str
    emoji: str
    compatibility: int              # 0-100%
    reason: str


@dataclass
class ToppingScore:
    name: str
    emoji: str
    compatibility: int              # 0-100%
    reason: str


@dataclass
class QuantityRecommendation:
    scoops: int
    scoops_label: str
    grams_estimate: int
    container: str                  # Cup or Cone
    container_rationale: str
    disclaimer: str = "Serving weights are fictional computational approximations for entertainment."


@dataclass
class AnalysisResult:
    necessity_score: int
    level: NecessityLevel
    dramatic_message: str
    top_flavor: FlavorScore
    runner_up_flavors: List[FlavorScore]
    quantity: QuantityRecommendation
    topping: ToppingScore
    confidence: float               # e.g. 93.5%
    scientific_explanation: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    input_snapshot: Optional[UserInput] = None
