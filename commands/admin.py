import discord
from discord.ext import commands
import io
import textwrap
import traceback
from contextlib import redirect_stdout

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.result = ""
        self._last_member = None

    def escape_quote(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command(name="saisyu", brief="最終宣告です")
    @commands.is_owner()
    async def cmd_saisyu(self, ctx, arg):
        await ctx.send(f"最終宣告だ踊れや{arg}")

    @commands.command(name="get_error", brief="エラーを取ります")
    @commands.is_owner()
    async def get_error(self, ctx, error_id):
        await ctx.send(embed = (await self.bot.get_channel(848217203073744916).fetch_message(error_id)).embeds[0])

    @commands.command(name="eval", pass_context=True, brief="evalしてﾘｸﾘｸﾘｰｸﾈｯ")
    @commands.is_owner()
    async def cmd_eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'self': self,
            '_': self.result
        }

        env.update(globals())

        body = self.escape_quote(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self.result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    return bot.add_cog(admin(bot))