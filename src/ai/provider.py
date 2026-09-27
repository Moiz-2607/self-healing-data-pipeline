from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Interface for AI-based pipeline diagnosis."""

    @abstractmethod
    def diagnose(
        self,
        drift: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Analyze a detected pipeline failure and return
        a structured diagnosis.
        """
        raise NotImplementedError
