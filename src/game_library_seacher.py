import os

from typing import List


class GameLibrarySearcher:
    def __init__(self, library_path: str):
        self.library_path = library_path
        self.library = os.listdir(self.library_path)

    def search_text(self, query: str) -> List[str]:
        if query in self.library:
            # We found an exact match return it
            return [query]
        
        matching = [match for match in self.library if query.lower() in match.lower()]
        
        top_ten = matching[:10]
        
        if len(matching) > 10:
            top_ten.append("And " + str(len(matching) - 10) + " more...")
        
        return top_ten
    
    
        
        
        
        
        
        
        
        
        

        
        

        
        
        
    
    
    
    
    