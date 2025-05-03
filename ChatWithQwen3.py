import discord
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
# Qwen 3 API URL
QWEN_API_URL = os.getenv("QWEN3_API_URL")

# Intents設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!chat '):
        prompt = message.content[len('!chat '):].strip()

        # Qwenに送信するPayload
        payload = {
            "model": "qwen3:latest",
            "prompt": prompt,
            "stream": False
        }

        try:
            # Qwen APIにリクエスト
            response = requests.post(QWEN_API_URL, json=payload, timeout=180)  
            response.raise_for_status()

            # レスポンスからtextを抽出し、<think>タグを削除
            text = response.json()['response']
            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

            if cleaned_text:
                await message.channel.send(cleaned_text)
            else:
                await message.channel.send("Qwenから返答がありませんでした。")

        except Exception as e:
            print("Error:", e)
            await message.channel.send("Qwen APIとの通信でエラーが発生しました。")

# Discord botの起動
client.run(DISCORD_TOKEN)
