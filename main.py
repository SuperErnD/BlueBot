# -*- coding: utf-8 -*-
import discord#discord as discord
#from discord import channel
#from discord.ext import commands
from discord.ext import ipc, commands
import random
from config import settings 
import asyncio
import asyncio
import logging
from urllib import request
import json
import requests
import sqlite3
file_name = 'economy.db'
import os
import sys
import random
import asyncio
import json

import asyncio
import random
import datetime
import os
import youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ""
from discord.enums import ButtonStyle
ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # Bind to ipv4 since ipv6 addresses cause issues at certain times
}
ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
class MyBot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "Swas")


    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc server is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)
intents = discord.Intents.default()
intents.members = True
bot = MyBot(command_prefix = settings['prefix'], intents=intents, pm_help=True, case_insensitive=True)#, intents = discord.Intents.default())

bot.remove_command("help")
client = bot

@client.command()

async def number(ctx, num : int):
    a = random.randint(1, 200)
    if num == a:
        print('You Win!')
        await ctx.send('You win!')
    else:
        print('You not win :(')
        await ctx.send('You not win :(')
        print(a)
@client.command()
async def helpgiver(ctx):
    # Help command that lists the current available commands and describes what they do
    ghelp = discord.Embed(color = 0x7289da)
    ghelp.set_author(name = 'Commands/Help', icon_url = '')
    ghelp.add_field(name= 'helpme', value = 'This command took you here!', inline = False)
    ghelp.add_field(name= 'version', value = 'Displays the current version number and recent updates.', inline = False)
    ghelp.add_field(name= 'giveaway', value = '__Can only be accessed by users with the "Giveaway Host" role.__\nStarts a giveaway for the server! This command will ask the host 3 questions.  The host will have 30 seconds per question to answer or they will be timed out!', inline = False)
    ghelp.add_field(name= 'reroll `#channel_name` `message id`', value = '__Can only be accessed by users with the "Giveaway Host" role.__\nThey must follow the command with the copied message id from the giveaway.', inline = False)
    ghelp.set_footer(text = 'Use the prefix "!" before all commands!')
    await ctx.send(embed = ghelp)
@client.command()
async def ball(ctx, clovo):
    clovo = clovo
    a = random.randint(0, 6)
    if a == 1:
        ctx.send('хз')
    elif a == 2:
        ctx.send('да')
    elif a == 3:
        ctx.send('неа')
    elif a == 4:
        ctx.send('наверное')
    elif a == 5:
        ctx.send('не советую')
    elif a == 6:
        ctx.send('я думаю не стоит')


@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['В каком канале хотите провести розыгрыш?', 'Какой приз?', 'Сколько будет идти (в секундах)?',]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('Вы не ответили вовремя. Пожалуйста, попробуйте еще раз и обязательно отправьте ответ в течение 30 секунд после вопроса.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'Вы не правильно указали канал. Пожалуйста, сделайте это следующим образом: {ctx.channel.mention}')
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(f'Розыгрыш {prize} начнется в ближайшее время.\nОбратите внимание на {channel.mention}, розыгрыш закончится через {time} секунд.')

    # Giveaway embed message
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'ВРЕМЯ РОЗЫГРЫША!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'{ctx.author.name} разыгрывает: {prize}!', value = f'Нажимайте на 🎉, чтобы принять участие!\n Заканчивается через {round(time/60, 2)} минут!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'Раздача закончится в {end} UTC!')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'РОЗЫГРЫШ ЗАКОНЧИЛСЯ!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Приз: {prize}', value = f'🥳 **Выиграл**: {winner.mention}\n 🎫 **Участвовало**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Спасибо за участвие!')
    await channel.send(embed = winning_announcement)



