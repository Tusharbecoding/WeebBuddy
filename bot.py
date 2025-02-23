import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
from aiohttp import web
import asyncio

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MAL_CLIENT_ID = os.getenv('MAL_CLIENT_ID')
PORT = int(os.getenv('PORT', 8080))  # Use PORT from environment or default to 8080

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to fetch anime recommendations
def get_anime_recommendations(genre=None):
    base_url = "https://api.myanimelist.net/v2/anime"
    headers = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}
    
    url = f"{base_url}?q={genre}&limit=5"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        anime_list = response.json().get('data', [])
        return anime_list
    else:
        return None

# Bot command to recommend anime
@bot.command(name="recommend_anime")
async def recommend_anime(ctx, genre: str = None):
    try:
        recommendations = get_anime_recommendations(genre)
        if recommendations:
            for anime in recommendations:
                anime_info = anime['node']
                title = anime_info.get('title', 'Title not available')
                main_picture = anime_info.get('main_picture', {}).get('large', 'No image available')

                message = f"**{title}**\n[Click here to view]({main_picture})"
                await ctx.send(message)
        else:
            await ctx.send("No recommendations found. Try a different genre!")
    except Exception as e:
        await ctx.send("Error fetching recommendations.")
        print(f"Error: {e}")

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is now running.')

# Function to handle the web server for Render
async def handle(request):
    return web.Response(text="Bot is running.")

# Start the web server in a separate async loop
async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)  # Bind to PORT variable
    await site.start()

# Run both the bot and web server
loop = asyncio.get_event_loop()

# Run web server in the background
loop.create_task(start_web_server())

# Run the bot
bot.run(DISCORD_TOKEN)
