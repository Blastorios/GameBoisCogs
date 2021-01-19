from .userjoin import UserJoin


def setup(bot):
    userjoin_cog = UserJoin(bot)
    bot.add_cog(userjoin_cog)
