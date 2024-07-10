import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread
import os

# Initialize Flask app
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='ticket')
async def ticket(ctx, action):
    if action == 'give':
        message = await ctx.send('React with 🇩 or 🇪 to get your ticket!')
        await message.add_reaction('🇩')
        await message.add_reaction('🇪')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['🇩', '🇪']

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '🇩':
                coach_type = 'B'
                coach_number = random.randint(1, 11)
            else:
                coach_type = 'E'
                coach_number = random.randint(1, 9)

            seat_number = random.randint(1, 64)
            await ctx.send(f'Your ticket: Coach {coach_type}{coach_number}, Seat {seat_number}')
        except discord.errors.TimeoutError:
            await ctx.send('You did not react in time!')

# Keep the bot alive
keep_alive()

# Run the bot
bot.run(os.getenv('MTI2MDU5OTUyOTk2Mzc4NjM0MA.Gok6Ew.MakXTT0GCVOshH_rNE6IGKpn7Q6kDpY8KGE-M8'))