@client.command()
@commands.has_permissions(administrator=True)
async def reroll(ctx, channel: discord.TextChannel, id : int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await channel.fetch_message(id)
    except:
        await ctx.send("Incorrect id.")
        return
    if not channel:
        await ctx.send('Вы не указали канал!')
    else:
        pass
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'Розыгрыш был повторен организатором!', icon_url = 'https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name = f'🥳 Новый победитель:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)
@bot.ipc.route()
async def get_guild_count(data):
    return len(bot.guilds) # returns the len of the guilds to the client
@client.command()
async def orel(ctx, rr=None):
    a = random.randint(1, 2)
    print(a)
    if rr == 'орел':
        rr = 1
        if a == rr:
            ctx.send('Вы выиграли!!')
        else:
            ctx.send('Вы не выиграли к сожалению...')
    if rr == 'решка':
        rr = 2
        if a == rr:
            ctx.send('Вы выиграли!!')
        else:
            ctx.send('Вы не выиграли к сожалению...')
            
@bot.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in bot.guilds:
        final.append(guild.id)
    return final # returns the guild ids to the client

@bot.ipc.route()
async def get_guild(data):
    guild = bot.get_guild(data.guild_id)
    if guild is None: return None

    guild_data = {
        "name": guild.name,
        "id": guild.id,
        "prefix" : "?"
    }

    return guild_data


async def open_bank(user):
    columns = ["wallet", "bank"] # You can add more Columns in it !

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO economy(userID) VALUES({user.id})")
        db.commit()

        for name in columns:
            cursor.execute(f"UPDATE economy SET {name} = 0 WHERE userID = {user.id}")
        db.commit()

        cursor.execute(f"UPDATE economy SET wallet = 5000 WHERE userID = {user.id}")
        db.commit()

    cursor.close()
    db.close()


