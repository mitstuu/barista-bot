import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BARISTA_BOT_TOKEN')
from datetime import datetime, timezone, timedelta

# Replace CHANNEL_ID with the ID of the channel where you want to display the kick message
bonk_CHANNEL_ID = 934288549946216541
general_CHANNEL_ID = 934288549266739224

#@Welcomers role ID

ROLE_ID = 934288548474007576

# Replace TOKEN with your bot's token
TOKEN = os.environ['BARISTA_BOT_TOKEN']

# Create a new Discord client instance
#intents = discord.Intents.default()
#intents.members = True
intents = discord.Intents.all()
client = commands.Bot(command_prefix='b!', intents=intents)


# Set the cooldown duration to 30 minutes (1800 seconds)
#cooldown_duration = commands.Cooldown(rate=1, per=1800, type=commands.BucketType.member)

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

    await ctx.send(embed=embed)


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

#Welcome message command

# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(general_CHANNEL_ID)
#     role = member.guild.get_role(ROLE_ID)
#     await channel.send(f'Welcome {member.mention} to the server! {role.mention}s assemble!')

# Define the ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: `{round(client.latency * 1000)}ms`')


@client.command()
@commands.cooldown(1, 1800, commands.BucketType.member)  # Apply the cooldown to the command
async def revivechat(ctx):
    channel = ctx.channel
    role = ctx.guild.get_role(934288548474007577)
    member = ctx.author
    await channel.send(f'{member.mention} would like to revive this chat. {role.mention}s assemble!')

# Error handling for the revivechat command cooldown
@commands.Cog.listener()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = error.retry_after
        minutes = remaining // 60
        seconds = remaining % 60
        await ctx.send(f"This command is on cooldown. Please try again in {minutes} minutes and {seconds} seconds.")

# Start the bot
client.run(TOKEN)
