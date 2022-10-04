import re
import math
import random

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cogs has been loaded ---------->")

    @commands.command(
        name = 'help', aliases=['h', 'commands'], description="The Help Commands"
    )
    async def help(self, ctx, cog='1'):
        helpEmbed = discord.Embed(
            title = "Help Commands", color= 0x992D22
        )
        helpEmbed.set_thumbnail(url=ctx.author.avatar_url)

        cogs = [c for c in self.client.cogs.keys()]
        cogs.remove('Misc')

        totalpages = math.ceil(len(cogs) / 4)

        cog = int(cog)
        if cog > totalpages or cog < 1:
            await ctx.send(f"Invalid page number : {cog}. Please pick from {totalpages} pages. \nAlternatively, simply run help command.")
            return

        neededCogs = []
        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass

        for cog in neededCogs:
            commandList = ""
            for command in self.client.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent != None:
                    continue

                commandList += f"**{command.name}** - *{command.description}*\n"

            commandList += "\n"

            helpEmbed.add_field(name=cog, value=commandList, inline=False)

        await ctx.send(embed=helpEmbed)

def setup(client):
    client.add_cog(Help(client))