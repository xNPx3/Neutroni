from discord.ext import commands
from discord.ext.commands import *
import json
import discord
import userdata
from datetime import datetime
from datetime import timedelta
from random import randint, randrange


class Economy(commands.Cog, name='Rahaa ja muuta'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Rahalista')
    async def rikkaat(self, ctx):
        users = userdata.load_users(ctx.message.guild.id)
        # with open('users.json', 'r') as f:
        #    users = json.load(f)
        high_score_list = sorted(
            users, key=lambda x: users[x].get('money', 0), reverse=True)
        message = ''
        for number, user in enumerate(high_score_list):
            message += '{0}. | {1} | {2}€\n'.format(
                number + 1, user, users[user].get('money', 0))

        await ctx.message.channel.send(content=message)

    @commands.command(brief="Noppapeli")
    async def noppa(self, ctx, panos: int):
        users = userdata.load_users(ctx.message.guild.id)
        if panos <= 0 or panos > users[ctx.message.author.name]['money']:
            return
        else:
            userdata.add_money(users, ctx.message.author, -panos)
            num1 = randint(1, 6)
            num2 = randint(1, 6)
            await ctx.message.channel.send(
                f"Heitit {num1}.\nNeutroni heitti {num2}.")
            if num1 > num2:
                await ctx.message.channel.send(f"Voitit {panos * 2}€!")
                userdata.add_money(users, ctx.message.author, panos * 2)
            else:
                if num1 == num2:
                    await ctx.message.channel.send(f"**TASAPELI!** Rahamääräsi pysyy samana.")
                    userdata.add_money(users, ctx.message.author, panos)
                else:
                    await ctx.message.channel.send(f"Hävisit {panos}€.")
        userdata.dump_users(ctx.message.guild.id, users)

    @commands.command(brief="Ryöstää käyttäjän.")
    async def ryöstö(self, ctx, käyttäjä: discord.User):
        users = userdata.load_users(ctx.message.guild.id)
        my_money = users[ctx.message.author.name]['money']
        target_money = users[käyttäjä.name]['money']
        try:
            if users[käyttäjä.name]['passive'] == True:
                await ctx.message.channel.send('Tätä käyttäjää ei voi ryöstää.')
                return
        except KeyError:
            pass
        if target_money > 2000:
            num = randrange(0, 22)
            if num <= 10:
                userdata.add_money(users, ctx.message.author, target_money / 3)
                userdata.add_money(users, käyttäjä,  -(target_money / 3))
                await ctx.message.channel.send(
                    "Varastit {}€ käyttäjältä {}!".format(int(target_money / 3), käyttäjä.name))
            elif num > 10 and num < 21:
                userdata.add_money(users, ctx.message.author, -(my_money / 3))
                userdata.add_money(users, käyttäjä, my_money / 3)
                await ctx.message.channel.send(
                    "**Voi ei!** Jäit kiinni ja joudut maksamaan {}€ käyttäjälle {}!".format(int(my_money / 3), käyttäjä.name))
            elif num == 21:
                userdata.add_money(users, ctx.message.author,
                                   target_money - 1000)
                users[käyttäjä.name]['money'] = 1000
                await ctx.message.channel.send(
                    "**JACKPOT!** Varastit {}€ käyttäjältä {}!".format(target_money - 1000, käyttäjä.name))
        else:
            await ctx.message.channel.send(f"Käyttäjällä {käyttäjä.name} on vain {target_money}€.")
        userdata.dump_users(ctx.message.guild.id, users)

    @commands.command(brief='Päivittäiset Kela-tuet')
    async def kelatuki(self, ctx):
        users = userdata.load_users(ctx.message.guild.id)
        try:
            last = users[ctx.message.author.name]['last-daily']
        except KeyError:
            userdata.update_data(users, ctx.message.author)
            return
        if last == None:
            userdata.add_money(users, ctx.message.author, 100)
            await ctx.message.channel.send("```Tässä päivitäiset Kela-tukesi! Rahat +100€```")
            users[ctx.message.author.name]['last-daily'] = datetime.now()
        else:
            t = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            hours = ((datetime.now() - t).total_seconds() / 60 / 60)
            if hours >= 24:
                if hours <= 48:
                    m = users[ctx.message.author.name]['daily-streak']
                    userdata.add_money(users, ctx.message.author, 100 + (m * 50))
                    await ctx.message.channel.send(f"```Tässä päivitäiset Kela-tukesi! Rahat +{100 + (m * 50)}€ (Putki: {m} päivää)```")
                    users[ctx.message.author.name]['last-daily'] = datetime.now()
                    users[ctx.message.author.name]['daily-streak'] += 1
                else:
                    userdata.add_money(users, ctx.message.author, 100)
                    await ctx.message.channel.send("```Tässä päivitäiset Kela-tukesi! Rahat +100€```")
                    users[ctx.message.author.name]['last-daily'] = datetime.now()
            else:
                td = timedelta(seconds=24*60*60 -
                               round((datetime.now() - t).total_seconds()))
                await ctx.message.channel.send(f"```Kela ei anna tukia vielä! Odota {td}.```")
        userdata.dump_users(ctx.message.guild.id, users)

    @commands.command(brief='Näyttää käyttäjän rahat')
    async def lompakko(self, ctx, käyttäjä: discord.User = None):
        users = userdata.load_users(ctx.guild.id)
        if käyttäjä == None:
            try:
                money = users[ctx.message.author.name]['money']
            except KeyError:
                userdata.update_data(users, ctx.message.author)
            await ctx.message.channel.send(f'Sinulla on {money}€.')
        else:
            try:
                money = users[käyttäjä.name]['money']
            except KeyError:
                userdata.update_data(users, käyttäjä)
            await ctx.message.channel.send(f'Käyttäjällä {käyttäjä.name} on {money}€.')

    @commands.command(brief='Lisää rahaa käyttäjälle')
    @has_permissions(manage_guild=True)
    async def lisääraha(self, ctx, käyttäjä: discord.User, määrä: int):
        users = userdata.load_users(ctx.guild.id)
        userdata.add_money(users, käyttäjä, määrä)
        userdata.dump_users(ctx.message.guild.id, users)
        await ctx.message.channel.send(f"Lisättiin {määrä}€ käyttäjän {käyttäjä.name} lompakkoon.")

    @commands.command(brief='Asettaa käyttäjän rahamäärän annettuun arvoon')
    @has_permissions(manage_guild=True)
    async def asetaraha(self, ctx, käyttäjä: discord.User, määrä: int):
        users = userdata.load_users(ctx.guild.id)
        try:
            users[käyttäjä.name]['money'] = määrä
            await ctx.message.channel.send(f"Asetettiin käyttäjän {käyttäjä.name} rahamäärä arvoon {määrä}€.")
        except KeyError:
            userdata.update_data(users, käyttäjä)
        userdata.dump_users(ctx.message.guild.id, users)

    @commands.command(brief='Lahjoittaa rahaa käyttäjälle.')
    async def lahjoita(self, ctx, käyttäjä: discord.User, määrä: int):
        users = userdata.load_users(ctx.guild.id)
        userdata.add_money(users, ctx.message.author, -määrä)
        userdata.add_money(users, käyttäjä, määrä)
        userdata.dump_users(ctx.message.guild.id, users)
        await ctx.message.channel.send(f'{ctx.message.author.name} lahjoitti {määrä}€ käyttäjälle {käyttäjä.name}.')


def setup(bot):
    bot.add_cog(Economy(bot))
