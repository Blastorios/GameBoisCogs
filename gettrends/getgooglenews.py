'''Get Google Trend Data inside of Discord
Created by: @Blastorios
Created on: 08/01/2021'''

# TODO
# - Actual function to get the links(preferablly with multiprocessing)
# - A responder when the function is called through the server. Giving periodic updates as the articles are being downloaded.
# - A selector so users can select how many papers they want to select(based on the amount of articles we found)
# - Provide a summary of all the articles, with emoticons, on which pressed, will perform a certain action like downloading or printing the article as regular text within a dm.


from redbot.core.bot import Red
from redbot.core import checks
from redbot.core import commands

from typing import Union, Dict, List, Tuple, Iterator

from spellchecker import SpellChecker
from random_word import RandomWords
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import discord
import nltk

__version__ = "1.0.0"

# Required to enable article downloading. Will throw a 422 error if specified differently.
BROWSER_USER_AGENT = user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

# Some default Google News values
DEFAULT_TIME_PERIOD = "7d"
DEFAULT_LANGUAGE = "en"
DEFAULT_ENCODING = "utf-8"
DEFAULT_ENGINE = ["news", "search"]
DEFAULT_MAX_PERIOD = 30


class GetNews(commands.Cog, name='Get News'):
    """Get The specified Google Content for a subject of your interest.
    Or: simply let a random word decide your curiousity!

    Current features..."""

    def __init__(self, bot,
                 browser_user_agent: str = BROWSER_USER_AGENT,
                 default_time_period: Union[str, int] = DEFAULT_TIME_PERIOD,
                 default_language: str = DEFAULT_LANGUAGE,
                 default_encoding: str = DEFAULT_ENCODING,
                 engine_options: List[str] = DEFAULT_ENGINE,
                 default_max_period: int = DEFAULT_MAX_PERIOD):

        self.bot = bot
        self.browser_user_agent = browser_user_agent
        self.default_time_period = default_time_period
        self.default_language = default_language
        self.default_encoding = default_encoding
        self.engine_options = engine_options
        self.default_max_period = default_max_period

    async def sendToUser(self, ctx, message, user: discord.Member = None, embed_bool=False):
        """"""
        try:
            # See if the user got set and verified
            if not user:
                # Embed the message
                if embed_bool:
                    await user.send(embed=message)
                # Send it as a regular text message
                else:
                    await user.send(message)
        # Ensure to provide an error when user has caused an error (for logging purposes)
        except discord.errors.Forbidden:
            pass

    def __verify_parsed_elements(self,
                                 keywords: List,
                                 time_period: Union[str, int],
                                 search_engine: Union[str, int],
                                 max_period: int
                                 ) -> Tuple:
        """Check all parsed values to prevent down-the-line errors.
        The current methodology ensures enough default values to
        create a secure processing after random variable insertions

        Input:
            keywords;
                A list of terms to search for within the google engine.

            time_period;
                Set the period by which to search for the specified keywords.

            search_engine;
                Choose which of Google's Engine you would like to use.

            max_period;
                The maximum period to look for articles 
                (recommended to limit for one month per search)

        Output:
            inserted_keywords;
                A parsed keyword list, checked for inappropriate terms (coming feature) 
                and typo's.
        """

        if not keywords:
            # When we have items
            inserted_keywords = keywords
        else:
            # Empty: add a single random word to use
            random_word_generator = RandomWords()
            keywords.append(random_word_generator.get_random_word())

        # Attempt to parse the inserted value. Revert to the default if all fails.
        try:
            # Add the condition after the first to prevent a type Error.
            if isinstance(time_period, int):
                # Ensure time period is below 30 dys.
                if time_period < max_period:
                    time_scale = f"{time_period}d"
                else:
                    time_scale = f"{max_period}d"
            else:
                if 'd' in time_period and int(''.join(filter(str.isdigit, time_period))) < max_period:
                    time_scale = time_period
                else:
                    time_scale = f"{max_period}d"
        except:
            time_scale = "7d"

        if isinstance(search_engine, int):
            used_engine = DEFAULT_ENGINE[search_engine]
        else:
            used_engine = search_engine.lower() if search_engine.lower(
            ) in DEFAULT_ENGINE else DEFAULT_ENGINE[0]

        return inserted_keywords, time_scale, used_engine

    async def _get_links_to_keywords(self,
                                     keywords: Dict = {},
                                     time_period: Union[str,
                                                        int] = self.default_time_period,
                                     language: str = self.default_language,
                                     encoding: str = self.default_encoding,
                                     search_engine: Union[str, int] = "",
                                     max_period: int = self.default_max_period
                                     ):
        """Retreive links from the Google Trends page by using the unofficial
        Google News Trends Python API"""

        try:
            self.inserted_keywords, self.time_scale, self.engine = await self.__verify_parsed_elements(
                keywords, time_period, search_engine, max_period)
        except Exception as e:
            raise ValueError(
                f"Unable to validate the parsed content... Encountered {e}")

    @commands.command()
    async def articles(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
