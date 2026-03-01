from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_ai_output(prompt):
    """
    Generate AI description using OpenAI.
    
    Args:
        prompt (str): The full prompt with instrument data
        
    Returns:
        str: Generated description
    """
    try:
        response = client.chat.completions.create(
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
        logger.error(f"OpenAI API error: {str(e)}")
        raise