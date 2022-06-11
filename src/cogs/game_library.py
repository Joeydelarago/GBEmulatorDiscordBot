import asyncio
import logging
import os
import zipfile

from typing import List, Set

from discord.ext import commands

from src.message_interaction import read_emoji_options

class GameLibraryManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.library_path = os.getcwd() + "/roms"
        self.library = self.load_library(self.library_path)
        self.search_results = []
        # self.search_options= ["⬅", "⬆", "⬇", "➡", "🅰", "🅱", "⏸", "️🈂"]
        self.search_options = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

    def load_library(self, path: str) -> Set[str]:
        """ Load names of all the roms stored in rom path. This includes zipped roms """
        files = os.listdir(self.library_path)
        #  Remove the file extensions
        rom_names = [file.split(".")[0] for file in files]
        return set(rom_names)

    def extract_zipped_game(self, path: str):
        """ Extracts zipped roms in rom path """
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self.library_path)

    def search_text(self, query: str) -> List[str]:
        """ Searches for game matching query and returns up to 10 rom names (Not file names) """
        matching = [match for match in self.library if query.lower() in match.lower()]
        
        top_ten = matching[:9]
        
        if len(matching) > 9:
            top_ten.append(f"And {str(len(matching) - 9)} more...")
        
        return top_ten

    def get_game_path(self, rom_name):
        """ Get the path of the gb file for the rom with rom_name """
        game_path = f"{self.library_path}/{rom_name}.gb"
        game_zipped_path = f"{self.library_path}/{rom_name}.zip"

        if os.path.exists(game_path):
            #  We have the game so return it
            return game_path
        elif os.path.exists(game_zipped_path):
            #  We have the game, but it is zipped so unzip it first
            self.extract_zipped_game(game_zipped_path)
            return game_path
        else:
            #  We can't find the requested game
            logging.warning(f"Could not fine game: {rom_name} in path: {game_path}")

    @commands.Command
    async def load(self, ctx, query: str):
        search_results = self.search_text(query)
        if len(search_results) == 1:
            rom_name = search_results[0]
            rom_path = self.get_game_path(rom_name)

            emulator = self.client.get_cog("Emulator")
            emulator.close_game()
            emulator.initialize_game(rom_name, rom_path)
        else:
            reaction = await self.choose_from_list(ctx, search_results)

            if reaction:
                rom_name = search_results[self.search_options.index(reaction) - 1]
                rom_path = self.get_game_path(rom_name)

                emulator = self.client.get_cog("Emulator")
                emulator.close_game()
                emulator.initialize_game(rom_name, rom_path)

    async def choose_from_list(self, ctx, search_results: List[str]) -> str:
        self.search_results = search_results
        numbered_results = [f"{str(number + 1)}: {game}" for number, game in enumerate(search_results)]
        one_word_per_line = '\n'.join(numbered_results)
        quote_text = f'These games matched your query:\n>>> {one_word_per_line}'
        rom_options = await ctx.send(quote_text)

        return await read_emoji_options(self.client, rom_options, self.search_options)


def setup(client: commands.Bot):
    client.add_cog(GameLibraryManager(client))
