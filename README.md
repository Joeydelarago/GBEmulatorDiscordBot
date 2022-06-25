# Discord Gameboy Emulator
A Discord bot allows you to play Gameboy games through chat.

![Peek 2022-06-25 14-54](https://user-images.githubusercontent.com/23387864/175774350-38de5ff7-c68b-42cc-a14b-6234c445c422.gif)


## Description
Play your favorite Gameboy games through discord chat, using reactions or
text inputs to press the buttons. The games are displayed through short gifs.

## Getting Started
Before starting you will need to add your own gb roms to the roms folder. These can either be zipped or raw .gb files.

You will also need to add your DISCORD_TOKEN to a .env file at src/.env

For more details on how to run a discord bot, [refer to the documentation](https://discordpy.readthedocs.io/en/stable/).

## Usage
Some useful commands are

### \>start_game

This command with start up the last played game. "\>load" can be used to start a different game

### \>save_state

This will save your game state. Adding a number afterwards will save to that save slot for the current game.
There is no limit to how many save slots can be used.

### \>load_state

This will load a save file. Adding a number afterwards will load that save slot for the current game.

### \>toggle_facade

This will toggle the Gameboy facade around the emulator.

### \>load

"\>load" has a search feature that allows to query your game libary and select options using reactions.

![image](https://user-images.githubusercontent.com/23387864/175774653-b848bb07-3926-468b-9205-e97f3962553d.png)



## Installing Required Libraries

```
pip install -r requirements.txt
```
## Running the bot
```
python3 gba_bot.py
```
