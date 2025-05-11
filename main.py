import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from twscrapper import get_tweet
from flask import Flask
from threading import Thread

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route('/')
def home():
    return "Discord bot is running."

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

previd = None

async def tweet_watcher(channel):
    global previd
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            tweet = await get_tweet(previd)
            if tweet:
                previd = tweet['id']
                message = f"\n{tweet['body']}\n🔗 {tweet['link']}"
                await channel.send(message)
        except Exception as e:
            print(f"Error fetching/sending tweet: {e}")
        await asyncio.sleep(1800)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user.name}")
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot is now online!")
        bot.loop.create_task(tweet_watcher(channel))
    else:
        print("Channel not found.")

# Start Flask in thread, then run bot
if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)