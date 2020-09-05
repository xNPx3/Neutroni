import discord
import json


def update_data(users, user):
    if not user.name in users:
        users[user.name] = {}
        users[user.name]['daily-streak'] = 1
        users[user.name]['experience'] = 0
        users[user.name]['level'] = 1
        users[user.name]['money'] = 100
        users[user.name]['last-daily'] = None
        users[user.name]['reports'] = None


def load_users(guildId):
    try:
        with open('./users/' + str(guildId) + '-users.json', 'r') as f:
            users = json.load(f)
        return users
    except FileNotFoundError:
        #open(message.guild.name + '-users.json', 'w+')
        print("error")
        f = open('./users/' + str(guildId) + '-users.json', 'a+')
        f.write("{}")
        f.close()
        return load_users(guildId)


def dump_users(guildId, users):
    try:
        with open('./users/' + str(guildId) + '-users.json', 'w') as f:
            json.dump(users, f, sort_keys=True, indent=4, default=str)
    except FileNotFoundError:
        #open(message.guild.name + '-users.json', 'w+')
        f = open('./users/' + str(guildId) + '-users.json', 'a+')
        f.write("{}")
        f.close()
        dump_users(guildId, users)

async def level_up(users, user, message):
    experience = users[user.name]['experience']
    lvl_start = users[user.name]['level']
    lvl_end = int(experience ** (1/3))
    if lvl_start < lvl_end:
        await message.channel.send(content=f'{user.mention} on saavuttanut tason {lvl_end}! Ansaitsit {lvl_end * 10}€')
        add_money(users, user, 10 * lvl_end)
        users[user.name]['level'] = lvl_end

def add_money(users, user, money):
    try:
        users[user.name]['money'] += int(money)
    except KeyError:
        users[user.name]['money'] = 100
        users[user.name]['money'] += int(money)