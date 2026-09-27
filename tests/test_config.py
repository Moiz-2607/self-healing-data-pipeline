from src.config import AI_PROVIDER, AI_API_KEY, AI_MODEL


def test_ai_provider():
    assert AI_PROVIDER in {"mock", "groq"}


def test_ai_api_key_is_string():
    assert isinstance(AI_API_KEY, str)


def test_ai_model_is_string():
    assert isinstance(AI_MODEL, str)
