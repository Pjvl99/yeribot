import requests
import json
import re
from typing import List, Optional
from .config import Config

class AIService:
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    @staticmethod
    def generate_persona_prompt(context: List[str]) -> str:
        """Constructs the system prompt."""
        chat_history = "\n- ".join(context)
        return f"""
        You are {Config.BOT_NAME}, a friendly assistant.
        Respond in Spanish. Use emojis.
        
        Context:
        {chat_history}
        
        Respond ONLY using JSON format:
        {{
            "response_text": "Your text here",
            "should_reply": true/false
        }}
        """

    def ask(self, context: List[str]) -> Optional[str]:
        prompt = self.generate_persona_prompt(context)
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {
            'Content-Type': 'application/json', 
            'X-goog-api-key': Config.GEMINI_KEY
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean Markdown code blocks if present
            clean_text = raw_text.strip().replace('```json', '').replace('```', '')
            data = json.loads(clean_text)
            
            if data.get("should_reply"):
                return data.get("response_text")
            return None
            
        except Exception as e:
            print(f"AI Service Error: {e}")
            return None