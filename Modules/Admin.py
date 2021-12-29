import nextcord, datetime, humanfriendly
from nextcord.ext import commands
from Functions.Permission import permissionCheck

class Admin(commands.Cog):
    """The Admin commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(
        name = "timeout",
        description = "⏱️ Timeout a user ( Basically mute them )",
        guild_ids = [904958479574401064]
    )
    async def timeout(
        self, interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(name = "user", description = "The user you want to timeout", required = True),
        time: str = nextcord.SlashOption(name = "time", description = "How long do you want to timeout the user?", required = True)
    ):
        if not permissionCheck(interaction.user, interaction, 'can_timeout'): 
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return
        
        await user.edit(timeout = nextcord.utils.utcnow()+datetime.timedelta(seconds = humanfriendly.parse_timespan(time)))

        embed = nextcord.Embed(
            description = f"\✅ {user.mention} was timed out for `{time}`.",
            color = nextcord.Colour.green()
        )
        await interaction.response.send_message(embed = embed)
    
def setup(bot: commands.Bot): bot.add_cog(Admin(bot))