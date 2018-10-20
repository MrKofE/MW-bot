import discord
import asyncio
import aiohttp
import requests
import os
from bs4 import BeautifulSoup, element
from urllib.parse import unquote as decode, quote as code
from datetime import datetime
from json import JSONDecodeError
from mcrcon import MCRcon, socket

from const import *

client = discord.Client()
mcr = MCRcon('trolling.ddns.net', 'MosFes224271')


@client.event
async def on_ready():
    global faq, chat
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    try:
        with open('faq.txt') as f:
            text = f.read()
        faq = eval(text)
    except SyntaxError:
        faq = {}  
    try:
        with open('chat.txt') as f:
            text = f.read()
        chat = eval(text)
    except SyntaxError:
        chat = {}  
    print('------')        
    
@client.event
async def on_message(message):  
    global m, faq#, u
    #u = await client.get_user_info('Google Translator#1934')    
    m = message
    print(message.server, '/',  message.channel, '/', message.author, 'написал', message.content)
    owners = []
    for i in message.server.members:
        for j in i.roles:
            if j.name == 'Owner':
                owners.append(i)
    
    if message.content.startswith('<@!' + client.user.id + '>:'):
        client.logs_from(message.channel, limit=1)
        pass

    if message.content.lower().startswith('!mc') or message.content.lower().startswith('!minecraft'):
        cmd = ' '.join(message.content.split()[1:])
        if cmd.lower().startswith('bots'):
            server = message.server.id
            global chat
            if message.author in owners:
                if len(cmd.lower().split()) == 2:
                    if not server in faq:
                        chat[server] = cmd.lower().split()[2]
            with open('chat.txt', 'w') as file:
                file.write(str(chat))          
        
        if cmd.lower().startswith('hello'):
            await client.send_message(message.channel, '!mc hello')  
            
        if cmd.lower().startswith('test'):
            await client.send_typing(message.channel)
            try:
                mcr.connect()
            except ConnectionRefusedError:
                for i in owners:
                    await client.send_message(i, 'Сервер упал! Сделай что-нибудь! Игрок ' + str(message.author) + ' только что пропинговал сервер и ничего не работает!')
                await client.send_message(message.channel, 'Сервер не работает. Отправлено сообщение владельцу сервера.')
            else:
                await client.send_message(message.channel, 'Сервер работает!')
                mcr.command('tellraw @a ["[",{"text":"Minecraft bot","color":"dark_purple"},"] '+message.author.display_name+' проверил сервер. Вот идиот!"]')
                mcr.disconnect()
            
        if cmd.lower().startswith('count'):
            counter = 0
            async for message in client.logs_from(message.channel, limit=9999999999999999999999999):
                if message.author == client.user:
                    counter += 1     
            await client.send_message(message.channel, counter)
        
        if cmd.lower().startswith('cmd'):
            for i in message.author.roles:
                if 'Админ' in i.name:
                    mcr.connect()
                    await client.send_message(message.channel, mcr.command(' '.join(cmd.split()[1:])))
                    mcr.disconnect()
                    break
            else:
            #await client.send_message(message.channel, 'Да что ты мне сделаешь, жалкий человечишка?')
                await client.send_message(message.channel, 'Обойдешься')
            
        if cmd.lower().startswith('search'):
            q = ' '.join(cmd.split()[1:])
            if '#' in q:
                q = q.split('#')
                q = [i.capitalize() for i in q]
                q = '#'.join([q[0]] + [code(i).replace('%', '.') for i in q[1:]])
            else:
                q = q.capitalize()
            for i in answer(q):
                if i[0]:      
                    await client.send_message(message.channel, '***' + i[1] + '*** (__*' + decode(i[2]).replace(' ', '_') + '*__)\n' + i[3] + '\n')
                else:
                    await client.send_message(message.channel, i[1].replace(' ', '_')) 
            print('sent')
        
        if cmd.lower().startswith('info'):
            await client.send_message(message.channel, embed=profile(' '.join(cmd.split()[1:])))
        
        if cmd.lower().startswith('time'):
            await client.send_message(message.channel, time())
        
        if cmd.lower().startswith('uuid'):
            await client.send_message(message.channel, get_nick(cmd.split()[1]))
        
        if cmd.lower().startswith('emoji'):
            for i in message.server.members:
                print(i.name)
                try:
                    await client.send_message(message.channel, i.avatar_url)
                except:
                    pass
            print('em')
        
        if cmd.lower().startswith('help'):
            embed=discord.Embed(title='Помощь по боту', color=0x008800, description='Вместо `!minecraft` можно использовать `!mc`')
            embed.set_author(name="Поиск по Minecraft Wiki") 
            embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9")
            embed.add_field(name='`!minecraft help`', value='Увидеть этот список', inline=True)
            embed.add_field(name='`!minecraft search <запрос>`', value='Искать по Minecraft Wiki', inline=True)
            embed.add_field(name='`!minecraft plugin <плагин> [сообщение]`', value='Попросить поставить плагин', inline=True)
            embed.add_field(name='`!minecraft info <ник игрока>`', value='Профиль игрока', inline=True)
            embed.add_field(name='`!minecraft time`', value='Узнать время', inline=True)
            embed.add_field(name='`!minecraft kill`', value='Остановить бота', inline=True)
            embed.add_field(name='`!minecraft faq`', value='FAQ сервера', inline=True)
            embed.add_field(name='`!minecraft world <название> [описание]`', value='Попросить создать мир', inline=True)
            embed.add_field(name='`!minecraft ip`', value='IP сервера', inline=True)
            embed.add_field(name='`!minecraft op [причина]`', value='Попросить `@op` и `/op`', inline=True)
            #embed.add_field(name='`!minecraft down [сообщение]`', value='Отправить сообщение о падении сервера', inline=True)
            embed.add_field(name='`!minecraft count`', value='Посчитать кол-во сообщений от бота в этом канале', inline=True)
            embed.add_field(name='`!minecraft test`', value='Проверить работу сервера. В будущем `!minecraft down` перестанет существовать. Бугага.', inline=True)
            embed.set_footer(text='Помоги создателю!\nWMR: R725794253675\nQiwi:+79166758407')
            await client.send_message(message.channel, embed=embed)
        
        if cmd.lower().startswith('ip'):
            await client.send_message(message.channel, '`trolling.ddns.net`')
        
        if cmd.lower().startswith('world'):
            for i in owners:
                prin
                await client.send_message(i, str(message.author) + ' хочет мир' + cmd.split()[2] + '.' + (cmd[3:] + '.' if cmd.split()[3] else ''))
        
        if cmd.lower().startswith('op'):
            for i in owners:
                if len(cmd.split()) == 1:
                    await client.send_message(i, str(message.author) + ' хочет оператора')
                else:
                    await client.send_message(i, str(message.author) + ' хочет оператора. Он сказал: ' + cmd[3:])
        
        #if cmd.lower().startswith('down'):
        #    for i in owners:
        #        if len(cmd.split()) == 1:
        #            await client.send_message(i, 'Сервер упал! Сделай что-нибудь!')
        #        else:
        #            await client.send_message(i, 'Сервер упал! Сделай что-нибудь! ' + str(message.author) + ' говорит: "' + cmd[5:] + '"')
        
        if cmd.lower().startswith('faq'):
            server = message.server.id
            if message.author in owners:
                if len(cmd.lower().split()) == 3 and cmd.lower().split()[1] == 'set':
                    if not server in faq:
                        faq[server] = cmd.lower().split()[2]
            with open('faq.txt', 'w') as file:
                file.write(str(faq))            
            if server in faq:
                embed=discord.Embed(title="FAQ", description="Вас не послали, вы просто задали частый вопрос", color=0x008800)
                async for i in client.logs_from(client.get_channel(faq[server]), reverse=True):
                    j = decodeFAQ(i.content)
                    print(j)
                    embed.add_field(name=j[0], value=j[1], inline=False)
                await client.send_message(message.channel, embed=embed)
            else:
                await client.send_message(message.channel, 'Сначала используйте `!mc faq set <ID канала с FAQ>`')
            
        if cmd.lower().startswith('plugin'):
            pl = '-'.join(cmd.split()[1])
            async with aiohttp.get('https://dev.bukkit.org/projects/'+ pl +'/files/latest') as r:
                print(plugin)
                if r.status == 200:
                    for i in owners:
                        await client.send_message(i, ' '.join(cmd.split()[2:]) + message.author + ' попросил поставить плагин https://dev.bukkit.org/projects/'+ pl +'/files/latest')
                        
        if cmd.lower().startswith('kill'):
            for i in message.author.roles:
                if i.name == 'Host':
                    await client.send_message(message.channel, 'Приятно было помочь!')
                    exit()
            await client.send_message(message.channel, 'Да что ты мне сделаешь, жалкий человечишка?')

