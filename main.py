# -*- coding: utf-8 -*-


import disnake as discord
from disnake import channel
from disnake.ext import commands
#from discord.ext import ipc
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
#import youtube_dl
import json
import lvls
import motor.motor_asyncio

cluster = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:4tuf0leqvNuG020Vb7WK@containers-us-west-29.railway.app:5998')
economy = cluster['ecodb']['users']
database = cluster['Logs']
shop = cluster['Phones']['shop']
collection = database['channellog']
phonesdata = cluster['Phones']
phonecol = phonesdata['Users']
store = phonesdata['Apps']
from StringProgressBar import progressBar
#youtube_dl.utils.bug_reports_message = lambda: ""
from disnake.enums import ButtonStyle
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

#ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


#class YTDLSource(discord.PCMVolumeTransformer):
#    def __init__(self, source, *, data, volume=0.5):
#        super().__init__(source, volume)

#        self.data = data
#
#        self.title = data.get("title")
#        self.url = data.get("url")
#
#    @classmethod
#    async def from_url(cls, url, *, loop=None, stream=False):
#        loop = loop or asyncio.get_event_loop()
#        data = await loop.run_in_executor(
#            None, lambda: ytdl.extract_info(url, download=not stream)
#        )
#
#        if "entries" in data:
#            # Takes the first item from a playlist
#           data = data["entries"][0]
#
#        filename = data["url"] if stream else ytdl.prepare_filename(data)
#        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)#

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = settings['prefix'], intents=intents, pm_help=True, case_insensitive=True)#, intents = discord.Intents.default())
bot.remove_command('help')
client = bot
#@bot.command()
async def python(ctx, *, code):
    code = code
    try:
        if code == 'open("config.py").read()':
            await ctx.send('Херушки тебе а не токен!')
            
            return
        elif code == 'exit(1)' or code == 'exit()' or code == 'exit(2)':
            await ctx.send('Эййй не выключай бота!')
            return
        result = exec(code)
        
        await ctx.send(str(result))
    except Exception as error:
        await ctx.send(str(error))


@bot.command()
@commands.has_permissions(administrator=True)
async def setlogchannel(ctx, channel : discord.TextChannel):
    guildid = ctx.guild.id
    channelid = channel.id
    data = {'guild': guildid, 'channel': channelid}
    result = collection.insert_one(data).inserted_id
    await ctx.send(embed=discord.Embed(title='<:checkmark:946826044583858266>', description='Успешно!'))
    return
#@bot.event
#async def on_member_update(before, after):
    #a = after.guild.id
    #b = collection.find_one({'guild': a})
    #if not b:
        #await ctx.send('Ошибка не был указан канал для логов!')
        #return
    #channel = bot.get_channel(b['channel'])
    #print(before)
    #print(after)
    #bef = before.roles
    #aft = after.roles
    #print(aft)
    
    #await channel.send(embed=discord.Embed(title='Логи - обновление юзера',description=f'Самая высокая роль до \n <@&{before.top_role.id}> \n после: \n <@&{after.top_role.id}> \n '))
@client.event
async def on_guild_channel_create(channel):
    a = channel.guild.id
    b = collection.find_one({'guild': a})
    if not b:
        return
    channel = bot.get_channel(b['channel'])
    await channel.send(embed=discord.Embed(title='Новый канал', description='Название канала: ' + str(channel.name) + '\n Категория ' + str(channel.category) + '\n Айди: ' + str(channel.id) + '\n Когда создан ' + str(channel.created_at)))#выведет имя канала
    print('Channel category: ', channel.category)#выведет категорию где он находится
    print('Channel id: ', channel.id)#выведет айди канала
    print('Channel created at', channel.created_at)#выведет час и дату когда он был создан
@bot.event
async def on_message(message):
    author = message.author
    if not author.bot:
        await lvls.addxp(message, author)
        await bot.process_commands(message)
    if author == client.user:
        return
@bot.command()
async def addmoney(ctx, col:int):
    id = ctx.author.id
    if id == 858307410757681172:
        await economy.update_one({"member_id": id, "guild_id": ctx.guild.id}, {'$inc': {'balance': col}})
        await ctx.send('Успешно!')
    else:
        await ctx.send('Вы не владелец бота!')
        return
