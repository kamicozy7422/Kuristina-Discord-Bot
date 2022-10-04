import discord
from discord.ext import commands

class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is online')

    #Commands
    @commands.command(name="ping", description="Returns ping of the bot.")
    async def ping(self, ctx):
        await ctx.send(f'!Pong {round(self.client.latency * 1000)}ms')

    @commands.command(name="clear", description="Deletes the chat.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount +1)

    @commands.command(name="kick", description="Kick the member from the guild.")
    @commands.has_permissions(manage_messages=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @commands.command(name="ban", description="Bans the member from the guild.")
    @commands.has_permissions(manage_messages=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @commands.command(name="unban", description="Unban the member from the guild.")
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

def setup(client):
    client.add_cog(General(client))