async def get_bank_data(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def update_bank(user, amount=0, mode="wallet"):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE economy SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        db.commit()

    cursor.execute(f"SELECT {mode} FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def get_lb():
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute("SELECT userID, wallet + bank FROM economy ORDER BY wallet + bank DESC")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return users


shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]


async def open_inv(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO inventory(userID) VALUES({user.id})")

        for item in shop_items:
            item_name = item["name"]
            cursor.execute(f"UPDATE inventory SET `{item_name}` = 0 WHERE userID = {user.id}")

        db.commit()

    cursor.close()
    db.close()


async def get_inv_data(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def update_inv(user, amount: int, mode):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is not None:
        cursor.execute(f"UPDATE inventory SET `{mode}` = `{mode}` + {amount} WHERE userID = {user.id}")
        db.commit()

    cursor.execute(f"SELECT `{mode}` FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users

@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    author = ctx.message.author
    userAvatarUrl = author.avatar_url
    if not avamember:
        embed = discord.Embed(description =  "Аватар " + author.mention, color = 0x00008b)
        embed.set_image(url = userAvatarUrl)
        embed.set_footer(text=f'{ctx.author}', icon_url = userAvatarUrl)
        await ctx.send(embed = embed)
    try:
        author = ctx.message.author
        userAvatarUrl = avamember.avatar_url
        embed = discord.Embed(description =  "Аватар " + avamember.mention, color = 0x00008b)
        embed.set_image(url = userAvatarUrl)
        embed.set_footer(text=f'{avamember}', icon_url = userAvatarUrl)
        await ctx.send(embed = embed)
    except discord.Forbidden:
        return
    except discord.HTTPException:
        return
@bot.event
async def on_member_join(member):
    server = member.server
    channel = server.default_channel
    retStr = str("""```yaml\nПривет!\nДобро пожаловать на наш сервер!\nНадеюсь тебе тут понравится.\nЕсли заблудешься пиши !help,кстати у нас все команды пишутся с !\nДля получения роли зайди в чат получения роли\nудачи тебе```""")
    embed = discord.Embed(title="Welcome",colour=discord.Colour.blue())
    embed.add_field(name="Привет",value=retStr)
    await bot.send_message(channel, embed=embed)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):

        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, команда не найдена!', colour = discord.Color.red()))
    if isinstance(error, commands.errors.MissingPermissions):

        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, вы не имеете права на испольнение команды!', colour = discord.Color.red()))
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name} вы не указали аргумент какой-то'))
        return
@client.command()
async def server(ctx):
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    
    BannerURl = ctx.guild.banner
    
    icon = ctx.guild.icon
    members = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
    bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
    all = len(ctx.guild.members)
    text = len(ctx.guild.voice_channels)
    voice = len(ctx.guild.text_channels)
    category = len(ctx.guild.categories)
    allchannels = len(ctx.guild.channels)
    noanimemoji = 0
    anim_emoji = 0
    allemoji = len(ctx.guild.emojis)
    limitemoji = ctx.guild.emoji_limit
    twofa = ctx.guild.mfa_level
    for emoji in ctx.guild.emojis:
        if emoji.animated == True:
            anim_emoji += 1
        elif emoji.animated == False:
            noanimemoji += 1
    public = ctx.guild.public_updates_channel
    rules = ctx.guild.rules_channel
    description = ctx.guild.description
    region = ctx.guild.region

    embed = discord.Embed(title=f"Информация о сервере {ctx.guild.name}", color = 0x00008b)
    embed.add_field(name = "Ролей:", value = len(ctx.guild.roles), inline = True)
    embed.add_field(name="Участников", value=f"<:all:942048151571947580>: {all}\n<:members:942049581926060072> : {members}\n<:bot:942049242325843968>: {bots}")
    embed.add_field(name = "Забаненных", value = len(await ctx.guild.bans()))
    embed.add_field(name="Статусы", value=f"🟢: {statuses[0]}\n🌙: {statuses[1]}\n⛔: {statuses[2]}\n<:offline:942040928904962050>: {statuses[3]}")
    embed.add_field(name = "Каналов:", value = f"Всего: {allchannels}\nТекстовых каналов: {text}\nГолосовых каналов: {voice}\nКатегорий: {category}")
    embed.add_field(name = "Эмодзи:", value = f"Всего: {allemoji}\nАним.: {anim_emoji}\nСтат.: {noanimemoji}\nЛимит: {limitemoji}")
    embed.add_field(name = "Регион:", value = ctx.guild.region)
    if twofa == 0:
        embed.add_field(name = 'Требование 2FA', value = 'Отключено')
    else:
        embed.add_field(name = 'Требование 2FA', value = 'Включено')
    embed.add_field(name = "ID сервера:", value = ctx.guild.id)
    embed.add_field(name = "Сервер создан (По времени UTC +0)", value = ctx.guild.created_at.strftime("%d.%m.%Y\n%H:%M:%S"))
    embed.add_field(name = "Роль бота:", value = ctx.guild.self_role.mention)
    if public == None:
        embed.add_field(name = "Канал для публичных обновлений:", value = 'Нету')
    else:
        embed.add_field(name = "Канал для публичных обновлений:", value = ctx.guild.public_updates_channel)
    if rules == None:
        embed.add_field(name = "Канал правил:", value = 'Нету')
    else:
        embed.add_field(name = "Канал правил:", value = 'Нету')
    embed.add_field(name = "Уровень сервера", value = ctx.guild.premium_tier)
    embed.add_field(name = "Приглашения", value = len(await ctx.guild.invites()))
    embed.add_field(name = "Бусты", value = ctx.guild.premium_subscription_count)
    embed.add_field(name = "Роль бустеров", value = ctx.guild.premium_subscriber_role)
    embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
    embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
    embed.add_field(name = "Бот", value = ctx.guild.me.mention)
    if icon:
        embed.set_thumbnail(url = icon)
    if BannerURl:
        embed.set_image(url = BannerURl)
    await ctx.send(embed=embed)

@bot.command()
async def ver(ctx):
    await ctx.reply(f"My ver " + settings['version'] + "!")
@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.
 #This should be at your other imports at the top of your code
@bot.event
async def on_guild_join(guild):
    pass
class HelpList(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label="Модерация", description="Команды модерации", emoji="🛠"
            ),
            discord.SelectOption(
                label="Веселое!", description="Команды веселости!", emoji="😄"
            ),
            discord.SelectOption(
                label="Экономика", description="Экономика", emoji="💸"
            ),
            discord.SelectOption(
                label='Аватары', description='Команды для аватаров', emoji='🔴'
            ),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Выберете пункт...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        if self.values[0] == 'Аватары':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description='`b!blue_avatar` \n `b!pink_avatar` \n `b!multi_avatar` \n `b!yellow_avatar` \n `b!red_avatar` \n `b!grey_avatar` \n `b!green_avatar`'), ephemeral=True)
        if self.values[0] == 'Модерация':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description="Команды модерации:\n`b!ban`\n`b!mute`\n`b!unban`\n`b!kick`\n`b!ping`\n`b!unmute\n`b!ver`"), ephemeral=True)
        if self.values[0] == 'Веселое!':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description='`b!hello`\n`b!avatar`\n`b!dog`\n`b!fox`\n`b!cat`\n`b!panda`'), ephemeral=True)
        #await interaction.response.send_message(f"Your favourite colour is {self.values[0]}")
        if self.values[0] == 'Экономика':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description='Ты экономист!) \n`b!balance`\n`b!with`\n`b!dep`'), ephemeral=True)
