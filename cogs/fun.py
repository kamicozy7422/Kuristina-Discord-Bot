from __future__ import print_function
import basc_py4chan

import discord
from discord.ext import commands
import os
import random, requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from decouple import config
import json
import praw
from prawcore import NotFound
from datetime import datetime as dt
from random import randint

deletable_messages = []

reddit = praw.Reddit(
    client_id=config('REDDIT_CLIENT_ID'),
    client_secret=config('REDDIT_CLIENT_SECRET'),
    user_agent=config('REDDIT_USER_AGENT').replace("-", " "),
    check_for_async=False
)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cogs has been loaded ---------->")

    @commands.command(name="gif", description="Returns a gif from tenor")
    async def gif(self, ctx):
        q = ctx.message.content[5:]
        # set the apikey and limit
        apikey = config('TENOR_KEY')  # test value
        lmt = 10

        # our test search
        search_term = q

        # get the top 8 GIFs for the search term
        r = requests.get(
            f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={str(lmt)}&contentfilter=medium&media_filter=minimal"
        )

        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            tenorjson = json.loads(r.content)
            urls = []
            for i in range(len(tenorjson["results"])):
                url = tenorjson["results"][i]["media"][0]["tinygif"]["url"]

                urls.append(url)
            if urls == []:
                await ctx.send(f"can't find any gifs related to {search_term}")
                return
            gif_msg = await ctx.send(random.choice(urls))
            # await gif_msg.add_reaction('🗑️')
            deletable_messages.append(gif_msg.id)
        else:
            tenorjson = None

    @commands.command(name="ship", description="Ships you ofc")
    async def ship(self, ctx, m1: discord.User = None, m2: discord.User = None):
        if (m1.id == 804294821925093407 and ctx.author.id == 799362855525810196) or (
            m1.id == 799362855525810196 and ctx.author.id == 804294821925093407
        ):
            pass
        elif ctx.author.id != 799362855525810196 and (
            m1.id == 804294821925093407 or m2.id == 804294821925093407
        ):
            await ctx.send(f"SIMP")
            return

        def center_text(img, font, text):
            strip_width, strip_height = 2560, 1261
            draw = ImageDraw.Draw(img)
            text_width, text_height = draw.textsize(text, font)
            position = (
                (strip_width - text_width) / 2,
                (strip_height - text_height) / 2,
            )
            draw.text(position, text, (255, 255, 255), font=font)
            return img

        if m1 == None:
            m1 = ctx.author
            m2 = ctx.author
        elif m2 == None:
            m2 = m1
            m1 = ctx.author
        perc = random.randint(0, 101)
        u1r = requests.get(m1.avatar_url)
        u1img = Image.open(BytesIO(u1r.content)).resize((1000, 1000))
        u2r = requests.get(m2.avatar_url)
        u2img = Image.open(BytesIO(u2r.content)).resize((1000, 1000))
        bg = Image.open("images/bg.jpg")
        y = 130
        x = 130
        bg.paste(u1img, (x, y))
        bg.paste(u2img, (x + 1280, y))
        fnt = ImageFont.truetype("files/font.ttf", 80)
        bg = center_text(bg, fnt, f"{perc}%")
        bg.save(f"images/generated/{ctx.author.id}.png", quality=40)
        file = discord.File(f"images/generated/{ctx.author.id}.png", filename="pic.jpg")
        emb = discord.Embed(
            title="", description=f"{m1.mention} x {m2.mention}", color=0xFF0055
        )
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)
        os.system(f"rm -rf images/generated/{ctx.author.id}.png")

    @commands.command(name="reddit", description="random post from a subreddit")
    async def reddit(self, ctx, *, sr):
        def sub_exists(sub):
            exists = True
            try:
                reddit.subreddits.search_by_name(sub, exact=True)
            except NotFound:
                exists = False
            return exists

        async with ctx.typing():
            if sub_exists(sr):
                sr = reddit.subreddit(sr)
                if not sr.over18 or ctx.channel.is_nsfw():
                    posts = sr.new(limit=100)
                    urls, u_titles = [], []

                    for m in posts:
                        urls.append(m.url)
                        u_titles.append(m.title)

                    n = random.randint(0, len(urls))
                    e = discord.Embed(title=u_titles[n], color=0xFF0055)
                    e.set_image(url=urls[n])
                    post = await ctx.send(embed=e)
                    # await post.add_reaction('🗑️')
                    deletable_messages.append(post.id)
                    return
                else:
                    await ctx.send("Use that in an NSFW channel >_<")
            else:
                await ctx.send("That subreddit doesnot exist :(")
                return

    @commands.command(name="meme", description="Returns meme.")
    async def meme(self, ctx):
        sr = reddit.subreddit("memes")
        posts = sr.new(limit=100)
        urls, u_titles = [], []

        for m in posts:
            urls.append(m.url)
            u_titles.append(m.title)

        n = random.randint(0, len(urls))
        e = discord.Embed(title=u_titles[n], color=0xFF0055)
        e.set_image(url=urls[n])
        await ctx.send(embed=e)

    @commands.command(name='joke', description='Tells a lame joke.')
    async def joke(self, ctx):
        jk = requests.get(
            "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist&format=txt"
        )
        if jk.status_code == 200:
            e = discord.Embed(title=str(jk.content.decode("utf-8")), color=0xFF0055)
            await ctx.send(embed=e)
        else:
            await ctx.send(f"```Error : {jk.status_code}```")

    @commands.command(name='img', description='Show a board from 4chan')
    async def img(self, ctx, b, num=5):
        board = basc_py4chan.Board(str(b))

        # select the first thread on the board
        all_thread_ids = board.get_all_thread_ids()
        first_thread_id = all_thread_ids[randint(0, len(all_thread_ids))]
        thread = board.get_thread(first_thread_id)

        i = 0
        for f in thread.file_objects():
            e = discord.Embed(title=str(f.filename), color=0xFB7839)
            e.set_image(url= f.file_url)
            await ctx.send(embed=e)
            i += 1

            if i > num:
                break


def setup(client):
    client.add_cog(Fun(client))