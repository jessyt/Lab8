from models import GameModel
from models import PlayerModel

class GameApp:
    def __init__(self):
        self.game = GameModel()
        self.player = PlayerModel()

    def create_game(self, params):
        return self.game.create_game(params)
    
    def get_game_by_id(self, item_id):
        return self.game.get_game_by_id(item_id)
    
    def get_games(self):
        return self.game.get_all_games()

    def update_Points(self, params):
        return self.game.update_Points(params)

    def increment_wins(self, params):
        return self.player.increment_wins(params)
    
    def increment_losses(self, params):
        return self.player.increment_losses(params)
    
    def create_player(self, playerName):
        return self.player.create_player(playerName)
    
    def get_players(self):
        return self.player.get_all_players()
