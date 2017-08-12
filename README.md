# Discord-Dice-Roller-Bot
A bot that handles most RPG dice rolls

# Dependencies
This bot is extended from [Discord.py](https://github.com/Rapptz/discord.py/). Install Discord.py prior to running this bot.

#Python Version
This requires Python 3.6+.

# Usage
1. Follow the directions [here] (https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a bot token.
2. Add the bot to the servers you want.
3. Place the token in the last line of the script.
4. Launch script.

# Commands
`!purge`
Deletes all messages made from the bot. Used to clean up after a session.

`!roll`
Supported rolls are
- !roll d - Rolls a d20
- !roll d8 - Rolls one 8-sided die
- !roll 3d6 - Rolls 3 6-sided die

#Modifiers
- `!n` Hit mode (n>0). `!roll 10d6!5` will give you the number of times the dice rolls 5 or higher.
- `>n` Threshold mode (n>0). `!roll d100>50` will say "Success" if result is over 50 or "Failure" if not.
- `+/-` Modifier. Used with any roll. Adds or substracts to roll. !roll d100+4 will add 4 to the roll. Currently to substract you need to 
	- When used in combination of the `!` Hit mode, the modifier is distributively added to every dice. 
	- When used in normal mode or `>` Threshold mode, the modifier is added to the sum only.

You can string these together:
- `!roll 3d6+4d8+3>40` would roll a 3 d6 and 4 d8, add 3, then let you know if the sum is over 40.
- `!roll 10d6+2!4` would roll 10 d6, add 2 to every die, count number of dice rolled that are ≧4.