class ChoicePhoneList(discord.ui.Select):
    def __init__(self, owner_id, ctx):
        # Set the options that will be presented inside the dropdown
        self.owner_id=owner_id
        self.ctx = ctx
        self.owner = self.ctx.author
        options = [
            discord.SelectOption(
                label="MI - 5000", description="телефон ксаоми"#, emoji="🛠"
            ),
            discord.SelectOption(
                label="Samsung - 10000", description="сомсунг"#, emoji="😄"
            ),
            discord.SelectOption(
                label="Google Pixel - 14000", description="клутой телефон ат Гуль"#, emoji="💸"
            ),
            discord.SelectOption(
                label='DIGMA - 2400', description='дигмочка дешевое говно'#, emoji='🔴'
            ),
            discord.SelectOption(
                label='OPPO - 3400', description='Телефон оппо пойдет ксати у создателя такой!'
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
        a = await function_new_phone(self.values[0], self.owner_id, self.owner)
        await interaction.response.send_message(a, ephemeral=True)
        
class ChoicePhoneINIT(discord.ui.View):
    def __init__(self, owner_id, ctx):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        
        self.ctx = ctx
        self.add_item(ChoicePhoneList(owner_id, self.ctx))
    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        else:
            await interaction.response.send_message('Вы не можете использовать команду другого человека!', ephemeral=True)
            return False

async def function_new_phone(brand, id, owner):
    phone = await phonecol.find_one({'owner': id})
    if not phone:
        if brand == "MI":

            data = {'owner': id, 'os': 'MIUI', 'brand': 'Xiaomi', 'recovery':'Mi Recovery v3.0', 'root':'No installed', 'magisk':'No installed', 'basic':'No installed', 'loader':'No unlock', 'apps':[], 'amount':5000}
            balance = await economy.find_one({"member_id": id, "guild_id": owner.guild.id})

        
            await economy.update_one({"member_id": id, "guild_id": owner.guild.id}, {"$inc": {"balance": -data['amount']}})
            result = await phonecol.insert_one(data)
            print(result)
            return 'Готово! Вы теперь  имеете ' + data['brand'] + ' с ' + data['os']
        
        elif brand == 'Samsung':
            data = {'owner': id, 'os':'OneUI', 'brand':'Samsung', 'recovery':'стоковый', 'root':'No installed', 'magisk':'No installed', 'basic':'No installed', 'loader':'No unlock', 'apps':[], 'amount':10000}
            balance = await economy.find_one({"member_id": id, "guild_id": owner.guild.id})

        
            await economy.update_one({"member_id": id, "guild_id": owner.guild.id}, {"$inc": {"balance": -data['amount']}})
            result = await phonecol.insert_one(data)
            print(result)
            return 'Готово! Вы теперь  имеете ' + data['brand'] + ' с ' + data['os']
        elif brand == 'DIGMA':
            data = {'owner': id, 'os':'Android Go!', 'brand':'Digma', 'recovery':'стоковый', 'root':'No installed', 'magisk':'No installed', 'basic':'No installed', 'loader':'No unlock', 'apps':[], 'amount':2400}
            balance = await economy.find_one({"member_id": id, "guild_id": owner.guild.id})

        
            await economy.update_one({"member_id": id, "guild_id": owner.guild.id}, {"$inc": {"balance": -data['amount']}})
            result = await phonecol.insert_one(data)
            print(result)
            return 'Готово! Вы теперь  имеете ' + data['brand'] + ' с ' + data['os']
        elif brand == 'Google Pixel':
            data = {'owner': id, 'os':'AOSP', 'brand':'Google Pixel', 'recovery':'стоковый', 'root':'No installed', 'magisk':'No installed', 'basic':'No installed', 'loader':'No unlock', 'apps':[], 'amount':14000}
            balance = await economy.find_one({"member_id": id, "guild_id": owner.guild.id})

        
            await economy.update_one({"member_id": id, "guild_id": owner.guild.id}, {"$inc": {"balance": -data['amount']}})
            result = await phonecol.insert_one(data)
            print(result)
            return 'Готово! Вы теперь  имеете ' + data['brand'] + ' с ' + data['os']
        elif brand == 'OPPO':
            
            data = {'owner': id, 'os':'ColorOS', 'brand':'OPPO', 'recovery':'стоковый', 'root':'No installed', 'magisk':'No installed', 'basic':'No installed', 'loader':'No unlock', 'apps':[], 'amount':3400}
            
            balance = await economy.find_one({"member_id": id, "guild_id": owner.guild.id})
            if balance['balance'] < data['amount']:
                pass
            
            await economy.update_one({"member_id": id, "guild_id": owner.guild.id}, {"$inc": {"balance": -data['amount']}})


            result = await phonecol.insert_one(data)
            print(result)
            return 'Готово! Вы теперь  имеете ' + data['brand'] + ' с ' + data['os']
    elif phone:
        print(phone)
        return 'Ошибка вы не можете иметь больше 1 телефона'
    else:
        return 'ОШИБКА возникла ошибка пожалуйста обратитесь к серверу поддержки'
async def progress(msg):
    await msg.edit(content='.')
    await asyncio.sleep(5)
    await msg.edit(content='..')
    await asyncio.sleep(5)
    await msg.edit(content='...')
    await asyncio.sleep(5)
    await msg.edit(content='....')
    await asyncio.sleep(5)
    await msg.edit(content='.....')
    await asyncio.sleep(5)
    await msg.edit(content='......')
    await asyncio.sleep(5)
    await msg.edit(content='.......')
    await asyncio.sleep(5)
    await msg.edit(content='........')
    await asyncio.sleep(5)
    await msg.edit(content='.........')
    await asyncio.sleep(5)
    await msg.edit(content='..........')
    await asyncio.sleep(5)
    await msg.edit(content='...........')
    await asyncio.sleep(5)
    await msg.edit(content='............')
    await asyncio.sleep(5)
    await msg.edit(content='.............')
@bot.command()
async def appstore(ctx, dia=None, app=None, desc=None):
    if not dia:
        await ctx.send('Добро пожаловать в магазин приложений виберете пункт \n install \n apps \n search')
    if dia == 'apps':
        id = ctx.author.id
        phone = await phonecol.find_one({'owner': id})
        apps = phone['apps']
        await ctx.send('Ваши приложения:')
        await ctx.send('\n'.join(apps))

    elif dia == 'install':
        if not app:
            await ctx.send('Вы не указали приложение!')
            return
        else:
            id = ctx.author.id
            phone = await phonecol.find_one({'owner': id})
            apps = phone['apps']
            app = app
            appinfo = await store.find_one({'name':app})
            if not appinfo:
                await ctx.send('[ERROR 404] appstore.com выдает ошибку приложение не найдено с статусом 404')
                return

            apps.append(appinfo['name'])
            print(apps)
            phonecol.update_one({
            'owner': id
            },{
                '$set': {
                'apps': apps
            }
            }, upsert=False)
            await ctx.send('Вы установили приложение!')
    elif dia == 'search':
        if not app:
            await ctx.send('Вы не указали приложение!')
            return
        else:
            appinfo = await store.find_one({'name':app})
            if not appinfo:
                await ctx.send('[ERROR 404] appstore.com выдает ошибку приложение не найдено с статусом 404')
                return
            await ctx.send(f'Название:' + appinfo['name'] + '\nОписание: ' + appinfo['description'])
    elif dia == 'upload': 
        if not app:
            await ctx.send('Вы не указали название!')
            return
        if not desc:
            await ctx.send('отсуствует описание!')
            return
        else:
            await ctx.send('Добавляем...')
            data = {'name':app,'description':desc}
            result = await store.insert_one(data)
            await ctx.send(f'[Успешно <:checkmark:946826044583858266> !] Вы залили ' + data['app'])
    else:
        await ctx.send('Неизвестная команда!')
@bot.command()
async def myphone(ctx, diia=None, diiasdiia=None, diiia=None):
    id = ctx.message.author.id
    phone = await phonecol.find_one({'owner': id})
    if not phone:
        await ctx.send('У вас отсуствует телефон!')
        return
    phone_name = phone['brand']
    phone_os = phone['os']
    phone_root = phone['root']
    phone_magisk = phone['magisk']
    phone_basicmagisk = phone['basic']
    phone_unlock = phone['loader']
    phone_id = phone['_id']
    phone_recovery = phone['recovery']
    if not diia:
        await ctx.send(embed=discord.Embed(title=f'Ваш {phone_name}', description=f'ИНФОРМАЦИЯ \nAйди: {phone_id}\n Имеет прошивку {phone_os} \n И имеет рековери {phone_recovery}\n СОСТОЯНИЕ \nСостояние рута {phone_root} \nСостояние магиска {phone_magisk}\n Состояние загрузчика {phone_unlock}\nБазовый комплект модулей магиск {phone_basicmagisk}'))
    if diia == 'install':
        if not diiasdiia:
            await ctx.send('Вы не указали что установить!\nСписок: \n TWRP \n custom <CUSTOM NAME> \n Magisk \n Root \n BasicPackMagisk \n Unlock')
        if diiasdiia == 'custom':
            if not diiia:
                await ctx.send('Вы не указали какой кастом надо поставить! ксати вот список: \n MIUI \n OneUI \n AndroidGo \n AOSP \n ColorOS')
            
            elif phone_unlock == 'No unlock':
                await ctx.send('У вас не разблокирован загрузчик!')
                return
            
            elif diiia == 'MIUI':
                a = random.randint(0, 100)
                brick = a>=75
                msg = await ctx.send('Установка откинтесь на спинку пока установится кастом на ваш телефон! (~60 секунд)')
                msd = await ctx.send('d')
                await progress(msd)
                if brick == True:
                    ctx.send('Упс....  у вас не получилось прошить он стал кирпичем и вы его викинули!')
                    phonecol.delete_one({'_id':phone_id})
                    return
                else:
                    pass
                    
                await msd.edit(content='Подготовка к запуску ~5 секунд')
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'os': 'MIUI'
                }
                }, upsert=False)
                await msg.delete()
                await msd.edit(content='Завершено!')
            elif diiia == 'AndroidGo':
                a = random.randint(0, 100)
                brick = a>=75
                msg = await ctx.send('Установка откинтесь на спинку пока установится кастом на ваш телефон! (~60 секунд)')
                msd = await ctx.send('d')
                await progress(msd)
                if brick == True:
                    ctx.send('Упс....  у вас не получилось прошить он стал кирпичем и вы его викинули!')
                    phonecol.delete_one({'_id':phone_id})
                    return
                elif brick == False:
                    pass
                await msd.edit(content='Подготовка к запуску ~5 секунд')
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'os': 'Android Go!'
                }
                }, upsert=False)
                await msg.delete()
                await msd.edit(content='Завершено!')
            elif diiia == 'OneUI':
                a = random.randint(0, 100)
                brick = a>=75
                msg = await ctx.send('Установка откинтесь на спинку пока установится кастом на ваш телефон! (~60 секунд)')
                msd = await ctx.send('d')
                await progress(msd)
                if brick == True:
                    ctx.send('Упс....  у вас не получилось прошить он стал кирпичем и вы его викинули!')
                    phonecol.delete_one({'_id':phone_id})
                    return
                elif brick == False:
                    pass
                await msd.edit(content='Подготовка к запуску ~5 секунд')
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'os': 'OneUI'
                }
                }, upsert=False)
                await msg.delete()
                await msd.edit(content='Завершено!')
            elif diiia == 'ColorOS':
                a = random.randint(0, 100)
                brick = a>=75
                msg = await ctx.send('Установка откинтесь на спинку пока установится кастом на ваш телефон! (~60 секунд)')
                msd = await ctx.send('d')
                await progress(msd)
                if brick == True:
                    ctx.send('Упс....  у вас не получилось прошить он стал кирпичем и вы его викинули!')
                    phonecol.delete_one({'_id':phone_id})
                    return
                elif brick == False:
                    pass
                await msd.edit(content='Подготовка к запуску ~5 секунд')
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'os': 'ColorOS'
                }
                }, upsert=False)
                await msg.delete()
                await msd.edit(content='Завершено!')
            elif diiia == 'AOSP':
                a = random.randint(0, 100)
                brick = a>=75
                msg = await ctx.send('Установка откинтесь на спинку пока установится кастом на ваш телефон! (~60 секунд)')
                msd = await ctx.send('d')
                await progress(msd)
                if brick == True:
                    ctx.send('Упс....  у вас не получилось прошить он стал кирпичем и вы его викинули!')
                    phonecol.delete_one({'_id':phone_id})
                    return
                elif brick == False:
                    pass
                await msd.edit(content='Подготовка к запуску ~5 секунд')
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'os': 'AOSP'
                }
                }, upsert=False)
                await msg.delete()
                await msd.edit(content='Завершено!')
            else:
                await ctx.send('Кастом не найден!')
                return 


        if diiasdiia == 'Unlock':
            if phone_unlock == 'Unlocked':
                await ctx.send('403 Forbidden Bot : Вы уже имеете разблокированый загрузчик!')
                return
            else:
                msg = await ctx.send('Разблокировка....')
                await asyncio.sleep(1)
                await msg.edit(content='.')
                await asyncio.sleep(1)
                await msg.edit(content='..')
                await asyncio.sleep(1)
                await msg.edit(content='...')
                await asyncio.sleep(1)
                await msg.delete()
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'loader': 'Unlocked'
                }
                }, upsert=False)
                await ctx.send('Готово!')
        if diiasdiia == 'Magisk':
            if phone_magisk == 'Installed':
                await ctx.send('У вас уже установлен рут!')
                return
            else:
                msg = await ctx.send('Установка....')
                await asyncio.sleep(1)
                await msg.edit(content='.')
                await asyncio.sleep(1)
                await msg.edit(content='..')
                await asyncio.sleep(1)
                await msg.edit(content='...')
                await asyncio.sleep(1)
                await msg.delete()
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'magisk': 'Installed'
                }
                }, upsert=False)
                await ctx.send('Готово!')
        if diiasdiia == 'Root':
            if phone_root == 'Installed':
                await ctx.send('У вас уже установлен рут!')
                return
            else:
                msg = await ctx.send('Установка....')
                await asyncio.sleep(1)
                await msg.edit(content='.')
                await asyncio.sleep(1)
                await msg.edit(content='..')
                await asyncio.sleep(1)
                await msg.edit(content='...')
                await asyncio.sleep(1)
                await msg.delete()
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'root': 'Installed'
                }
                }, upsert=False)
                await ctx.send('Готово!')
        if diiasdiia == 'BasicPackMagisk':
            if phone_basicmagisk == 'Installed':
                await ctx.send('интересно зачем тебе это ты его уже поставил...')
                return
            elif phone_root == 'Not installed': 
                await ctx.send('Вы не установили рут!')
                return
            else:
                msg = await ctx.send('Установка.....')
                
                await asyncio.sleep(1)
                await msg.edit(content='.')
                await asyncio.sleep(1)
                await msg.edit(content='..')
                await asyncio.sleep(1)
                await msg.edit(content='...')
                    

                await msg.delete()
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'basic': 'Installed'
                }
                }, upsert=False)
                msg = await ctx.send('Готово!')
                await asyncio.sleep(5)
                await msg.delete()
        if diiasdiia == 'TWRP':
            if phone_unlock == 'No unlock':
                await ctx.reply('Вы не можете поставить ТВРП без открытого загрузчика!')
                return
            elif phone_unlock == 'Unlocked':
                if phone_recovery == 'TWRP':
                    await ctx.send('У вас уже установлен ТВРП')
                    return
                msg = await ctx.send('Установка.....')
                
                await asyncio.sleep(1)
                await msg.edit(content='.')
                await asyncio.sleep(1)
                await msg.edit(content='..')
                await asyncio.sleep(1)
                await msg.edit(content='...')
                    

                await msg.delete()
                phonecol.update_one({
                'owner': id
                },{
                    '$set': {
                    'recovery': 'TWRP'
                }
                }, upsert=False)
                msg = await ctx.send('Готово!')
                await asyncio.sleep(5)
                await msg.delete()
            else:
                await ctx.send('500 Bot is have error!')
