import random

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 10
        self.leave_rate = random.randint(1,25)
        self.last_move = ""
        self.history = []

    def record_round_info(self, player1, player2, player1_action, player2_action, player_count, reward):
        
        self.history.append({
            'state': {
                'player_count': player_count,
                'player1': player1, 
                'player2': player2,
                'player1_action': player1_action,
                'player2_action': player2_action,
            },
            'reward': reward
        })

    def move(self, other_player):
        return self.choose_move(other_player)

    def choose_move(self, other_player):
        return Match.MOVES[random.randint(0,5)]

    def choose_opponent(self, player_list, banned_names):
        # Ensures the player chooses a valid opponent, not himself or a previously chosen player
        valid_opponents = [player for player in player_list if player.name not in banned_names]
        return player_list.index(valid_opponents[random.randint(0, len(valid_opponents) - 1)])

    def check_leave(self):
        return random.randint(1,100) < self.leave_rate
            
    def __str__(self):
        return f"Player {self.name} with {self.chips} chips."

class HumanPlayer(Player):
    def choose_move(self, others):
        print(f"Your turn, {self.name}. You have {self.chips} chips.")
        while True:
            move = input("Choose your move (Rock, Paper, Scissors, Cooperate, Betray, Block): ")
            if move in Match.MOVES:
                return move
            else:
                print("Invalid move. Please choose again.")

    def check_leave(self):
        return random.randint(1,1000) < self.leave_rate

