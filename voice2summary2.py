from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import requests
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
api_key = os.environ.get("OPENAI_API_KEY")
AUTHORIZED_USERS = [os.environ.get('YOUR_TELEGRAM_ID')]

async def transcribe_audio(file_path, api_key=api_key):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        'model': (None, 'whisper-1'),
        'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')
    }
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()['text']
    else:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_user.id) in AUTHORIZED_USERS:
        await update.message.reply_text('Hi! Send me an audio file, and I will convert it to text. Use /summarize to get a summary of the latest text.')
    else:
        await update.message.reply_text('Sorry, you are not authorized to use this bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_user.id) in AUTHORIZED_USERS:
        await update.message.reply_text('Send me an audio file or use /summarize to summarize the latest transcribed text.')
    else:
        await update.message.reply_text('Sorry, you are not authorized to use this bot.')

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle received audio files, convert to text, and reply."""
    audio_file = await context.bot.get_file(update.message.voice.file_id)
    file_path = 'audio.ogg'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(audio_file.file_path) as resp:
            if resp.status == 200:
                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

    text = await transcribe_audio(file_path)
    context.user_data['recent_text'] = text

    await update.message.reply_text(f'Transcribed Text: \n\n{text}')
    if os.path.exists(file_path):
        os.remove(file_path)
    

async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarize the most recent transcribed text."""
    recent_text = context.user_data.get('recent_text')
    if recent_text and recent_text.strip() != "":
        summary = await generate_summary(recent_text)
        await update.message.reply_text(f'Summary: \n\n{summary}')
    else:
        await update.message.reply_text("No text available to summarize. Please send an audio file first.")

async def generate_summary(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points. Respond in the same language as the text you are receiving."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        summary = response.json()["choices"][0]["message"]["content"]
        return summary.strip()
    else:
        return None

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))
    application.add_handler(CommandHandler("summarize", summarize_text))

    application.run_polling()

if __name__ == '__main__':
    main()
