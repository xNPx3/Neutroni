import discord
from discord.ext import commands
from discord.ext.commands import *
import hashlib


class Salaus(commands.Cog, name='Salaus'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Salaa tekstin avaimella.')
    async def salaa(self, ctx):
        await ctx.message.delete()

        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        msg1 = await ctx.message.channel.send("Teksti:")
        text_msg = await self.bot.wait_for('message', check=check, timeout=60)
        text = str(text_msg.content)
        await msg1.delete()
        await text_msg.delete()

        msg2 = await ctx.message.channel.send("Avain:")
        key_msg = await self.bot.wait_for('message', check=check, timeout=60)
        key = str(key_msg.content)
        await key_msg.delete()
        await msg2.delete()

        # region spagettikoodia
        t = []
        for c in text:
            t.append(int(ord(c)))
        k = []
        for c in key:
            k.append(int(ord(c)))
        while len(k) < len(t):
            k += k
        e = []
        for i in range(len(t)):
            e.append(t[i] * k[i])
        a = []
        for c in e:
            a.append(str(chr(c)))
        f = ''
        for c in a:
            f += c
        # endregion

        await ctx.message.channel.send("Salattu teksti:", delete_after=60)
        await ctx.message.channel.send(content=f, delete_after=60)

    @commands.command(brief='Purkaa tekstin avaimella')
    async def pura(self, ctx):
        await ctx.message.delete()

        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        msg1 = await ctx.message.channel.send("Teksti:")
        text_msg = await self.bot.wait_for('message', check=check, timeout=60)
        text = str(text_msg.content)
        await msg1.delete()
        await text_msg.delete()

        msg2 = await ctx.message.channel.send("Avain:")
        key_msg = await self.bot.wait_for('message', check=check, timeout=60)
        key = str(key_msg.content)
        await key_msg.delete()
        await msg2.delete()

        # region spagettikoodia
        t = []
        for c in text:
            t.append(int(ord(c)))
        k = []
        for c in key:
            k.append(int(ord(c)))
        while len(k) < len(t):
            k += k
        e = []
        for i in range(len(t)):
            e.append(int(t[i] / k[i]))
        a = []
        for c in e:
            a.append(str(chr(c)))
        f = ''
        for c in a:
            f += c
        # endregion

        await ctx.message.channel.send("Purettu teksti:", delete_after=60)
        await ctx.message.channel.send(content=f, delete_after=60)

    @commands.command(brief='Hash')
    async def hash(self, ctx, hash_type: str):
        await ctx.message.channel.send('Syötä viesti', delete_after=30)
        m = await self.bot.wait_for('message', check=check, timeout=30)
        result = ''
        if hash_type.lower() == 'md5':
            result = str(hashlib.md5(m.content.encode('utf-8')).hexdigest())
        elif hash_type.lower() == 'sha256':
            result = str(hashlib.sha256(m.content.encode('utf-8')).hexdigest())
        else:
            await ctx.message.channel.send('ei-tunnettu hash-tyyppi', delete_after=30)
        await m.delete()
        await ctx.message.channel.send(result)


def setup(bot):
    bot.add_cog(Salaus(bot))
