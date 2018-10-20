from const import *
import discord
import asyncio

client = discord.Client()                              			# get client
functions = {}                                          		# define the functions dict

@client.event
async def on_ready():                                   		# some logging
	print('All set and ready!')
	print('Bot logged in as', client.user.name, 'with id', client.user.id)
	print('-----')

@client.event
async def on_message(message):
	await asyncio.sleep(0.2)                            		# make it feel natural
	await client.send_typing(message.channel)
	await asyncio.sleep(3)
	text = message.content.lower()                      		# parse message
	content = text.split()
	if content[0] in prefixes:
		print("Recieved message:", text)                		# more logging
		if content[1] in functions.keys():
			functions[content[1]].func(message, content[2:])	# call the function
		else:
			pass

class Command:
	def __init__(self, name, func, syntax=None, sdesc='Not provided.', desc='No description for the command provided.'):
		if name in functions.keys():							# check for repeating 
			raise KeyError()
		self.name = name
		self.func = func
		if syntax is None:
			self.syntax = prefixes[0] + ' ' + name
		else:
			self.syntax = syntax
		self.sdesc = sdesc
		self.desc = desc
		functions[name] = self

# Functions go here
async def help(message, *args):
	if args.count() == 0:
		print('Listing commands.')
		embed = discord.Embed(title='Помощь по боту', color=0x008800)
		embed.set_author('Minecraft Бот')
		embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9")
		for function in functions:
			embed.add_field(name='`' + function.syntax + '`', value=function.sdesc, inline=True)
		await client.send_message(message.channel, embed=embed)
	elif args.count() == 1 or args.count() == 2 and args[0] in prefixes:
		if args.count() == 2:
			args = [args[1]]
		print('Getting help for', args[1] + '.')
		if args[0] in functions.keys():
			function = args[0]
			embed = discord.Embed(title='Помощь по ' + args[0], color=0x008800)
			embed.set_author('Minecraft Бот')
			embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9")
			embed.add_field(name='`' + function.syntax + '`', value=function.desc, inline=True)
			await client.send_message(message.channel, embed=embed)
		else:
			print('Unknown command.')
			await client.send_message(message.channel, 'Я не знаю, что такое `' + prefixes[0] + ' ' + args[0] + '`!')
	else:
		print('Too many arguments!')
		await client.send_message(message.channel, 'Я твоя не понимать, ты говорить коротко!')

async def kill(message, *args):
	client.close()
# Functions end

# Commands go here
prefixes = ['!minecraft', '!mc']
Command("help", help, syntax='!minecraft help [команда]', sdesc='Этот список или помощь по команде.', desc='Показывает список всех команд или подробное описание указаной команды (как то, что вы сейчас читаете).')
Command("kill", kill, syntax='!minecraft kill', sdesc='Остановить бота.', desc='Останавливает бота. Доступно только @Owner.')
# Commands end

client.run(token)