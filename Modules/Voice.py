import nextcord, random, json
from nextcord.ext import commands
from Functions.Response import embed
from Functions.Permission import permissionCheck
from Functions.Integration import DiscordInteraction

class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(
        name = "song",
        description = "🎶 Pick out a song from the database",
        guild_ids = [ 904958479574401064 ]
    )
    async def song(
        self, interaction: nextcord.Interaction,
        filter: str = nextcord.SlashOption(name = "filter", description = "Name of an artist / genre [ TODO ]", required = False)
    ):
        if not permissionCheck(interaction.user, 'use_song'): 
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return

        if not filter:
            with open("Data/Songs.json") as raw_data: song_data: dict = json.load(raw_data)
        else: 
            with open("Data/Songs.json") as raw_data: song_data: dict = json.load(raw_data)
        song: str = random.choice(list(song_data.keys()))

        await embed(3, f"Artist: **{song_data[song]['Artist'].capitalize()}**\n\nAdded By: {song_data[song]['Added By']}\nLink: [Click Here]({song_data[song]['Link']})", title = song.capitalize(), target = interaction)
    
    @nextcord.slash_command(
        name = "add_song",
        description = "📝 Add a new song to the bot",
        guild_ids = [ 904958479574401064 ]
    )
    async def addsong(
        self, interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(name = "name", description = "Name of the song", required = True),
        artist: str = nextcord.SlashOption(name = "artist", description = "Name of the artist", required = True),
        link: str = nextcord.SlashOption(name = "link", description = "A spotify / youtube link to the song", required = True),
    ):
        if not permissionCheck(interaction.user, 'can_add-song'): 
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return

        with open("Data/Songs.json") as raw_data: song_data: dict = json.load(raw_data)

        if name.lower() in song_data.keys(): 
            await embed(2, description = "This song is already in the database", target = interaction)
            return 
        
        song_data[name.lower()] = {
            "Link": link,
            "Added By": str(interaction.user.name),
            "Artist": artist.lower()
        }

        with open("Data/Songs.json", "w") as raw_writable: json.dump(song_data, raw_writable, indent = 4)

        await embed(1, f"Added **{name}** to the database!", target = interaction)
    
    @nextcord.slash_command(
        name = "remove_song",
        description = "🔐 Remove a song from the database",
        guild_ids = [ 904958479574401064 ]
    )
    async def delsong(
        self, interaction: nextcord.Interaction,
        filter: str = nextcord.SlashOption(name = "filter", description = "Name of the song", required = True)
    ):
        if not permissionCheck(interaction.user, 'can_remove-song'): 
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return
        
        with open("Data/Songs.json") as raw_data: song_data: dict = json.load(raw_data)

        if filter.lower() in song_data.keys(): 
            song_data.pop(filter.lower())
            with open("Data/Songs.json", "w") as raw_writable: json.dump(song_data, raw_writable, indent = 4)

            await embed(1, description = f"Removed **{filter.capitalize()}** from the database", target = interaction)
            return 

        emb = await embed(2, description = "I couldn't find that song in the database... Try to check for spelling errors and try again!")
        await interaction.response.send_message(embed = emb, ephemeral = True)
    
    @nextcord.slash_command(
        name = "game",
        description = "⚡ Start a game activity!",
        guild_ids = [ 904958479574401064 ]
    )
    async def  game(
        self, interaction: nextcord.Interaction, 
        game: str = nextcord.SlashOption(
            name = "game", 
            description = "The game you want to start", 
            required = True, 
            choices = { 
                "Poker": "poker", 
                "Chess": "chess", 
                "Fishing": "fishing", 
                "Betrayal": "betrayal",
                "Letter Tile": "letter-tile",
                "Word Snack": "word-snack",
                "Doodle Crew": "doodle-crew",
                "Spellcast": "spellcast",
                "Awkword": "awkword",
                "Checkers": "checkers"
            }
        )
    ):
        """Start a game activity"""
        if not interaction.user.voice: return await interaction.response.send_message("You aren't in a voice channel!", ephemeral = True)
        else: channel = interaction.user.voice.channel

        Control = DiscordInteraction(self.bot)
        Link = await Control.new(channel.id, game)

        embed = nextcord.Embed(
            title = f"{game.capitalize()}",
            description = f"Created a new {game.capitalize()} party!\n\nTo get started or join, click **[here](https://discord.gg/{Link})**",
            color = nextcord.Colour.random()
        )
        await interaction.response.send_message(f"https://discord.gg/{Link}", embed = embed)
    
    @nextcord.slash_command(
        name = "youtube",
        description = "▶️ Start a youtube activity in your channel!",
        guild_ids = [ 904958479574401064 ]
    )
    async def  youtube(
        self, interaction: nextcord.Interaction
    ):
        """Start a youtube activity"""
        if not interaction.user.voice: return await interaction.response.send_message("You aren't in a voice channel!", ephemeral = True)
        else: channel = interaction.user.voice.channel

        Control = DiscordInteraction(self.bot)
        Link = await Control.new(channel.id, 'youtube')

        embed = nextcord.Embed(
            title = f"YouTube",
            description = f"Created a new YouTube party!\n\nTo get started or join, click **[here](https://discord.gg/{Link})**",
            color = nextcord.Colour.random()
        )
        await interaction.response.send_message(f"https://discord.gg/{Link}", embed = embed)

def setup(bot: commands.Bot): bot.add_cog(Voice(bot))