def answer(query):
    r = requests.get('https://minecraft-ru.gamepedia.com/index.php?search=' + query)
    soup = BeautifulSoup(r.text, 'html5lib')
    if 'Результаты поиска' in soup.text:
        yield (True, 'Результаты поиска по запросу `' + query + '`', 'https://minecraft-ru.gamepedia.com/index.php?search=' + query + ' _:_', '')
        for i in soup.find('ul', {'class':'mw-search-results'}).children:
            divs = [j for j in i.children if type(j) != element.NavigableString][:-1]
            s = [j.text for j in divs]
            a = i.find('a')
            title = a.text
            url = 'https://minecraft-ru.gamepedia.com' + a.attrs['href']
            for j in set(divs[1].findAll('span', {'class':'searchmatch'})):
                s[1] = s[1].replace(j.text, '**' + j.text + '**')
            yield (True, title, url, s[1])
    else:
        yield (False, 'https://minecraft-ru.gamepedia.com/' + query)

def decodeFAQ(text):
    text = text.split('О: ')
    text[0] = text[0][3:]
    return text

def saveFAQ():
    f = faq.copy()
    f
    print(f is faq)
    for i in f:
        for j in range(len(f[i]['messages'])):
            f[i]['messages'][j] = f[i]['messages'][j].code
    with open('faq.txt', 'w') as file:
        file.write(str(f))

