import time
import logging
from src.config import Config
from src.whatsapp_driver import WhatsAppDriver
from src.bot_logic import BotHandler

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    driver = WhatsAppDriver()
    bot = BotHandler()
    
    # Target specific group defined in config
    target_group = "The Real Ogs" # Or load from Config
    
    try:
        logging.info("Waiting for WhatsApp Web login...")
        time.sleep(15) # Give time for QR scan if needed or cache load

        if driver.select_chat(target_group):
            logging.info(f"Connected to {target_group}")
            
            last_processed_msgs = set()
            
            while True:
                # 1. Get Context
                messages = driver.get_last_messages(limit=5)
                
                # 2. Check if there is a new message (Simplified logic)
                if not messages:
                    time.sleep(2)
                    continue

                latest_msg = messages[-1]
                
                if latest_msg not in last_processed_msgs:
                    logging.info(f"New Message: {latest_msg}")
                    
                    # 3. Process Logic
                    # (In a real scenario, you'd parse the sender from the HTML too)
                    response = bot.process_message(latest_msg, sender_number="Unknown", context=messages)
                    
                    # 4. Respond
                    if response:
                        logging.info(f"Responding: {response}")
                        driver.send_message(response)
                        # Add response to processed set so we don't reply to ourselves immediately
                        last_processed_msgs.add(response) 
                    
                    last_processed_msgs.add(latest_msg)
                
                time.sleep(5) # Poll interval
        
    except KeyboardInterrupt:
        logging.info("Stopping bot...")
    except Exception as e:
        logging.error(f"Critical error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()