import asyncio
import discord
import contextlib

from typing import Any, Union, Iterable, Optional
from discord.utils import get

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import pagify, escape
from redbot.core.utils.menus import menu, close_menu
from redbot.core.utils.predicates import ReactionPredicate

from redbot.core.bot import Red

__author__ = "saurichable"

Cog: Any = getattr(commands, "Cog", object)


class SauriHelp(Cog):
    """
    Menu like help
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.controls = {
            "🏠": self.home_page,
            "👾": self.base_page,
            "🎮": self.lfg_page,
            "🎶": self.music_page,
            "🏦": self.bank_page,
            "🍪": self.cookie_page,
            "🔰": self.xp_page,
            "❌": close_menu,
        }

    async def home_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 0:
            page = 0
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def base_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 1:
            page = 1
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def lfg_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 2:
            page = 2
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def music_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 3:
            page = 3
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def bank_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 4:
            page = 4
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def cookie_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 5:
            page = 5
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    async def xp_page(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        if page != 6:
            page = 6
        else:
            return
        return await menu(
            ctx, pages, controls, message=message, page=page, timeout=timeout
        )

    @commands.command(aliases=["commands"])
    @commands.guild_only()
    async def h(self, ctx: commands.Context):
        bot = self.bot
        ng_id = 482560976307355658

        if ctx.guild.id == ng_id:
            home_info = """React to see the commands.

🏠 - this page
👾 - basic and fun commands
🎮 - LFG commands
🎶 - music commands
🏦 - bank commands
🍪 - cookie commands
🔰 - XP commands
❌ - close the menu

**Type `{0}mod [message]` to call the Mods.**
""".format(
                ctx.clean_prefix
            )
            info = """If you want to specifically talk to Ellie, DM me (the bot, not Ellie) and describe what you need.
If you have any issue with anyone in the server, you can report them to our Mods in <#483055779490955285>.
If you have any more questions, check out <#513832730782466048> before DMing me or opening a support ticket.
If you are stuck with your `I can't read` role, read the rules. Staff members will not help you in any other way nor will Ellie. Note that by complaning about the ping, you're breaking our rule no. 16.
"""

        else:
            home_info = """React to see the commands.

🏠 - this page
👾 - basic and fun commands
🎮 - LFG commands (NG only)
🎶 - music commands
🏦 - bank commands
🍪 - cookie commands
🔰 - XP commands
❌ - close the menu
"""
            info = """`{0}suggest <message>` - Suggest something (global).

If you want to specifically talk to Ellie, DM me (the bot, not Ellie) and describe what you need.
""".format(
                ctx.clean_prefix
            )

        home = discord.Embed(color=ctx.guild.me.top_role.colour, description=home_info)
        home.add_field(name="**__Various information:__**", value=info)
        home.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        home.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        base_commands = """`{0}owner` - Get basic information about Ellie.
`{0}social` - Get Ellie's social media.
`{0}funfact` - Get a random funfact about Ellie.
`{0}bothosting` - Have Ellie host your bot.
`{0}serversetup` - Have Ellie set your server.
`{0}donate` - Support NG and SauriBot.
`{0}link` - Get our invite link.
""".format(
            ctx.clean_prefix
        )

        fun_commands = """`{0}oof [message_ID]` - React oof to previous message (if not specified).
