from copy import deepcopy
import random
import numpy as np
from game import Game, Move, Player

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        '''Do just a random acceptable move'''
        self._board = game.get_board()
        self._player = game.get_current_player()

        return random.choice(self.get_possible_moves(self._board, self._player))


    def get_possible_moves(self, board: list[list[int]], player: int) -> list[tuple[tuple[int, int], Move]]:
        possible_moves = []
        # len of ndarray returns the shape of the first dimension
        for row in range(len(board)):
            for col in range(len(board[row])):
                # If the piece belongs to the current player or is neutral
                if board[row][col] == player or board[row][col] == -1:
                    if row == 0:
                        if col == 0:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row == len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row != 0 and row != len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
        return possible_moves





class MinMaxPlayer(Player):
    def __init__(self, depth: int) -> None:
        super().__init__()
        self._depth = depth
        self.__maxdepthreached = 0
        self.agent = "MinMax Agent"
        self._minmax_bestmove = None
        self._minmax_bestmove_histroy = []
        self._minmax_memory = {}

    def __str__(self) -> str:
        return f"{self.agent} with depth {self._depth}"

# check for occasional loops
    def check_loops(self):
        LENGTH = 10
        if len(self._minmax_bestmove_histroy) > LENGTH:
            #we have returned the same position "length" times
            return all(self._minmax_bestmove_histroy[-1] == item for item in self._minmax_bestmove_histroy[-LENGTH:])
        return False


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:  
        self._minmax_bestmove = None
        self._game = game
        board = game.get_board()
        player = game.get_current_player()
        self._maximizer_player = player
        self._minimizer_player = 1 - player
        self.minmax(board, player,deepcopy(self._depth))
        
        if self.check_loops():
            print("-----------------------loop detected-------------------------")
            print("selecting a random move")
            # return a random move
            possible_moves = self.get_possible_moves(board, player)
            print(possible_moves)
            print(len(possible_moves))
            print(board)
            #possible_moves.remove(self._minmax_bestmove_histroy[-1])
            self._minmax_bestmove = random.choice(possible_moves)
            self._minmax_bestmove_histroy = []
            # self._depth += 1
            # print(f"depth increased to {self._depth}")


        
        self._minmax_bestmove_histroy.append(self._minmax_bestmove)
        #print(f" here is the returned move history {self._minmax_bestmove_histroy}")
        return ((self._minmax_bestmove[0][1],self._minmax_bestmove[0][0]), self._minmax_bestmove[1])
    

    def minmax(self, board: list[list[int]], player: int, depth: int) -> int:

        possible_moves = self.get_possible_moves(board, player)

        # terminal node check
        if depth == 0 or self.check_winner(board,player) != -1 or len(possible_moves) == 0:
            return self.get_score(board, player)

        # here mini player
        if player == self._minimizer_player:
            value = float('inf')
            for move in possible_moves:
                # avoid extra calls to minmax if the value is already in memory
                if (tuple(board.flatten()),move,player) in self._minmax_memory.keys():
                    score = self._minmax_memory[(tuple(board.flatten()),move,player)]
                else:
                    new_board = self.make_move_board(deepcopy(board), deepcopy(move), player)
                    score = self.minmax(deepcopy(new_board), deepcopy(1-player), deepcopy(depth - 1)) 

                    self._minmax_memory[(deepcopy(tuple(board.flatten())),deepcopy(move),deepcopy(player))] = deepcopy(score)

                # take minimum score of childs
                if score < value:
                    value = score
            return value

        # here max player
        if player == self._maximizer_player:
            value = float('-inf')
            for move in possible_moves:
                if (tuple(board.flatten()),move,player) in self._minmax_memory.keys():
                    score = self._minmax_memory[(tuple(board.flatten()),move,player)]
                else:
                    new_board = self.make_move_board(deepcopy(board), deepcopy(move), player)
                    score = self.minmax(deepcopy(new_board), deepcopy(1-player),deepcopy(depth - 1))

                    self._minmax_memory[(deepcopy(tuple(board.flatten())),deepcopy(move),deepcopy(player))] = deepcopy(score)

                # take the maximum score of childs
                if score > value:
                    value = score
                    self._minmax_bestmove = deepcopy(move)
            return value

         

    # Get the possible moves from the board
    # TESTED
    def get_possible_moves(self, board: list[list[int]], player: int) -> list[tuple[tuple[int, int], Move]]:
        possible_moves = []
        # len of ndarray returns the shape of the first dimension
        for row in range(len(board)):
            for col in range(len(board[row])):
                # If the piece belongs to the current player or is neutral
                if board[row][col] == player or board[row][col] == -1:
                    if row == 0:
                        if col == 0:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row == len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row != 0 and row != len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
        return possible_moves
    
    
    

    def get_score(self, board: list[list[int]], player: int) -> int:
        '''The value of each tree node: items considered are:
        - the winner: +10
        - the center region of the board: +1 for each piece
        - Four consecutive pieces in a row or column: +2 for each'''

        score = 0
        if player != 1 and player != 0:
            raise ValueError("player must be 0 or 1")
        

        winner = self.check_winner(board,player)
        if winner == self._maximizer_player:
            score += 10
        elif winner == self._minimizer_player:
            score -= 10


        #the player having the center of the board has a higher chance of winning
        center_positions = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
        center_score = 0
        for pos in center_positions:
            if board[pos] == player:
                center_score += 1
        score += center_score

        # consecutive_score = 0
        # # if the player has 4 consecutive pieces in a row
        # for x in range(board.shape[0]):
        #     if (board[x, 0] == player and all(board[x, 0:4] == board[x, 0])) or (board[x, 1] == player and all(board[x, 1:] == board[x, 1])):
        #         consecutive_score += 1
        # # if the player has 4 consecutive pieces in a column
        # for y in range(board.shape[1]):
        #     if (board[0, y] == player and all(board[0:4, y] == board[0, y])) or (board[1, y] == player and all(board[1:, y] == board[1, y])):
        #         consecutive_score += 1

        # score += consecutive_score * 2

        # Try monte carlo rollouts to compute the static evaluation of the state
        # winner = self.check_winner(board,player)
        # if winner == self._maximizer_player:
        #     score += 100
        # elif winner == self._minimizer_player:
        #     score -= 100
        # else:
        #     number_of_games = 10
        #     number_of_wins = {0: 0, 1: 0}
        #     player1 = RandomPlayer()
        #     player2 = RandomPlayer()    
        #     # if np.array_equal(board, self._game.get_board()):
        #     #     print("the current board is the same as the game board")
        #     # else:
        #     #     print("the current board is not the same as the game board")

        #     for x in range(number_of_games):      
        #         winner = self._game.play(player1, player2)
        #         number_of_wins[winner] += 1
        #     score += number_of_wins[player] * 0.7

        return deepcopy(score)


    def make_random_move(self,board,player) -> tuple[tuple[int, int], Move]:
        '''Do just a random acceptable move'''
        return random.choice(self.get_possible_moves(board, player))


    def make_move_board(self, board: list[list[int]], move: tuple[tuple[int, int], Move], player: int) -> list[list[int]]:
        '''Get the new board after making the move; same logic as the GAME class'''

        # inside all function I use row, col coordinates; I will switch places in the final return value of the agent move.
        # passed move
        row, col = move[0]
        direction = move[1]

        if player > 2:
            raise ValueError("player must be 0 or 1")
        
        #prev_value = deepcopy(board[(row, col)])
        acceptable, board = self.take((row, col), player, board)
        if acceptable:
            acceptable,new_board = self.slide((row, col), direction, board)
            if not acceptable:
                raise ValueError(f"slide tried in the {self.agent} is not acceptable!")
            return new_board
        raise ValueError(f"piece taken in the {self.agent} is not acceptable! the current board is \n {board} and the current player is {player} and the front position is {row,col}")


    def take(self, from_pos: tuple[int, int], player_id: int, board: list[list[int]]) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (board[from_pos] < 0 or board[from_pos] == player_id)
        if acceptable:
            board[from_pos] = player_id
        return acceptable, board

    def slide(self, from_pos: tuple[int, int], slide: Move, board: list[list[int]] ) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
            
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = board[from_pos]
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    board[(from_pos[0], i)] = board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    board[(from_pos[0], i)] = board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                board[(from_pos[0], board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    board[(i, from_pos[1])] = board[(
                        i - 1, from_pos[1])]
                # move the piece up
                board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    board[(i, from_pos[1])] = board[(
                        i + 1, from_pos[1])]
                # move the piece down
                board[(board.shape[0] - 1, from_pos[1])] = piece
        return acceptable,board
    

    # Some simple cases tested
    # def check_winner(self, board: list[list[int]],player: int) -> int:
    #     '''In case there are two complete rows or columns, the current player  loses (i.e., if at the same time player completes a rows for himself and the other, the current player will lose)
    #     this seems to reduce the win rate of the agent because the GAME class does not detect two row or col case.'''

    # #flags to check for two complete rows or columns at the same time
    #     player_already_completed = -1
    #     final_winner = -1


    #     # for each row
    #     winner = -1
    #     for x in range(board.shape[0]):
    #         # if a player has completed an entire row
    #         if board[x, 0] != -1 and all(board[x, :] == board[x, 0]):
    #             winner = board[x, 0]
    #             final_winner = winner
    #     if winner > -1:
    #         player_already_completed = deepcopy(winner)
    #         #check for another row for the other player
    #         for x in range(board.shape[0]):
    #             # if the other player has completed an entire row
    #             if board[x, 0] != -1 and board[x,0] != player_already_completed and all(board[x, :] == board[x, 0]):
    #                 final_winner = 1 - player
    #                 return final_winner
    #         return player_already_completed
                       
    #     # for each column, no rows found
    #     for y in range(board.shape[1]):
    #         # if a player has completed an entire column
    #         if board[0, y] != -1 and all(board[:, y] == board[0, y]):
    #             winner = board[0, y]
    #             final_winner = winner
    #     if winner > -1:
    #         player_already_completed = deepcopy(winner)
    #         #check for another column for the other player
    #         for y in range(board.shape[1]):
    #             # if the other player has completed an entire column
    #             if board[0, y] != -1 and board[0,y] != player_already_completed and all(board[:, y] == board[0, y]):
    #                 final_winner = 1 - player
    #                 return final_winner
    #         return player_already_completed
        

    #     # if a player has completed the principal diagonal
    #     if board[0, 0] != -1 and all([board[x, x] for x in range(board.shape[0])] == board[0, 0]):
    #         # return the relative id
    #         winner = board[0, 0]
    #     if winner > -1:
    #         final_winner=winner
    #         return final_winner
        
    #     # if a player has completed the secondary diagonal
    #     if board[0, -1] != -1 and all([board[x, -(x + 1)] for x in range(board.shape[0])] == board[0, -1]):
    #         # return the relative id
    #         winner = board[0, -1]
    #     if winner > -1:
    #         final_winner=winner
    #         return final_winner
        
    #     return final_winner


    def check_winner(self, board: list[list[int]],player: int) -> int:
        '''Same Logic as the GAME class'''

     # for each row
        winner = -1
        for x in range(board.shape[0]):
            # if a player has completed an entire row
            if board[x, 0] != -1 and all(board[x, :] == board[x, 0]):
                # return winner is this guy
                winner = board[x, 0]
        #if winner > -1 and winner != player:
        if winner > -1:
            return winner
        # for each column
        for y in range(board.shape[1]):
            # if a player has completed an entire column
            if board[0, y] != -1 and all(board[:, y] == board[0, y]):
                # return the relative id
                winner = board[0, y]
        #if winner > -1 and winner != player:
        if winner > -1:
            return winner
        # if a player has completed the principal diagonal
        if board[0, 0] != -1 and all(
            [board[x, x]
                for x in range(board.shape[0])] == board[0, 0]
        ):
            # return the relative id
            winner = board[0, 0]
        #if winner > -1 and winner != self.get_current_player():
        if winner > -1:
            return winner
        # if a player has completed the secondary diagonal
        if board[0, -1] != -1 and all(
            [board[x, -(x + 1)]
             for x in range(board.shape[0])] == board[0, -1]
        ):
            # return the relative id
            winner = board[0, -1]
        return winner



