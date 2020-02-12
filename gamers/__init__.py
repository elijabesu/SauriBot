from .gamers import Gamers


def setup(bot):
    bot.add_cog(Gamers(bot))
