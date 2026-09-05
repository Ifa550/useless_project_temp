"""Session calculation history manager for ICECREAM OS."""
from dataclasses import dataclass
from typing import List
from engine.models import AnalysisResult, UserInput


@dataclass
class HistoryRecord:
    timestamp: str
    mood: str
    temperature_c: float
    score: int
    level_label: str
    flavor: str
    quantity: str
    result: AnalysisResult
    input_data: UserInput


class HistoryManager:
    """Stores session calculations and supports filtering and clearing."""

    def __init__(self):
        self._records: List[HistoryRecord] = []

    def add_record(self, res: AnalysisResult, inp: UserInput) -> HistoryRecord:
        record = HistoryRecord(
            timestamp=res.timestamp,
            mood=inp.mood,
            temperature_c=inp.temperature_c,
            score=res.necessity_score,
            level_label=res.level.label,
            flavor=f"{res.top_flavor.emoji} {res.top_flavor.name}",
            quantity=res.quantity.scoops_label,
            result=res,
            input_data=inp,
        )
        self._records.insert(0, record)  # Most recent first
        return record

    def get_records(self) -> List[HistoryRecord]:
        return list(self._records)

    def clear(self) -> None:
        self._records.clear()

    def count(self) -> int:
        return len(self._records)