@bot.command()
async def new_phone(ctx):
    owner = ctx.message.author
    owner_id = owner.id
    await ctx.send('Выберете телефон ниже!', view=ChoicePhoneINIT(owner_id, ctx))
@bot.slash_command(name='rank', description='Показывает ваш уровень')
async def rank(inter):
    
    author = inter.author
    authorid = author.id
    information = await lvls.open_user(authorid)
    level = str(information['lvls'])
    dolevel = information['dolevel']
    total = 1000
    bardata = progressBar.filledBar(total, dolevel, size=10)
    print(author)
    print(bardata[0])
    print(bardata[1])
    author = str(author)
    await inter.response.send_message(embed=discord.Embed(title='Ранги - уровни', description='Вы ' + author + ' имеете \n ' + level + ' уровень и вам осталось до следущего уровня(в прогресс баре!) \n' + bardata[0] + '\n в процентах это ' + str(bardata[1]) + '%'))
  
@bot.command()
async def rank(ctx, author=None):
    if author == None:
        author = ctx.message.author
        authorid = author.id
    information = await lvls.open_user(authorid)
    level = str(information['lvls'])
    dolevel = information['dolevel']
    total = 1000
    bardata = progressBar.filledBar(total, dolevel, size=10)
    print(author)
    print(bardata[0])
    print(bardata[1])
    author = str(author)
    await ctx.send(embed=discord.Embed(title='Ранги - уровни', description='Вы ' + author + ' имеете \n ' + level + ' уровень и вам осталось до следущего уровня(в прогресс баре!) \n' + bardata[0] + '\n в процентах это ' + str(bardata[1]) + '%'))
