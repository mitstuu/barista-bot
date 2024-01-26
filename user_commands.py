import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, user!")

    # Define the ping command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: `{round(self.bot.latency * 1000)}ms`')


def setup(bot):
    bot.add_cog(UserCommands(bot))