class Match:
    MOVES = ["Rock", "Paper", "Scissors", "Cooperate", "Betray", "Block"]
    MOVE_RESULTS = {
        ("Rock", "Rock"): lambda self, player1, player2: self.tie(player1, player2),
        ("Rock", "Paper"): lambda self, player1, player2: self.lose(player1, player2),
        ("Rock", "Scissors"): lambda self, player1, player2: self.win(player1, player2),
        ("Rock", "Cooperate"): lambda self, player1, player2: self.win(player1, player2),
        ("Rock", "Betray"): lambda self, player1, player2: self.lose(player1, player2),
        ("Rock", "Block"): lambda self, player1, player2: self.tie(player1, player2),

        ("Paper", "Rock"): lambda self, player1, player2: self.win(player1, player2),
        ("Paper", "Paper"): lambda self, player1, player2: self.tie(player1, player2),
        ("Paper", "Scissors"): lambda self, player1, player2: self.lose(player1, player2),
        ("Paper", "Cooperate"): lambda self, player1, player2: self.win(player1, player2),
        ("Paper", "Betray"): lambda self, player1, player2: self.lose(player1, player2),
        ("Paper", "Block"): lambda self, player1, player2: self.tie(player1, player2),

        ("Scissors", "Rock"): lambda self, player1, player2: self.lose(player1, player2),
        ("Scissors", "Paper"): lambda self, player1, player2: self.win(player1, player2),
        ("Scissors", "Scissors"): lambda self, player1, player2: self.tie(player1, player2),
        ("Scissors", "Cooperate"): lambda self, player1, player2: self.win(player1, player2),
        ("Scissors", "Betray"): lambda self, player1, player2: self.lose(player1, player2),
        ("Scissors", "Block"): lambda self, player1, player2: self.tie(player1, player2),

        ("Cooperate", "Rock"): lambda self, player1, player2: self.lose(player1, player2),
        ("Cooperate", "Paper"): lambda self, player1, player2: self.lose(player1, player2),
        ("Cooperate", "Scissors"): lambda self, player1, player2: self.lose(player1, player2),
        ("Cooperate", "Cooperate"): lambda self, player1, player2: self.share(player1, player2),
        ("Cooperate", "Betray"): lambda self, player1, player2: self.betrayed(player1, player2),
        ("Cooperate", "Block"): lambda self, player1, player2: self.win(player1, player2),

        ("Betray", "Rock"): lambda self, player1, player2: self.win(player1, player2),
        ("Betray", "Paper"): lambda self, player1, player2: self.win(player1, player2),
        ("Betray", "Scissors"): lambda self, player1, player2: self.win(player1, player2),
        ("Betray", "Cooperate"): lambda self, player1, player2: self.betray(player1, player2),
        ("Betray", "Betray"): lambda self, player1, player2: self.double_betray(player1, player2),
        ("Betray", "Block"): lambda self, player1, player2: self.lose(player1, player2),

        ("Block", "Rock"): lambda self, player1, player2: self.tie(player1, player2),
        ("Block", "Paper"): lambda self, player1, player2: self.tie(player1, player2),
        ("Block", "Scissors"): lambda self, player1, player2: self.tie(player1, player2),
        ("Block", "Cooperate"): lambda self, player1, player2: self.lose(player1, player2),
        ("Block", "Betray"): lambda self, player1, player2: self.win(player1, player2),
        ("Block", "Block"): lambda self, player1, player2: self.tie(player1, player2),
    }

    def __init__(self, player1, player2, pot, player_list):
        self.PLAYER_LIST = player_list
        self.players = [player1, player2]
        self.pot = pot
        self.round = 0
        self.last_move = [None, None]
        self.player_to_id = {player.name: i for i, player in enumerate(self.PLAYER_LIST)}

    def record_round_info(self, player1, player2, player1_action, player2_action):
        for player in self.PLAYER_LIST:
            player.record_round_info(self.player_to_id[player1], self.player_to_id[player2], player1_action, player2_action, len(self.PLAYER_LIST), self.reward_function(player))

    def reward_function(self, player):
        player_count = len(self.PLAYER_LIST)
        reward = (player.chips + self.pot/player_count) * player_count
        return reward

    def play_round(self):
        self.round += 1
        p1_move = self.players[0].move(self.players[1])
        p2_move = self.players[1].move(self.players[0])
        self.record_round_info(
            self.players[0].name,
            self.players[1].name,
            p1_move,
            p2_move
        )
        output_override = None
        print()
        print(f"Round {self.round}! Rock, Paper, Scissors, Cooperate, Betray, Block, SHOOT!")
        print(f"{self.players[0].name} chooses {p1_move}.")
        print(f"{self.players[1].name} chooses {p2_move}.")
        
        if p1_move == "Block" and self.last_move[0] == "Block" and p2_move == "Betray":
            print(f"{self.players[0].name} tried blocking twice in a row!")
            output_override = self.betray(*self.players[::-1])
        if p2_move == "Block" and self.last_move[1] == "Block" and p1_move == "Betray":
            print(f"{self.players[1].name} tried blocking twice in a row!")
            output_override = self.betray(*self.players)
        if p1_move == "Betray" and self.last_move[0] == "Betray" and self.last_move[1] == "Block":
            print(f"{self.players[0].name} tried to betray after being blocked!")
            output_override = self.win(*self.players[::-1])
        if p2_move == "Betray" and self.last_move[1] == "Betray" and self.last_move[0] == "Block":
            print(f"{self.players[1].name} tried to betray after being blocked!")
            output_override = self.win(*self.players)

        self.last_move = [p1_move, p2_move]
        if output_override != None: return output_override
        return self.MOVE_RESULTS[(p1_move, p2_move)](self, self.players[0], self.players[1])

    def play_game(self):
        result = ""
        while self.players[0].chips > 0 and self.players[1].chips > 0 and not (result == "tie" and self.round > 1):
            result = self.play_round()
            print(self)

    def __str__(self):
        return f"Pot: {self.pot} chips.\n{self.players[0]}\n{self.players[1]}"

    def lose(self, player1, player2): self.win(player2, player1)
    def win(self, player1, player2):
        player1.chips += 1
        player2.chips -= 1
        print(f"{player1.name} wins this round taking 1 chip!")
        return "win"

    def betrayed(self, player1, player2): self.betray(player2, player1)
    def betray(self, player1, player2):
        player1.chips += 3
        player2.chips -= 3
        print(f"{player1.name} betrays {player2.name} and takes three chips!")
        return "betray"

    def tie(self, player1, player2):
        print(f"It's a tie!")
        return "tie"

    def share(self, player1, player2):
        player1.chips += 3
        player2.chips += 3
        self.pot -= 6
        print(f"{player1.name} and {player2.name} share six chips from the pot!(3 each)")
        return "share"

    def double_betray(self, player1, player2):
        self.pot += 10
        player1.chips -= 4
        player2.chips -= 4
        print(f"{player1.name} and {player2.name} both betray! Each put 5 chips in the pot!")
        return "double_betray"

