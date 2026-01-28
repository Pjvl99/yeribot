import random
from dataclasses import dataclass
from typing import List, Optional
from .database import DatabaseClient
from .ai_service import AIService
from .config import Config

@dataclass
class CommandResult:
    text: str
    attachment_path: Optional[str] = None

class BotHandler:
    def __init__(self):
        self.db = DatabaseClient()
        self.ai = AIService()

    def process_message(self, raw_msg: str, sender_number: str, context: List[str]) -> Optional[str]:
        """Main entry point for processing incoming messages."""
        
        # 1. Check for Explicit Commands
        if raw_msg.startswith(f":{Config.BOT_NAME.lower()}"):
            return self._handle_command(raw_msg, sender_number)
            
        # 2. If no command, check if AI should reply based on context
        # (Only if mentioned or in direct flow - simplified logic)
        return self.ai.ask(context)

    def _handle_command(self, msg: str, sender: str) -> str:
        parts = msg.split()
        if len(parts) < 2:
            return "Available commands: help, stats, community"
        
        cmd = parts[1].lower()
        args = parts[2:]

        if cmd == "help":
            return "🤖 Commands: help, community count, stats"
        
        elif cmd == "community" and args:
            if args[0] == "count":
                df = self.db.query_df(f"SELECT COUNT(1) as cnt FROM {Config.TABLES['terciopelo']}")
                count = df.iloc[0]['cnt'] if not df.empty else 0
                return f"Community members: {count}"
        
        return "Unknown command."