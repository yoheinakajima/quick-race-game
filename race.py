# race.py
import os
import discord
import csv
import random


# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

from dotenv import load_dotenv

filename = "speed.csv"
fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rows[:5]:
    # parsing each column of a row
    for col in row:
        print("%10s"%col),
    print('\n')

def maximum(a, b):
    if a >= b:
        return a
    else:
        return b

def fullname(id):
    if id > 1000:
        return "#"+str(id)
    if id > 100:
        return "#0"+str(id)
    if id > 10:
        return "#00"+str(id)
    if id > -1:
        return "#000"+str(id)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix="$")


@bot.command(name="race")
async def race_function(ctx, *args):

    x=0
    for arg in args:
        if x == 0:
            player1 = int(arg)
            speed1 = rows[player1-1][1]
        if x == 1:
            player2 = int(arg)
            speed2 = rows[player2-1][1]
        x+=1

    await ctx.channel.send("player 1: "+fullname(player1)+" speed: "+str(speed1)+", player 2: "+fullname(player2)+" speed: "+str(speed2))
    await ctx.channel.send("Each player will roll an X-sided dice (where X is their speed), until the first person reaches 100. May the best beastie win!")

    max = 0
    distance1 = 0
    distance2 = 0
    while max < 100:
	    move1 = random.randint(0, int(speed1))
	    move2 = random.randint(0, int(speed2))
	    distance1 = distance1 + move1
	    distance2 = distance2 + move2
	    await ctx.channel.send(fullname(player1)+" moves "+str(move1)+" to "+str(distance1)+". "+fullname(player2)+" moves "+str(move2)+" to "+str(distance2))
	    max = maximum(distance1, distance2)
	    if max > 99:
	        if (distance1 > distance2):
	            await ctx.channel.send(fullname(player1)+" wins!")
	        if (distance1 < distance2):
	            await ctx.channel.send(fullname(player2)+" wins!")

bot.run(TOKEN)