class Helpbl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(HelpList())
    @discord.ui.button(label="Мой инвайт!", style=ButtonStyle.blurple, row=1)
    async def myinvite(
        self, button: discord.ui.Button, interaction: discord.MessageInteraction
    ):
        await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=" + str(settings['id']) + "&permissions=8&scope=bot", ephemeral=True)

    @discord.ui.button(label = 'Сервер поддержки', emoji="🥳", style=ButtonStyle.green, row=2)
    async def supportserver(
        self, button: discord.ui.Button, interaction: discord.MessageInteraction
    ):
        await interaction.response.send_message("https://discord.gg/zy3qJM4mvE", ephemeral=True)
@bot.command()
async def buttons(ctx):

    # Sends a message with a row of buttons.
    await ctx.send("Here are some buttons!", view=Helpbl())

    # This is how the command would look like: https://i.imgur.com/ZYdX1Jw.png


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help | " + str(len(bot.guilds)) + " серверов"))
    await bot.ipc.start()




    print("Bot is ready!")
    print('Im at {bot.user.name} and {bot.user.id}')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Ban пользователя', value='Пользователь {} был забанен! по причине {reason}'.format(member.mention))
    await ctx.reply(embed = emb)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Kick пользователя', value='Пользователь {} был забанен! /n по причине {reason}'.format(member.mention))
    await ctx.reply(embed = emb)
