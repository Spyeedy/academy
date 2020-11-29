import datetime
import pymongo

from datetime import timedelta

import discord
from discord.ext import commands
from constants import *
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

client = pymongo.MongoClient('localhost', 27017)
database = client['academy']

bot = commands.Bot(command_prefix='-', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


@bot.event
async def on_member_join(member):
    welcome = bot.get_channel(717863274909139055)
    await welcome.send(JOIN_MESSAGE.format(member))


@bot.command()
async def time(ctx):
    await ctx.send(TIME.format(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")))


@bot.command()
async def build(ctx, arg):
    builds = database['builds']
    search = builds.find_one({"name": arg})
    if search:
        await ctx.send(search["value"])
    else:
        await ctx.send(BUILD_NOT_EXISTS)


@bot.command()
async def passives(ctx, arg):
    characters = database['characters']

    character = characters.find_one(
        {'acronym': arg},
        {'passives': 3})

    passives_text = ''
    for p in character["passives"]:
        passives_text +=  "**" + p['name'] + "**\n" + p["description"] + "\n"
        for buff in p['buffs']:
            passives_text += "*" + buff + "*\n"
        passives_text += '\n'
    await ctx.send(passives_text)


@bot.command()
async def specials(ctx, arg):
    characters = database['characters']

    character = characters.find_one(
        {'acronym': arg},
        {'specials': 3})

    specials_text = ''
    for sp in character["specials"]:
        specials_text +=  "**" + sp['name'] + "**\n" + sp["description"] + "\n"
        for buff in sp['buffs']:
            specials_text += "*" + buff + "*\n"
        specials_text += '\n'
    await ctx.send(specials_text)


@bot.command()
async def supermove(ctx, arg):
    characters = database['characters']

    character = characters.find_one(
        {'acronym': arg},
        {'supermove': 1})

    supermove_text =  "**" + character['name'] + "**\n" + character["description"] + "\n"
    for buff in character['buffs']:
        supermove_text += "*" + buff + "*\n"
    supermove_text += '\n'
    await ctx.send(supermove_text)


@bot.command()
async def name(ctx, arg):
    characters = database['characters']

    character = characters.find_one(
        {'acronym': arg},
        {'name': 1})
    await ctx.send(character["name"])


@bot.command()
async def predators(ctx):
    await ctx.send(PREDATORS)


@bot.command()
async def tower(ctx):
    await ctx.send(TOWER)


@bot.command()
async def knights(ctx):
    await ctx.send(KNIGHTS)


@bot.command()
async def reverse(ctx):
    await ctx.send(REVERSE)


@bot.command()
async def vipers(ctx):
    await ctx.send(VIPERS)


@bot.command()
async def stars(ctx):
    await ctx.send(STARS)


@bot.command()
async def batman(ctx):
    await ctx.send("**Who am i ?**", file=discord.File("gif/batmanson2.gif"))


@bot.command()
async def lasteris(ctx):
    await ctx.send(file=discord.File("gif/lasteris.gif"))


@bot.command()
async def kirito(ctx):
    await ctx.send("**All hail to The King**")


@bot.command()
async def imqrx(ctx):
    await ctx.send("**Meet The Big Boss**", file=discord.File("gif/imqrx.gif"))


@bot.command()
async def blackwolf(ctx):
    await ctx.send("**King's knight**", file=discord.File("gif/blackwolf.gif"))


@bot.command()
async def thera(ctx):
    await ctx.send(file=discord.File("gif/cap.gif"))

@bot.command()
async def myee(ctx):
    await ctx.send("**Bring ur hot Bootylicious ESF  mammy  out.**", file=discord.File("emoji/myee.jpg"))


@bot.command()
async def dx2(ctx):
    await ctx.send("**The Courageous knight for the people**")


@bot.command()
async def makslays(ctx):
    await ctx.send(file=discord.File("emoji/mac.jpeg"))


@bot.command()
async def ramza(ctx):
    await ctx.send("**It was me, Barry!**", file=discord.File("gif/ramza.gif"))


@bot.command()
async def misty(ctx):
    await ctx.send("I am the night!", file=discord.File("gif/misty.gif"))

@bot.command()
async def nyryon(ctx):
    await ctx.send("**South Italy Nyry-Don**", file=discord.File("emoji/4407.png"))


@bot.command()
async def spyeedy(ctx):
    await ctx.send("**do ur work properly ss boy ? or no salary for u**", file=discord.File("gif/spyeedy.gif"))

@bot.command()
async def tony(ctx):
    tony_member = await ctx.guild.fetch_member(552431423165038628)
    await ctx.send("**The Boot Legend** - {0.mention}".format(
        tony_member
    ))


@bot.command()
async def haitodo(ctx):
    await ctx.send("Relax Alex", file=discord.File("gif/haitodo.gif"))


@bot.command()
async def newplayer(ctx):
    choose_league_channel = ctx.guild.get_channel(717026493557112963)
    fast_improve_channel = ctx.guild.get_channel(753734930583781437)
    await ctx.send(NEW_PLAYER.format(
    choose_league_channel,
    fast_improve_channel))


@bot.command()
async def join(ctx, *args):
    role_predator = ctx.guild.get_role(717029499463794718)
    role_star = ctx.guild.get_role(717029493088452688)
    role_viper = ctx.guild.get_role(717029489124573224)
    role_jumpers = ctx.guild.get_role(775433895020855326)

    joined = False

    if len(args) == 1:
        league = args[0].lower()
        if league in ["predators", "vipers", "stars", "jumpers"]:
            if league == "predators":
                if role_predator in ctx.author.roles:
                    joined = True
                else:
                    await ctx.author.add_roles(role_predator)
            elif league == "vipers":
                if role_viper in ctx.author.roles:
                    joined = True
                else:
                    await ctx.author.add_roles(role_viper)
            elif league == "stars":
                if role_star in ctx.author.roles:
                    joined = True
                else:
                    await ctx.author.add_roles(role_star)
            elif league == "jumpers":
                if role_jumpers in ctx.author.roles:
                    joined = True
                else:
                    await ctx.author.add_roles(role_jumpers)
            if joined:
                await ctx.send("{0.mention}, you have already joined in {1}!".format(ctx.author, args[0]))
            else:
                await ctx.send("role {0} is added to {1}".format(args[0], ctx.author.mention))
        else:
            await ctx.send("You can interact only with those roles:\npredators, vipers, stars")
    else:
        await ctx.send("you can not change role of other member.")


@bot.command()
async def remove(ctx, *args):
    role_predator = ctx.guild.get_role(717029499463794718)
    role_star = ctx.guild.get_role(717029493088452688)
    role_viper = ctx.guild.get_role(717029489124573224)
    role_jumpers = ctx.guild.get_role(775433895020855326)

    removed = False

    if len(args) == 1:
        league = args[0].lower()
        if league in ["predators", "vipers", "stars", "jumpers"]:
            if league == "predators":
                if role_predator not in ctx.author.roles:
                    removed = True
                else:
                    await ctx.author.remove_roles(role_predator)
            elif league == "vipers":
                if role_viper in ctx.author.roles:
                    removed = True
                else:
                    await ctx.author.remove_roles(role_viper)
            elif league == "stars":
                if role_star not in ctx.author.roles:
                    removed = True
                else:
                    await ctx.author.remove_roles(role_star),
            elif league == "jumpers":
                if role_jumpers not in ctx.author.roles:
                    removed = True
                else:
                    await ctx.author.remove_roles(role_jumpers)
            if removed:
                await ctx.send("{0}, you have already removed from {1}!".format(ctx.author.name, args[0]))
            else:
                await ctx.send("role {0} is removed from {1}".format(args[0], ctx.author.mention))
        else:
            await ctx.send("You can interact only with those roles:\npredators, vipers, stars")
    else:
        await ctx.send("you can not change role of other member. It is not implemented yet.")


@bot.command()
async def help(ctx):
    await ctx.send(HELP)


@bot.command(name='jump-cd')
async def cooldown(ctx, *args):
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    end_time = cur_time + timedelta(days=21)

    cds = database['cooldowns']

    jumper_id_str = str(ctx.author.id)
    cur_str = cur_time.strftime(DATE_TIME_FORMAT)
    end_str = end_time.strftime(DATE_TIME_FORMAT)

    if not args:
        cds.update_one(
            filter= {'memberId': jumper_id_str},
            update= {
                "$set": {
                    'memberId': jumper_id_str,
                    'start': cur_str,
                    'end': end_str,
                    'name': ctx.author.display_name
                    }
                },
                upsert= True)

        await ctx.send(CD_START_MESSAGE.format(
            ctx.author,
            cur_str,
            end_str))

    elif args[0] == 'status':
        jumper = cds.find_one({'memberId': jumper_id_str})
        if jumper:
            days_left = (
                datetime.datetime.strptime(jumper['end'], DATE_TIME_FORMAT) -
                datetime.datetime.strptime(jumper['start'], DATE_TIME_FORMAT)
                ).days
            if days_left > 0:
                await ctx.send(CD_STATUS.format(ctx.author, days_left))
            else:
                await ctx.send(CD_EXPIRED.format(ctx.author))


token_src = database["authorization"].find_one({"current": True})

bot.run(token_src["token"])