@bot.slash_command(name='clear', description='Очищяет текущий канал')
async def clear(inter, limit=20):
    """Delete the messages sent in current text-channel"""
    
    
    try:
        await inter.message.channel.purge(limit=limit)
        await inter.response.send_message('Очищено!')
    except discord.Forbidden:
        await inter.response.send_message("I don't have permission to `Manage Messages`:disappointed_relieved:")
@bot.command(name='clear', aliases=['cls'])
async def clear(ctx, limit=20):
    """Delete the messages sent in current text-channel"""
    
    
    try:
        await ctx.message.channel.purge(limit=limit)
    except discord.Forbidden:
        await ctx.send("I don't have permission to `Manage Messages`:disappointed_relieved:")
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
@client.slash_command(description='Игра простенькая!')
async def number(inter, num : int):
    a = random.randint(1, 200)
    if num == a:
        print('You Win!')
        await inter.response.send_message('You win!')
    else:
        print('You not win :(')
        await inter.response.send_message('You not win :(')
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
        await ctx.send("Неизвестный айди.")
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
#@bot.ipc.route()
#async def get_guild_count(data):
    #return len(bot.guilds) # returns the len of the guilds to the client

#@bot.ipc.route()
#async def get_guild_ids(data):
    #final = []
    #for guild in bot.guilds:
        #final.append(guild.id)
    #return final # returns the guild ids to the client

