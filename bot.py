import discord
from discord.ext import commands
from discord import app_commands
import csv

with open("info.txt") as f:
    values = f.read().splitlines()

TOKEN = values[0]
GUILD = int(values[1])
CHANNEL_ID = int(values[2])
OUTPUT_CHANNEL_ID = int(values[3])
CSV_FILE = values[4]
BOT_ID = int(values[5])
MY_ID = int(values[6])

## Initializing Bot
intents = discord.Intents.default()
intents.message_content = True
SERVER = discord.Object(id=GUILD)

client = commands.Bot(command_prefix="?", intents=intents)


## For when bot connects to server
@client.event
async def on_ready():
    print('Hello {0.user}!'.format(client))

    
## When message is sent in chat
@client.event
async def on_message(message):

    if (message.channel.id == CHANNEL_ID and message.author.id != BOT_ID): # Will only run if on the "verification" channel
        user = message.author

        message_content = message.content

    
        with open(CSV_FILE) as csv_file:
            registered = False
            csv_reader = csv.reader(csv_file)

            rowindex = 0
            for row in csv_reader:
                if row[3] == message_content:
                    level = row[5]
                        
                    if level == "":
                        foundations = True
                        academic_essentials = False
                        engg_camp = False

                    elif level == "Level 2: Academic Essentials Only Group":
                        foundations = True
                        academic_essentials = True
                        engg_camp = False

                    elif level == "Level 3: ENGG Camp Group":
                        foundations = True
                        academic_essentials = True
                        engg_camp = True

                    registered = True
                    break

                rowindex += 1

            if registered:
                # Gives the proper correct role(s)
                if foundations:
                    Role = discord.utils.get(user.guild.roles, name="Foundations")
                    if user.id != client.user.id:
                        await user.add_roles(Role) # Gives user the right role
                if academic_essentials:
                    Role = discord.utils.get(user.guild.roles, name="Academic Essentials")
                    if user.id != client.user.id:
                        await user.add_roles(Role) # Gives user the right role
                if engg_camp:
                    Role = discord.utils.get(user.guild.roles, name="ENGG Camp")
                    if user.id != client.user.id:
                        await user.add_roles(Role) # Gives user the right role

                output_message = "Welcome to B2E 2024 "
                output_channel = client.get_channel(OUTPUT_CHANNEL_ID)
                await output_channel.send(output_message + f"{user.mention}! Your account has now been verified \U0001F973")

            elif not registered: # If CCID not found in CSV file
                output_message = "Verification may take up to 24 hours to complete. Please check that you have entered your CCID correctly or that you're registered in our 'Bridge2Engg 2024' eClass page. If both are correct, please try again in 24 hours."
                output_channel = client.get_channel(OUTPUT_CHANNEL_ID)
                await output_channel.send(f"{user.mention} " + output_message)
    
        
client.run(TOKEN)