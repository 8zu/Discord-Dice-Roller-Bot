# A dice rolling bot for use on Discord servers
# LICENSE: This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# @category   Tools
# @copyright  Copyright (c) 2016 Robert Thayer (http://www.gamergadgets.net)
# @version    1.1
# @link       http://www.gamergadgets.net
# @author     Robert Thayer

from typing import List
from random import randint
from itertools import chain
import discord # Imported from https://github.com/Rapptz/discord.py
import asyncio
from discord.ext import commands

# A dice bot for use with Discord
bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="A bot to handle all your RPG rolling needs")

# Determines if a message is owned by the bot
def is_me(m):
    return m.author == bot.user

# Determines if the value can be converted to an integer
# Parameters: s - input string
# Returns: boolean. True if can be converted, False if it throws an error.
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Roll a list of random variables to their values
def evaluate_randvars(randvars: List[str]): # -> List[int]
    def roll_single(randvar):
        if 'd' in randvar:
            num, dice_type = randvar.split('d')
            try:
                if num == '': num = 1
                if dice_type == '': dice_type = 20
                num, dice_type = int(num), int(dice_type)
            except:
                raise ValueError(f"{randvar} is not a valid dice syntax")
            return [randint(1, dice_type) for _ in range(num)]
        else:
            try:
                return [int(randvar)]
            except:
                raise ValueError(f"{randvar} is not a valid integer")

    return list(chain(*[roll_single(cmd) for cmd in randvars]))

# Roll die and get a random number between a and b (inclusive) adding/subtracting the modifier
# Parameters: a [low number], b [high number], modifier [amount to add/subtract to total]
# threshold [number that result needs to match or exceed to count as a success]
# Returns: str
def test_threshold(cmd: str, threshold: int):
    n = sum(evaluate_randvars(cmd.split('+')))
    if n >= threshold:
        return f"***Success***: {cmd} = {n} meets or beats the threshold {threshold}."
    else:
        return f"***Failure***: {cmd} = {n} < {threshold}"

# Rolls a set of die and returns either number of hits or the total amount
# Parameters: num_of_dice [Number of dice to roll], dice_type[die type (e.g. d8, d6), 
# hit [number that must be exceeded to count as a success], modifier [amount to add to/subtract from total],
# threshold [number of successes needed to be a win]
# Returns: String with results
def test_hit(cmd: str, hit_thresh: int, success_thresh=None):
    symbols = cmd.split("+")
    dices = evaluate_randvars(filter(lambda s: "d" in s, symbols))
    modifier = sum(evaluate_randvars(filter(lambda s: "d" not in s, symbols)))

    numbers = [d + modifier for d in dices]

    total = sum(1 for n in numbers if n >= hit_thresh)
    result = " + ".join(f"**{n}**" if n >= hit_thresh else str(n)
                        for n in numbers)
    result += f" = {total}"

    if success_thresh is not None:
        if total >= threshold:
            result += " meets or beats the {success_thresh} threshold. ***Success***"
        else:
            result += " does not meet the {success_thresh} threshold. ***Failure***"
    return result

@bot.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Parse !roll verbiage
@bot.command(pass_context=True,description='Rolls dice.\nExamples:\n100  Rolls 1-100.\n50-100  Rolls 50-100.\n3d6  Rolls 3 d6 dice and returns total.\nModifiers:\n! Hit success. 3d6!5 Counts number of rolls that are greater than 5.\nmod: Modifier. 3d6mod3 or 3d6mod-3. Adds 3 to the result.\n> Threshold. 100>30 returns success if roll is greater than or equal to 30.\n\nFormatting:\nMust be done in order.\nSingle die roll: 1-100mod2>30\nMultiple: 5d6!4mod-2>2')
@asyncio.coroutine
def roll(ctx, cmd : str = ""):
    numbers, hit, threshold = [], None, None
    # author: Writer of discord message
    author = ctx.message.author.split('#')[0]

    try:
        if cmd == "":
            raise ValueError("Please enter some dice")

        if '>' in cmd:
            cmd, threshold = cmd.split('>')
            try:
                threshold = int(threshold)
            except:
                raise ValueError("Threshold value format error. Must be integer")
        elif '!' in cmd:
            cmd, hit = cmd.split('!')
            try:
                hit = int(hit)
            except:
                raise ValueError("Hit value format error. Must be integer")

        if hit is not None:
            yield from bot.say(f"{author} rolled {cmd} = " + test_hit(cmd, hit, threshold))
        elif threshold is not None:
            yield from bot.say(f"{author} rolled {cmd}: " + test_threshold(cmd, threshold))
        else:
            numbers = rolldice(cmd.split('+'))
            results = " + ".join(map(str, numbers))
            yield from bot.say(f"{author} rolls {cmd} = {results} = {sum(numbers)}")
    except ValueError as err:
        # Display error message to channel
        yield from bot.say(err)

#Bot command to delete all messages the bot has made.        
@bot.command(pass_context=True,description='Deletes all messages the bot has made')
@asyncio.coroutine
def purge(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=100, check=is_me)
    yield from bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

# Follow this helpful guide on creating a bot and adding it to your server. 
# https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
bot.run('token')
