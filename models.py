import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('cribbage.db')
        self.create_game_table()
        self.create_player_table()
    
    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_game_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Game" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        GameDate Date,
        Player1Id INTEGER FOREIGNKEY REFERENCES Player(_id),
        Player1Score INTEGER DEFAULT 0,
        Player2Id INTEGER FOREIGNKEY REFERENCES Player(_id),
        Player2Score INTEGER DEFAULT 0,
        WinnerId INTEGER FOREIGNKEY REFERENCES Player(_id),
        WinningScore INTEGER
        );
        """
        self.conn.execute(query)
    
    def create_player_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Player" (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name Text,
        WINS INTEGER DEFAULT 0,
        LOSSES INTEGER DEFAULT 0
        );
        """
        self.conn.execute(query)

class GameModel:
    TABLENAME = "Game"

    def __init__(self):
        self.conn = sqlite3.connect('cribbage.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()


    def create_game(self, params):
        query = f'insert into {self.TABLENAME} (GameDate, Player1Id, Player2Id, WinningScore) values ("{params.get("gameDate")}",{params.get("player1Id")},{params.get("player2Id")},{params.get("winningScore")});'
        print(query)
        result = self.conn.execute(query)
        print(result)
        return 'Successfully created game!'

    def get_game_by_id(self, id):
        query = f"SELECT * from {self.TABLENAME} where id = {id}"
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
            for i, column in enumerate(result_set[0].keys())}
            for row in result_set]
        return result
    
    def get_all_games(self):
        query = f"SELECT * from {self.TABLENAME}"
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
            for i, column in enumerate(result_set[0].keys())}
            for row in result_set]
        return result
    
    def update_Points(self, params):
        playerNumber = params.get("playerNumber") 
        gameId = params.get("gameId")   
        if playerNumber == 1:
            query = f"UPDATE {self.TABLENAME} " \
                f'SET Player1Score  = Player1Score + {params.get("scoredAmount")} ' \
                f'WHERE id = {gameId}'
        elif playerNumber == 2:
            query = f"UPDATE {self.TABLENAME} " \
                f'SET Player2Score  = Player2Score + {params.get("scoredAmount")} ' \
                f'WHERE id = {gameId}' 
        else:
            return "ERROR - Please only enter 1 or 2"
        self.conn.execute(query)
        
        isThereWinner = self.check_for_winner(gameId,playerNumber)

        if(isThereWinner == True):
            return "Player " + str(playerNumber) + " wins!"
        return self.get_game_by_id(params.get("gameId"))

    def check_for_winner(self, gameId, playerNumber):
        currentGame = self.get_game_by_id(gameId)
        winningScore = currentGame[0]['WinningScore']
        currentWinner = currentGame[0]['WinnerId']
        
        if(playerNumber == 1):
            playerScore = currentGame[0]['Player1Score']
        elif(playerNumber == 2):
            playerScore = currentGame[0]['Player2Score']
        
        if(playerScore >= winningScore and currentWinner is None):
            self.set_winner(gameId, currentGame[0][f'Player{playerNumber}Id'])
            return bool(True)
        else:
            return bool(False)

    def set_winner(self,gameId, playerId):
        query = f"UPDATE {self.TABLENAME} " \
            f"SET WinnerId  = {playerId}" \
            f" WHERE id = {gameId}"
        self.conn.execute(query)


class PlayerModel:
    TABLENAME = "Player"

    def __init__(self):
        self.conn = sqlite3.connect('cribbage.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()


    def get_player_by_id(self, id):
        query = f"SELECT * from {self.TABLENAME} where _id = {id}"
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
            for i, column in enumerate(result_set[0].keys())}
            for row in result_set]
        return result
    
    def create_player(self, playerName):
        query = f'insert into {self.TABLENAME} (Name) values ("{playerName}");'
        result = self.conn.execute(query)
        return "Successfully Created Player " + playerName

    def get_all_players(self):
        query = f"SELECT * from {self.TABLENAME}"
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
            for i, column in enumerate(result_set[0].keys())}
            for row in result_set]
        return result

    def increment_wins(self,params):
        playerId = params.get("playerId") 
        query = f"UPDATE {self.TABLENAME} " \
            f"SET WINS  = WINS + 1 " \
            f"WHERE _id = {playerId}"

        self.conn.execute(query)
        return self.get_player_by_id(playerId)        

    def increment_losses(self,params):
        playerId = params.get("playerId") 
        query = f"UPDATE {self.TABLENAME} " \
            f"SET LOSSES  = LOSSES + 1 " \
            f"WHERE _id = {playerId}"

        self.conn.execute(query)
        return self.get_player_by_id(playerId)        

