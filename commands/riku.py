import discord
from discord.ext import commands
import random
import json
import aiofiles
import asyncio

class riku(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="test", aliases=["question", "q", "tsts"], brief="これが本題")
    async def cmd_test(self, ctx):
        test_load = json.load(open("questions.json", 'r'))
        q_number = random.randint(1, 6)
        q = test_load[q_number]["q"]
        a = test_load[q_number]["a"]
        embed = discord.Embed(title="もんだい！", description=f"{q}\n答え合わせは10秒後！", color=0x36b8fa)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        ans_embed = discord.Embed(title="もんだい！", description=q, color=0x36b8fa)
        ans_embed.add_field(name="答え", value=f"||**{a}**||")
        await msg.edit(embed=ans_embed)

    @commands.command(name="rikuriku", brief="色々なりくりく")
    async def cmd_riku2(self, ctx):
        rikuarr = ["ﾘｸﾘｸﾘｰｸﾈｯ", "りくりくりーくねっ！", ":metal:(´>∀<`*):metal:ﾘｯｸﾘｯｸﾆｰ:hearts:"]
        await ctx.send(random.choice(rikuarr))

    @commands.command(name="hello", brief="はろー！")
    async def cmd_hello(self, ctx):
        await ctx.send("はろー！")

    @commands.command(name="prefix", brief="Prefixを変えます")
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix):
        async with aiofiles.open("prefix.json") as f:
            contents = await f.read()
            data = json.loads(contents)  # json形式として読み込む
            before_prefix = data.get(str(ctx.guild.id),"rkts:")
            data[str(ctx.guild.id)] = prefix  # 辞書内で prefix を変更しておく

            async with aiofiles.open("prefix.json","w") as f:
                await f.write(json.dumps(data))  # 変更済みの辞書をjson形式で出力
                await ctx.send(f"Prefixが`{before_prefix}`から`{prefix}`に変更されてりくりく！")
                await ctx.guild.me.edit(nick=f"[{prefix}] {self.bot.user.name}")

def setup(bot):
    return bot.add_cog(riku(bot))