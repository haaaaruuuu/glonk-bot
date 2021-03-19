from discord.ext import commands, tasks
import discord

from bot import glonkB
from boards import build_board
from boards import error_embed

import os
from dotenv import load_dotenv

load_dotenv()
go_api_key = os.getenv('A_YOUTUBE')
yt_channel = os.getenv('S_YOUTUBE')

class glonkCog(commands.Cog):
    def __init__(self, bot: glonkB):
        self.bot = bot
        self.update_board.start()

    @commands.command()
    async def glonk(self, ctx):
        ytboard = await build_board()
        message = await ctx.send(embed = ytboard)
        with open('boardmsg.txt', 'w') as x:
            x.write(str(message.id))
        with open('boardchan.txt', 'w') as y:
            y.write(str(message.channel.id))
    
    @tasks.loop(minutes=15.0)
    async def update_board(self):
        with open('boardmsg.txt') as x:
            msg_id = "".join(x.readlines())
        with open('boardchan.txt') as y:
            msg_channel = "".join(y.readlines())
        msg_id = int(msg_id)
        msg_channel = int(msg_channel)
        
        channel = self.bot.get_channel(msg_channel)
        msg = await channel.fetch_message(msg_id)

        embed = await build_board()
        await msg.edit(embed=embed)
    
    @update_board.before_loop
    async def before_update_board(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(glonkCog(bot))
