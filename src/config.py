import os
import json
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

class Config:
    # Paths
    FIREFOX_BINARY = os.getenv("FIREFOX_BINARY_PATH")
    GECKODRIVER = os.getenv("GECKODRIVER_PATH")
    PROFILE_PATH = os.getenv("FIREFOX_PROFILE_PATH")
    
    # Credentials
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    GCP_PROJECT = os.getenv("GCP_PROJECT_ID")
    
    # Bot Settings
    BOT_NAME = os.getenv("BOT_NAME", "Bot")
    ADMINS: List[str] = os.getenv("ADMIN_NUMBERS", "").split(",")
    
    # Group Mapping (Logical Name -> WhatsApp Title/Alt Text)
    GROUPS: Dict[str, str] = json.loads(os.getenv("GROUP_MAPPINGS", "{}"))
    
    # Database Tables (Mapping logical names to BQ tables)
    TABLES: Dict[str, str] = {
        "terciopelo": "whatsapp.terciopelo",
        "platica": "whatsapp.platica",
        # Add others as needed
    }