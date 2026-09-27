from src.ai.provider import AIProvider
from src.ai.mock_provider import MockAIProvider
from src.ai.groq_provider import GroqProvider
from src.config import AI_PROVIDER, AI_API_KEY, AI_MODEL


def get_ai_provider() -> AIProvider:
    """Create the configured AI provider."""

    if AI_PROVIDER == "mock":
        return MockAIProvider()

    if AI_PROVIDER == "groq":
        return GroqProvider(
            api_key=AI_API_KEY,
            model=AI_MODEL,
        )

    raise ValueError(
        f"Unsupported AI provider: {AI_PROVIDER}"
    )
