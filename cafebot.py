import asyncio
import discord
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

cogs = ['user_commands', 'admin_commands', 'mod_commands', 'fun_commands', 'music_commands', 'economy_commands', 'games_commands', 'help_commands', 'error_handler']

TOKEN = os.getenv('BARISTA_BOT_TOKEN')

@client.event
async def on_ready_event():
    await client.change_presence(activity=Game(name="with the API"))
    #await client.load_extension('user_commands')
    # await client.load_extension('admin_commands')
    # await client.load_extension('mod_commands')
    # await client.load_extension('fun_commands')
    # await client.load_extension('music_commands')
    # await client.load_extension('economy_commands')
    # await client.load_extension('games_commands')
    # await client.load_extension('help_commands')
    # await client.load_extension('error_handler')

# Replace CHANNEL_ID with the ID of the channel where you want to display the kick message

ids: dict[str, int] = {
    'bonk_channel'      :   934288549946216541,
    'general_channel'   :   934288549266739224,
    'role'              :   934288548474007576,
}
bonk_CHANNEL_ID = 934288549946216541
general_CHANNEL_ID = 934288549266739224



#@Welcomers role ID

ROLE_ID = 934288548474007576

# Replace TOKEN with your bot's token
TOKEN = os.environ['BARISTA_BOT_TOKEN']


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="with the API"))

# Set the cooldown duration to 30 minutes (1800 seconds)
#cooldown_duration = commands.Cooldown(rate=1, per=1800, type=commands.BucketType.member)

#   Info commands

# Define the serverinfo command
@client.command(name='serverinfo')
async def server_info(ctx):
    server = ctx.guild
    number_of_text_channels = len(server.text_channels)
    number_of_voice_channels = len(server.voice_channels)
    server_description = server.description
    number_of_people = server.member_count
    server_name = server.name
    server_picture = server.icon.url if server.icon else None

    embed = discord.Embed(title=server_name, description=server_description, color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
    if server_picture:
        embed.set_thumbnail(url=server_picture)
    embed.add_field(name="Members", value=number_of_people)
    embed.add_field(name="Text Channels", value=number_of_text_channels)
    embed.add_field(name="Voice Channels", value=number_of_voice_channels)

    embed.set_footer(text="Sent:")
    await ctx.send(embed=embed)

# Define the userinfo command
@client.command(name='userinfo')
async def user_info(ctx, target: Union[discord.Member, None] = None):
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

    #  Listeners

# Listen for the on_member_join event
@client.event
async def on_member_join(member):
    # Get the account age of the member in minutes
    age_minutes = (datetime.now(timezone.utc) - member.created_at).total_seconds() // 60
    gchannel = client.get_channel(general_CHANNEL_ID)
    role = member.guild.get_role(ROLE_ID)
    
    if isinstance(gchannel, discord.TextChannel):  # Check if gchannel is a TextChannel
        if age_minutes < 15:
            await member.kick(reason='Account age less than 15 minutes')
            await gchannel.send(f'<@{member.id}> has been kicked for having an account less than 15 minutes old.')
        else:
            await gchannel.send(f'Welcome {member.mention} to the server! {role.mention}s assemble!')


# Define the ping command
# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Pong! Latency: `{round(client.latency * 1000)}ms`')


# Define the revivechat command
@client.command()
@commands.cooldown(1, 1800, commands.BucketType.guild)  # Apply the cooldown to the command
async def revivechat(ctx):
    role = ctx.guild.get_role(934288548474007577)
    await ctx.send(f'{ctx.author.mention} would like to revive this chat. {role.mention}s assemble!')

# Error handling for the revivechat command cooldown
@revivechat.error
async def revivechat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = error.retry_after
        minutes = remaining // 60
        seconds = remaining % 60
        await ctx.send(f"This command is on cooldown. Please try again in {minutes} minutes and {seconds} seconds.")

# Define the help command
@client.command()
async def commandhelp(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.from_rgb(126, 169, 107), timestamp=datetime.utcnow())
    embed.add_field(name="b!serverinfo", value="Displays information about the server")
    embed.add_field(name="b!userinfo", value="Displays information about a user")
    embed.add_field(name="b!ping", value="Displays the bot's current latency")
    embed.add_field(name="b!revivechat", value="Asks the Welcomers to revive the chat")
    embed.set_footer(text="Sent:")
    await ctx.send(embed=embed)


async def main():
    for cog in cogs:
        await client.load_extension(cog)

    await client.start(TOKEN)

# Run the main function
asyncio.run(main())

if __name__ == '__main__':
    client.run(TOKEN)
