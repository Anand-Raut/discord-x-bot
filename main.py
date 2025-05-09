import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from twscrapper import get_tweet


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode= 'w')
intents = discord.Intents.default()
intents.guilds = True  # required for on_ready and accessing guilds
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)

previd = None  # This tracks the last tweet ID

@bot.event
async def on_ready():
    print(f"ready, {bot.user.name}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot is now online!")
        bot.loop.create_task(tweet_watcher(channel))  # Start the task


async def tweet_watcher(channel):
    global previd
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            tweet = await get_tweet(previd)
            if tweet:
                previd = tweet['id']  # Update ID
                message = f"\n{tweet['body']}\n🔗 {tweet['link']}"
                if tweet.get("media"):
                    for media_url in tweet["media"]:
                        await channel.send(media_url)
                await channel.send(message)
        except Exception as e:
            print(f"Error fetching/sending tweet: {e}")
        await asyncio.sleep(3000)  # Check every 30 seconds


bot.run(TOKEN, log_handler= handler, log_level= logging.DEBUG)