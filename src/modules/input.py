class Input(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.buttons = {
            "up": "up",
            "down": "down",
            "right": "right",
            "left": "left",
            "a": "a",
            "b": "b",
            "start": "start",
            "select": "select"
        }
    
        self.button_map_words = {
            **self.buttons,
            "A": self.buttons["a"],
            "B": self.buttons["b"],
            "🅰": self.buttons["a"],
            "🅱": self.buttons["b"],
            "Start": self.buttons["start"],
            "Select": self.buttons["select"],
            "⏸": self.buttons["start"],
            "🈂": self.buttons["select"],
            "Up": self.buttons["up"],
            "Down": self.buttons["down"],
            "Right": self.buttons["right"],
            "Left": self.buttons["left"],
            "u": self.buttons["up"],
            "d": self.buttons["down"],
            "r": self.buttons["right"],
            "l": self.buttons["left"],
            "U": self.buttons["up"],
            "D": self.buttons["down"],
            "R": self.buttons["right"],
            "L": self.buttons["left"],
            "⬆": self.buttons["up"],
            "⬇": self.buttons["down"],
            "⬅": self.buttons["right"],
            "➡": self.buttons["left"]
        }


def setup(client: commands.Bot):
    client.add_cog(Input(client))