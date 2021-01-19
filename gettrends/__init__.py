'''Initialization File
Created by: @Blastorios
Created on: 09/01/2021'''

from .getgooglenews import GetNews
import nltk


def setup(bot):
    if nltk.download('punkt'):
        pass
    else:
        nltk.download('punkt')

    bot.add_cog(GetGoogleNews())