class GameGroup:
    def __init__(self, players, initial_pot):
        self.past_players = []
        self.players = players
        self.current_match = None
        self.pot = initial_pot
        self.match_count = 0
        self.player_to_id = {player.name: i for i, player in enumerate(players)}
    
    def start_new_match(self, player1, player2):
        self.current_match = Match(player1, player2, self.pot, self.players)

    def play_all_matches(self):
        # Select the first player
        player_index = random.randint(0, len(self.players)-1)
        challenger = self.players[player_index]
        banned_names = [challenger.name]

        while len(self.players) > 2 and self.pot > 0:
            # Select opponent
            opponent_index = challenger.choose_opponent(self.players, banned_names)
            opponent = self.players[opponent_index]
            self.match_count += 1
            print()
            print(f"\nNew match, Match {self.match_count}: {challenger.name} challenges {opponent.name}!")
            #input()
            self.start_new_match(challenger, opponent)
            self.current_match.play_game()

            # Update the pot after the match
            self.pot = self.current_match.pot

            # If a player has no chips left, they leave the game
            if challenger.chips <= 0 or challenger.check_leave():
                if challenger.chips <= 0:
                    print(f"\n{challenger.name} has no more chips and leaves the game.")
                    self.pot += challenger.chips
                    challenger.chips = 0
                    self.past_players.append(
                        self.players.pop(player_index)
                    )
                else:
                    self.past_players.append(
                        self.players.pop(player_index)
                    )
                    print(f"\n{challenger.name} leaves with what they have.")
                challenger = opponent
            elif opponent.chips <= 0 or opponent.check_leave():
                if opponent.chips <= 0:
                    print(f"\n{opponent.name} has no more chips and leaves the game.")
                    self.pot += opponent.chips
                    opponent.chips = 0
                    self.past_players.append(
                        self.players.pop(opponent_index)
                    )
                else:
                    print(f"\n{opponent.name} leaves with what they have.")
                    self.past_players.append(
                        self.players.pop(opponent_index)
                    )
            if not challenger in self.players:
                challenger = opponent.choose_opponent(self.players, [opponent.name])
            player_index = self.players.index(challenger)
            if opponent in self.players:
                opponent_index = self.players.index(opponent)
            
            # Select next player
            banned_names = []
            if opponent in self.players:
                player_index = self.players.index(opponent)
                banned_names.append(self.players[self.players.index(challenger)].name)
            challenger = self.players[player_index]
            banned_names.append(challenger.name)

        print(f"\nEnd of game, {self.players[0].name} and {self.players[1].name} win and split the last {self.pot} chips!")

        #Distribute the last of the prize pot
        if self.pot != 0:
            for player in self.players:
                player.chips += int(self.pot/len(self.players))
            self.pot = 0
        
        for idx in range(len(self.players)):
            self.past_players.append(
                self.players.pop(0)
            )
        self.past_players = sorted(self.past_players, key=lambda player: player.chips, reverse=True)
        
        for player in self.past_players: print(player)
        input()
    
if __name__ == "__main__":
    group = GameGroup([
        Player("Opponent 1"),
        Player("Opponent 2"),
        Player("Opponent 3"),
        Player("Opponent 4"),
        #HumanPlayer("You"),
    ], initial_pot = 100)

    group.play_all_matches()