#@bot.ipc.route()
#async def get_guild(data):
    #guild = bot.get_guild(data.guild_id)
    #if guild is None: return None

    #guild_data = {
        #"name": guild.name,
        #"id": guild.id,
        #"prefix" : "?"
    #}

    #return guild_data


@bot.slash_command(description='Показывает аватарку пользователя')
async def avatar(inter, *,  avamember : discord.Member=None):
    author = inter.author
    userAvatarUrl = author.avatar
    if not avamember:
        embed = discord.Embed(description =  "Аватар " + author.mention, color = 0x00008b)
        embed.set_image(url = userAvatarUrl)
        embed.set_footer(text=f'{inter.author}', icon_url = userAvatarUrl)
        await inter.response.send_message(embed = embed)
    try:
        author = inter.author
        userAvatarUrl = avamember.avatar.url
        embed = discord.Embed(description =  "Аватар " + avamember.mention, color = 0x00008b)
        embed.set_image(url = userAvatarUrl)
        embed.set_footer(text=f'{avamember}', icon_url = userAvatarUrl)
        await inter.response.send_message(embed = embed)
    except discord.Forbidden:
        return
    except discord.HTTPException:
        return
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    author = ctx.author
    userAvatarUrl = author.avatar
    if not avamember:
        embed = discord.Embed(description =  "Аватар " + author.mention, color = 0x00008b)
        embed.set_image(url = userAvatarUrl)
        embed.set_footer(text=f'{ctx.author}', icon_url = userAvatarUrl)
        await ctx.send(embed = embed)
    try:
        author = ctx.message.author
        userAvatarUrl = avamember.avatar.url
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
#@bot.event
#async def on_command_error(ctx, error):
    #if isinstance(error, commands.CommandNotFound):

        #await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, команда не найдена!', colour = discord.Color.red()))
    #if isinstance(error, commands.errors.MissingPermissions):

        #await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, вы не имеете права на испольнение команды!', colour = discord.Color.red()))
        #return
    #if isinstance(error, commands.MissingRequiredArgument):
        #await ctx.send(embed = discord.Embed(description = f'{ctx.author.name} вы не указали аргумент какой-то'))
        #return
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
@client.slash_command(description='Показывает инфу об сервере')
async def server(inter):
    ctx = inter
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    if ctx.guild.banner:
        BannerURl = ctx.guild.banner.url
    else:
        BannerURl = None
    icon = ctx.guild.icon.url
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
    await ctx.response.send_message(embed=embed)
