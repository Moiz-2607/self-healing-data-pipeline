import os

from dotenv import load_dotenv


load_dotenv()


AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "")

ALERT_PROVIDER = os.getenv("ALERT_PROVIDER", "console")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
