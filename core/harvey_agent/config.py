import os

HARVEY_API_KEY = os.environ.get("HARVEY_API_KEY")

if not HARVEY_API_KEY:
    raise ValueError("HARVEY_API_KEY environment variable not set")

HARVEY_BASE_URL = os.environ.get(
    "HARVEY_BASE_URL",
    "https://eu.api.harvey.ai",
)

HARVEY_ENDPOINT = "/api/v2/completion"

HARVEY_TIMEOUT = int(os.environ.get("HARVEY_TIMEOUT", "240"))
