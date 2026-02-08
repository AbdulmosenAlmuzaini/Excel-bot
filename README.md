# Excel & Google Sheets AI Bot

A Telegram bot specialized in helping users with Excel and Google Sheets formulas, shortcuts, and data analysis.

## Features
- **Excel Expert**: Answers ONLY Excel and Sheets related questions.
- **Multilingual**: Supports Arabic and English.
- **Excel Analysis**: Upload `.xlsx` or `.csv` for insights and forecasting.
- **Usage Limits**: Daily quotas per user.
- **FAQ Cache**: Quick answers for common formulas.

## Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install python-telegram-bot pandas openpyxl httpx python-dotenv
   ```
3. Create a `.env` file based on `.env.example` and add your tokens.
4. Run the bot:
   ```bash
   python bot.py
   ```

## Admin Commands
- `/stats`: View user count and interaction logs.
