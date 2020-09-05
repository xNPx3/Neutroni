import os
import string
import discord
import discord.ext.commands
import discord.ext.tasks
import userdata
import random
from discord.ext.tasks import loop
from discord.ext.commands import *
from discord.ext.commands.errors import *
from itertools import cycle

BOT_PREFIX = '!'
client = discord.ext.commands.Bot(command_prefix=BOT_PREFIX)

with open('status.txt', 'r') as f:
    st = f.read().splitlines()
status = cycle(st)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


def word_check(input):
    with open('words.txt', 'r') as f:
        content = f.read().splitlines()
    words = input.split()  # split
    if any(item in content for item in words):
        return True
    else:
        return False


@loop(seconds=30)
async def change_status():
    activity = discord.Activity(
        name=(next(status)), type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)


@client.event
async def on_ready():
    change_status.start()
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    users = userdata.load_users(member.guild.id)
    userdata.update_data(users, member)
    userdata.dump_users(member.guild.id, users)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(content="Sinulla ei ole riittäviä oikeuksia komennon suorittamiseen", delete_after=10)
    elif isinstance(error, MissingRequiredArgument):
        await ctx.channel.send(content="Lisää puuttuva parametri", delete_after=10)
    elif isinstance(error, BotMissingPermissions):
        await ctx.channel.send(content="Botilla ei ole riittäviä oikeuksia komennon suorittamiseen.", delete_after=10)
    elif isinstance(error, KeyError):
        await ctx.channel.send(content="Avainta ei löydy.", delete_after=10)
    else:
        print(error)
    pass


@client.event
async def on_message(message):
    if message.author.id != 366482170405191690:
        if message.channel == client.get_channel(743788691809632276):
            return
    if client.user.mention in message.content.split():
        await message.channel.send(f'Tee {client.command_prefix}help nähdäksesi kaikki komennot.')
    if message.author.bot == False:
        new_message = message.content.translate(str.maketrans(
            string.punctuation, ' '*len(string.punctuation)))
        if word_check(str.lower(new_message)):
            await message.delete()
            await message.channel.send(content="Viestisi on poistettu koska se sisälsi kielletyn sanan.", delete_after=10)

        if "uwu" in str.lower(message.content):
            await message.channel.send(content='Warning, the Council of High Intelligence and Educational Findings (C.H.I.E.F.), has detected an "uwu". This is a code BRUH #4 level threat. Stay indoors and do not interact with cringe weebs until the threat has been classified as "it". Unless the code BRUH is retracted, "uwu" will be classified under "not it" until further notice.')
        elif "owo" in str.lower(message.content):
            await message.channel.send(content='Warning, the Council of High Intelligence and Educational Findings (C.H.I.E.F.), has detected an "owo". This is a code BRUH #4 level threat. Stay indoors and do not interact with cringe weebs until the threat has been classified as "it". Unless the code BRUH is retracted, "owo" will be classified under "not it" until further notice.')

        users = userdata.load_users(message.guild.id)
        userdata.update_data(users, message.author)
        users[message.author.name]['experience'] += random.randint(1, 10)
        await userdata.level_up(users, message.author, message)
        userdata.dump_users(message.guild.id, users)

        try:
            await client.process_commands(message)
        except Exception as e:
            message.channel.send(e)


client.run('token')