@bot.command()
async def ver(ctx):
    await ctx.reply(f"My ver " + settings['version'] + "!")
@bot.slash_command(description='Версия бота')
async def ver(inter):
    await inter.response.send_message(f"My ver " + settings['version'] + "!")
@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.
 #This should be at your other imports at the top of your code
@bot.event
async def on_guild_join(guild):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help | " + str(len(bot.guilds)) + " серверов"))
class HelpList(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label="Модерация", description="Команды модерации", emoji="🛠"
            ),
            discord.SelectOption(
                label="Веселое!/Разное!", description="Команды веселости!", emoji="😄"
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
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description="Команды модерации:\n`b!ban`\n`b!mute`\n`b!unban`\n`b!kick`\n`b!ping`\n`b!unmute`\n`b!ver`"), ephemeral=True)
        if self.values[0] == 'Веселое!/Разное!':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description='`b!hello`\n`b!avatar`\n`b!dog`\n`b!fox`\n`b!cat`\n`b!panda`\n`b!rank`\n'), ephemeral=True)
        #await interaction.response.send_message(f"Your favourite colour is {self.values[0]}")
        if self.values[0] == 'Экономика':
            await interaction.response.send_message(embed=discord.Embed(title='Команды', description='Ты экономист!) \n`b!bal`\n`b!work`\n`b!pay`\n`b!crime`'), ephemeral=True)