`{0}react <message> [message_ID]` - Add letter(s) as reaction to previous message (if not specified).
`{0}choose <"option 1" "option 2" ...>` - Choose between multiple options.
`{0}lmgtfy <search_terms>` - Create a lmgtfy link.
`{0}urban <word>` - Search the Urban Dictionary.
""".format(
            ctx.clean_prefix
        )

        special_commands = """`{0}suggest <message>` - Suggest something. [<#548934952000159770>]
`{0}apply` - Apply to be a member of our staff team. [<#482569528145084416>]
`{0}report <message>` - Report someone/something (this is anonymous). [<#483055779490955285>]
`{0}support [message]` - Request help from Mods. [<#510525920638009344>]
`{0}request` - Request verification. [<#482571815668023306>]
""".format(
            ctx.clean_prefix
        )

        base = discord.Embed(
            color=ctx.guild.me.top_role.colour, description=base_commands
        )
        base.title = "**__Base commands:__**"
        if ctx.guild.id == ng_id:
            base.add_field(name="**__Special commands:__**", value=special_commands)
        base.add_field(name="**__Fun commands:__**", value=fun_commands)
        base.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        base.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        if ctx.guild.id == ng_id:
            lfg_commands = """*Note that you may only use these commands when you're looking to play and in their appropriate channels!*

`{0}al <message>` - Ping the 'Apex Legends' role.
`{0}cod <message>` - Ping the 'Call of Duty' role.
`{0}d2 <message>` - Ping the 'Destiny 2' role.
`{0}fortnite <message>` - Ping the 'Fortnite' role.
`{0}lol <message>` - Ping the 'LoL' role.
`{0}ow <message>` - Ping the 'Overwatch' role.
`{0}rl <message>` - Ping the 'Rocket League' role.
""".format(
                ctx.clean_prefix
            )

        else:
            lfg_commands = (
                "This page is specific for NG server only so it's hidden from you!"
            )

        lfg = discord.Embed(
            color=ctx.guild.me.top_role.colour, description=lfg_commands
        )
        lfg.title = "**__LFG commands:__**"
        lfg.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        lfg.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        if ctx.guild.id == ng_id:
            music_commands = """*Note that you need to be level at least 5 to use music commands! Check your level in <#482565077292154894>.*

`{0}play <song>` - Play a URL or search for a song.
`{0}search <song>` - Pick a song with a search.
`{0}now` - Now playing.
`{0}prev` - Skips to the start of the previously played track.
`{0}skip` - Skips to the next track, 75% vote is needed.
`{0}queue` - Lists the queue.
`{0}bump <index>` - Bump a track number to the top of the queue.
`{0}remove <index>` - Remove a specific song number from the queue.
`{0}pause` and `>resume` - Self explanatory.
`{0}stop` - Stops playback and clears the queue.
`{0}volume <number>` - Sets the volume, 1 - 150%.
`{0}repeat` - Toggle repeat.
`{0}shuffle` Toggle shuffle.
`{0}disconnect` - Disconnect from the voice channel.
""".format(
                ctx.clean_prefix
            )

        else:
            music_commands = """`{0}play <song>` - Play a URL or search for a song.
`{0}search <song>` - Pick a song with a search.
`{0}now` - Now playing.
`{0}prev` - Skips to the start of the previously played track.
`{0}skip` - Skips to the next track, 75% vote is needed.
`{0}queue` - Lists the queue.
`{0}bump <index>` - Bump a track number to the top of the queue.
`{0}remove <index>` - Remove a specific song number from the queue.
`{0}pause` and `>resume` - Self explanatory.
`{0}stop` - Stops playback and clears the queue.
`{0}volume <number>` - Sets the volume, 1 - 150%.
`{0}repeat` - Toggle repeat.
`{0}shuffle` Toggle shuffle.
`{0}disconnect` - Disconnect from the voice channel.
""".format(
                ctx.clean_prefix
            )

        music = discord.Embed(
            color=ctx.guild.me.top_role.colour, description=music_commands
        )
        music.title = "**__Music commands:__**"
        music.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        music.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        if ctx.guild.id == ng_id:
            bank_commands = """What is Naughty Bank? Read <#483365987111141376> for info about the Monthly Competition!
        
`{0}bank balance` - Shows your bank balance.
`{0}payday` - Get free 100 metres of rope. Can be used every 24 hours.
`{0}bank transfer <@someone> <amount>` - Transfer metres of rope to other user.
`{0}leaderboard` - Leaderboard for the current month.
""".format(
                ctx.clean_prefix
            )

        else:
            bank_commands = """`{0}bank balance` - Shows your bank balance.
`{0}payday` - Get free 100 metres of rope. Can be used every 24 hours.
`{0}bank transfer <@someone> <amount>` - Transfer metres of rope to other user.
`{0}leaderboard` - Leaderboard for the current month.
""".format(
                ctx.clean_prefix
            )

        bank = discord.Embed(
            color=ctx.guild.me.top_role.colour, description=bank_commands
        )
        bank.title = "**__Bank commands:__**"
        bank.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        bank.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        cookie_commands = """`{0}cookie` - Get your daily dose of cookies.
`{0}cookies [@someone]` - Check how many cookies you have.
`{0}gift <@someone> <amount>` - Give someone some yummy cookies.
`{0}steal [@someone]` - Steal some cookies from someone. If someone isn't specified, it's a randomly picked user.
`{0}cookielb` - Shows you the cookie leaderboard.
""".format(
            ctx.clean_prefix
        )

        store_commands = """`{0}buy [item name]` - Buy an item from the cookie store. If an item isn't listed, shows all available items.
`{0}return <item name>` - Return an item, you will only get 50% of the price.
`{0}redeem <item name>` - Redeem a redeemable item (f.e. games).
`{0}inventory [@someone]` - See all items you own.
`{0}rminventory <item name>` - Get rid of an item.
""".format(
            ctx.clean_prefix
        )

        cookie = discord.Embed(
            color=ctx.guild.me.top_role.colour, description=cookie_commands
        )
        cookie.title = "**__Cookie commands:__**"
        cookie.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        cookie.add_field(name="**__Store commands:__**", value=store_commands)
        cookie.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        xp_commands = """`{0}profile [@someone]` - Displays your profile.
`{0}rank [@someone]` - Displays your rank.
`{0}rep [@someone]` - Gives a reputation point to a designated player.
`{0}top [-global/-rep]` - Displays leaderboard. If nothing is specified, displays server's leaderboard.
""".format(
            ctx.clean_prefix
        )

        set_commands = """`{0}backgrounds [profile/rank]` - Gives a list of available backgrounds.
`{0}lvlset profile bg <image_name>` - Set your profile background.
`{0}lvlset profile color <section> <colour>` - Set info color. Sections: *exp/rep/badge/info/all*; colours: *default/white/hex*
`{0}lvlset profile info <info> ` - Set your user info.
`{0}lvlset profile title <title> ` - Set your title.
`{0}lvlset rank bg <image_name>` - Set your rank background
`{0}lvlset rank color <section> <colour>` - Set info color. Sections: *exp/info*; colours: *default/white/hex*
""".format(
            ctx.clean_prefix
        )

        xp = discord.Embed(color=ctx.guild.me.top_role.colour, description=xp_commands)
        xp.title = "**__XP commands:__**"
        xp.set_author(
            name="{0} Help Manual".format(bot.user.name), icon_url=bot.user.avatar_url
        )
        xp.add_field(name="**__Settings commands:__**", value=set_commands)
        xp.set_footer(
            text="{0}#{1} is a private bot hosted by Ellie~♡#0001. If you have any inquiries, DM me.".format(
                bot.user.name, bot.user.discriminator
            )
        )

        embeds = [home, base, lfg, music, bank, cookie, xp]
        await menu(ctx, embeds, self.controls)
