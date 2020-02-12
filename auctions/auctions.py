import asyncio
import re
import discord

from typing import Any
from discord.utils import get
from datetime import datetime

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.predicates import MessagePredicate
from redbot.cogs.bank import check_global_setting_guildowner, check_global_setting_admin

from redbot.core.bot import Red


Cog: Any = getattr(commands, "Cog", object)

class Auction(Cog):
    """
    Simple auctions cog, basically.
    """

    __author__ = "saurichable"
    __version__ = "0.1.0"


    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=5489465465514652, force_registration=True)

        default_guild = {
        "db": []
        "price": 1500,
        }

        default_member = {
        "name": None,
        "age": 0,
        "dob": None,
        "about": None,
        "bought": False,
        "slave_ids": [],
        "owner_id": None,
        }

        self.config.register_member(**default_member)
        self.config.register_guild(**default_guild)

#    async def _is_registered(self, member):
#        async with self.config.guild(member.guild).database() as db:
#            return member.id in db

#    async def _register_user(self, member):
#        data = await self.config.guild(member.guild).database()
#        if data is None:
#            await self.config.guild(member.guild).database.set([])
#        async with self.config.guild(member.guild).database() as db:
#            db.append(member.id)
#        await self.config.member(member).exp.set(0)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def register(self, ctx: commands.Context):
        """"""
        author = ctx.author
        member = ctx.author
        guild = ctx.guild
        bot = self.bot
        role_add = get(guild.roles, name="Registered")
        master = (get(guild.get_member(author.id).roles, name="Master") is not None)
        slave = (get(guild.get_member(author.id).roles, name="slave") is not None)
        channel = get(guild.text_channels, name='registrations')
        money = await bank.get_balance(author)
        currency = await bank.get_currency_name(guild)

        if role_add is None:
            await ctx.send("Uh oh. Looks like your Admins haven't added the required role.")
            return

        if channel is None:
            await ctx.send("Uh oh. Looks like your Admins haven't added the required channel.")
            return

        try:
            await author.send("Let's start right away! You have maximum of 2 minutes for each question.\nWhat is your full name?")
        except discord.Forbidden:
            await ctx.send("I don't seem to be able to DM you. Do you have closed DMs?")
            return

        await ctx.message.add_reaction('✅')

        def check(m):
            return m.author == author
        try:
            name = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long. Try again, please.")
            return
        await self.config.member(member).name.set(name.content)

        await author.send("How old are you?")
        try:
            age = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long. Try again, please.")
            return
        await self.config.member(member).age.set(age.content)

        await author.send("Date of birth?")
        try:
            dob = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long. Try again, please.")
            return
        await self.config.member(member).dob.set(dob.content)

        await author.send("Write something about you - you have 5 minutes.")
        try:
            about = await bot.wait_for("message", timeout=300, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long. Try again, please.")
            return
        await self.config.member(member).about.set(about.content)

        embed = discord.Embed(color=await ctx.embed_colour(), timestamp=datetime.now())
        embed.set_author(name="{0}'s Profile".format(author.name), icon_url=author.avatar_url)
        embed.set_footer(text="{0}#{1} ({2})".format(author.name, author.discriminator, author.id))
        embed.title=("User: {0}#{1} ({2})".format(author.name, author.discriminator, author.id))
        embed.add_field(name="Name:", value=name.content, inline=True)
        embed.add_field(name="Age:", value=age.content, inline=True)
        embed.add_field(name="DOB:", value=dob.content, inline=True)
        embed.add_field(name="About:", value=about.content, inline=False)
        embed.add_field(name="Joined:", value=joined, inline=True)
        embed.add_field(name="Money:", value=("{0} {1}".format(money, currency)), inline=True)
        if master:
            embed.add_field(name="Can buy:", value=buy, inline=True)
            if not await self.config.guild(ctx.guild).slaves.get_raw(author.id, default=None):
                slaves = "None"
            else:
                slaves = await self.config.guild(ctx.guild).slaves.get_raw(author.id, default=None)
                embed.add_field(name="Slaves:", value=slaves, inline=False)
        elif slave:
            embed.add_field(name="Can be bought:", value=buy, inline=True)
            if not await self.config.guild(ctx.guild).owners.get_raw(author.id, default=None):
                owner = "None"
            else:
                owner = await self.config.guild(ctx.guild).owner.get_raw(author.id, default=None)
            embed.add_field(name="Owner:", value=owner, inline=False)

        await channel.send(embed=embed)
        await self.config.guild(ctx.guild).profiles.set_raw(author.id, value=embed)

        await author.add_roles(role_add)

        await author.send("Your application has been sent to the Admins, thank you!")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def profile(self, ctx: commands.Context, target: discord.Member = None):
        """"""
        author = ctx.author
        guild = ctx.guild
        if not target:
            target = author
        profile = await self.config.guild(ctx.guild).profiles.get_raw(target.id)
        await ctx.send(embed = profile)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def freemyself(self, ctx: commands.Context):
        """"""
        author = ctx.author
        guild = ctx.guild
        master = (get(guild.get_member(author.id).roles, name="Master") is not None)
        slave = (get(guild.get_member(author.id).roles, name="slave") is not None)
        profile = await self.config.member(author).all()
        currency = await bank.get_currency_name(guild)
        price = await self.config.guild(guild).price()
        amount = price*1.5

        if await bank.can_spend(author, amount):
            pass
        else:
            await ctx.send("You don't have enough money.")
            return

        if slave:
            pass
        else:
            await ctx.send("What are you trying to achieve? You're a Master.")
            return

        if profile["bought"] is False:
            await ctx.send("What are you trying to achieve? You're not owned.")
            return
        else:
            profile["bought"] = False
            profile["owner"] = None
            await bank.withdraw_credits(author, amount)
            await ctx.send("{0} has freed himself! Yey freedom!".format(author.mention))

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def disown(self, ctx: commands.Context, target: discord.Member):
        """"""
        author = ctx.author
        guild = ctx.guild
        author_master = (get(guild.get_member(author.id).roles, name="Master") is not None)
        target_slave = (get(guild.get_member(target.id).roles, name="slave") is not None)
        author_profile = await self.config.member(author).all()
        target_profile = await self.config.member(member).all()
        currency = await bank.get_currency_name(guild)
        price = await self.config.guild(guild).price()
        amount = price*2

        if await bank.can_spend(author, amount):
            pass
        else:
            await ctx.send("You don't have enough money.")
            return

        if author_master:
            pass
        else:
            await ctx.send("What are you trying to achieve? You're a slave.")
            return

        if target_slave:
            pass
        else:
            await ctx.send("What are you trying to achieve? He's not a slave.")
            return

        if target_profile["bought"] is False:
            await ctx.send("What are you trying to achieve? He's not owned.")
            return
        elif target_profile["owner"] != author.id:
            await ctx.send("What are you trying to achieve? You don't own him.")
            return
        else:
            target_profile["bought"] = False
            target_profile["owner"] = None
            async with await self.config.member(author).slaves() as slaves:
                slaves.remove(targed.id)
            await bank.withdraw_credits(author, amount)
            await ctx.send("{0} has diowned {1}.".format(author.mention, target.mention))

