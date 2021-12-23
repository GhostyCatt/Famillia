import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from Functions.Config import getConfig

class Doge(commands.Bot):
    def __init__(self):
        data = getConfig()

        super().__init__(
            command_prefix = data['Prefix'],
            activity = nextcord.Activity(type = nextcord.ActivityType.playing, name = data["Status"])
        )
    
bot = Doge()

load_dotenv('Settings/Secure.env')
bot.run(os.getenv('DiscordToken'))