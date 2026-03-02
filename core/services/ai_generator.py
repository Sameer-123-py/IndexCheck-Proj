from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize AI client based on settings
AI_PROVIDER = getattr(settings, 'AI_PROVIDER', 'openai').lower()

if AI_PROVIDER == 'harvey':
    try:
        from core.harvey_agent.client import HarveyClient
        harvey_client = HarveyClient()
        logger.info("Using Harvey AI for text generation")
    except Exception as e:
        logger.error(f"Failed to initialize Harvey client: {str(e)}")
        raise
else:
    from openai import OpenAI
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    logger.info("Using OpenAI for text generation")


def generate_ai_output(prompt):
    """
    Generate AI description using configured AI provider (OpenAI or Harvey).
    
    Args:
        prompt (str): The full prompt with instrument data
        
    Returns:
        str: Generated description
    """
    try:
        if AI_PROVIDER == 'harvey':
            # Use Harvey AI
            system_message = "You are a financial analyst. Create structured ETF/stock descriptions without markdown."
            response = harvey_client.complete(prompt, system_message)
            
            # Harvey returns response as string or dict
            if isinstance(response, dict):
                content = response.get('response', str(response))
            else:
                content = str(response)
            
            return content.strip()
        else:
            # Use OpenAI (default)
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Create structured ETF/stock descriptions without markdown."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            return content
        
    except Exception as e:
        logger.error(f"{AI_PROVIDER.upper()} API error: {str(e)}")
        raise