def names(uuid):
    a = requests.get('https://api.mojang.com/user/profiles/%s/names'%uuid).json()
    for i in a[1:]:
        #print(i)
        i['changedToAt'] = datetime.strftime(datetime.utcfromtimestamp(i['changedToAt']//1000), "%Y.%m.%d %H:%M:%S")
    return a
    
def time():
    return datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

def get_uuid(nick):
    return requests.get('https://api.mojang.com/users/profiles/minecraft/' + nick).json()['id']

def get_nick(uuid):
    try:
        return requests.get('https://sessionserver.mojang.com/session/minecraft/profile/' + uuid).json()['name']
    except JSONDecodeError:
        return 'Игрок не существует'    

def profile(nick):
    try:
        uuid = get_uuid(nick)
        nick = get_nick(uuid)
        #if type(uuid) == str:
        embed = discord.Embed(title="Скин", colour=0x008800, url="https://crafatar.com/skins/" + uuid, description="Профиль игрока `"+nick+"`")
    
        embed.set_image(url="https://crafatar.com/renders/body/"+uuid+"?overlay=.png")
        embed.set_thumbnail(url="https://crafatar.com/renders/body/"+uuid + '.png')
        embed.set_author(name=nick, icon_url="https://crafatar.com/avatars/"+uuid+"?overlay=.png")
        embed.set_footer(text="Thank you to https://crafatar.com for providing avatars.\nПомоги создателю!\nWMR: R725794253675\nQiwi:+79166758407", icon_url="https://pbs.twimg.com/profile_images/548311612919009281/EFh9Pwgc_400x400.png")
    
        embed.add_field(name="UUID", value=uuid, inline=True)
    
        for i in names(uuid)[:0:-1]:
            t = i['changedToAt'].split()
            t[0] = '.'.join(t[0].split('.')[::-1])
            embed.add_field(name="`"+i['name']+"`", value=' '.join(t), inline=True)
        embed.add_field(name="`"+names(uuid)[0]['name']+"`", value="Изначальный ник", inline=True)
    except JSONDecodeError:
        uuid = get_uuid('MHF_Alex')
        embed = discord.Embed(title="404", colour=0x008800, description="Игрок `"+nick+"` не существует")
    embed.set_image(url="https://crafatar.com/renders/body/"+uuid+"?overlay=.png")
    embed.set_thumbnail(url="https://crafatar.com/renders/body/"+uuid + '.png')
    embed.set_author(name=nick, icon_url="https://crafatar.com/avatars/"+uuid+"?overlay=.png")
    embed.set_footer(text="Thank you to https://crafatar.com for providing avatars.\nПомоги создателю!\nWMR: R725794253675\nQiwi:+79166758407", icon_url="https://pbs.twimg.com/profile_images/548311612919009281/EFh9Pwgc_400x400.png")   
    return embed    

def format_text(text):
    pass

#async def translate(text, channel):
#    await client.send_message(channel'?en !ru ' + text)

faq = {}
chat = {}
u = ''
client.run(token)