class Helpbl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(HelpList())
    @discord.ui.button(label="Мой инвайт!", style=ButtonStyle.blurple, row=1)
    async def myinvite(
        self, button: discord.ui.Button, interaction: discord.MessageInteraction
    ):
        await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=935590256093331526&permissions=8&scope=bot", ephemeral=True)

    @discord.ui.button(label = 'Сервер поддержки', emoji="🥳", style=ButtonStyle.green, row=2)
    async def supportserver(
        self, button: discord.ui.Button, interaction: discord.MessageInteraction
    ):
        await interaction.response.send_message("https://discord.gg/zy3qJM4mvE", ephemeral=True)
    @discord.ui.button(label = 'Донат', emoji="🥳", style=ButtonStyle.green, row=2)
    async def donate(
        self, button: discord.ui.Button, interaction: discord.MessageInteraction
    ):
        await interaction.response.send_message("Смотри ты получиш особенную роль на дискорд сервере \n и это поможет нам разрабатывать бота! \n Duino-coin: Mordsdima \n также чтобы получить роль донатера на нашем сервере напиши в личку создателя и кинь скрин что это действительно вы! \n Discord: TheDiman#2022", ephemeral=True)
#@bot.command()
#async def buttons(ctx):

    # Sends a message with a row of buttons.
    #await ctx.send("Here are some buttons!", view=Helpbl())

    # This is how the command would look like: https://i.imgur.com/ZYdX1Jw.png



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!help | " + str(len(bot.guilds)) + " серверов"))
    print("Bot is ready!")
    print(f'Im at {bot.user.name} and {bot.user.id}')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member, *, reason):
    print(type(member))
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Ban пользователя', value='Пользователь {} был забанен! по причине {reason}'.format(member.mention))
    await ctx.reply(embed = emb)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason):
    
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Kick пользователя', value='Пользователь {} был забанен! /n по причине {reason}'.format(member.mention))
    await ctx.reply(embed = emb)
@bot.command()
async def ban_id(ctx, user_id=None, time1: str=None, reason=None):
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

ALL_ACTIVITIES = [act.name for act in discord.PartyType]
@bot.command(pass_context=True,name='activity')
async def activity(ctx, game=None):
    
    if not game:
        await ctx.send(embed=discord.Embed(title='[ERROR 400 BAD REQUEST] вы не указали игру!\n' + '\n'.join(ALL_ACTIVITIES)))
        return
    
    
    if not ctx.author.voice:
        return await ctx.send("you're not in voice channel")
    channel = ctx.author.voice.channel
    #wait = await ctx.send(embed=discord.Embed(title='Генерация...'))
    link = await channel.create_invite(reason='Activity created',target_type=discord.InviteTarget.embedded_application,target_application=getattr(discord.PartyType, game))
    print(link)
    await ctx.send(f'[click here to start the activity]({link})')
@bot.slash_command()
async def create_invite(self, inter: discord.ApplicationCommandInteraction,
                        custom_activity: commands.option_enum(ALL_ACTIVITIES)):
    """
    Select custom activity
    """

    if not inter.user.voice:
        return await inter.response.send_message("you're not in voice channel")
    voice_channel = inter.user.voice.channel
    link = await voice_channel.create_invite(reason='Activity created',
                                                 target_type=discord.InviteTarget.embedded_application,
                                                 target_application=getattr(discord.PartyType, custom_activity))
    await inter.response.send_message(f"[click here to start the activity]({link})")
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








@bot.command()
async def mute(ctx, member: discord.Member=None, time:str=None, reason=None):
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
@bot.slash_command(description='раз мьют')
async def unmute(ctx, member: discord.Member=None):
    ctx.send = ctx.response.send_message
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
    emb = discord.Embed(title = 'Инвайт бота', description='Инвайт бота: https://discord.com/api/oauth2/authorize?client_id=935590256093331526&permissions=8&scope=bot', color=discord.Color.orange())
    emb.add_field(name = 'Сервер', value = 'Ссылка на сервер бота! : https://discord.gg/bzk5MRDREB')
    await ctx.send(embed = emb)
@bot.slash_command(description='инвайт на сервер и инвайт бота ничего особеного')
async def invite(ctx):
    emb = discord.Embed(title = 'Инвайт бота', description='Инвайт бота: https://discord.com/api/oauth2/authorize?client_id=935590256093331526&permissions=8&scope=bot', color=discord.Color.orange())
    emb.add_field(name = 'Сервер', value = 'Ссылка на сервер бота! : https://discord.gg/bzk5MRDREB')
    await ctx.response.send_message(embed = emb)
@bot.command(pass_context=False)
async def ping(ctx):
  # Вывод задержки в чат с помощью команды .пинг
  await ctx.send('Пинг: {0}'.format(bot.latency)) 
