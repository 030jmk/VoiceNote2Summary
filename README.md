# VoiceNote2Summary Telegram Bot
The bot is built using the python-telegram-bot library and leverages OpenAI's API for both audio transcription (Whisper) and text summarization. 
It's an excellent tool for quickly converting spoken or recorded information into written summaries for meeting notes, lectures, or any audio content that users wish to distill into text.
In other words, I got annoyed that friends and family would send me voice notes and voice messages as answers to questions that could have been answered with an absolute yes or no. (Still love you guys though)

# Features and Usage

- Users can send audio files to the bot, which will then be transcribed into text using OpenAI's Whisper model.
- Users can request a summary of the text, which the bot provides using either OpenAI's GPT-3.5 or GPT-4 model to condense the info.
- super simple authorization mechanism, ensuring that only users with specified IDs can interact with it.

# Setup 
- Clone the repository to your local machine.
- Ensure you have Python 3.10+ installed.
- Install required dependencies by running `pip install -r requirements.txt` in your terminal.
- Set the environment variables `TELEGRAM_TOKEN` with your Telegram bot token and `OPENAI_API_KEY` with your OpenAI API key.
- Run the script using `python voice2summary2.py` to start the bot.
