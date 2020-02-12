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
    Various custom made commands for IG and NG server.
    """

    __author__ = "saurichable"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.servers = [482560976307355658, 438252747007983616, 565475499007148043]
        self.config = Config.get_conf(self, identifier=5165146516515491)

    # FOR MEMBERS:
    @commands.command()
    @commands.guild_only()
    async def support(self, ctx: commands.Context, *, message=""):
        """Opens a support ticket."""
        if ctx.guild.id not in self.servers:
            return

        role_add = get(ctx.guild.roles, id=482562270077911070)  # PENDING SUPPORT
        role_men = get(ctx.guild.roles, id=482562007443439646)  # Mods

        await ctx.author.add_roles(role_add)
        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(
                "**Thank you for reaching out to us, {0}!**\n\n{1} have been notified that you need assistance.\n\n**Problem:** Not specified.\n*Please state your problem/issue now so we can get to you as soon as possible. If it is personal, state it as well.*".format(
                    ctx.author.mention, role_men.mention
                )
            )
        else:
            await ctx.send(
                "**Thank you for reaching out to us, {0}!**\n\n{1} have been notified that you need assistance.\n\n**Problem:** {2}".format(
                    ctx.author.mention, role_men.mention, message
                )
            )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def mod(self, ctx: commands.Context, *, message=""):
        """Calls Mods."""
        if ctx.guild.id not in self.servers:
            return

        role_men = get(ctx.guild.roles, id=482562007443439646)  # Mods

        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(f"{role_men.mention}")
        else:
            await ctx.send(
                "{0}\n{1}: {2}".format(role_men.mention, ctx.author.mention, message)
            )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def link(self, ctx: commands.Context):
        """Sends a default invite link."""
        if ctx.guild.id not in self.servers:
            return

        link_invite = await self.config.guild(ctx.guild).invite()

        await ctx.send("Our invite link is {0}".format(link_invite))

    # PING ROLES:
    @commands.command()
    @commands.guild_only()
    async def event(self, ctx: commands.Context, *, message=""):
        """For Event hosts only."""
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
                return

        role_men = get(ctx.guild.roles, id=485582775970168832)  # Event ping

        await ctx.message.delete()
        await role_men.edit(mentionable=True)
        await ctx.send("{0}\n{1}".format(role_men.mention, message))
        await role_men.edit(mentionable=False)

    @checks.admin_or_permissions(administrator=True)
    @commands.command()
    @commands.guild_only()
    async def poll(self, ctx: commands.Context, *, message=""):
        """For Poll hosts only."""
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
                return

        role_men = get(ctx.guild.roles, id=485756032614793216)  # Poll ping

        await ctx.message.delete()
        await role_men.edit(mentionable=True)
        await ctx.send("{0}\n{1}".format(role_men.mention, message))
        await role_men.edit(mentionable=False)

    # FOR MODS:
    @checks.mod_or_permissions(ban_members=True)
    @commands.command()
    @commands.guild_only()
    async def close(self, ctx: commands.Context, target: discord.Member):
        """Closes an open ticket."""
        if ctx.guild.id not in self.servers:
            return

        role_rem1 = get(ctx.guild.roles, id=482562270077911070)  # PENDING SUPPORT
        role_rem2 = get(ctx.guild.roles, id=519847615882330113)  # Personal

        await target.remove_roles(role_rem1)
        await target.remove_roles(role_rem2)
        await ctx.send("Successfully closed {0}'s ticket.".format(target.name))

    @checks.mod_or_permissions(ban_members=True)
    @commands.command()
    @commands.guild_only()
    async def personal(self, ctx: commands.Context, target: discord.Member):
        """In case someone has a personal issue."""
        if ctx.guild.id not in self.servers:
            return

        role_add = get(ctx.guild.roles, id=519847615882330113)  # Personal
        channel_men = get(ctx.guild.channels, id=519848071832535040)  # personal-support

        await target.add_roles(role_add)
        await ctx.send(
            "{0}, move to {1} please.".format(target.mention, channel_men.mention)
        )

    # FOR ME ONLY:
    @checks.is_owner()
    @commands.command()
    @commands.guild_only()
    async def end(self, ctx: commands.Context):
        """ End the Monthly Competition """
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
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
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
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
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
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
                "{0}, {1} would like to get verified.".format(
                    role_men.mention, ctx.author.mention
                )
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
        author = ctx.author
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return
        await ctx.message.delete()

        role_add = get(ctx.guild.roles, id=482693992732164098)  #'Secret role' role
        role_rem = get(ctx.guild.roles, id=491277913862176769)  #'I can't read' role

        if role_rem in author.roles:  # Checks if author has 'I can't read'
            await author.add_roles(role_add)  # Adds 'Secret role'
            await author.remove_roles(role_rem)  # Removes 'I can't read' role
            await author.send(
                "Congratulations, {0}, you can officially read! <:sauriHype:528330460779118603> You have received your 10 cookies!".format(
                    author.name
                )
            )
        else:
            await ctx.send("Good try.")

    # FOR VERIFIERS:
    @commands.command()
    @commands.guild_only()
    async def v(self, ctx: commands.Context, target: discord.Member):
        """Verified"""
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add = get(ctx.guild.roles, id=482562076364242944)  # Verified
        role_rem = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role

        if role_add in target.roles:
            return await ctx.send("Uh oh, {0} is already verified.".format(target.mention))
        if role_rem in target.roles:
            await target.add_roles(role_add)  # Adds Verified
            await target.remove_roles(role_rem)  # Removes 'PENDING VERIFICATION' role
            await ctx.send("{0}, welcome to the adulthood.".format(target.mention))
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(),
                title="Verification approved",
            )
            embed.set_author(
                name="{0}#{1} ({2})".format(
                    target.name, target.discriminator, target.id
                ),
                icon_url=target.avatar_url,
            )
            embed.add_field(
                name="Moderator:",
                value="{0}#{1} ({2})".format(
                    ctx.author.name, ctx.author.discriminator, ctx.author.id
                ),
            )
            await log.send(embed=embed)
        else:
            await ctx.send(
                "Uh oh, {0} did not request verification.".format(target.mention)
            )

    @commands.command()
    @commands.guild_only()
    async def d(self, ctx: commands.Context, target: discord.Member):
        """Denies verification."""
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
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
                name="{0}#{1} ({2})".format(
                    target.name, target.discriminator, target.id
                ),
                icon_url=target.avatar_url,
            )
            embed.add_field(
                name="Moderator:",
                value="{0}#{1} ({2})".format(
                    ctx.author.name, ctx.author.discriminator, ctx.author.id
                ),
            )
            await log.send(embed=embed)
        else:
            await ctx.send(
                "Uh oh, {0} did not request verification.".format(target.mention)
            )
