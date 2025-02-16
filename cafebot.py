import asyncio
from re import T
import discord
from discord.abc import PrivateChannel
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import Union
from discord import Game

load_dotenv()

# Create a new Discord client instance
intents = discord.Intents.all()
client = commands.Bot(command_prefix='b!', intents=intents)
# Define the cogs to be loaded
cogs: list[str] = ['user_commands', 'mod_commands']

TOKEN = os.getenv('BARISTA_BOT_TOKEN')

# Replace TOKEN with your bot's token
TOKEN = os.environ['BARISTA_BOT_TOKEN']

# @client.event
# async def on_ready():
#     await client.change_presence(activity=Game(name="with the API"))
#     cafeguild = client.get_guild(934288548474007572)
#     await client.tree.sync(guild=cafeguild)  # sync slash commands with Discord

# bonk_CHANNEL_ID = 934288549946216541
# general_CHANNEL_ID = 934288549266739224
ids: dict[str, int] = {
    'bonk_channel': 934288549946216541,
    'general_channel': 934288549266739224,
    'chat_reviver': 934288548474007577,
    'modlogs_channel': 937500768657887252,
}

# @Welcomers role ID
WELCOMER_ROLE_ID = 934288548474007576

# Listen for the on_member_join event
@client.event
async def on_member_join(member):
    age_minutes = (datetime.now(timezone.utc) - member.created_at).total_seconds() // 60
    gchannel = client.get_channel(ids['general_channel'])
    kick_channel = client.get_channel(ids['modlogs_channel'])
    welcome_role = member.guild.get_role(WELCOMER_ROLE_ID)

    if age_minutes < 15:
        await member.kick(reason='Account age less than 15 minutes')
        if isinstance(kick_channel, discord.TextChannel):
            await kick_channel.send(f'<@{member.id}> has been kicked for having an account less than 15 minutes old.')
    else:
        if isinstance(gchannel, discord.TextChannel):
            await gchannel.send(f'Welcome {member.mention} to the server! {welcome_role.mention}s assemble!')


# # Define the help command
# @client.command()
# async def commandhelp(ctx):
#     embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
#     embed.add_field(name="b!serverinfo", value="Displays information about the server")
#     embed.add_field(name="b!userinfo", value="Displays information about a user")
#     embed.add_field(name="b!ping", value="Displays the bot's current latency")
#     embed.add_field(name="b!revivechat", value="Asks the Welcomers to revive the chat")
#     embed.set_footer(text="Sent:")
#     await ctx.send(embed=embed)


async def main():
    for cog in cogs:
        await client.load_extension(cog)

    if TOKEN is not None:
        await client.start(TOKEN)
    else:
        raise ValueError('No token found. Please set the BARISTA_BOT_TOKEN environment variable.')
    
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="with the API"))
    cafeguild = client.get_guild(934288548474007572)
    client.tree.clear_commands(guild=cafeguild)
    await client.tree.sync(guild=cafeguild)  # sync slash commands with Discord

# Run the main function
asyncio.run(main())

# if __name__ == '__main__':
#     client.run(TOKEN)