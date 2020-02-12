import asyncio
import re
import random
import discord

from typing import Any
from discord.utils import get
from inspect import getsource
from textwrap import dedent

from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import warning, pagify, error

from redbot.core.bot import Red

BaseCog = getattr(commands, "Cog", object)


class Source(BaseCog):
    """Get a source code of any command. I do not support this cog, use at your own risk."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(
        lambda ctx: getattr(ctx.bot.get_cog("Dev"), "__module__", None)
        == "redbot.core.dev_commands"
    )
    @checks.is_owner()
    async def dump_module_cache(self, ctx: commands.Context, module_prefix: str):
        import sys

        dumped = 0

        for k in list(sys.modules.keys()):
            if k.startswith(module_prefix):
                dumped += 1
                del sys.modules[k]

        await ctx.send(f"Dumped {dumped} modules from the cache")

    @checks.is_owner()
    @commands.command()
    async def src(self, ctx: commands.Context, *, command_name: str):
        """ Get the source for a command or sub command."""
        command = self.bot.get_command(command_name)
        try:
            callback = command.callback
            if hasattr(callback, "__actual_callback__"):
                callback = callback.__actual_callback__
            source = pagify(dedent(getsource(callback)))
        except OSError:
            await ctx.send(error(translate("src.cannot_retrieve")))
        else:
            await ctx.send_interactive(source, box_lang="py")
