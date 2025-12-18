import anthropic
from app.config import settings

class ClaudeService:
    def __init__(self):
        # Initialize with API key if available, otherwise it might fail on request
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-haiku-20240307" # Most widely available model
    
    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096):
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise e
    
    async def generate_with_history(self, system_prompt: str, messages: list, max_tokens: int = 4096):
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise e
