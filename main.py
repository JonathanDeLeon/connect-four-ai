#!/usr/bin/env python3
# Jonathan De Leon && Ethan Beaver
# CPTR 430 Artificial Intelligence
# Final Project
# June 6, 2018
#
# Problem:
# Create a Connect Four game and implement an AI bot that uses minimax algorithm with alpha-beta pruning
#
# References
# GUI was created by AI Sweigart; we did some code refactoring and connected our algorithm/classes to the GUI
# http://inventwithpython.com/blog/2011/06/10/new-game-source-code-four-in-a-row/

from fourInARowGUI import fourInARowGUI as GUI

infinity = float('inf')


class Game:
    AI = -1
    PLAYER = 0

    def __init__(self, game_board):
        self.current_state = State(0, 0)
        self.turn = self.AI
        self.first = self.turn
        self.board = game_board

    def is_game_over(self):
        if self.has_winning_state():
            """Display who won"""
            print("AI Bot won!") if ~self.turn == self.AI else print("Congratulations, you won!")
            return True
        elif self.draw():
            print("Draw...Thank you...come again")
            return True
        return False

    def draw(self):
        """Check current state to determine if it is in a draw"""
        return State.is_draw(self.current_state.game_position) and not self.has_winning_state()

    def has_winning_state(self):
        return State.is_winning_state(self.current_state.ai_position) or State.is_winning_state(
            self.current_state.player_position)

    def next_turn(self):
        if self.turn == self.AI:
            self.query_AI()
        else:
            self.query_player()

        # self.turn = (self.turn + 1) % 2
        # Apply one's complement (invert bits); 0 ~= -1
        self.turn = ~self.turn

    def query_player(self):
        """Make a move by querying standard input."""
        print("\nPlayer's Move...")
        column = None
        while column is None:
            # column = input('Your move identify column [0-6]? ')
            try:
                # column = int(column)
                column = GUI.getHumanInteraction(self.board)
                # Check if move is legal
                if not 0 <= column <= 6:
                    raise ValueError
                if self.current_state.game_position & (1 << (7 * column + 5)):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid move. Try again...")
                column = None

        GUI.dropHumanToken(self.board, column)

        new_position, new_game_position = make_move(self.current_state.player_position,
                                                    self.current_state.game_position, column)
        self.current_state = State(self.current_state.ai_position, new_game_position, self.current_state.depth + 1)

    def query_AI(self):
        """ AI Bot chooses next best move from current state """
        print("\nAI's Move...")
        temp_position = self.current_state.ai_position
        self.current_state = alphabeta_search(self.current_state, self.first, d=7)

        # Get column for GUI
        column = temp_position ^ self.current_state.ai_position
        column = (column.bit_length() - 1) // 7
        GUI.animateComputerMoving(self.board, column)
        GUI.makeMove(self.board, GUI.BLACK, column)


