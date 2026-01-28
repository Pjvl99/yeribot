from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import logging
from .config import Config

class WhatsAppDriver:
    def __init__(self):
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 30)

    def _init_driver(self):
        logging.info("Initializing Firefox Driver...")
        opts = Options()
        opts.binary_location = Config.FIREFOX_BINARY
        opts.add_argument("--profile")
        opts.add_argument(Config.PROFILE_PATH)
        
        service = Service(Config.GECKODRIVER)
        driver = webdriver.Firefox(service=service, options=opts)
        driver.get("https://web.whatsapp.com/")
        return driver

    def select_chat(self, chat_name: str) -> bool:
        """Searches for a chat and clicks it."""
        try:
            # 1. Search Box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(chat_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2) # Wait for UI load
            return True
        except Exception as e:
            logging.error(f"Could not select chat {chat_name}: {e}")
            return False

    def get_last_messages(self, limit: int = 5) -> list[str]:
        """Scrapes the visible messages in the current chat."""
        try:
            # Generic selector for message containers
            msg_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.message-in, div.message-out')
            recent = msg_elements[-limit:]
            
            extracted = []
            for msg in recent:
                try:
                    # Try to find text content
                    text_el = msg.find_element(By.CSS_SELECTOR, 'span.selectable-text')
                    extracted.append(text_el.text)
                except:
                    continue # Skip image-only or system messages
            return extracted
        except Exception as e:
            logging.error(f"Error reading messages: {e}")
            return []

    def send_message(self, text: str):
        try:
            input_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
            )
            # Use clipboard for emoji support and speed
            pyperclip.copy(text)
            input_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

    def quit(self):
        self.driver.quit()