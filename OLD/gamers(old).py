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

__author__ = "saurichable"

Cog: Any = getattr(commands, "Cog", object)


class Gamers(Cog):
    """
    Various custom made commands for IG and NG server.
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.servers = [482560976307355658, 438252747007983616, 565475499007148043]
        self.config = Config.get_conf(
            self, identifier=5165146516515491, force_registration=True
        )
        default_guild = {
            "moderator": None,
            "admin": None,
            "invite": None,
            "appeal": None,
            "invite18": None,
        }

        self.config.register_guild(**default_guild)

    # ROLES SETUP:
    @commands.group(autohelp=True)
    @commands.guild_only()
    @checks.is_owner()
    async def serverroles(self, ctx):
        """Set server roles by typing their names."""
        if ctx.guild.id not in self.servers:
            return

        pass

    @serverroles.command()
    async def moderator(self, ctx, moderator_name=None):
        """Set moderator role."""
        if not moderator_name:
            await self.config.guild(ctx.guild).moderator.set(None)
            return await ctx.send("Moderator role removed.")
        await self.config.guild(ctx.guild).moderator.set(str(moderator_name))
        await ctx.send(f"Moderator role has been set to {moderator_name}.")

    @serverroles.command()
    async def admin(self, ctx, admin_name=None):
        """Set admin role."""
        if not admin_name:
            await self.config.guild(ctx.guild).admin.set(None)
            return await ctx.send("Admin role removed.")
        await self.config.guild(ctx.guild).admin.set(str(admin_name))
        await ctx.send(f"Admin role has been set to {admin_name}.")

    @serverroles.command()
    async def invite(self, ctx, invite_link=None):
        """Set default invite link."""
        if not invite_link:
            await self.config.guild(ctx.guild).invite.set(None)
            return await ctx.send("Invite link removed.")
        await self.config.guild(ctx.guild).invite.set(str(invite_link))
        await ctx.send(f"Invite link has been set to {invite_link}.")

    @serverroles.command(name="appeal")
    async def _serverroles_appeal(self, ctx, invite_link=None):
        """Set appeal-here invite link."""
        if ctx.guild.id == 565475499007148043:
            return
        if not invite_link:
            await self.config.guild(ctx.guild).appeal.set(None)
            return await ctx.send("Appeal invite link removed.")
        await self.config.guild(ctx.guild).appeal.set(str(invite_link))
        await ctx.send(f"Appeal invite link has been set to {invite_link}.")

    @serverroles.command()
    async def invite18(self, ctx, invite_link=None):
        """Set below-18 invite link."""
        if ctx.guild.id == 565475499007148043:
            return
        if not invite_link:
            await self.config.guild(ctx.guild).invite18.set(None)
            return await ctx.send("<18 invite link removed.")
        await self.config.guild(ctx.guild).invite18.set(str(invite_link))
        await ctx.send(f"<18 invite link has been set to {invite_link}.")

    @serverroles.command()
    async def settings(self, ctx):
        """Get current settings."""
        data = await self.config.guild(ctx.guild).all()

        try:
            arole = discord.utils.get(ctx.guild.roles, name=data["admin"]).name
        except AttributeError:
            arole = None
        try:
            mrole = discord.utils.get(ctx.guild.roles, name=data["moderator"]).name
        except AttributeError:
            mrole = None
        dlink = data["invite"]
        alink = data["appeal"]
        link18 = data["invite18"]

        msg = (
            f"**Admin role:** {arole}\n"
            f"**Moderator role:** {mrole}\n"
            f"**Default link:** {dlink}\n"
            f"**Third strike link:** {alink}\n"
            f"**<18 invite link:** {link18}"
        )

        embed = discord.Embed(
            colour=ctx.guild.me.top_role.colour,
            title="__Gamers settings__",
            description=msg,
        )
        return await ctx.send(embed=embed)

    # FOR MEMBERS:
    @commands.command()
    @commands.guild_only()
    async def support(self, ctx: commands.Context, *, message=""):
        """Opens a support ticket."""
        if ctx.guild.id not in self.servers:
            return

        author = ctx.message.author
        name_moderator = await self.config.guild(ctx.guild).moderator()
        role_add = get(ctx.guild.roles, name="PENDING SUPPORT")
        role_men = get(ctx.guild.roles, name=name_moderator)

        await author.add_roles(role_add)
        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(
                "**Thank you for reaching out to us, {0}!**\n\n{1} have been notified that you need assistance.\n\n**Problem:** Not specified.\n*Please state your problem/issue now so we can get to you as soon as possible. If it is personal, state it as well.*".format(
                    author.mention, role_men.mention
                )
            )
        else:
            await ctx.send(
                "**Thank you for reaching out to us, {0}!**\n\n{1} have been notified that you need assistance.\n\n**Problem:** {2}".format(
                    author.mention, role_men.mention, message
                )
            )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def appeal(self, ctx: commands.Context):
        """Appeal for a strike removal."""
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
                return

        author = ctx.message.author
        name_moderator = await self.config.guild(ctx.guild).moderator()
        role_men = get(ctx.guild.roles, name=name_moderator)

        await role_men.edit(mentionable=True)
        await ctx.send(
            "{0}, {1} have been notified that you'd like to appeal.".format(
                author.mention, role_men.mention
            )
        )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def mod(self, ctx: commands.Context, *, message=""):
        """Calls Mods."""
        if ctx.guild.id not in self.servers:
            return

        author = ctx.message.author
        name_moderator = await self.config.guild(ctx.guild).moderator()
        role_men = get(ctx.guild.roles, name=name_moderator)

        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send(f"{role_men.mention}")
        else:
            await ctx.send(
                "{0}\n{1}: {2}".format(role_men.mention, author.mention, message)
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

    # FOR SAURICORD MEMBERS:
    @commands.command()
    @commands.guild_only()
    async def sc(self, ctx: commands.Context):
        """Opens a SauriCord ticket."""
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
                return

        author = ctx.message.author
        role_men = get(ctx.guild.roles, name="🖤 Twitch Mods 🖤")

        await role_men.edit(mentionable=True)
        await ctx.send(
            "{0}, {1} needs help with their roles!".format(
                role_men.mention, author.mention
            )
        )
        await role_men.edit(mentionable=False)

    @commands.command()
    @commands.guild_only()
    async def tmod(self, ctx: commands.Context, *, message=""):
        """Calls Twitch Mods."""
        if ctx.guild.id not in self.servers:
            return
        else:
            if ctx.guild.id == 565475499007148043:
                return

        author = ctx.message.author
        role_men = get(ctx.guild.roles, name="🖤 Twitch Mods 🖤")

        await role_men.edit(mentionable=True)
        if not message:
            await ctx.send("{0}".format(role_men.mention))
        else:
            await ctx.send(
                "{0}\n{1}: {2}".format(role_men.mention, author.mention, message)
            )
        await role_men.edit(mentionable=False)

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

        is_host = (
            get(ctx.guild.get_member(user.id).roles, id=503344113920245761) is not None
        )
        if is_host:
            pass
        else:
            return

        role_men = get(ctx.guild.roles, name="Event ping")

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

        role_men = get(ctx.guild.roles, name="Poll ping")

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

        role_rem1 = get(ctx.guild.roles, name="PENDING SUPPORT")
        role_rem2 = get(ctx.guild.roles, name="Personal")

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

        role_add = get(ctx.guild.roles, name="Personal")
        channel_men = get(ctx.guild.channels, name="personal-support")

        await target.add_roles(role_add)
        await ctx.send(
            "{0}, move to {1} please.".format(target.mention, channel_men.mention)
        )

    @commands.group(autohelp=True)
    @commands.guild_only()
    @checks.mod_or_permissions(ban_members=True)
    async def message(self, ctx):
        """Message specified users about Mod things."""
        if ctx.guild.id not in self.servers:
            return
        pass

    @message.command()
    async def strike(self, ctx: commands.Context, target: discord.Member):
        """Sends user a DM about them getting kicked out due to receiving a third strike."""
        guild = ctx.guild
        channel_men = get(ctx.guild.channels, name="appeal-here")
        link_invite = await self.config.guild(ctx.guild).appeal()
        await target.send(
            "You've been kicked from {0} upon receiving a third warning. You can rejoin using the link below and appeal by typing `>appeal` in {1}.\n{2}".format(
                guild.name, channel_men.mention, link_invite
            )
        )
        await ctx.send(
            "Sent the kick message to {0}#{1} ({2})".format(
                target.name, target.discriminator, target.id
            )
        )

    @message.command(aliases=["18"])
    async def underage(self, ctx: commands.Context, target: discord.Member):
        """Sends user a DM about them getting kicked out due being underaged."""
        if ctx.guild.id == 565475499007148043:
            return
        guild = ctx.guild
        channel_men = get(ctx.guild.channels, name="below-18")
        link_invite = await self.config.guild(ctx.guild).invite18()
        await target.send(
            "You've been kicked from {0} upon being underaged. You can rejoin using the link below and talking to Mods in {1}.\n{2}".format(
                guild.name, channel_men.mention, link_invite
            )
        )
        await ctx.send(
            "Sent the kick message to {0}#{1} ({2})".format(
                target.name, target.discriminator, target.id
            )
        )

    @message.command()
    async def ban(self, ctx: commands.Context, target: discord.Member):
        """Sends user a DM about them getting a banned."""
        guild = ctx.guild
        await target.send(
            "You've been banned from {0}. If you'd like to appeal, add `Add me to appeal#5028` and wait for them to message you.".format(
                guild.name
            )
        )
        await ctx.send(
            "Sent the ban message to {0}#{1} ({2})".format(
                target.name, target.discriminator, target.id
            )
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

        five = get(ctx.guild.roles, name="5+")
        channel = get(ctx.guild.text_channels, name="naughty-bank")
        await channel.set_permissions(five, read_messages=True, send_messages=False)
        await ctx.message.add_reaction("✅")
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

        five = get(ctx.guild.roles, name="5+")
        channel = get(ctx.guild.text_channels, name="naughty-bank")
        await channel.set_permissions(five, read_messages=True, send_messages=True)
        await bank.wipe_bank(guild=ctx.guild)
        await ctx.message.add_reaction("✅")
        await channel.send(
            "---------------------------------MONTHLY COMPETITION HAS STARTED---------------------------------"
        )

    # NAUGHTY GAMERS SERVER ONLY:
    @commands.command()
    @commands.guild_only()
    async def request(self, ctx: commands.Context):
        """Opens a verification ticket."""
        author = ctx.message.author
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role
        role_req1 = get(ctx.guild.roles, id=482562113055752193)  #'Male' role
        role_req2 = get(ctx.guild.roles, id=482562112909082624)  #'Female' role
        role_req3 = get(ctx.guild.roles, id=488340447220072459)  #'Trans' role
        role_men = get(ctx.guild.roles, id=482977157581373465)  #'Verifiers' role

        if (
            role_req1 in author.roles
            or role_req2 in author.roles
            or role_req3 in author.roles
        ):  # Checks if author has a gender role
            await author.add_roles(role_add)  # Adds 'PENDING VERIFICATION' role
            await role_men.edit(mentionable=True)  # Makes 'Verifiers' mentionable
            await ctx.send(
                "{0} have been notified that you need assistance.\n\n**What role(s) are you requesting, {1}?**".format(
                    role_men.mention, author.mention
                )
            )
            await role_men.edit(mentionable=False)  # Makes 'Verifiers' unmentionable
        else:
            await ctx.send(
                "Are you sure you've read <#482572215330799627> properly? Because it doesn't look like it."
            )

    @commands.command(hidden=True)
    @commands.guild_only()
    async def cupcake(self, ctx: commands.Context):
        """That's a secret."""
        author = ctx.message.author
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add = get(ctx.guild.roles, id=482693992732164098)  #'Secret role' role
        role_rem = get(ctx.guild.roles, id=491277913862176769)  #'I can't read' role
        role_men = get(ctx.guild.roles, id=482653546357981184)  #'Admins' role

        if role_rem in author.roles:  # Checks if author has 'I can't read'
            await author.add_roles(role_add)  # Adds 'Secret role'
            await author.remove_roles(role_rem)  # Removes 'I can't read' role
            await author.send(
                "Congratulations, {0}, you can officially read! <:sauriHype:528330460779118603> Admins will give you some yummy cookies in a bit.".format(
                    author.name
                )
            )
            await role_men.edit(mentionable=True)  # Makes 'Admins' mentionable
            await ctx.send(
                "{0} - {1} ({2})".format(role_men.mention, author.mention, author.id)
            )
            await role_men.edit(mentionable=False)  # Makes 'Admins' unmentionable
        else:
            await ctx.send("Good try.")

    # FOR VERIFIERS:
    @commands.command()
    @commands.guild_only()
    async def a(self, ctx: commands.Context, target: discord.Member):
        """Age Verified"""
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add = get(ctx.guild.roles, id=482562076364242944)  #'Age Verified' role
        role_rem = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role
        role_check = get(ctx.guild.roles, id=482562100170850308)  #'Non Catfish' role

        if role_check in target.roles and role_rem in target.roles:
            await target.add_roles(role_add)  # Adds 'Age Verified' role
            await target.remove_roles(role_rem)  # Removes 'PENDING VERIFICATION' role
            await ctx.send(
                "{0}, please assign additional roles in <#484432494288961566>.".format(
                    target.mention
                )
            )
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(),
                title="Verification approved for __Age Verified__.",
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
        elif role_rem in target.roles:
            await ctx.send(
                "Uh oh, {0} needs to be `Non Catfish` first.".format(target.mention)
            )
        else:
            await ctx.send(
                "Uh oh, {0} did not request verification.".format(target.mention)
            )

    @commands.command()
    @commands.guild_only()
    async def b(self, ctx: commands.Context, target: discord.Member):
        """Non Catfish + Age Verified"""
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add1 = get(ctx.guild.roles, id=482562076364242944)  #'Age Verified' role
        role_add2 = get(ctx.guild.roles, id=482562100170850308)  #'Non Catfish' role
        role_rem1 = get(ctx.guild.roles, id=482664678955286538)  #'Catfish' role
        role_rem2 = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role

        if role_rem2 in target.roles:
            await target.add_roles(role_add1)  # Adds 'Age Verified' role
            await target.add_roles(role_add2)  # Adds 'Non Catfish' role
            await target.remove_roles(role_rem1)  # Removes 'Catfish' role
            await target.remove_roles(role_rem2)  # Removes 'PENDING VERIFICATION' role
            await ctx.send(
                "{0}, please assign additional roles in <#484432494288961566>.".format(
                    target.mention
                )
            )
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(),
                title="Verification approved for both __Catfish__ and __Age Verified__.",
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
    async def c(self, ctx: commands.Context, target: discord.Member):
        """Non Catfish"""
        ng_id = 482560976307355658
        if ctx.guild.id != ng_id:
            return

        role_add = get(ctx.guild.roles, id=482562100170850308)  #'Non Catfish' role
        role_rem1 = get(ctx.guild.roles, id=482664678955286538)  #'Catfish' role
        role_rem2 = get(
            ctx.guild.roles, id=482655573964488706
        )  #'PENDING VERIFICATION' role

        if role_rem2 in target.roles:
            await target.add_roles(role_add)  # Adds 'Non Catfish' role
            await target.remove_roles(role_rem1)  # Removes 'Catfish' role
            await target.remove_roles(role_rem2)  # Removes 'PENDING VERIFICATION' role
            await ctx.send(
                "{0}, see you in <#482572653459275776>.".format(target.mention)
            )
            log = get(ctx.guild.text_channels, id=483698888386019335)  # mod-log channel
            embed = discord.Embed(
                colour=await ctx.embed_colour(),
                title="Verification approved for __Catfish__.",
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
                colour=await ctx.embed_colour(), title="Verification denied."
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
