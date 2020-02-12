import asyncio
import discord

from typing import Any
from discord.utils import get

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import humanize_timedelta

from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class Kavliaris(Cog):
    """
    Various custom made commands for Kavliaris Mansion.
    """

    __author__ = "saurichable"
    __version__ = "0.1.0"


    def __init__(self, bot: Red):
        self.bot = bot
        self.kavliaris = [565475499007148043]
        self.config = Config.get_conf(
            self, identifier=54646513215498531, force_registration=True
        )
        self.config.register_guild(members={}, blacklist={})

    @checks.mod_or_permissions(kick_members=True)
    @commands.command()
    @commands.guild_only()
    async def reserved(self, ctx: commands.Context, aff: str, category: str, name: str):
        if ctx.guild.id not in self.kavliaris:
            return
        try:
            if await self.config.guild(ctx.guild).blacklist.get_raw(aff) is not None:
                return await ctx.send("They're blacklisted!!")
        except:
            pass
        try:
            already_name = await self.config.guild(ctx.guild).member.get_raw(category, name)
            if already_name.get("arrived") is True:
                return await ctx.send("This member has already arrived.")
            if already_name.get("reserved") is True:
                return await ctx.send("This member has already been reserved.")
        except:
            pass
        await self.config.guild(ctx.guild).members.set_raw(
            category,
            name,
            value={
                "aff": aff,
                "free": False,
                "reserved": True,
            },
        )
        await ctx.tick()

    @checks.mod_or_permissions(kick_members=True)
    @commands.command()
    @commands.guild_only()
    async def delreserved(
        self, ctx: commands.Context, aff: str, category: str, name: str
    ):
        if ctx.guild.id not in self.kavliaris:
            return
        try:
            if await self.config.guild(ctx.guild).blacklist.get_raw(aff) is not None:
                return await ctx.send("They're blacklisted!!")
        except:
            pass
        try:
            already_name = await self.config.guild(ctx.guild).member.get_raw(category, name)
            if already_name.get("aff") != aff:
                return await ctx.send("The aff username doesn't match.")
            if already_name.get("arrived") is True:
                return await ctx.send("This member has already arrived.")
        except:
            return
        await self.config.guild(ctx.guild).members.set_raw(
            category,
            name,
            value={"aff": None, "free": True, "reserved": False},
        )
        await ctx.tick()

    @checks.mod_or_permissions(kick_members=True)
    @commands.command()
    @commands.guild_only()
    async def arrived(
        self,
        ctx: commands.Context,
        member: discord.Member,
        aff: str,
        category: str,
        name: str,
    ):
        if ctx.guild.id not in self.kavliaris:
            return
        try:
            already_name = await self.config.guild(ctx.guild).member.get_raw(category, name)
            if already_name.get("aff") != aff:
                return await ctx.send("The aff username doesn't match.")
            if already_name.get("arrived") is True:
                return await ctx.send("This member has already arrived.")
        except:
            return await ctx.send("They haven't been reserved!")
        await self.config.guild(ctx.guild).members.set_raw(
            category, name, value={"discord": member.id, "arrived": True}
        )
        await member.add_roles(
            get(ctx.guild.roles, id=565543724743131136)
        )  # Actual members
        channel = get(ctx.guild.text_channels, id=565575851270471681)  # arrivals
        await channel.send(f"Welcome our newest member, {member.mention}! :tada:")
        await ctx.tick()

    @checks.mod_or_permissions(kick_members=True)
    @commands.command()
    @commands.guild_only()
    async def departed(self, ctx: commands.Context, aff: str, category: str, name: str, member: discord.Member=None):
        if ctx.guild.id not in self.kavliaris:
            return
        try:
            already_name = await self.config.guild(ctx.guild).member.get_raw(category, name)
            if already_name.get("aff") != aff:
                return await ctx.send("The aff username doesn't match.")
            if already_name.get("arrived") is False:
                return await ctx.send("This member has never arrived.")
            if already_name.get("reserved") is False:
                return await ctx.send("This member has never been reserved.")
            await self.config.guild(ctx.guild).members.set_raw(
                category,
                name,
                value={
                    "aff": None,
                    "discord": 0,
                    "free": True,
                    "reserved": False,
                    "arrived": False,
                },
            )
            if member is not None:
                await member.remove_roles(
                    get(ctx.guild.roles, id=565543724743131136)
                )
            channel = get(ctx.guild.text_channels, id=565575993448726538)  # departures
            await channel.send(f"{name} has left us...")
            await ctx.tick()
        except:
            return await ctx.send("They have never been here.")

    @checks.mod_or_permissions(kick_members=True)
    @commands.command()
    @commands.guild_only()
    async def blacklisted(self, ctx: commands.Context, aff: str, *, reason: str=None):
        if ctx.guild.id not in self.kavliaris:
            return
        if not reason:
            try:
                already_name = await self.config.guild(ctx.guild).blacklist.get_raw(aff)
                if already_name is None:
                    return await ctx.send(f"{aff} has never never been blacklisted. Run the command again with a reason to add them.")
                else:
                    reason = already_name.get("reason")
                    return await ctx.send(f"{aff} has been blacklisted with the following reason:\n{reason}")
            except:
                return await ctx.send(f"{aff} has never never been blacklisted. Run the command again with a reason to add them.")
        await self.config.guild(ctx.guild).blacklist.set_raw(
            aff,
            value={
                "reason": reason,
            },
        )
        await ctx.tick()