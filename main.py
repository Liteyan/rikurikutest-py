import os
from dotenv import load_dotenv
load_dotenv()
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json
import aiofiles
import random

async def prefix_from_json(bot, message):
    async with aiofiles.open("prefix.json") as f:
        contents = await f.read()
    data = json.loads(contents)  # json形式として読み込む
    return data.get(str(message.guild.id),"rkts:")

token = os.environ['token']
bot = commands.Bot(
    command_prefix=prefix_from_json,
    #commands.when_mentioned_or(prefix_from_json),
    case_insensitive=True,
    #help_command=None,
    activity=discord.Game("rkts:help | りくりくりーくねっ！")
  )

INITIAL_EXTENSIONS = [
    "jishaku",
    "commands.admin",
    "commands.embed",
    "commands.riku"
]

@bot.event
async def on_ready():
    print("Logged in as {0.user}!".format(bot))
    
    for cmd in INITIAL_EXTENSIONS:
        try:
            bot.load_extension(cmd)
        except Exception as error:
            print(f"[Error] {cmd} -> {error}")
        else:
            print(f"{cmd} was loaded!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        sai56 = ["裁BAN", "5656"]
        await ctx.send(f"陸ちゃん「そんなコマンドないから{random.choice(sai56)}ね？＾＾」")
        return
    if isinstance(error, commands.errors.MissingPermissions): #エラーの内容を判別
        await ctx.send("権限無いからﾘｸﾘｸﾘｰｸﾈｯ")
        return
    ch = 848217203073744916
    embed = discord.Embed(title="エラー情報", description="", color=0xf00)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    m = await bot.get_channel(ch).send(embed=embed)
    await ctx.send(f"なんかエラー発生したからﾘｸﾘｸﾘｰｸﾈｯ\nちなみにエラーIDこれ: `{m.id}`")


def command_not_found(self, string):
    sai56 = ["裁BAN", "5656"]
    return f"陸ちゃん「`{string}`なんてコマンドないから{random.choice(sai56)}ね？＾＾」"

def subcommand_not_found(self, command, string):
    if isinstance(command, commands.Group) and len(command.all_commands) > 0:
        # もし、そのコマンドにサブコマンドが存在しているなら
        return f"{command.qualified_name} に {string} なんてサブコマンドはないぞ＾＾"
    return f"{command.qualified_name} にサブコマンドは無いって知ってる？"

bot.run(token)