@bot.command()
async def ban_id(ctx, user_id=None, time1: str=None,*, reason=None):
    if not user_id:
        await ctx.message.add_reaction("<:error:925385765188419604>")
        Eembed = discord.Embed(description = '❌ **Ошибка! Вы не указали ID пользователя**\n**Аргументы данной команды**\n**[] обязательный аргумент, () необязательный аргумент**\n\n**Gides!ban_id [ID участника] (Длительность бана `w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд`)**', color=0x00008b)
        await ctx.send(embed = Eembed)
        return
    if not ctx.author.guild_permissions.ban_members:
        await ctx.message.add_reaction("<:error:925385765188419604>")
        Embed = discord.Embed(description = '❌ **Ошибка! У вас недостаточно прав**', color=0x00008b)
        await ctx.send(embed = Embed)
        return
    if user_id == ctx.author:
        await ctx.message.add_reaction("<:error:925385765188419604>")
        Embed = discord.Embed(description = '❌ **Ошибка! Вы не можете забанить себя**', color=0x00008b)
        await ctx.send(embed = Embed)
        return
    try:
        user = await client.fetch_user(user_id=user_id)
        Embed = discord.Embed(title = f"✅ {user} был успешно забанен", description = f'\nМодератор: {ctx.author.mention}\nДлительность бана: {time1} \nПричина: {reason}', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.guild.ban(user)
        await ctx.message.add_reaction("<:succesfully:925385120280612864>")
        Embed = discord.Embed(description = f'Тебя забанили на сервере {ctx.guild.name} по причине {reason}, Модератор: {ctx.author}, длительность: {time1}', color=0x00008b)
        await user.send(embed=Embed)
        seconds, str_time = str_time_to_seconds(time1)
        await asyncio.sleep(seconds)
        await ctx.guild.unban(user)
        link = await ctx.channel.create_invite(max_age=300)
        Embed = discord.Embed(description = f'У тебя закончился бан на сервере "{ctx.guild.name}"!Заходи по ссылке: {link}', color=0x00008b)
        await user.send(embed = Embed)
        
    except discord.Forbidden:
        return

    except discord.HTTPException:
        return
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    
    banned_users = await ctx.guild.bans()
    await ctx.channel.purge(limit=0)

    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        emb = discord.Embed(color=344462)
        emb.add_field(name='✅ UnBan пользователя', value='Пользователь {} был разбанен.'.format(member))
        await ctx.reply(embed = emb)
        return

@bot.command(aliases=["bal"])
@commands.guild_only()
async def balance(ctx):
    user = ctx.author

    await open_bank(user)

    users = await get_bank_data(user)

    wallet_amt = users[1]
    bank_amt = users[2]

    net_amt = int(wallet_amt + bank_amt)

    em = discord.Embed(
            title= f"{user.name}'s Balance",
            description= f"Wallet: {wallet_amt}\nBank: {bank_amt}",
            color=discord.Color(0x00ff00)
        )

    await ctx.send(embed=em)


@bot.command(aliases=["with"])
@commands.guild_only()
async def withdraw(ctx, *,amount= None):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    bank_amt = users[2]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, +1*bank_amt)
        await update_bank(user, -1*bank_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {bank_amt} in your wallet")

    bank = users[1]

    amount = int(amount)

    if amount > bank:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, +1 * amount)
    await update_bank(user, -1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")

#@bot.command()
#async def create_table(ctx):
    #db = sqlite3.connect(file_name)
    #cursor = db.cursor()
    
    #cols = ["wallet", "bank"] # You can add as many as columns in this !!!
    
    #cursor.execute("""CREATE TABLE economy(userID BIGINT)""")
    #db.commit()
    
    #for col in cols:
        #cursor.execute(f"ALTER TABLE economy ADD COLUMN {col}")

    #db.commit()

    #cursor.close()
    #db.close()

    #await ctx.send("Table created successfully !")

@bot.command(aliases=["dep"])
@commands.guild_only()
async def deposit(ctx, *,amount= None):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    wallet_amt = users[1]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, -1*wallet_amt)
        await update_bank(user, +1*wallet_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {wallet_amt} in your wallet")

    amount = int(amount)

    if amount > wallet_amt:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, -1 * amount)
    await update_bank(user, +1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")

@bot.command(aliases=["lb"])
#@commands.guild_only(aliases=["lb"])
async def leaderboard(ctx):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    data = []
    index = 1

    for member in users:
        if index > 10:
            break

        member_name = self.bot.get_user(member[0])
        member_amt = member[1]

        if index == 1:
            msg1 = f"**🥇 `{member_name}` -- {member_amt}**"
            data.append(msg1)

        if index == 2:
            msg2 = f"**🥈 `{member_name}` -- {member_amt}**"
            data.append(msg2)

        if index == 3:
            msg3 = f"**🥉 `{member_name}` -- {member_amt}**\n"
            data.append(msg3)

        if index >= 4:
            members = f"**{index} `{member_name}` -- {member_amt}**"
            data.append(members)
        index += 1

    msg = "\n".join(data)

    em = discord.Embed(
        title=f"Top {index} Richest Users - Leaderboard",
        description=f"It's Based on Net Worth (wallet + bank) of Global Users\n\n{msg}",
        color=discord.Color(0x00ff00),
        timestamp=datetime.datetime.utcnow()
    )
    em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
    await ctx.send(embed=em)



@bot.command()
async def mute(ctx, member: discord.Member=None, time:str=None,*, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="MutedBB")
    if not mutedRole:
        mutedRole = await guild.create_role(name="MutedBB")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
            speak=False,
            send_messages=False, 
            read_message_history=True, 
            read_messages=True)         
    if not member:
        Embed = discord.Embed(description = '❌ **Ошибка! Вы не указали пользователя**\n**Аргументы данной команды**\n**[] обязательный аргумент, () необязательный аргумент**\n\n**!mute [участник] [длительность `w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд`] (причина)**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if not time:
        Embed = discord.Embed(description = '❌ **Ошибка! Вы не указали время мута**\n**Аргументы данной команды**\n**[] обязательный аргумент, () необязательный аргумент**\n\n**!mute [участник] [длительность `w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд`] (причина)**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if member == ctx.author:
        Embed = discord.Embed(description = '❌ **Ошибка! Вы не можете замутить себя**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if member.top_role >= ctx.author.top_role:
        Embed = discord.Embed(description = '❌ **Ошибка! Вы не можете замутить участника с более высокой ролью**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if not ctx.author.guild_permissions.manage_messages:
        Embed = discord.Embed(description = '❌ **Ошибка! У вас недостаточно прав**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return                              
    try:
        mutedRole=discord.utils.get(ctx.guild.roles, name="MutedBB")
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempmute= int(time[0]) * time_convert[time[-1]]
        await member.add_roles(mutedRole)
        await member.timeout(duration=tempmute, reason=reason)
        embed = discord.Embed(description= f"✅|{member.mention} был замьючен\nМодератор: {ctx.author.mention}\nВремя: {time}\nПричина: {reason}", color=discord.Color.green())
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("<:succesfully:925385120280612864>")
        await asyncio.sleep(tempmute)
        await member.remove_roles(mutedRole)
    except discord.Forbidden:
        return

    except discord.HTTPException:
        return
@bot.command()
async def unmute(ctx, member: discord.Member=None):
    if not member:
        Embed = discord.Embed(description = ':x: **Ошибка! Вы не указали пользователя**\n**Аргументы данной команды**\n**[] обязательный аргумент**\n\n**Gides!unmute [участник]**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if member == ctx.author:
        Embed = discord.Embed(description = ':x: **Ошибка! Вы не можете размутить себя**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if member.top_role >= ctx.author.top_role:
        Embed = discord.Embed(description = ':x: **Ошибка! Вы не можете размутить участника с более высокой ролью**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    if not ctx.author.guild_permissions.manage_messages:
        Embed = discord.Embed(description = ':x: **Ошибка! У вас недостаточно прав**', color=0x00008b)
        await ctx.send(embed = Embed)
        await ctx.message.add_reaction("<:error:925385765188419604>")
        return
    try:
        mutedRole = discord.utils.get(ctx.guild.roles, name="MutedBB")
        await member.remove_roles(mutedRole)
        embed = discord.Embed(description= f":white_check_mark:|{member.mention} был размучен\nМодератор: {ctx.author.mention}", color=discord.Color.green())
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("<:succesfully:925385120280612864>")
    except discord.Forbidden:
        return

    except discord.HTTPException:
        return
@bot.command()
async def invite(ctx):
    emb = discord.Embed(title = 'Инвайт бота', description='Инвайт бота: https://discord.com/api/oauth2/authorize?client_id=' + str(settings['id']) + '&permissions=8&scope=bot', color=discord.Color.orange())
    emb.add_field(name = 'Сервер', value = 'Ссылка на сервер бота! : https://discord.gg/bzk5MRDREB')
    await ctx.send(embed = emb)

@bot.command(pass_context=False)
async def ping(ctx):
  # Вывод задержки в чат с помощью команды .пинг
  await ctx.send('Пинг: {0}'.format(bot.latency)) 
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "help", description = "используйте !help <Команда>")
    em.add_field(name = "Модерация!", value = "Выберете из списка `Модерация`")
    em.add_field(name = "Веселое!", value = "Выберете из списка `Веселое`")
    em.add_field(name = "Экономика", value = "Выберете из списка `Экономика`")    



    await ctx.send(embed = em, view=Helpbl())
@help.command(name='mute')
async def mutehelp(ctx):
    await ctx.send(embed=discord.Embed(title='Команда мьюта', description='[] - Обязаталеные аргументы , () - не обязательные аргументы \n !mute [участник] [время] (причина)'))
@help.command(name='ban')
async def banan(ctx):
    await ctx.send(embed=discord.Embed(title='Команда бана', description='[] - Обязаталеные аргументы , () - не обязательные аргументы \n !ban [участник] [время] (причина)'))
@help.command(name='ban_id')
async def banidhelp(ctx):
    await ctx.send(embed=discord.Embed(title='Команда бана(по айди!)', description='[] - Обязаталеные аргументы , () - не обязательные аргументы \n !ban_id [айди участника] [время] (причина)'))
@help.command(name='animals')
async def animals(ctx):
    await ctx.send(embed=discord.Embed(title='Команды животных', description='[] - Обязаталеные аргументы , () - не обязательные аргументы \n !fox \n !cat \n !panda \n !dog'))
@help.command(name='avatars')
async def avatars(ctx):
    await ctx.send(embed=discord.Embed(title='Команды', description='`!blue_avatar` \n `!pink_avatar` \n `!multi_avatar` \n `!yellow_avatar` \n `!red_avatar` \n `!grey_avatar` \n `!green_avatar`'))


@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Разная лисичка') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
@bot.command()
async def blue_avatar(ctx):
    embed = discord.Embed(title="Синяя аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("blue.png", filename="blue.png")
    embed.set_image(url="attachment://blue.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def yellow_avatar(ctx):
    embed = discord.Embed(title="Желтая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("yellow.png", filename="yellow.png")
    embed.set_image(url="attachment://yellow.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def multi_avatar(ctx):
    embed = discord.Embed(title="Мульти аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("multi.gif", filename="multi.gif")
    embed.set_image(url="attachment://multi.gif")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def red_avatar(ctx):
    embed = discord.Embed(title="Красная аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("red.png", filename="red.png")
    embed.set_image(url="attachment://red.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def gray_avatar(ctx):
    embed = discord.Embed(title="Серая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("gray.png", filename="gray.png")
    embed.set_image(url="attachment://gray.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def green_avatar(ctx):
    embed = discord.Embed(title="Зеленая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("green.png", filename="green.png")
    embed.set_image(url="attachment://green.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def pink_avatar(ctx):
    embed = discord.Embed(title="Розовая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("pink.png", filename="pink.png")
    embed.set_image(url="attachment://pink.png")
    await ctx.send(file=file, embed=embed)
@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Разные собаки') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Разные коты') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
@bot.command()
async def panda(ctx):
    response = requests.get('https://some-random-api.ml/img/panda') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Разные пандочки') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def meme(ctx):
    response = requests.get('https://some-random-api.ml/meme') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Мемы!', description = json_data['caption']) # Создание Embed'a
    embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a

    await ctx.send(embed = embed) # Отправляем Embed
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def playnorelease(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )

        await ctx.send(f"Now playing: {query}")

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        if not url:
            await ctx.send('Need URL!')
            return
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @playnorelease.before_invoke
    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
bot.add_cog(Music(bot))
#bot.ipc.start()
while True:
    try:
        bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
    except:
        pass  
