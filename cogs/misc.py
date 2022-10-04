import discord
from discord.ext import commands
import os
import requests
from PIL import Image
from io import BytesIO
from math import *
from disputils import BotEmbedPaginator

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cogs has been loaded ---------->")

    @commands.command(aliases=["av","avatar"])
    async def pfp(self,ctx):
        members=ctx.message.mentions
        if members==[]:members=[ctx.author]
        imgs=[]
        
        for mem in members:
            url = requests.get(mem.avatar_url)
            im = Image.open(BytesIO(url.content)).resize((500,500))
            imgs.append(im)
        s=len(imgs)
        bg = Image.new(mode = "RGBA", size = (500*s, 500))
        i=0
        for x in range(0,s):
            try:
                bg.paste(imgs[i],(500*x,0))
                i+=1
            except Exception as e:
                print(e,i)
                pass
        bg.save(f'images/generated/{ctx.author.id}.png',quality=10)
        file = discord.File(f"images/generated/{ctx.author.id}.png",filename='pic.jpg')
        emb=discord.Embed(title="",description=f"",color=0xFF0055)
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)
        #await ctx.send(file=file)
        os.system(f"rm -rf images/generated/{ctx.author.id}.png")

    @commands.command()
    async def stats(self,ctx):
        emb = discord.Embed(title="**Kuristina Stats**",color=0xFB0515)
        emb.add_field(name="Total Servers",value=str(len(self.client.guilds)),inline=False)
        emb.add_field(name="Latency(s)",value=str(round(self.client.latency,3)),inline=False)
        emb.add_field(name=f"{ctx.guild} members",value=f'{ctx.guild.member_count}',inline=False)
        await ctx.send(embed=emb)

    @commands.command()
    async def servers(self,ctx):
        server_per_page=10
        svr = self.client.guilds
        embeds=[]
        for i in range(0,len(svr),server_per_page):
            emb = discord.Embed(title=f"**Kuristina Servers [{len(svr)}]**",color=0xFF0055)
            j=i
            while j<i+server_per_page:
                try:
                    emb.add_field(name=svr[j],value=f'members : {svr[j].member_count}',inline=False)
                except:
                    break
                j+=1
            embeds.append(emb)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command()
    async def say(self,ctx):
        if ctx.author.id==799362855525810196:
            await ctx.send(ctx.message.content[5:])
            await ctx.message.delete()

def setup(client):
    client.add_cog(Misc(client))