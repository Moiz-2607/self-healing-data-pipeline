from typing import Any

from src.ai.provider import AIProvider
from src.diagnosis.diagnosis_engine import diagnose_drift


class MockAIProvider(AIProvider):
    """
    Deterministic AI provider used for development and testing.

    It follows the same interface that a real LLM provider
    will use later.
    """

    def diagnose(
        self,
        drift: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a structured diagnosis for the detected drift."""

        return diagnose_drift(drift)
