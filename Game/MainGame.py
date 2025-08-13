from ConnectionManager import ConnetionManager


class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:None


game = MainGame()
game.connection = ConnetionManager()