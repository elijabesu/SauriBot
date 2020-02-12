from .kavliaris import Kavliaris


def setup(bot):
    bot.add_cog(Kavliaris(bot))
