import json
from typing import Any

from openai import OpenAI

from src.ai.provider import AIProvider
from src.ai.response_validator import validate_ai_diagnosis


class GroqProvider(AIProvider):
    """AI diagnosis provider using Groq's OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        if not api_key:
            raise ValueError("Groq API key is required.")

        if not model:
            raise ValueError("Groq model is required.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = model

    def diagnose(
        self,
        drift: dict[str, Any],
    ) -> dict[str, Any]:
        """Ask Groq to diagnose detected schema drift."""

        system_prompt = """
You are a cautious data engineering diagnosis agent.

Analyze the provided schema drift.

You must:
1. Identify the failure type.
2. Explain the failure briefly.
3. Estimate diagnostic confidence from 0.0 to 1.0.
4. Suggest a safe recovery action.
5. Create a repair plan only when the repair is clearly safe.

Never invent columns or datatypes.

Return ONLY valid JSON with this structure:

{
  "issue": "string",
  "description": "string",
  "suggested_action": "string",
  "confidence": 0.0,
  "repair_plan": []
}

For a datatype repair, repair_plan should contain objects like:

{
  "operation": "CONVERT_DTYPE",
  "column": "column_name",
  "from_dtype": "current_type",
  "to_dtype": "expected_type"
}

For high-risk or uncertain problems, use:
"suggested_action": "HUMAN_REVIEW"
and:
"repair_plan": []
"""

        user_prompt = json.dumps(
            {
                "schema_drift": drift,
            },
            indent=2,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Groq returned an empty response.")

        try:
            diagnosis = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Groq returned invalid JSON."
            ) from error

        return validate_ai_diagnosis(diagnosis)
