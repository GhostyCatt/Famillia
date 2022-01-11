import nextcord, datetime, humanfriendly
from nextcord.ext import commands
from Functions.Permission import permissionCheck
from Functions.Response import embed

class Admin(commands.Cog):
    """The Admin commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(
        name = "timeout",
        description = "⏱️ Timeout a user ( Basically mute them )",
        guild_ids = [ 904958479574401064 ]
    )
    async def timeout(
        self, interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(name = "user", description = "The user you want to timeout", required = True),
        time: str = nextcord.SlashOption(name = "time", description = "How long do you want to timeout the user?", required = True)
    ):
        if not permissionCheck(interaction.user, 'can_timeout'): 
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return
        
        await user.edit(timeout = nextcord.utils.utcnow()+datetime.timedelta(seconds = humanfriendly.parse_timespan(time)))
        await embed(1, f"{user.mention} was timed out for `{time}`", target = interaction)
    
    @nextcord.slash_command(
        name = "ban",
        description = "🔨 Ban a user from the server",
        guild_ids = [ 904958479574401064 ]
    )
    async def ban(
        self, interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(name = "user", description = "The user you want to ban", required = True),
        reason: str = nextcord.SlashOption(name = "reason", description = "Why do you want to ban this user?", required = False)
    ):
        if not permissionCheck(interaction.user, 'can_ban'):
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return
        
        await interaction.guild.ban(user, reason = reason if reason else "Banned by moderators!")
        await embed(1, f"{user.mention} was banned from the guild!", target = interaction)
    
    @nextcord.slash_command(
        name = "kick",
        description = "🪓 Kick a user from the server",
        guild_ids = [ 904958479574401064 ]
    )
    async def kick(
        self, interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(name = "user", description = "The user you want to kick", required = True),
        reason: str = nextcord.SlashOption(name = "reason", description = "Why do you want to kick this user?", required = False)
    ):
        if not permissionCheck(interaction.user, 'can_kick'):
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return
        
        await interaction.guild.kick(user, reason = reason if reason else "Kicked by moderators!")
        await embed(1, f"{user.mention} was kicked from the guild!", target = interaction)
    
    @nextcord.slash_command(
        name = "purge",
        description = "🧹 Purge upto 50 messages from a channel",
        guild_ids = [ 904958479574401064 ]
    )
    async def purge(
        self, interaction: nextcord.Interaction,
        limit: int = nextcord.SlashOption(name = "limit", description = "Number of messages to be purged", required = True),
        channel: nextcord.abc.GuildChannel = nextcord.SlashOption(name = "channel", description = "The channel you want to purge", required = False)
    ):
        if not permissionCheck(interaction.user, 'can_purge'):
            await interaction.response.send_message(f"You can't run this command", ephemeral = True)
            return

        if not channel: channel = interaction.channel
        
        if not isinstance(channel, nextcord.TextChannel): 
            await embed(2, f"I can't purge those channels...", target = interaction)
            return
        
        await channel.purge(limit = limit)
        await embed(1, f"{limit} messages were purged from {channel.mention}", target = interaction)

def setup(bot: commands.Bot): bot.add_cog(Admin(bot))