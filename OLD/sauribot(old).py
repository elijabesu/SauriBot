import aiohttp
import discord
import asyncio
import datetime
import os
import string
import time
import io
import re
import random

from redbot.core import commands
from redbot.core import checks, bank
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.data_manager import cog_data_path

from discord import Webhook, AsyncWebhookAdapter
from discord.utils import get

__author__ = "saurichable"


class SauriBot(getattr(commands, "Cog", object)):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(aliases=["ss"])
    async def silentsay(self, ctx: commands.Context, *, message: str):
        """Say things as the bot and deletes the command if it can"""
        await ctx.message.delete()
        await ctx.send(message)

    @checks.is_owner()
    @commands.command()
    async def pingtime(self, ctx: commands.Context):
        bot = self.bot
        await ctx.send("Latency: :ping_pong: {}ms".format(round(bot.latency * 1000)))
        t1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send("Typing: :ping_pong: {}ms".format(round((t2 - t1) * 1000)))

    @commands.command()
    async def donate(self, ctx: commands.Context):
        """Donate to the development of SauriBot!"""
        await ctx.send(
            "Support Naughty Gamers and SauriBot by becoming our Patron https://www.patreon.com/naughty_gamers <:sauriheart:528330433918664705>"
        )

    @commands.command()
    async def serversetup(self, ctx: commands.Context):
        """Have Ellie set your server!"""
        await ctx.send(
            "Want Ellie to set up your server? Check out her Fiverr: http://bit.ly/ServerSetUp"
        )

    @commands.command()
    async def bothosting(self, ctx: commands.Context):
        """Have Ellie host your bots!"""
        await ctx.send(
            "Want our Ellie to host your bots? Check out her Fiverr: http://bit.ly/BotHosting"
        )

    @commands.command()
    async def social(self, ctx: commands.Context):
        """Ellie's social media."""
        await ctx.send(
            "**Ellie~♡#0001's social media:**\n<:saurichable:501192362630840330> <http://saurich.com/>\n<:patreon:501192327662927893> <https://patreon.com/saurichable>\n<:fiverr:501192306448400384> <https://fiverr.com/saurichable>\n<:twitch:501193435198521354> <https://twitch.tv/saurichable/>\n<:youtube:501193443993714709> <https://youtube.com/EllieSaurich>\n<:twitter:501193504089964545> <https://twitter.com/saurichable>\n<:instagram:501193685346549762> <https://instagram.com/saurichable/>"
        )

    @commands.command()
    async def owner(self, ctx: commands.Context):
        """Get basic information about my owner."""
        bot = self.bot
        music = """Monsta X, Jacob Lee, Bring Me The Horizon, Day6, SHINee, TAEMIN, VIXX, BTS, The Rose, PENTAGON, Astro"""
        games = """Overwatch, Destiny 2, Rainbow Six Siege, PAYDAY2, Portal, Half-Life, BioShock, Arma 3, Subnautica, This War of Mine"""
        bnet = """saurichable#2151 (main), CarryMeDaddy#2550, Ǣllie#2586, StanMonstaX#2938"""
        em = discord.Embed(colour=int("ffb8d7", 16))
        em.description = "Basic information about the owner."
        em.add_field(name="**Full name:**", value="Ellie Saurich", inline=True)
        em.add_field(name="**Nickname:**", value="saurichable", inline=True)
        em.add_field(name="**Birthday:**", value="5th of February", inline=True)
        em.add_field(name="**Funfact:**", value="Type `sb.funfact`.", inline=True)
        em.add_field(
            name="**Homepage:**",
            value="[saurich.com](http://saurich.com/)",
            inline=True,
        )
        em.add_field(
            name="**Other social media:**", value="Type `sb.social`.", inline=True
        )
        em.add_field(name="**Battletags:**", value=bnet, inline=False)
        em.add_field(
            name="**Steam:**",
            value="[saurichable](https://steamcommunity.com/id/saurichable/)",
            inline=True,
        )
        em.add_field(name="**Uplay:**", value="saurichable", inline=True)
        em.add_field(name="**Favourite games:**", value=games, inline=False)
        em.add_field(name="**Favourite music:**", value=music, inline=False)
        em.set_author(name="Ellie~♡#0001", icon_url="https://i.imgur.com/n5J4GQv.png")
        em.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )
        await ctx.send(embed=em)

    @commands.command()
    async def funfact(self, ctx: commands.Context):
        """Get a random funfact about Ellie."""
        bot = self.bot
        facts = [
            "Ellie's favourite animal is a dog :dog:",  # 1
            "Ellie's favourite dog breed is German Shepherd :wolf:",  # 2
            "Ellie's favourite colour is black :black_heart:",  # 3
            "Ellie studied 'Physical engineering and nanotechnology' for 3 semesters but got bored.",  # 4
            "Ellie's working as an IT support for one beauty eshop.",  # 5
            "Ellie used to be a beauty blogger before GoDaddy stole her domain <:sauriCry:532515272049819649>",  # 6
            "Ellie's favourite coffee is Macchiato and Mocha :coffee:",  # 7
            "Ellie owns a beautiful black GSD named Fancy <:sauriHeart:528330433918664705>",  # 8
            "Ellie has a sugar addiction. Yep, I said it.",  # 9
            "Ellie has arachnophobia :spider: and entomophobia :bug:",  # 10
            "Ellie is terrified of space :rocket:",  # 11
            "Ellie loves science and technology way too much :rolling_eyes:",  # 12
            "Ellie is an extremely messy person :mask:",  # 13
            "Ellie spent too much money on her monitor (`sb.specs`) but doesn't regret it.",  # 14
            "Ellie has Canon EOS 80D but rarely uses it :camera:",  # 15
            "Normal Pepsi is better than Coca Cola <:sauriShrug:532515331239837697>",  # 16
            "Coca Cola Light (Diet Coke) is better than Pepsi Light <:sauriShrug:532515331239837697>",  # 17
            "Pineapple belongs on pizza <:sauriShrug:532515331239837697>",  # 18
            "Ellie's favourite cocktail is piña colada :cocktail:",  # 19
            "Ellie and Adrian met purely because of Monsta X (kpop group) :musical_note:",  # 20
            "Ellie's favourite drink is water and Pepsi Max <:sauriShrug:532515331239837697>",  # 21
            "Ellie's favourite pizza is Milano (cream based with corn) :pizza:",  # 22
            "KFC is better than McDonald's <:sauriShrug:532515331239837697>",  # 23
            "Ellie loves Korean dishes, mainly japchae, bibimbap and ramyeon :ramen:",  # 24
            "Ellie's favourite side dish is rice :rice:",  # 25
            "Sweet potatoes are way better than normal potatoes :sweet_potato:",  # 26
            "Ellie loves Japanese dishes, mainly tonkotsu, sushi and takoyaki :sushi:",  # 27
            "Ellie loves sea food (except oysters and mussels) :squid:",  # 28
            "Ellie has always wanted a pet snake but still no luck :snake:",  # 29
            "When Ellie was ~7 years old, she got bitten by a bumblebee multiple times, since then she's had entomophobia :bee:",  # 30
            "Ellie's favourite games are Half-Life, Portal and BioShock series.",  # 31
            "Ellie still believes Half-Life 3 will be released <:sauriCry:532515272049819649>",  # 32
            "Ellie has 4 accounts of Overwatch, yet she doesn't play on any of them <:lullmfao:483059520210206741>",  # 33
            "Ellie has many games she loves only periodically, examples being Destiny 2 and PAYDAY2.",  # 34
            "Ellie doesn't usually eat breakfast but if yes, it's a sweet breakfast.",  # 35
            "One of the reasons why Ellie wants to live in the UK is Sainsbury's <:sauriShrug:532515331239837697>",  # 36
            "Ellie is a Slytherin :snake:",  # 37
            "I advise you not to start political talks with Ellie, she can argue about it for hours :sleeping:",  # 38
            "Ellie loves her bullet journal but keeps it very simple :book:",  # 39
            "Ellie learned bookbinding on her own a few years ago so she doesn't need to buy empty notebooks anymore :books:",  # 40
            "Ellie's obsessed with makeup, mainly eyeshadow palettes and highlighters :lipstick:",  # 41
            "Ellie's favourite makeup brand is Jeffree Star Cosmetics.",  # 42
            "Ellie's favourite part of her makeup routine is putting on highlighter so she can blind everyone.",  # 43
            "Ellie's favourite perfume has been YSL Black Opium for quite a few years.",  # 44
            "Ellie loves candles way too much :candle:",  # 45
            "Ellie's favourite candle brand is WoodWick :candle:",  # 46
            "Ellie's favourite hair colour on her is black.",  # 47
            "Ellie dyed her hair for the first time when she was 13 and it was black.",  # 48
            "Ellie's favourite cereal is Coco Pops (chocolate version of Rice Krispies).",  # 49
            "Ellie really enjoys baking, mainly cupcakes and cookies.",  # 50
        ]
        em = discord.Embed(
            color=discord.Color.from_hsv(random.random(), 0.278, 1),
            description=random.choice(facts),
        )
        em.set_author(
            name="Ellie~♡#0001's fun fact", icon_url="https://i.imgur.com/n5J4GQv.png"
        )
        em.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )
        await ctx.send(embed=em)
