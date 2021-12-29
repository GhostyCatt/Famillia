import os, json
from nextcord.ext import commands

from Functions.Config import resetConfig

def setupBot(bot: commands.Bot, config_data: dict):
    # Reset Mode
    if config_data["Launch Settings"]["Reset Mode"] == True:
        resetConfig()

        with open("Data/Bot.json", "r") as raw_botdata: botdata = json.load(raw_botdata)
        botdata["Runs"] == 0
        with open("Data/Bot.json", "w") as writable_botdata: json.dump(botdata, writable_botdata, indent = 4)
        exit()

    # Config Validity
    if config_data['Roles'] == None or config_data['Users'] == None: 
        print("ALERT: The config file isn't fully setup!")
        exit()

    # Normal Run
    with open("Data/Bot.json", "r") as raw_botdata: botdata = json.load(raw_botdata)
    botdata["Runs"] += 1
    with open("Data/Bot.json", "w") as writable_botdata: json.dump(botdata, writable_botdata, indent = 4)

    try: bot.load_extension('jishaku')
    except Exception as e: print(e)

    for filename in os.listdir("Modules/"):
        if filename.endswith(".py"):
            try: bot.load_extension(f"Modules.{filename[:-3]}")
            except Exception as error: print(error)