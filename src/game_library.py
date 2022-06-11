import logging
import os
import zipfile

from typing import List, Set


class GameLibrary:
    def __init__(self, library_path: str):
        self.library_path = library_path
        self.library = self.load_library(library_path)

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
        
        top_ten = matching[:10]
        
        if len(matching) > 10:
            top_ten.append(f"And {str(len(matching) - 10)} more...")
        
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
    
    
        
        
        
        
        
        
        
        
        

        
        

        
        
        
    
    
    
    
    