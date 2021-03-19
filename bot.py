# modules
import os
from dotenv import load_dotenv

# discord commands
import discord
from discord.ext import commands


# measure days ago
from datetime import datetime

# asyncio and scheduler
import asyncio
import schedule

# credential variables
load_dotenv()
TOKEN = os.getenv('D_TOKEN')
GUILD = os.getenv('D_GUILD')
MOD_ROLE = os.getenv('M_ROLE')
yt_channel = os.getenv('S_YOUTUBE')

# glonk bot class to schedule events
# define time constants to pull info at intervals of X
class glonkB(commands.Bot):
    # commands.Bot 
    def __init__(self):
        # inherit from discord.Client & commands.Bot
        super().__init__(command_prefix='$')

        self.load_extension("coms")
        self.run(TOKEN)

        self.channel = yt_channel
        

    async def on_ready(self):
        for guild in self.guilds:
            if guild == GUILD:
                break
        print(
            f'{self.user} has connected to Discord! \n'
            f'Server: {guild.name} \n'
            f'ID: {guild.id} \n'
            )
        self.activity = discord.Activity(name='You', type=discord.ActivityType.watching)
        await self.change_presence(activity=self.activity)
        await asyncio.sleep(0.5)
        schedule.run_pending()

    async def on_message(self, message: discord.Message):
        if self.is_mod(message.author):
            try:
                await self.process_commands(message)
            except discord.ext.commands.errors.CommandNotFound:
                pass
            

    def is_mod(self, member: discord.member):
        mod = discord.utils.get(member.roles, id=int(MOD_ROLE))
        if mod:
            return True
        return False

if __name__ == "__main__":
    bot = glonkB()
