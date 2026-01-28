# WhatsApp AI Bot (Selenium + Gemini + BigQuery)

A modular Python automation bot for WhatsApp Web that integrates Google's Gemini AI for conversation and BigQuery for data persistence.

## Features
- **Automated Interaction**: Uses Selenium to control a real WhatsApp Web instance.
- **AI Persona**: Integrated with Google Gemini 2.5 Flash for natural language responses.
- **Data Analysis**: Connects to Google BigQuery to fetch and store user stats.
- **Modular Design**: Separation of concerns (Driver, AI, Database, Logic).

## Prerequisites

1. **Python 3.9+**
2. **Firefox Browser** installed.
3. **Google Cloud Account** with BigQuery and Vertex AI/Gemini API enabled.
4. **Service Account JSON** for Google Cloud.

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/whatsapp-bot.git](https://github.com/Pjvl99/yeribot)
   cd whatsapp-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Create requirements.txt with: `selenium`, `google-cloud-bigquery`, `pandas`, `requests`, `python-dotenv`, `pyperclip`)*

3. **Environment Setup:**
   Copy `env.example` to `.env` and fill in your details:
   ```bash
   cp env.example .env
   ```

   **Important:** You need to locate your Firefox Profile path to persist your WhatsApp Web login session.
   - *Linux:* `~/.mozilla/firefox/xxxx.default-release`
   - *Windows:* `%APPDATA%\Mozilla\Firefox\Profiles\`

## Usage

1. **Start the Bot:**
   ```bash
   python main.py
   ```

2. **First Run:**
   - The browser will open.
   - Scan the WhatsApp QR code (if not using a persistent profile that is already logged in).
   - The bot will navigate to the configured chat and start listening.

## Project Structure

- `src/whatsapp_driver.py`: Handles Selenium interactions (DOM manipulation).
- `src/ai_service.py`: Wrapper for Gemini API calls.
- `src/bot_logic.py`: The brain of the bot (decides when to reply).
- `src/database.py`: Handles SQL queries.

## Disclaimer

This project is for educational purposes. Automated interaction with WhatsApp may violate their Terms of Service. Use at your own risk.
