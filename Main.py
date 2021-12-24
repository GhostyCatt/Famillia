import nextcord, os
from nextcord.ext import commands
from dotenv import load_dotenv
from Functions.Config import getConfig
from Functions.Setup import setupBot

class Doge(commands.Bot):
    def __init__(self):
        data = getConfig()
        super().__init__(
            command_prefix = data['Prefix'],
            activity = nextcord.Activity(type = nextcord.ActivityType.playing, name = data["Status"]),
            intents = nextcord.Intents.all()
        )
    async def on_ready(self): print("Connected to discord!")
bot = Doge()

setupBot(bot, getConfig())

load_dotenv('Settings/Secure.env')
bot.run(os.getenv('DiscordToken'))