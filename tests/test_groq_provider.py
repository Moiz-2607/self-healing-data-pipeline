import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from src.ai.groq_provider import GroqProvider


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@pytest.mark.integration
def test_groq_provider_real_request():
    api_key = os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL")

    assert api_key, "AI_API_KEY was not loaded from .env"
    assert model, "AI_MODEL was not loaded from .env"

    provider = GroqProvider(
        api_key=api_key,
        model=model,
    )

    drift = {
        "has_drift": True,
        "missing_columns": [],
        "unexpected_columns": [],
        "dtype_mismatches": {
            "age": {
                "expected": "int64",
                "actual": "str",
            }
        },
    }

    diagnosis = provider.diagnose(drift)

    assert "issue" in diagnosis
    assert "description" in diagnosis
    assert "suggested_action" in diagnosis
    assert "confidence" in diagnosis
    assert "repair_plan" in diagnosis