class State:
    """
    State class
    Each position is a 6x7 board with top row as sentinel row of 0's; so a 7x7 bitboard
    Bit positions corresponding to the board are as follows...
    -  -   -   -   -   -   -
    5  12  19  26  33  40  47
    4  11  18  25  32  39  46
    3  10  17  24  31  38  45
    2  9   16  23  30  37  44
    1  8   15  22  29  36  43
    0  7   14  21  28  35  42
    """

    status = 3

    def __init__(self, ai_position, game_position, depth=0):
        self.ai_position = ai_position
        self.game_position = game_position
        self.depth = depth

    @property
    def player_position(self):
        return self.ai_position ^ self.game_position

    @staticmethod
    def is_winning_state(position):
        # Horizontal check
        m = position & (position >> 7)
        if m & (m >> 14):
            return True
        # Diagonal \
        m = position & (position >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = position & (position >> 8)
        if m & (m >> 16):
            return True
        # Vertical
        m = position & (position >> 1)
        if m & (m >> 2):
            return True
        # Nothing found
        return False

    @staticmethod
    def is_draw(position):
        return all(position & (1 << (7 * column + 5)) for column in range(0, 7))

    def terminal_node_test(self):
        """ Test if current state is a terminal node """
        if self.is_winning_state(self.ai_position):
            # AI Wins
            self.status = -1
            return True
        elif self.is_winning_state(self.player_position):
            # Player Wins
            self.status = 1
            return True
        elif self.is_draw(self.game_position):
            # Draw
            self.status = 0
            return True
        else:
            return False

    def calculate_heuristic(self):
        """
        Score based on who can win. Score computed as 22 minus number of moves played
        i.e. AI wins with 4th move, score = 22 - 4 = 18
        """
        if self.status == -1:
            # AI Wins
            return 22 - (self.depth // 2)
        elif self.status == 1:
            # Player Wins
            return -1 * (22 - (self.depth // 2))
        elif self.status == 0:
            # Draw
            return 0
        elif self.depth % 2 == 0:
            # MAX node returns
            return infinity
        else:
            # MIN node returns
            return -infinity

    def generate_children(self, who_went_first):
        """ For each column entry, generate a new State if the new position is valid"""
        for i in range(0, 7):
            # Select column starting from the middle and then to the edges index order [3,2,4,1,5,0,6]
            column = 3 + (1 - 2 * (i % 2)) * (i + 1) // 2
            if not self.game_position & (1 << (7 * column + 5)):
                if (who_went_first == -1 and self.depth % 2 == 0) or (who_went_first == 0 and self.depth % 2 == 1):
                    # AI (MAX) Move
                    new_ai_position, new_game_position = make_move(self.ai_position, self.game_position, column)
                else:
                    # Player (MIN) move
                    new_ai_position, new_game_position = make_move_opponent(self.ai_position, self.game_position,
                                                                            column)
                yield State(new_ai_position, new_game_position, self.depth + 1)

    def __str__(self):
        return '{0:049b}'.format(self.ai_position) + ' ; ' + '{0:049b}'.format(self.game_position)

    def __hash__(self):
        return hash((self.ai_position, self.game_position, self.depth % 2))

    def __eq__(self, other):
        return (self.ai_position, self.game_position, self.depth % 2) == (
            other.ai_position, other.game_position, other.depth % 2)


def alphabeta_search(state, turn=-1, d=7):
    """Search game state to determine best action; use alpha-beta pruning. """

    # Functions used by alpha beta
    def max_value(state, alpha, beta, depth):
        if cutoff_search(state, depth):
            return state.calculate_heuristic()

        v = -infinity
        for child in state.generate_children(turn):
            if child in seen:
                continue
            v = max(v, min_value(child, alpha, beta, depth + 1))
            seen[child] = alpha
            if v >= beta:
                # Min is going to completely ignore this route
                # since v will not get any lower than beta
                return v
            alpha = max(alpha, v)
        if v == -infinity:
            # If win/loss/draw not found, don't return -infinity to MIN node
            return infinity
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_search(state, depth):
            return state.calculate_heuristic()

        v = infinity
        for child in state.generate_children(turn):
            if child in seen:
                continue
            v = min(v, max_value(child, alpha, beta, depth + 1))
            seen[child] = alpha
            if v <= alpha:
                # Max is going to completely ignore this route
                # since v will not get any higher than alpha
                return v
            beta = min(beta, v)
        if v == infinity:
            # If win/loss/draw not found, don't return infinity to MAX node
            return -infinity
        return v

    # Keep track of seen states using their hash
    seen = {}

    # Body of alpha beta_search:
    cutoff_search = (lambda state, depth: depth > d or state.terminal_node_test())
    best_score = -infinity
    beta = infinity
    best_action = None
    for child in state.generate_children(turn):
        v = min_value(child, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = child
    return best_action


def make_move(position, mask, col):
    """ Helper method to make a move and return new position along with new board position """
    opponent_position = position ^ mask
    new_mask = mask | (mask + (1 << (col * 7)))
    return opponent_position ^ new_mask, new_mask


def make_move_opponent(position, mask, col):
    """ Helper method to only return new board position """
    new_mask = mask | (mask + (1 << (col * 7)))
    return position, new_mask


def print_board(state):
    """
    Helper method to pretty print binary board (6x7 board with top sentinel row of 0's)
    """
    ai_board, total_board = state.ai_position, state.game_position
    for row in range(5, -1, -1):
        print("")
        for column in range(0, 7):
            if ai_board & (1 << (7 * column + row)):
                print("1", end='')
            elif total_board & (1 << (7 * column + row)):
                print("2", end='')
            else:
                print("0", end='')
    print("")


if __name__ == "__main__":
    print("Welcome to Connect Four!")

    GUI.run()
    while True:
        # Set up a blank board data structure.
        game_board = GUI.getNewBoard()
        GUI.drawBoard(game_board)
        GUI.updateDisplay()
        # Start game data structure
        game = Game(game_board)
        while not game.is_game_over():
            game.next_turn()
            print_board(game.current_state)
            GUI.drawBoard(game.board)
            GUI.updateDisplay()

        # Necessary for GUI
        WINNER = '' if game.draw() else GUI.COMPUTER if ~game.turn == -1 else GUI.HUMAN
        GUI.processGameOver(WINNER, game.board)
