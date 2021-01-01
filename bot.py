# IMPORTS
import os
import discord
import psycopg2
from dotenv import load_dotenv
from discord.ext import commands

# VARIABLES
load_dotenv()
token = os.environ["BOT_TOKEN"]
cid = os.environ["CLIENT_ID"]
oa2 = os.environ["CLIENT_SECRET"]
status = 'TEST STATUS'

bot = commands.Bot(command_prefix='•')


# BASE EVENTS ----------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    """
    TODO: DOCUMENTATION
    """
    # PRINT BOT INFORMATION TO CONSOLE
    print(f'\n• python 3.8.3')
    print(f'\n• Discord.py(Version: {discord.__version__})')
    print(f'\n•• Bot connected as {bot.user.name}')
    print(f'\n•• Bot ID: {bot.user.id}')
    print('\n••• All events and commands loaded •••')
    print('\n••• All systems nominal....')
    bot.remove_command('help')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="LFG Radio"))


# ADMIN COMMANDS / EVENTS ----------------------------------------------------------------------------------------------
@bot.command()
@commands.is_owner()
async def test(message):
    """
    TODO: DOCUMENTATION
    """
    print('\nTest successful!')
    await message.channel.send('Testing 1 2 3!')


@bot.event  # IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
async def on_message(message):
    """
    TODO: DOCUMENTATION
    """
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    await bot.process_commands(message)


# ----------------------------------------------------------------------------------------------------------------------
@bot.command()
async def submit(ctx, *, arg):  # |!| COMPLETE MODULE WITH WORKING CODE
    """
   [D]
   """
    discord_id = ctx.message.author.id
    username = ctx.message.author
    link = arg

    sql = """INSERT INTO sys_monday(discord_id, username, link)
           VALUES(%s) RETURNING id;"""
    conn = None
    id = None

    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (discord_id, username, link))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print('\nSubmitting ** to sys_monday')
        await ctx.message.channel.send("Submission received!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("\nThere was an error submitting to sys_monday!")
        await ctx.message.channel.send("There was an error submitting to sys_monday!")
    finally:
        if conn is not None:
            conn.close()
# ----------------------------------------------------------------------------------------------------------------------

bot.run(os.environ["BOT_TOKEN"])
