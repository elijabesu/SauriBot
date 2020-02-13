import discord
import asyncio
import time
import random

from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box


class SauriBot(getattr(commands, "Cog", object)):

    __author__ = "saurichable"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @checks.bot_has_permissions(manage_messages=True)
    @commands.command(aliases=["ss"])
    async def silentsay(self, ctx: commands.Context, *, message: str):
        """Say things as the bot and deletes the command."""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def social(self, ctx: commands.Context):
        """Ellie's social media."""
        await ctx.send("""**Ellie~♡#0001's social media:**
<:saurichable:501192362630840330> <http://saurich.com/>
<:patreon:501192327662927893> <https://patreon.com/saurichable>
<:twitch:501193435198521354> <https://twitch.tv/saurichable/>
<:youtube:501193443993714709> <https://youtube.com/EllieSaurich>
<:twitter:501193504089964545> <https://twitter.com/saurichable>
<:instagram:501193685346549762> <https://instagram.com/saurichable/>
""")

    @commands.command()
    async def owner(self, ctx: commands.Context):
        """Get basic information about my owner."""
        music = """Monsta X, ATEEZ, ONEUS, Stray Kids, The Rose, Jacob Lee, The Neighbourhood, Bring Me The Horizon, Day6, TAEMIN, PENTAGON, BTS, Lauv"""
        games = """Beat Saber, Overwatch, R6: Siege, PAYDAY2, Portal, Half-Life, BioShock, Arma 3, Subnautica, This War of Mine"""
        bnet = """saurichable#2151 (main), CarryMeDaddy#2550, Ǣllie#2586, StanMonstaX#2938"""
        em = discord.Embed(colour=int("ffa0ba", 16))
        em.description = "Basic information about the owner."
        em.add_field(name="**Full name:**", value="Ellie Saurich", inline=True)
        em.add_field(name="**Nickname:**", value="saurichable", inline=True)
        em.add_field(name="**Birthday:**", value="5th of February", inline=True)
        em.add_field(
            name="**Funfact:**", value=f"Type `{ctx.clean_prefix}funfact`", inline=True
        )
        em.add_field(
            name="**Homepage:**",
            value="[saurich.com](https://saurich.com/)",
            inline=True,
        )
        em.add_field(
            name="**Other social media:**",
            value=f"Type `{ctx.clean_prefix}social`",
            inline=True,
        )
        em.add_field(name="**Battletags:**", value=bnet, inline=False)
        em.add_field(
            name="**Steam:**",
            value="[saurichable](https://steamcommunity.com/id/saurichable/)",
            inline=True,
        )
        em.add_field(name="**Uplay:**", value="saurichable", inline=True)
        em.add_field(name="**Origin:**", value="saurich-com", inline=True)
        em.add_field(name="**Favourite games:**", value=games, inline=False)
        em.add_field(name="**Favourite music:**", value=music, inline=False)
        em.set_author(name="Ellie~♡#0001", icon_url="https://i.imgur.com/n5J4GQv.png")
        em.set_footer(
            text=f"{self.bot.user.name}#{self.bot.user.discriminator} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me."
        )
        await ctx.send(embed=em)

    @commands.command()
    async def funfact(self, ctx: commands.Context):
        """Get a random funfact about Ellie."""
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
            text=f"{self.bot.user.name}#{self.bot.user.discriminator} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me."
        )
        await ctx.send(embed=em)
