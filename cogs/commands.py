from discord.ext import commands
from discord.ext.commands import *
from random import randint
from typing import Union
import json
import discord
import requests
import userdata


class Commands(commands.Cog, name='Komennot'):

    def __init__(self, bot):
        self.bot = bot

    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author

    @commands.command(brief='pommikone :DDDDDD')
    async def pommikone(self, ctx, kohde: Union[discord.User, discord.TextChannel]):
        await ctx.channel.send("Syötä viesti")
        r = await self.bot.wait_for('message', check=check, timeout=30)
        m = str(r.content)

        e = discord.Embed(title="POMMIKONE :DDD", description="Tupolev Tu-160 strateginen pommikone iskee kohteeseen " +
                          kohde.name + "!", color=0xff1111)
        e.set_image(
            url="https://cdn.discordapp.com/attachments/743799682131689502/748872241017782272/f2.jpg")
        e.add_field(name="Viesti käyttäjältä " +
                    ctx.message.author.name, value=m)
        #e.add_field(name="Bomber Captain", value=ctx.message.author)
        if isinstance(kohde, discord.User):
            await kohde.create_dm()
            await kohde.dm_channel.send(embed=e)
        else:
            await kohde.send(embed=e)

    @commands.command(brief='')
    async def äänestys(self, ctx):
        await ctx.message.delete()

        d = await ctx.channel.send("Syötä äänestyksen aihe")
        r = await self.bot.wait_for('message', check=check, timeout=30)
        m = str(r.content)

        await d.delete()
        await r.delete()

        e = discord.Embed(title="**ÄÄNESTYS!**", description=m, color=0x00ff00)
        message = await ctx.message.channel.send(embed=e)
        up = '\N{THUMBS UP SIGN}'
        down = '\N{THUMBS DOWN SIGN}'
        await message.add_reaction(up)
        await message.add_reaction(down)

    @commands.command(brief='Tarkistaa kryptovaluutan hinnan')
    async def btc(self, ctx, valuutta):
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + \
            valuutta + '&vs_currencies=eur'
        response = requests.get(url)
        value = response.json()[valuutta]["eur"]
        await ctx.message.channel.send("Hinta: {}€".format(value))

    @commands.command(brief='Poistaa viestejä.')
    @has_permissions(manage_messages=True)
    async def poista(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)
        await ctx.channel.send(content='{} viestiä poistettu.'.format(amount), delete_after=5)

    @commands.command(brief='')
    async def top(self, ctx):
        users = userdata.load_users(ctx.message.guild.id)
        # with open('users.json', 'r') as f:
        #    users = json.load(f)
        high_score_list = sorted(
            users, key=lambda x: users[x].get('experience', 0), reverse=True)
        message = ''
        for number, user in enumerate(high_score_list):
            message += '{0}. | {1} | {2}xp | Level {3}\n'.format(
                number + 1, user, users[user].get('experience', 0), users[user].get('level', 0))

        await ctx.message.channel.send(content=message)

    @commands.command(brief='Näyttää käyttäjän tason.')
    async def taso(self, ctx, käyttäjä: discord.User):
        users = userdata.load_users(ctx.message.guild.id)
        await ctx.channel.send(f"Käyttäjä {käyttäjä.name} on tasolla {users[käyttäjä.name]['level']} ja hänellä on {users[käyttäjä.name]['experience']} XP.")

    @commands.command(brief='')
    async def arvo(self, ctx, käyttäjä: discord.User, asia: str):
        p = randint(0, 100)
        await ctx.message.channel.send(f'{käyttäjä.name} on {p}% {asia}')

    @commands.command(brief='Arpoo numeroita')
    async def numero(self, ctx, määrä: int = 10, min: int = 0, max: int = 9):
        if määrä > 1000:
            await ctx.message.channel.send(content='Numeroiden maksimimäärä on 1000.', delete_after=10)
            return
        msg = ''
        for i in range(määrä):
            msg += str(randint(min, max))
        if len(msg) <= 2000:
            await ctx.message.channel.send(msg)
        else:
            splits = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
            for j in range(len(splits)):
                await ctx.message.channel.send(splits[j])


def setup(bot):
    bot.add_cog(Commands(bot))
