from .sauribot import SauriBot


def setup(bot):
    bot.add_cog(SauriBot(bot))
