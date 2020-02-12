import asyncio
import re
import discord
import random

from typing import Any
from discord.utils import get

from redbot.core import Config, checks, bank, modlog, commands
from redbot.core.utils.chat_formatting import pagify, box, warning, error
from redbot.cogs.bank import check_global_setting_guildowner, check_global_setting_admin

from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class Gamers(Cog):
    """
    Various custom made commands for NG server.
    """

    __author__ = "saurichable"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot

    # FOR MEMBERS:
    @commands.command()
    @commands.guild_only()
    async def support(self, ctx: commands.Context, *, message=""):
        """Opens a support ticket."""
        if ctx.guild.id != 482560976307355658:
            return

        role_add = get(ctx.guild.roles, id=482562270077911070)  # PENDING SUPPORT
        role_men = get(ctx.guild.roles, id=482562007443439646)  # Mods

        await ctx.author.add_roles(role_add)
        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(
                f"**Thank you for reaching out to us, {ctx.author.mention}!**\n\n{role_men.mention} have been notified that you need "
                "assistance.\n\n**Problem:** Not specified.\n*Please state your problem/issue now so we can get to you as soon as possible."
                " If it is personal, state it as well.*"
            )
        else:
            await ctx.send(
                f"**Thank you for reaching out to us, {ctx.author.mention}!**\n\n{role_men.mention} have been notified that you need assistance.\n\n"
                f"**Problem:** {message}"
            )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def mod(self, ctx: commands.Context, *, message=""):
        """Calls Mods."""
        if ctx.guild.id != 482560976307355658:
            return

        role_men = get(ctx.guild.roles, id=482562007443439646)  # Mods

        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(f"{role_men.mention}")
        else:
            await ctx.send(
                f"{role_men.mention}\n{ctx.author.mention}: {message}"
            )
        await role_men.edit(mentionable=False)

    # PING ROLES:
    @commands.command()
    @commands.guild_only()
    async def event(self, ctx: commands.Context, *, message=""):
        """For Event hosts only."""
        if ctx.guild.id != 482560976307355658:
            return

        role_men = get(ctx.guild.roles, id=485582775970168832)  # Event ping

        await ctx.message.delete()
        await role_men.edit(mentionable=True)
        await ctx.send(f"{role_men.mention}\n{message}")
        await role_men.edit(mentionable=False)

    @checks.admin_or_permissions(administrator=True)
    @commands.command()
    @commands.guild_only()
    async def poll(self, ctx: commands.Context, *, message=""):
        """For Poll hosts only."""
        if ctx.guild.id != 482560976307355658:
            return

        role_men = get(ctx.guild.roles, id=485756032614793216)  # Poll ping

        await ctx.message.delete()
        await role_men.edit(mentionable=True)
        await ctx.send(f"{role_men.mention}\n{message}")
        await role_men.edit(mentionable=False)

    # FOR MODS:
    @checks.mod_or_permissions(ban_members=True)
    @commands.command()
    @commands.guild_only()
    async def close(self, ctx: commands.Context, target: discord.Member):
        """Closes an open ticket."""
        if ctx.guild.id != 482560976307355658:
            return

        role_rem1 = get(ctx.guild.roles, id=482562270077911070)  # PENDING SUPPORT
        role_rem2 = get(ctx.guild.roles, id=519847615882330113)  # Personal

        await target.remove_roles(role_rem1)
        await target.remove_roles(role_rem2)
        await ctx.send(f"Successfully closed {target.display_name}'s ticket.")

    @checks.mod_or_permissions(ban_members=True)
    @commands.command()
    @commands.guild_only()
    async def personal(self, ctx: commands.Context, target: discord.Member):
        """In case someone has a personal issue."""
        if ctx.guild.id != 482560976307355658:
            return

        role_add = get(ctx.guild.roles, id=519847615882330113)  # Personal
        channel_men = get(ctx.guild.channels, id=519848071832535040)  # personal-support

        await target.add_roles(role_add)
        await ctx.send(
            f"{target.mention}, move to {channel_men.mention} please."
        )

    # FOR ME ONLY:
    @checks.is_owner()
    @commands.command()
    @commands.guild_only()
    async def end(self, ctx: commands.Context):
        """ End the Monthly Competition """
        if ctx.guild.id != 482560976307355658:
            return

        five = get(ctx.guild.roles, id=483715523482222613)  # 5+
        channel = get(ctx.guild.text_channels, id=483365869565509635)  # naughty-bank
        await channel.set_permissions(five, read_messages=True, send_messages=False)
        await ctx.tick()
        await channel.send(
            "---------------------------------MONTHLY COMPETITION HAS ENDED---------------------------------"
        )

    @checks.is_owner()
    @commands.command()
    @commands.guild_only()
    async def start(self, ctx: commands.Context):
        """ Start the Monthly Competition """
        if ctx.guild.id != 482560976307355658:
            return

        five = get(ctx.guild.roles, id=483715523482222613)  # 5+
        channel = get(ctx.guild.text_channels, id=483365869565509635)  # naughty-bank
        await channel.set_permissions(five, read_messages=True, send_messages=True)
        await bank.wipe_bank(guild=ctx.guild)
        await ctx.tick()
        await channel.send(
            "---------------------------------MONTHLY COMPETITION HAS STARTED---------------------------------"
        )

    # NAUGHTY GAMERS SERVER ONLY:
    @commands.command()
    @commands.guild_only()
    async def request(self, ctx: commands.Context):
        """Opens a verification ticket."""
        if ctx.guild.id != 482560976307355658:
            return

        role_add = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role
        av = get(ctx.guild.roles, id=482562076364242944) # Verified
        age1 = get(ctx.guild.roles, id=585837902798520333)  # <15
        age2 = get(ctx.guild.roles, id=514129601883275267)  # 16-17
        age3 = get(ctx.guild.roles, id=482582198248275995)  # 18-21
        age4 = get(ctx.guild.roles, id=482582199204446209)  # 22-25
        age5 = get(ctx.guild.roles, id=482582199753900032)  # 26-29
        age6 = get(ctx.guild.roles, id=482582200181850123)  # 30-34
        age7 = get(ctx.guild.roles, id=482872100420321281)  # 35+
        role_men = get(ctx.guild.roles, id=482977157581373465)  #'Verifiers' role

        if av in ctx.author.roles:
            return await ctx.send("You're already verified, what more do you want from me?!")
        if age1 in ctx.author.roles or age2 in ctx.author.roles:
            return await ctx.send("Uh oh, verification is only for people above 18.")
        if (
            age3 in ctx.author.roles
            or age4 in ctx.author.roles
            or age5 in ctx.author.roles
            or age6 in ctx.author.roles
            or age7 in ctx.author.roles
        ):
            await ctx.author.add_roles(role_add)  # Adds 'PENDING VERIFICATION' role
            await role_men.edit(mentionable=True)  # Makes 'Verifiers' mentionable
            await ctx.send(
                f"{role_men.mention}, {ctx.author.mention} would like to get verified."
            )
            await role_men.edit(mentionable=False)  # Makes 'Verifiers' unmentionable
        else:
            await ctx.send(
                "Are you sure you've read <#482572215330799627> properly? Because it doesn't look like it."
            )

    @commands.command(hidden=True)
    @commands.guild_only()
    async def coconut(self, ctx: commands.Context):
        """That's a secret."""
        if ctx.guild.id != 482560976307355658:
            return

        await ctx.message.delete()

        role_add = get(ctx.guild.roles, id=482693992732164098)  #'Secret role' role
        role_rem = get(ctx.guild.roles, id=491277913862176769)  #'I can't read' role

        if role_rem in ctx.author.roles:  # Checks if author has 'I can't read'
            await ctx.author.add_roles(role_add)  # Adds 'Secret role'
            await ctx.author.remove_roles(role_rem)  # Removes 'I can't read' role
            await ctx.author.send(
                f"Congratulations, {ctx.author.name}, you can officially read! <:sauriHype:528330460779118603> You have received your 10 cookies!"
            )
        else:
            await ctx.send("Good try.")

    # FOR VERIFIERS:
    @commands.command()
    @commands.guild_only()
    async def v(self, ctx: commands.Context, target: discord.Member):
        """Verified"""
        if ctx.guild.id != 482560976307355658:
            return

        role_add = get(ctx.guild.roles, id=482562076364242944)  # Verified
        role_rem = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role

        if role_add in target.roles:
            return await ctx.send(f"Uh oh, {target.mention} is already verified.")
        if role_rem in target.roles:
            await target.add_roles(role_add)  # Adds Verified
            await target.remove_roles(role_rem)  # Removes 'PENDING VERIFICATION' role
            await ctx.send(f"{target.mention}, welcome to the adulthood.")
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(),
                title="Verification approved",
            )
            embed.set_author(
                name=f"{target.name}#{target.discriminator} ({target.id})",
                icon_url=target.avatar_url,
            )
            embed.add_field(
                name="Moderator:",
                value=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
            )
            await log.send(embed=embed)
        else:
            await ctx.send(
                f"Uh oh, {target.display_name} did not request verification."
            )

    @commands.command()
    @commands.guild_only()
    async def d(self, ctx: commands.Context, target: discord.Member):
        """Denies verification."""
        if ctx.guild.id != 482560976307355658:
            return

        role_rem = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role

        if role_rem in target.roles:
            await target.remove_roles(role_rem)  # Removes 'PENDING VERIFICATION' role
            await ctx.send("Awww, maybe next time...")
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(), title="Verification denied"
            )
            embed.set_author(
                name=f"{target.name}#{target.discriminator} ({target.id})",
                icon_url=target.avatar_url,
            )
            embed.add_field(
                name="Moderator:",
                value=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
            )
            await log.send(embed=embed)
        else:
            await ctx.send(
                f"Uh oh, {target.display_name} did not request verification."
            )
