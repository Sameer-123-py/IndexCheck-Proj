import httpx

from .config import HARVEY_API_KEY, HARVEY_BASE_URL, HARVEY_ENDPOINT, HARVEY_TIMEOUT
from .logger import get_logger
from .retries import retry_harvey_call

logger = get_logger(__name__)


class HarveyClient:
    def __init__(self):
        self.base_url = HARVEY_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {HARVEY_API_KEY}",
        }

    @retry_harvey_call
    def complete(self, prompt: str, system_message: str = None) -> str:
        """
        Sends a text completion request to Harvey API.
        This is adapted for text-based prompts (not document extraction).
        Automatically retries up to 3 times on timeout / network errors.
        
        Args:
            prompt (str): The user prompt/message
            system_message (str, optional): System message for context
            
        Returns:
            str: The completion response from Harvey
        """
        
        # Combine system message and prompt if system message is provided
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        data = {
            "prompt": full_prompt,
            "stream": False,  # Boolean instead of string
            "mode": "assist",
        }

        url = f"{self.base_url}{HARVEY_ENDPOINT}"

        try:
            with httpx.Client(timeout=HARVEY_TIMEOUT) as client:
                response = client.post(
                    url,
                    headers=self.headers,
                    data=data,  # Use data instead of json for form-encoded
                )

            response.raise_for_status()

            result = response.json()

            logger.info("Harvey response received")

            return result.get("response", result)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Harvey API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Harvey API error: {str(e)}")
            raise
