import discord
from discord.ext import commands
import datetime

from numpy import delete

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Warns a member."""
        await ctx.send(f'{member.mention} has been warned for {reason}.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked from the server.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned from the server.')

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """Mutes a member for a specified duration."""
        timenow: datetime.datetime = datetime.datetime.now()
        await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
        await ctx.send(f'{member.mention} has been muted for {duration} minutes.')

    @commands.command()
    @commands.has_permissions(unmute_members=True)
    async def unmute(self, ctx, member: discord.Member, reason=None):
        """Unmutes a member."""
        await member.timeout(None, reason=reason)
        await ctx.send(f'{member.mention} has been unmuted.')

    @commands.command()
    @commands.has_permissions(unban=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        """Unbans a member from the server."""
        await member.unban(reason=reason)
        await ctx.send(f'{member.mention} has been unbanned from the server.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount_to_check=1000, user=None, amount_to_delete=0):
        """Deletes a specified amount of messages."""
        deleted_from_user = 0
        def is_user(m):
            nonlocal deleted_from_user
            if (m.author == user or user==None) and deleted_from_user < amount_to_delete:
                deleted_from_user += 1
                return True
            return False 
        
        deleted = await ctx.channel.purge(limit=amount_to_check, check=is_user)
        await ctx.send(f'{len(deleted)} messages have been deleted.')

def setup(bot):
    bot.add_cog(Moderation(bot))