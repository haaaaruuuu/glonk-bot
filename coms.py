# discord
from discord.ext import commands
import discord

import schedule

from bot import glonkB
from boards import get_info
from boards import set_info
from boards import build_board

import os
from dotenv import load_dotenv

load_dotenv()
go_api_key = os.getenv('A_YOUTUBE')
yt_channel = os.getenv('S_YOUTUBE')

class glonkCog(commands.Cog):
    def __init__(self, bot: glonkB):
        self.bot = bot

    @commands.command()
    async def glonk(self, ctx):
        ytboard = await build_board()
        message = await ctx.send(embed = ytboard)
        with open('board.txt', 'w') as x:
            x.write(str(message.id))
            x.close()

def setup(bot):
    bot.add_cog(glonkCog(bot))
