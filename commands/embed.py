import discord
from discord.ext import commands

class embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="testembed")
    async def cmd_testembed(self, ctx):
        await ctx.send(embed = discord.Embed(title="はろー！", description="pythonで作ってるお", color=0x1bff49))

def setup(bot):
    bot.add_cog(embed(bot))