@bot.slash_command(pass_context=False)
async def ping(ctx):
  # Вывод задержки в чат с помощью команды .пинг
  await ctx.response.send_message('Понг! \nПинг: {0}'.format(bot.latency)) 
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "help", description = "используйте !help <Команда>")
    em.add_field(name = "Модерация!", value = "Выберете из списка `Модерация`")
    em.add_field(name = "Веселое!", value = "Выберете из списка `Веселое`")
    em.add_field(name = "Экономика", value = "Выберете из списка `Экономика`")    



    await ctx.send(embed = em, view=Helpbl())
@bot.slash_command(description='Хелп хелп обычный', name='help')
async def help_slash(ctx):
    ctx.send = ctx.response.send_message
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
@bot.slash_command(description='Команда из серии рандом апи')
async def fox(ctx):
    ctx.send = ctx.response.send_message
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
@bot.slash_command(description='Самая стандарт синяя ава!')
async def blue_avatar(ctx):
    embed = discord.Embed(title="Синяя аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("blue.png", filename="blue.png")
    embed.set_image(url="attachment://blue.png")
    await ctx.response.send_message(file=file, embed=embed)
@bot.command()
async def yellow_avatar(ctx):
    embed = discord.Embed(title="Желтая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("yellow.png", filename="yellow.png")
    embed.set_image(url="attachment://yellow.png")
    await ctx.send(file=file, embed=embed)
@bot.slash_command(description='охх желтая ава')
async def yellow_avatar(ctx):
    embed = discord.Embed(title="Желтая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("yellow.png", filename="yellow.png")
    embed.set_image(url="attachment://yellow.png")
    await ctx.response.send_message(file=file, embed=embed)
@bot.command()
async def multi_avatar(ctx):
    embed = discord.Embed(title="Мульти аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("multi.gif", filename="multi.gif")
    embed.set_image(url="attachment://multi.gif")
    await ctx.send(file=file, embed=embed)
@bot.slash_command(description='мульти ава')
async def multi_avatar(ctx):
    embed = discord.Embed(title="Мульти аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("multi.gif", filename="multi.gif")
    embed.set_image(url="attachment://multi.gif")
    await ctx.response.send_message(file=file, embed=embed)
@bot.command()
async def red_avatar(ctx):
    embed = discord.Embed(title="Красная аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("red.png", filename="red.png")
    embed.set_image(url="attachment://red.png")
    await ctx.send(file=file, embed=embed)
@bot.slash_command(description='серия авы дс только красная')
async def red_avatar(ctx):
    embed = discord.Embed(title="Красная аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("red.png", filename="red.png")
    embed.set_image(url="attachment://red.png")
    await ctx.response.send_message(file=file, embed=embed)
@bot.command()
async def gray_avatar(ctx):
    embed = discord.Embed(title="Серая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("gray.png", filename="gray.png")
    embed.set_image(url="attachment://gray.png")
    await ctx.send(file=file, embed=embed)
@bot.slash_command(description='Серая ава дс')
async def gray_avatar(ctx):
    embed = discord.Embed(title="Серая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("gray.png", filename="gray.png")
    embed.set_image(url="attachment://gray.png")
    await ctx.response.send_message(file=file, embed=embed)
@bot.command()
async def green_avatar(ctx):
    embed = discord.Embed(title="Зеленая аватарка", description="нету :(", color=0x00ff00) #creates embed
    file = discord.File("green.png", filename="green.png")
    embed.set_image(url="attachment://green.png")
    await ctx.send(file=file, embed=embed)
@bot.slash_command(description='зеленая ава')
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
@bot.slash_command(description='розовая стандартная аватарка!')
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
@bot.slash_command()
async def dog(ctx):
    ctx.send = ctx.response.send_message
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
@bot.slash_command(description='Рандомный кот....')
async def cat(ctx):
    ctx.send = ctx.response.send_message
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
@bot.slash_command(description='Рандомная панда')
async def panda(ctx):
    ctx.send = ctx.response.send_message
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
@bot.slash_command(description='Показывает мемчики (спасибо some-random-api)')
async def meme(ctx):
    response = requests.get('https://some-random-api.ml/meme') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Мемы!', description = json_data['caption']) # Создание Embed'a
    embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a

    await ctx.response.send_message(embed = embed) # Отправляем Embed
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
    @commands.slash_command(description='Играет музыку')
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        if not url:
            await ctx.response.send_message('Нужна сыллка!')
            return
        async with ctx.response.defer():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.response.send_message(f"Now playing: {player.title}")
    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}")
    @commands.slash_command(description='Играет музон из стрима')
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.response.defer():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.response.send_message(f"Now playing: {player.title}")
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
    @commands.slash_command(description='Изменение уровня музыки')
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
    @commands.slash_command(description='Остановка музона ')
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
for filename in os.listdir("./cogs/"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
        
