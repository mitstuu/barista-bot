import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from typing import Union
from discord import Client, Game
import math
from discord import app_commands
#from discord.ext import menus

class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ids: dict[str, int] = {
        'bonk_channel'      :   934288549946216541,
        'general_channel'   :   934288549266739224,
        'chat_reviver'      :   934288548474007577,
        }

    # async def cog_load(self):
    #     self.bot.tree.add_command(self.ping_slash)

    @commands.command()
    async def hello(self, ctx):
        """ Say hello to the bot """
        await ctx.send("Hello, user!")

    # Existing text command can be removed or kept for fallback:
    # @commands.command()
    # async def ping(self, ctx):
    #     """Get the bot's latency"""
    #     await ctx.send(f'Pong! Latency: `{round(self.bot.latency * 1000)}ms`')

    # New slash command replacing b!ping:
    # @app_commands.command(name="ping", description="Get the bot's latency")
    # async def ping_slash(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f'Pong! Latency: {round(self.bot.latency * 1000)} ms')

    @commands.command(name='serverinfo')
    async def server_info(self, ctx):
        """ Get information about the server """
        server = ctx.guild
        number_of_text_channels = len(server.text_channels)
        number_of_voice_channels = len(server.voice_channels)
        server_description = server.description
        number_of_people = server.member_count
        server_name = server.name
        server_picture = server.icon.url if server.icon else None
        # Create the embed
        embed = discord.Embed(title=server_name, description=server_description, color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
        if server_picture:
            embed.set_thumbnail(url=server_picture)
        embed.add_field(name="Members", value=number_of_people)
        embed.add_field(name="Text Channels", value=number_of_text_channels)
        embed.add_field(name="Voice Channels", value=number_of_voice_channels)
        embed.set_footer(text="Sent:")

        await ctx.send(embed=embed)

    # Define the userinfo command
    @commands.command(name='userinfo')
    async def user_info(self, ctx, target: Union[discord.Member, None] = None):
        """ Get information about a user """
        target = target or ctx.author
        user_roles = [role for role in target.roles]
        embed = discord.Embed(title="User information", color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar)
        embed.set_footer(text="Sent")
        embed.add_field(name="ID:", value=target.id, inline=False)
        embed.add_field(name="Name:", value=target.display_name, inline=False)
        embed.add_field(name="Created at:", value=target.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        if target.joined_at is not None:
            embed.add_field(name="Joined at:", value=target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name=f"Roles ({len(user_roles)})", value=" ".join([role.mention for role in user_roles]), inline=False)
    
        await ctx.send(embed=embed)

    # Define the revivechat command
    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.guild)  # Apply the cooldown to the command
    async def revivechat(self, ctx):
        """ Revive the chat """
        # Get the role
        role = ctx.guild.get_role(self.ids['chat_reviver'])
        await ctx.send(f'{ctx.author.mention} would like to revive this chat. {role.mention}s assemble!')

    @revivechat.error
    async def revivechat_error(self, ctx, error):
        minutes = 0
        seconds = 0
        if isinstance(error, commands.CommandOnCooldown):
            remaining: float = error.retry_after
            minutes: int = math.floor(remaining // 60) 
            seconds: int = math.floor(remaining % 60)
        await ctx.send(f"`b!revivechat` is in cooldown mode. Please try again in {minutes} minutes and {seconds} seconds.")

    # Define the help command
    @commands.command()
    async def commandhelp(self, ctx):
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
        embed.add_field(name="b!serverinfo", value="Displays information about the server")
        embed.add_field(name="b!userinfo", value="Displays information about a user")
        embed.add_field(name="b!ping", value="Displays the bot's current latency")
        embed.add_field(name="b!revivechat", value="Asks the Welcomers to revive the chat")
        embed.set_footer(text="Sent:")
        await ctx.send(embed=embed)



# class HelpMenu(menus.ListPageSource):
#     def __init__(self, data):
#         super().__init__(data, per_page=5)  # Change this to control how many items per page

#     async def format_page(self, menu, entries):
#         offset = menu.current_page * self.per_page
#         embed = discord.Embed(title="Help", description="List of available commands:")
#         for i, command in enumerate(entries, start=offset):
#             embed.add_field(name=command[0], value=command[1], inline=False)
#         return embed

# @commands.command()
# async def commandhelp(self, ctx):
#     data = [
#         ("b!serverinfo", "Displays information about the server"),
#         ("b!userinfo", "Displays information about a user"),
#         ("b!ping", "Displays the bot's current latency"),
#         ("b!revivechat", "Asks the Welcomers to revive the chat"),
#         # Add more commands here
#     ]
#     pages = menus.MenuPages(source=HelpMenu(data), clear_reactions_after=True)
#     await pages.start(ctx)



async def setup(client: commands.Bot):
    await client.add_cog(UserCommands(client))